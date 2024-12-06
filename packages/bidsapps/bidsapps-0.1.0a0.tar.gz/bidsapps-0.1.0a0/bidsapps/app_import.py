import requests
import yaml
from rich.console import Console
from rich.table import Table
import questionary
import os
from bidsapps.manifest_management import auto_update_and_validate_manifest

# Constants
BIDS_APPS_YAML_URL = "https://raw.githubusercontent.com/bids-standard/bids-website/main/data/tools/apps.yml"
DOCKER_TAGS_API_URL = "https://hub.docker.com/v2/repositories/{repo}/tags"

console = Console()

def fetch_bids_apps():
    """Fetch the BIDS apps YAML from the BIDS website repository."""
    try:
        response = requests.get(BIDS_APPS_YAML_URL)
        response.raise_for_status()
        apps_dict = yaml.safe_load(response.text)

        apps = apps_dict.get('apps',None)

        # Ensure the fetched data is a list
        if not isinstance(apps, list):
            console.print("[bold red]Unexpected data format: Expected a list of apps.[/bold red]")
            return []

        return apps
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error fetching BIDS apps list: {e}[/bold red]")
        return []
    except yaml.YAMLError as e:
        console.print(f"[bold red]Error parsing YAML: {e}[/bold red]")
        return []

def list_bids_apps():
    """Display a table of all BIDS apps."""
    apps = fetch_bids_apps()
    if not apps:
        console.print("[bold red]No apps found.[/bold red]")
        return

    # Create a Rich table
    table = Table(title="BIDS Apps", show_lines=True)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Input Datatypes", style="magenta")
    table.add_column("Use Raw", style="green")
    table.add_column("Use Derivatives", style="green")
    table.add_column("Description", style="white")

    for app in apps:
        if not isinstance(app, dict):  # Skip invalid entries
            console.print(f"[bold yellow]Skipping invalid app entry: {app}[/bold yellow]")
            continue

        name = app.get("gh", "").split("/")[-1]
        datatypes = ", ".join(app.get("datatype", []))
        use_raw = ":white_check_mark:" if "raw" in app.get("ds_type", []) else ":no_entry_sign:"
        use_derivatives = ":white_check_mark:" if "derivative" in app.get("ds_type", []) else ":no_entry_sign:"
        description = app.get("description") or "No description available"

        # Replace newline characters in the description
        description = description.replace("\n", " ")

        table.add_row(
            name,
            datatypes,
            use_raw,
            use_derivatives,
            description,
        )

    console.print(table)



def fetch_docker_tags(repo):
    """Fetch available Docker tags for a given repository."""
    try:
        response = requests.get(DOCKER_TAGS_API_URL.format(repo=repo))
        response.raise_for_status()
        tags = response.json().get("results", [])
        return [tag["name"] for tag in tags]
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error fetching Docker tags for {repo}: {e}[/bold red]")
        return []

def import_new_bids_app(apps_dir="apps"):
    """Interactive process to import a new BIDS app."""
    # Step 1: Fetch and display the list of apps
    apps = fetch_bids_apps()
    if not apps:
        console.print("[bold red]No apps available to import.[/bold red]")
        return

    # Create a selection list for the user
    app_choices = [
        f"{app.get('gh', '').split('/')[-1]} ({', '.join(app.get('datatype', []))})"
        for app in apps
    ]
    selected_app = questionary.select("Select an app to import:", choices=app_choices).ask()
    if not selected_app:
        console.print("[bold yellow]Import cancelled.[/bold yellow]")
        return

    # Find the selected app data
    app_index = app_choices.index(selected_app)
    app = apps[app_index]

    # Step 2: Query Docker Hub for available tags
    docker_repo = app.get("dh", "").lower()
    docker_tags = fetch_docker_tags(docker_repo) if docker_repo else []
    if docker_tags:
        selected_tag = questionary.select("Select a Docker tag:", choices=docker_tags).ask()
    else:
        selected_tag = questionary.text("Enter a Docker tag manually:").ask()

    # Step 3: Gather additional fields
    config = {
        "name": questionary.text("Enter a unique name identifier for this app:").ask(),
        "container": f"docker://{docker_repo}:{selected_tag}",
        "description": app.get("description", "No description available"),
        "analysis_level": questionary.text("Enter the analysis level (e.g., participant):").ask(),
        "opts": questionary.text("Enter any additional options for this app:").ask(),
        "resources": {
            "cores": int(questionary.text("Number of CPU cores (default 4):").ask() or 4),
            "mem_mb": int(questionary.text("Memory in MB (default 8000):").ask() or 8000),
            "runtime": int(questionary.text("Runtime in minutes (default 120):").ask() or 120),
            "gpus": int(questionary.text("Number of GPUs (default 0):").ask() or 0),
        },
    }

    # Step 4: Save the new configuration
    app_name = config["name"]
    app_subdir = os.path.join(apps_dir, app_name.split("_")[0])
    os.makedirs(app_subdir, exist_ok=True)
    app_file = os.path.join(app_subdir, f"{app_name}.yaml")
    try:
        with open(app_file, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        console.print(f"[bold green]App '{app_name}' imported successfully! Configuration saved to {app_file}.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error saving app configuration: {e}[/bold red]")

    # Step 5: update manifest
    auto_update_and_validate_manifest()
