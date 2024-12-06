import click
from types import ModuleType
from typing import List
import requests
from typing import Optional

from nema.utils.global_config import GLOBAL_CONFIG, GlobalConfig, GlobalConfigWorkflow
from nema.workflow.workflow import Workflow
from nema.connectivity.connectivity_manager import save_auth_data
from nema.run.utils import convert_app_output_to_nema_data
from nema.run.workflow import InternalWorkflowOutput
from nema.utils.create_data_for_workflow import (
    get_new_data_for_workflow,
    submit_new_data_to_nema,
    update_workflow_file_with_new_global_ids,
)


def authenticate_user(username, password):

    # Authenticate the user
    if GLOBAL_CONFIG.is_set:

        tenant_url = GLOBAL_CONFIG.tenant_api_url

        login_url = f"{tenant_url}/authentication/login"

    else:
        raise Exception(
            "There is no nema.toml file in this directory. Please run `nema init` to create one."
        )

    # Make a request to the login URL
    response = requests.post(
        login_url, json={"username": username, "password": password}
    )

    if not response.ok:
        if response.status_code == 401:
            print("Invalid credentials")
        else:
            print(response.status_code, response.text)
            print("Failed to login")
        return None

    # save the authentication and refresh token to the home directory
    response_data = response.json()
    tokens = response_data["tokens"]
    refresh_token = tokens["refresh_token"]
    access_token = tokens["access_token"]

    # create the directory if it does not exist
    save_auth_data(refresh_token=refresh_token, access_token=access_token)

    print("Login successful \U00002705")


@click.group()
def cli():
    pass


@cli.command()
def login():
    """Login to Nema."""
    username = click.prompt("Please enter your username or email address")
    password = click.prompt("Please enter your password", hide_input=True)
    authenticate_user(username, password)


@cli.command()
def init():
    "Initialize nema.toml file"
    print("Initializing nema.toml file")

    new_global_config = GlobalConfig()

    new_global_config.project_url = click.prompt(
        "Please enter the project URL", type=str
    )

    new_workflow_key = click.prompt(
        "Please enter a workflow identifier (this is only used locally)",
        type=str,
        default="my-first-workflow",
    )
    new_workflow_name = click.prompt(
        "Please enter a name for the workflow", type=str, default=new_workflow_key
    )
    new_workflow_description = click.prompt(
        "Please enter a workflow description",
        type=str,
        default="A Python workflow",
    )

    new_workflow = GlobalConfigWorkflow(
        key=new_workflow_key,
        name=new_workflow_name,
        description=new_workflow_description,
        script="nema_workflow.py",
    )

    new_global_config.workflows[new_workflow_key] = new_workflow

    new_global_config.save()


@cli.group()
def workflow():
    pass


@workflow.command()
@click.argument("identifier", required=False)
def init(identifier: Optional[str]):
    "Create a new workflow"

    if identifier is None:
        print("No workflow specified -- initializing all workflows")
        all_identifiers = GLOBAL_CONFIG.workflows.keys()
    else:
        all_identifiers = [identifier]

    for this_identifier in all_identifiers:
        print(f"Initializing workflow with identifier '{this_identifier}'")
        existing_workflow = GLOBAL_CONFIG.workflows[this_identifier]

        if existing_workflow.global_id > 0:
            print("Workflow already exists. Skipping.")
            continue

        workflow = Workflow(
            global_id=0,
            name=existing_workflow.name,
            description=existing_workflow.description,
        )

        global_id = workflow.create()
        print(f"Workflow successfully created with global id {global_id}. \U00002705")

        existing_workflow.global_id = global_id

    # save the global ID to the config file
    GLOBAL_CONFIG.save()


@workflow.command()
@click.argument("identifier", required=False)
def run(identifier: Optional[str]):
    "Run the workflow"

    if identifier is None:
        print("No workflow specified -- running all workflows")
        all_identifiers = GLOBAL_CONFIG.workflows.keys()
    else:
        all_identifiers = [identifier]

    for this_identifier in all_identifiers:
        print(f"Running workflow with identifier '{this_identifier}'")

        existing_workflow = GLOBAL_CONFIG.workflows[this_identifier]

        python_file = existing_workflow.script

        # read the python file
        with open(python_file, "r") as f:
            code_to_execute = f.read()

        # execute the application code
        user_module = ModuleType("user_module")

        # load code into module
        exec(code_to_execute, user_module.__dict__)

        # execute code
        output: InternalWorkflowOutput = user_module.run()

        # put output back into the right format
        converted_nema_data = convert_app_output_to_nema_data(
            output.output_data, output.output_global_id_mapping
        )

        # sync output to API
        this_wf = Workflow(
            global_id=existing_workflow.global_id,
            name=existing_workflow.name,
            description=existing_workflow.description,
            # output_folder=output_folder,
        )

        used_data = []
        for key_used, value_used in output.input_global_id_mapping.items():
            used_data.append(
                {
                    "artifact": value_used,
                    "id_in_app": key_used,
                }
            )

        this_wf.process_local_update(
            updated_data=converted_nema_data,
            used_data=used_data,
        )

        print(
            f"Workflow '{this_identifier}' successfully run \U0001F680 and results uploaded to Nema. \U00002705"
        )


@workflow.command(name="create-data")
@click.argument("identifier", required=False)
def create_data(identifier: Optional[str]):
    "Create data for the workflow"

    if identifier is None:
        print("No workflow specified -- creating data for all workflows")
        all_identifiers = GLOBAL_CONFIG.workflows.keys()
    else:
        all_identifiers = [identifier]

    for this_identifier in all_identifiers:
        print(f"Creating data for workflow with identifier '{this_identifier}'")

        existing_workflow = GLOBAL_CONFIG.workflows[this_identifier]

        python_file = existing_workflow.script

        # read the python file
        with open(python_file, "r") as f:
            code_to_execute = f.read()

        # execute the application code
        user_module = ModuleType("user_module")

        # load code into module
        exec(code_to_execute, user_module.__dict__)

        # execute code
        run_function = user_module.run

        annotations = run_function.__annotations__
        arg_name = list(annotations)[0]
        input_type = annotations[arg_name]
        output_type = annotations["return"]

        data_to_create_inputs = get_new_data_for_workflow(
            run_function.__workflow_attributes__["input_global_id_mapping"], input_type
        )
        data_to_create_outputs = get_new_data_for_workflow(
            run_function.__workflow_attributes__["output_global_id_mapping"],
            output_type,
        )

        data_to_create = data_to_create_inputs + data_to_create_outputs

        # create the data
        submit_new_data_to_nema(data_to_create)

        new_workflow_file = update_workflow_file_with_new_global_ids(
            code_to_execute, data_to_create_inputs, data_to_create_outputs
        )

        # save the new workflow file
        with open(python_file, "w") as f:
            f.write(new_workflow_file)


if __name__ == "__main__":
    cli()
