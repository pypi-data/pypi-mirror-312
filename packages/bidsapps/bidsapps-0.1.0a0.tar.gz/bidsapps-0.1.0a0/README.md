# 🧠 BIDS Apps CLI 🚀

Manage and run your **BIDS apps** with ease! This tool is designed to streamline running multiple BIDS apps on your BIDS datasets, 
whether the apps are containerized BIDS apps, or SnakeBIDS apps that use containers for different rules of the workflow. 

### ✨ Features:
- 📂 **Organize and manage** your BIDS apps configuration with a central repository.
- 🏃 **Run BIDS apps** seamlessly from the command line, passing custom arguments.
- 🖥️ **SnakeBIDS batching** runs any BIDS App using a snakemake/snakebids wrapper with parallelization. 
- 📦 **Zip outputs** and run in isolated temp directories for HPC systems, including smart merging of participant zipfiles.
- 🔍 **Discover new apps** from the [BIDS Apps Registry](https://bids-apps.neuroimaging.io/).


---

## Installation

To install the CLI, clone the repository and install the dependencies:

```bash
git clone https://github.com/khanlab/bidsapps
cd bidsapps
pip install -e .
```

## Usage

Below is the latest CLI usage:

```
Usage: bidsapps [OPTIONS] COMMAND [ARGS]...

  CLI tool for managing BIDS apps repository.

Options:
  --help  Show this message and exit.

Commands:
  add                Add a new app to the repository.
  configure          Configure the repository.
  edit               Edit an existing app interactively.
  import             Commands for importing BIDS apps.
  list
  pull               Pull the latest changes from the repository.
  run                Run a specified BIDS app with the given arguments.
  show-repo          Show the currently configured repository.
  update-manifest
  validate-manifest
```
