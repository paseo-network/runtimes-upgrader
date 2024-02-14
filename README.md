# Paseo Upgrader tool.

This tool facilitates the process of upgrading the Paseo blockchain runtime by cloning a specific version of the Polkadot runtime from a GitHub repository. 
It creates a new branch in the local Paseo repository, copies the specified Polkadot runtime directory into the Paseo runtime, applies predefined text replacements to accommodate Paseo's specific configurations, and performs cleanup after the operations.

## Help

usage: runtimes-upgrader.py [-h] --repo_url REPO_URL --tag TAG --source_subdir SOURCE_SUBDIR --destination_dir DESTINATION_DIR --config_file CONFIG_FILE --paseo_repo_dir PASEO_REPO_DIR

optional arguments:
  -h, --help            show this help message and exit
  --repo_url REPO_URL   GitHub URL of the Polkadot runtime repository.
  --tag TAG             Tag of the Polkadot repository to clone.
  --source_subdir SOURCE_SUBDIR
                        Subdirectory in the cloned repository to copy.
  --destination_dir DESTINATION_DIR
                        Destination directory in the local Paseo repository.
  --config_file CONFIG_FILE
                        JSON configuration file for text replacements.
  --paseo_repo_dir PASEO_REPO_DIR
                        Root directory of the local Paseo repository.
➜  upgrader git:(main) ✗

## Example

```
python upgrader.py --repo_url https://github.com/polkadot-fellows/runtimes.git --tag v1.1.2 --source_subdir relay/polkadot --destination_dir /local/paseo/runtimes/relay/paseo --config_file replacements_config.json --paseo_repo_dir /local/blockchain/paseo/runtimes
```