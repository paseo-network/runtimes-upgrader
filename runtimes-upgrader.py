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
    subprocess.run(["git", "clone", "--branch", tag, "--depth", "1", repo_url, temp_dir], check=True)

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
    try:
        os.chdir(paseo_repo_dir)
        if subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True).returncode != 0:
            print("Error: Specified directory is not a Git repository.")
            return
        existing_branches = subprocess.getoutput("git branch --list {}".format(branch_name))
        if branch_name in existing_branches:
            print(f"Branch '{branch_name}' already exists. Switching to it.")
            subprocess.run(["git", "checkout", branch_name], check=True)
        else:
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        os.chdir(current_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    Simplifies the upgrade process of the Paseo runtime by cloning and copying the Polkadot runtime 
    from a specified GitHub repository tag into the Paseo runtime directory. It supports text replacements 
    for compatibility adjustments and creates a new branch for the upgrade within the Paseo repository.""")
    
    parser.add_argument("--repo_url", required=True, help="GitHub URL of the Polkadot runtime repository.")
    parser.add_argument("--tag", required=True, help="Tag of the Polkadot repository to clone.")
    parser.add_argument("--source_subdir", required=True, help="Subdirectory in the cloned repository to copy.")
    parser.add_argument("--destination_dir", required=True, help="Destination directory in the local Paseo repository.")
    parser.add_argument("--config_file", required=True, help="JSON configuration file for text replacements.")
    parser.add_argument("--paseo_repo_dir", required=True, help="Root directory of the local Paseo repository.")

    args = parser.parse_args()

    current_dir = os.getcwd()  # Save the current working directory

    config = read_config(args.config_file)
    replacements = config["replacements"]
    remove_block_pattern = config["remove_block_pattern"]

    create_branch_in_paseo_repo(args.paseo_repo_dir, f"release-{args.tag}")

    temp_dir = "./polkadot-runtimes"
    clone_repo(args.repo_url, args.tag, temp_dir)

    source_dir = os.path.join(temp_dir, args.source_subdir)
    copy_directory_contents(source_dir, args.destination_dir)

    apply_replacements_to_directory(args.destination_dir, replacements, remove_block_pattern)

    shutil.rmtree(temp_dir)  # Cleanup
    os.chdir(current_dir)  # Restore the original working directory

    print("Runtime upgrade process completed successfully.")
