from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from bidsapps.manifest_management import auto_update_and_validate_manifest
import questionary
import yaml

console = Console()

def interactive_edit_yaml(file_path):
    """Interactive editor for a YAML file with support for dicts and lists."""
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f) or {}
    except Exception as e:
        console.print(f"[bold red]Error loading YAML file: {e}[/bold red]")
        return

    def edit_value(value):
        """Interactively edit a value, handling dicts, lists, and primitives."""
        if isinstance(value, dict):
            return edit_dict(value)
        elif isinstance(value, list):
            return edit_list(value)
        else:
            # Edit a primitive value
            new_value = questionary.text(
                f"Current value: {value}. Enter new value (or leave blank to keep):"
            ).ask()
            return value if not new_value else yaml.safe_load(new_value)

    def edit_dict(d):
        """Interactively edit a dictionary."""
        while True:
            key_to_edit = questionary.select(
                "Which key would you like to edit?",
                choices=list(d.keys()) + ["[Add new key]", "[Back]"]
            ).ask()

            if key_to_edit == "[Back]":
                break
            elif key_to_edit == "[Add new key]":
                new_key = questionary.text("Enter the new key:").ask()
                new_value = questionary.text("Enter the value for the new key:").ask()
                d[new_key] = yaml.safe_load(new_value)
            else:
                d[key_to_edit] = edit_value(d[key_to_edit])

        return d

    def edit_list(lst):
        """Interactively edit a list."""
        while True:
            action = questionary.select(
                "What would you like to do?",
                choices=["Edit an item", "Add a new item", "Remove an item", "[Back]"]
            ).ask()

            if action == "[Back]":
                break
            elif action == "Edit an item":
                index = questionary.select(
                    "Select the item to edit:",
                    choices=[f"{i}: {item}" for i, item in enumerate(lst)]
                ).ask()
                index = int(index.split(":")[0])  # Extract the index
                lst[index] = edit_value(lst[index])
            elif action == "Add a new item":
                new_item = questionary.text("Enter the new item:").ask()
                lst.append(yaml.safe_load(new_item))
            elif action == "Remove an item":
                index = questionary.select(
                    "Select the item to remove:",
                    choices=[f"{i}: {item}" for i, item in enumerate(lst)]
                ).ask()
                index = int(index.split(":")[0])  # Extract the index
                lst.pop(index)

        return lst

    # Display the current YAML
    syntax = Syntax(yaml.dump(data, default_flow_style=False), "yaml", theme="monokai", line_numbers=True)
    panel = Panel(syntax, title="Current YAML")
    console.print(panel)

    # Edit the YAML interactively
    if isinstance(data, dict):
        data = edit_dict(data)
    else:
        console.print("[bold red]Top-level YAML must be a dictionary![/bold red]")
        return

    # Display updated YAML
    syntax = Syntax(yaml.dump(data, default_flow_style=False), "yaml", theme="monokai", line_numbers=True)
    panel = Panel(syntax, title="Updated YAML")
    console.print(panel)

    # Confirm and save changes
    save_changes = questionary.confirm("Save changes to the file?").ask()
    if save_changes:
        try:
            with open(file_path, "w") as f:
                yaml.dump(data, f, default_flow_style=False)
            console.print(f"[bold green]Changes saved to {file_path}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error saving YAML file: {e}[/bold red]")
    else:
        console.print("[bold yellow]Changes discarded.[/bold yellow]")


    update_manifest = questionary.confirm("Update manifest file?").ask()
    if update_manifest:
        #update and validate manifest
        auto_update_and_validate_manifest()

