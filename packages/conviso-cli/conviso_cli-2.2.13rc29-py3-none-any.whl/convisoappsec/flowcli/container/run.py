import traceback
import click
import json
import subprocess
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli.common import asset_id_option
from convisoappsec.flow.graphql_api.beta.models.issues.container import CreateOrUpdateContainerFindingInput
from convisoappsec.common.graphql.errors import ResponseError
from convisoappsec.common.retry_handler import RetryHandler
from convisoappsec.logger import log_and_notify_ast_event
from convisoappsec.flowcli.requirements_verifier import RequirementsVerifier
from copy import deepcopy as clone
from convisoappsec.flowcli.common import (
    asset_id_option,
    project_code_option,
)


@click.command()
@project_code_option(
    help="Not required when --no-send-to-flow option is set",
    required=False
)
@asset_id_option(required=False)
@click.option(
    '-r',
    '--repository-dir',
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=False,
    help="The source code repository directory.",
)
@click.option(
    "--send-to-flow/--no-send-to-flow",
    default=True,
    show_default=True,
    required=False,
    hidden=True,
    help="""Enable or disable the ability of send analysis result
    reports to flow. When --send-to-flow option is set the --project-code
    option is required""",
)
@click.option(
    "--company-id",
    required=False,
    envvar=("CONVISO_COMPANY_ID", "FLOW_COMPANY_ID"),
    help="Company ID on Conviso Platform",
)
@click.option(
    '--asset-name',
    required=False,
    envvar=("CONVISO_ASSET_NAME", "FLOW_ASSET_NAME"),
    help="Provides a asset name.",
)
@click.option(
    '--vulnerability-auto-close',
    default=False,
    is_flag=True,
    hidden=True,
    help="Enable auto fixing vulnerabilities on cp.",
)
@click.argument('image_name')
@help_option
@pass_flow_context
@click.pass_context
def run(
        context, flow_context, project_code, asset_id, company_id, repository_dir, send_to_flow, asset_name, vulnerability_auto_close, image_name,

):
    """ Run command for container vulnerability scan focused on OS vulnerabilities """
    context.params['company_id'] = company_id if company_id is not None else None
    prepared_context = RequirementsVerifier.prepare_context(clone(context))

    params_to_copy = [
        'asset_id', 'send_to_flow', 'asset_name', 'vulnerability_auto_close', 'project_code', 'repository_dir'
    ]

    for param_name in params_to_copy:
        context.params[param_name] = (
                locals()[param_name] or prepared_context.params[param_name]
        )

    scan_command = f"trivy image --pkg-types os --format json --output result.json {image_name}"

    asset_id = context.params['asset_id']
    company_id = context.params['company_id']

    try:
        log_func(f"🔧 Scanning image {image_name} ...")
        run_command(scan_command)
        log_func("✅ Scan completed successfully.")
        conviso_api = flow_context.create_conviso_api_client_beta()
        process_result(conviso_api, flow_context, asset_id, company_id)
    except Exception as error:
        log_func(f"❌ Scan failed: {error}")


def run_command(command):
    """
    Runs a shell command and logs its execution.
    """
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result

def process_result(conviso_api, flow_context, asset_id, company_id):
    """
    Process and send result to conviso platform.
    """
    log_func("🔧 Processing results ...")
    result_file = "result.json"

    try:
        with open(result_file, 'r') as file:
            scan_results = json.load(file)

        results = scan_results.get("Results", [])
        if results and isinstance(results, list) and len(results) > 0:
            vulnerabilities = results[0].get("Vulnerabilities", [])
        else:
            vulnerabilities = []

        if vulnerabilities:
            log_func(f"🔍 Sending {len(vulnerabilities)} vulnerabilities to conviso platform.")

            for vulnerability in vulnerabilities:
                issue_model = CreateOrUpdateContainerFindingInput(
                    asset_id=asset_id,
                    title=vulnerability.get("Title", ""),
                    description=vulnerability.get("Description", "No description provided."),
                    severity=vulnerability.get("Severity", ""),
                    solution="Use latest image version",
                    reference=parse_conviso_references(vulnerability.get("References", [])),
                    affected_version=vulnerability.get("InstalledVersion", ""),
                    package=vulnerability.get("PkgName", ""),
                    cve=vulnerability.get("VulnerabilityID", ""),
                    patched_version=None,
                    category=parse_category(vulnerability.get('CweIDs', [])),
                    original_issue_id_from_tool=vulnerability.get("PkgIdentifier", "").get("UID", "")
                )

                try:
                    conviso_api.issues.create_container(issue_model)
                except ResponseError as error:
                    if error.code == 'RECORD_NOT_UNIQUE':
                        continue
                    else:
                        retry_handler = RetryHandler(
                            flow_context=flow_context, company_id=company_id, asset_id=asset_id
                        )
                        retry_handler.execute_with_retry(conviso_api.issues.create_iac, issue_model)
                except Exception:
                    retry_handler = RetryHandler(
                        flow_context=flow_context, company_id=company_id, asset_id=asset_id
                    )
                    retry_handler.execute_with_retry(conviso_api.issues.create_iac, issue_model)

                continue
        else:
            log_func("✅ No vulnerabilities found.")

    except FileNotFoundError:
        log_func(f"❌ {result_file} not found. Ensure the scan was successful.")
        full_trace = traceback.format_exc()
        log_and_notify_ast_event(
            flow_context=flow_context, company_id=company_id, asset_id=asset_id, ast_log=full_trace
        )
    except json.JSONDecodeError:
        log_func(f"❌ Failed to parse {result_file}. Ensure it is valid JSON.")
        full_trace = traceback.format_exc()
        log_and_notify_ast_event(
            flow_context=flow_context, company_id=company_id, asset_id=asset_id, ast_log=full_trace
        )
    except Exception:
        full_trace = traceback.format_exc()
        log_func(f"❌ An error occurred while processing results: {full_trace}")
        log_and_notify_ast_event(
            flow_context=flow_context, company_id=company_id, asset_id=asset_id, ast_log=full_trace
        )

def parse_conviso_references(references):
    DIVIDER = "\n"

    return DIVIDER.join(references)


def parse_category(category):
    """ Parse and convert CWE values to string and split with comma """
    category = ", ".join(category)

    return category


def log_func(msg, new_line=True):
    click.echo(click.style(msg), nl=new_line, err=True)
