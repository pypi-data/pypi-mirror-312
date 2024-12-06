import subprocess
import os

README_FILE = "README.md"

def get_cli_usage():
    """Extract CLI usage from the main command."""
    try:
        result = subprocess.run(["bidsapps", "--help"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running 'bidsapps --help': {e}")
        return ""

def update_readme():
    """Update the README with installation and CLI usage instructions."""
    cli_usage = get_cli_usage()

    # Define the new sections
    installation_section = """
## Installation

To install the CLI, clone the repository and install the dependencies:

```bash
git clone https://github.com/khanlab/bidsapps
cd bidsapps
pip install -e .
```
"""

    usage_section = f"""
## Usage

Below is the latest CLI usage:

```
{cli_usage.strip()}
```
"""

    # Read the current README
    if os.path.exists(README_FILE):
        with open(README_FILE, "r") as f:
            readme_content = f.read()
    else:
        readme_content = ""

    # Update or append sections
    new_readme_content = installation_section + usage_section

    if "## Installation" in readme_content:
        # Replace existing sections
        readme_content = (
            readme_content.split("## Installation")[0] + new_readme_content
        )
    else:
        # Add new sections at the end
        readme_content += "\n" + new_readme_content

    # Write updated README
    with open(README_FILE, "w") as f:
        f.write(readme_content)
    print("README.md updated successfully.")

if __name__ == "__main__":
    update_readme()


