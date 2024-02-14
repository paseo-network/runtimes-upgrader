import argparse
import json
import os
import re
import shutil
import subprocess

def read_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def clone_repo(repo_url, tag, temp_dir):
    # Ensure temp_dir is a string, especially if it's dynamically generated
    temp_dir_str = str(temp_dir)  # Explicitly convert to string to avoid type errors
    
    # Ensure tag is a string (this should normally be the case)
    tag_str = str(tag)
    
    # Run the git clone command
    subprocess.run(["git", "clone", "--branch", tag_str, "--depth", "1", repo_url, temp_dir_str], check=True)


def copy_directory_contents(source_dir, destination_dir):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)

def replace_in_file(file_path, replacements):
    with open(file_path, 'r') as file:
        content = file.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file_path, 'w') as file:
        file.write(content)

def replace_cargo_file(source_cargo, destination_cargo, replacements):
    # Copy the Cargo.toml file
    shutil.copy2(source_cargo, destination_cargo)
    
    # Apply replacements to the copied Cargo.toml file
    replace_in_file(destination_cargo, replacements)


def remove_text_block(file_path, pattern):
    with open(file_path, 'r') as file:
        content = file.read()

    content = re.sub(pattern, "", content, flags=re.DOTALL)

    with open(file_path, 'w') as file:
        file.write(content)

def apply_replacements_to_directory(directory_path, replacements, remove_pattern):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith('.rs') or file_name == 'Cargo.toml':
                file_path = os.path.join(root, file_name)
                replace_in_file(file_path, replacements)
                remove_text_block(file_path, remove_pattern)
                
def create_branch_in_paseo_repo(paseo_repo_dir, branch_name):
    print(f"create_branch_in_paseo_repo  paseo_repo_dir: '{paseo_repo_dir}' branch_name: '{branch_name}'")
    # Save the current working directory
    current_dir = os.getcwd()
    try:
        # Change to the paseo repository directory
        os.chdir(paseo_repo_dir)
        # Verify if the directory is a Git repository
        if subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True).returncode != 0:
            print("Error: Specified directory is not a Git repository.")
            return
        # Check if branch already exists and switch to it, else create it
        existing_branches = subprocess.getoutput("git branch --list {}".format(branch_name))
        if branch_name in existing_branches:
            print(f"Branch '{branch_name}' already exists. Switching to it.")
            subprocess.run(["git", "checkout", branch_name], check=True)
        else:
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Change back to the original working directory
        os.chdir(current_dir)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    This script facilitates the process of upgrading the Paseo testnet runtime by cloning a specific version of the Polkadot runtime from a GitHub repository. 
    It creates a new branch in the local Paseo repository, copies the specified Polkadot runtime subdirectory and the Cargo.toml configuration file into the Paseo runtime,
    applies predefined text replacements to accommodate Paseo's specific configurations, and performs cleanup after the operations.
    """)
    
    parser.add_argument("--repo_url", required=True, help="The GitHub URL of the Polkadot runtime repository to clone. Example: https://github.com/polkadot-fellows/runtimes.git")
    parser.add_argument("--tag", required=True, help="The tag or release of the Polkadot Runtime repository to clone. This specifies the exact snapshot of the Polkadot runtime to use for the upgrade.")
    parser.add_argument("--source_subdir", required=True, help="The subdirectory within the cloned Polkadot repository containing the runtime source code. Path is relative to the repository root. Example: 'src/runtime'")
    parser.add_argument("--destination_dir", required=True, help="The destination directory in the local Paseo repository where the Polkadot runtime source will be copied. This should be the path to the Paseo runtime directory.")
    parser.add_argument("--config_file", required=True, help="Path to the JSON configuration file that contains text replacements and configurations specific to Paseo. These replacements are applied to the copied Polkadot runtime source files to ensure compatibility.")
    parser.add_argument("--paseo_repo_dir", required=True, help="The root directory of the local Paseo repository. A new branch for the runtime upgrade will be created here.")
    parser.add_argument("--polkadot_cargo", required=True, help="Relative path to the Polkadot runtime's Cargo.toml file in the cloned repository. This file contains dependencies and configurations for the runtime.")
    parser.add_argument("--paseo_cargo", required=True, help="The destination path for the Polkadot runtime's Cargo.toml file within the Paseo repository. This replaces Paseo's existing Cargo.toml to integrate the new runtime configurations.")

    args = parser.parse_args()

    config = read_config(args.config_file)
    replacements = config["replacements"]
    remove_block_pattern = config["remove_block_pattern"]

    branch_name = f"release-{args.tag}"
    create_branch_in_paseo_repo(args.paseo_repo_dir, branch_name)

    temp_dir = "./polkadot-runtimes"
    clone_repo(args.repo_url, args.tag, temp_dir)

    source_dir = os.path.join(temp_dir, args.source_subdir)
    copy_directory_contents(source_dir, args.destination_dir)

    source_cargo_path = os.path.join(temp_dir, args.polkadot_cargo)
    destination_cargo_path = args.paseo_cargo
    shutil.copy2(source_cargo_path, destination_cargo_path)
    replace_in_file(destination_cargo_path, replacements)

    apply_replacements_to_directory(args.destination_dir, replacements, remove_block_pattern)

    shutil.rmtree(temp_dir)
    print("Processing completed successfully.")
