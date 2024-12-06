import click
from bidsapps.app_management import add_app
from bidsapps.manifest_management import load_manifest
from bidsapps.repo_management import configure_repo, get_repo
from bidsapps.interactive_edit import console, interactive_edit_yaml
import os

@click.group()
def cli():
    """CLI tool for managing BIDS apps repository."""
    pass


import subprocess
import sys
import os
from bidsapps.manifest_management import load_manifest

@cli.command(name="run")
@click.argument("bids_dir", type=click.Path(exists=True, file_okay=False))
@click.argument("output_dir", type=click.Path(file_okay=False))
@click.argument("app_name")  # Allow only one app name
@click.argument("optional_args", nargs=-1, type=click.UNPROCESSED)
def run_app(bids_dir, output_dir, app_name, optional_args):
    """
    Run a specified BIDS app with the given arguments.

    \b
    BIDS_DIR: Path to the BIDS directory.
    OUTPUT_DIR: Path to the output directory.
    APP_NAME: Name of the BIDS app to run.
    OPTIONAL_ARGS: Additional arguments to pass to the app's CLI.
    """
    try:
        # Load the manifest to find the app configuration
        manifest, repo_path = load_manifest()
        app_entry = next((app for app in manifest["apps"] if app["name"] == app_name), None)

        if not app_entry:
            console.print(f"[bold red]App '{app_name}' not found in the manifest.[/bold red]")
            sys.exit(1)

        # Identify the console script or entry point
        console_script = 'sbbatch/run.py'

        # Build the command
        command = (
            [sys.executable, console_script, bids_dir, output_dir, app_name]
            + list(optional_args)
        )
        console.print(f"[bold cyan]Running: {' '.join(command)}[/bold cyan]")

        # Execute the command
        result = subprocess.run(command, check=False)  # Use check=False to avoid exiting on errors
        if result.returncode != 0:
            console.print(f"[bold red]App '{app_name}' failed with return code {result.returncode}.[/bold red]")
            sys.exit(result.returncode)

    except Exception as e:
        console.print(f"[bold red]Error running app: {e}[/bold red]")
        sys.exit(1)


@cli.command()
@click.option("--repo", required=True, help="Path to a local repo or GitHub URI.")
def configure(repo):
    """Configure the repository."""
    configure_repo(repo)

@cli.command()
def show_repo():
    """Show the currently configured repository."""
    try:
        config = get_repo()
        print(f"Currently configured repository: {config['repo_path']} ({config['repo_type']})")
    except FileNotFoundError as e:
        print(e)

@cli.command(name="list")
@click.option("--verbose", is_flag=True, help="Display detailed information about each app.")
def list_apps(verbose):
    from bidsapps.manifest_management import list_apps 
    """List all current apps."""
    try:
        list_apps(verbose)
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)


@cli.command()
@click.option("--name", required=True, help="Name of the new app.")
@click.option("--type", type=click.Choice(["container", "snakebids"]), required=True, help="Type of app.")
@click.option("--file", type=click.Path(), help="Path to YAML file with app details.")
def add(name, type, file):
    """Add a new app to the repository."""
    add_app(name, type, file)


@cli.command()
@click.argument("app_name")
def edit(app_name):
    """Edit an existing app interactively."""
    try:
        manifest, repo_path = load_manifest()
        app = next((app for app in manifest["apps"] if app["name"] == app_name), None)
        if not app:
            console.print(f"[bold red]App '{app_name}' not found in the manifest.[/bold red]")
            return
        file_path = os.path.join(repo_path, app["path"])
        interactive_edit_yaml(file_path)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


@cli.command()
def update_manifest():
    from bidsapps.manifest_management import auto_update_and_validate_manifest
    """Update and validate the manifest based on the current apps."""
    auto_update_and_validate_manifest()

@cli.command()
def pull():
    """Pull the latest changes from the repository."""
    pull_repo()



@click.group()
def import_cmd():
    """Commands for importing BIDS apps."""
    pass

@import_cmd.command(name="list")
def list_apps():
    from bidsapps.app_import import list_bids_apps
    """List available BIDS apps from the BIDS apps list."""
    list_bids_apps()


@import_cmd.command(name="new")
@click.option("--apps-dir", default="apps", help="Directory to save imported app configurations.")
def import_new(apps_dir):
    from bidsapps.app_import import import_new_bids_app
    """Interactively import a new BIDS app."""
    import_new_bids_app(apps_dir)

cli.add_command(import_cmd, name="import")




if __name__ == "__main__":
    cli()

