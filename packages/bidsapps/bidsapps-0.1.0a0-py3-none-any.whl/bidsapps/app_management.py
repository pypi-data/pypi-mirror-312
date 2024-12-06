import os
import yaml
from bidsapps.manifest_management import auto_update_and_validate_manifest

REPO_PATH = None

def set_repo_path(repo):
    global REPO_PATH
    REPO_PATH = repo

def add_app(name, app_type, file_path):
    """Add a new app to the repository."""
    if not REPO_PATH:
        raise ValueError("Repository path not configured.")
    app_dir = os.path.join(REPO_PATH, "apps", name)
    os.makedirs(app_dir, exist_ok=True)
    app_file = os.path.join(app_dir, f"{name}.yaml")
    with open(file_path, "r") as f:
        app_data = yaml.safe_load(f)
    with open(app_file, "w") as f:
        yaml.dump(app_data, f)
    print(f"Added {name} to {app_dir}.")


    auto_update_and_validate_manifest()
