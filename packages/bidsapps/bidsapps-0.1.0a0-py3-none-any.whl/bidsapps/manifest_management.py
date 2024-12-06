import os
import json
from bidsapps.repo_management import get_repo
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.align import Align
import yaml

console = Console()

def load_manifest():
    """Load the manifest from the configured repository."""
    config = get_repo()
    repo_path = config["repo_path"]
    manifest_path = os.path.join(repo_path, "manifest.json")

    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest not found at {manifest_path}.")

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    return manifest, repo_path







def list_apps(verbose=False):
    """List apps from the manifest with pretty output using Rich."""
    try:
        manifest, repo_path = load_manifest()
    except FileNotFoundError as e:
        console.print(f"[bold red]{e}[/bold red]")
        return

    if verbose:
        # Long view: Full YAML for each app
        for app in manifest["apps"]:
            app_path = app["path"]
            app_full_path = f"{repo_path}/{app_path}"
            try:
                with open(app_full_path, "r") as f:
                    app_yaml = yaml.safe_load(f)
                    yaml_syntax = Syntax(yaml.dump(app_yaml), "yaml", theme="monokai", line_numbers=True)
                    panel = Panel(yaml_syntax, title=app["name"], subtitle=app_path)
                    console.print(panel)
            except Exception as e:
                console.print(f"[bold red]Error loading {app_full_path}: {e}[/bold red]")
    else:
        # Short view: Table with name and either container or url
        table = Table(title="BIDS Apps")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Container/URL", style="magenta")

        for app in manifest["apps"]:
            app_path = app["path"]
            app_full_path = f"{repo_path}/{app_path}"
            try:
                with open(app_full_path, "r") as f:
                    app_yaml = yaml.safe_load(f)
                    container_or_url = app_yaml.get("container", app_yaml.get("url", "N/A"))
                    table.add_row(app["name"], container_or_url)
            except Exception as e:
                table.add_row(app["name"], f"[red]Error loading app: {e}[/red]")

        console.print(table)


def update_manifest():
    """Update the manifest based on the current apps."""
    try:
        _, repo_path = load_manifest()
    except FileNotFoundError:
        # Create a new manifest if none exists
        config = get_repo()
        repo_path = config["repo_path"]

    apps_dir = os.path.join(repo_path, "apps")
    manifest_path = os.path.join(repo_path, "manifest.json")

    manifest = {"apps": []}
    for root, _, files in os.walk(apps_dir):
        for file in files:
            if file.endswith(".yaml"):
                with open(os.path.join(root, file), "r") as f:
                    app_data = yaml.safe_load(f)
                manifest["apps"].append({
                    "name": app_data["name"],
                    "type": "snakebids" if "url" in app_data else "container",
                    "path": os.path.relpath(os.path.join(root, file), repo_path),
                })

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)

    
 


def validate_manifest():
    """Validate the manifest against the apps directory."""
    try:
        manifest, repo_path = load_manifest()
    except FileNotFoundError as e:
        print(e)
        return

    apps_dir = os.path.join(repo_path, "apps")
    manifest_files = {app["path"] for app in manifest["apps"]}
    yaml_files = {
        os.path.relpath(os.path.join(root, file), repo_path)
        for root, _, files in os.walk(apps_dir)
        for file in files if file.endswith(".yaml")
    }

    missing_in_manifest = yaml_files - manifest_files
    missing_in_directory = manifest_files - yaml_files

    if missing_in_manifest:
        print("Files missing in the manifest:")
        for f in missing_in_manifest:
            print(f"  - {f}")
    if missing_in_directory:
        print("Files listed in the manifest but missing in the directory:")
        for f in missing_in_directory:
            print(f"  - {f}")

    if not missing_in_manifest and not missing_in_directory:
        return


def auto_update_and_validate_manifest():
    """
    Automatically update and validate the manifest whenever app configurations change.
    """
    try:
        console.print("[cyan]Updating the manifest...[/cyan]")
        update_manifest()
        console.print("[green]Manifest updated successfully![/green]")

        console.print("[cyan]Validating the manifest...[/cyan]")
        validate_manifest()
        console.print("[green]Manifest validated successfully![/green]")
    except Exception as e:
        console.print(f"[bold red]Error during manifest update/validation: {e}[/bold red]")
        raise


