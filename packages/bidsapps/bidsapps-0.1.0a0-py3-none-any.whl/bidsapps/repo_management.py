import os
import json
import subprocess
from appdirs import AppDirs

# Define app-specific directories
dirs = AppDirs("bids_apps", "my_app")
CONFIG_FILE = os.path.join(dirs.user_config_dir, "config.json")

# Ensure the config directory exists
os.makedirs(dirs.user_config_dir, exist_ok=True)

def configure_repo(repo):
    """Configure the repository, supporting both local paths and GitHub URIs."""
    # Check if the repo is a GitHub URI
    if repo.startswith("http://") or repo.startswith("https://"):
        repo_type = "github"
        local_repo_dir = os.path.join(dirs.user_data_dir, os.path.basename(repo).replace(".git", ""))
        if not os.path.exists(local_repo_dir):
            print(f"Cloning repository from {repo}...")
            subprocess.run(["git", "clone", repo, local_repo_dir], check=True)
        repo_path = local_repo_dir
    else:
        # Assume it's a local path
        repo_type = "local"
        repo_path = os.path.abspath(repo)
        if not os.path.exists(repo_path):
            raise FileNotFoundError(f"Local repository path '{repo_path}' does not exist.")

    # Save configuration
    config_data = {"repo_type": repo_type, "repo_path": repo_path}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
    print(f"Configured repository: {repo_path} ({repo_type})")

def get_repo():
    """Retrieve the currently configured repository."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError("No repository configured. Please run `configure` first.")
    with open(CONFIG_FILE, "r") as f:
        config_data = json.load(f)
    return config_data

