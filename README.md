# Paseo Upgrader tool.

This tool facilitates the process of upgrading the Paseo blockchain runtime by cloning a specific version of the Polkadot runtime from a GitHub repository. 
It creates a new branch in the local Paseo repository, copies the specified Polkadot runtime subdirectory and the Cargo.toml configuration file into the Paseo runtime, applies predefined text replacements to accommodate Paseo's specific configurations, and performs cleanup after the operations.

## Help

usage: `upgrader.py [-h] --repo_url REPO_URL --tag TAG --source_subdir SOURCE_SUBDIR --destination_dir DESTINATION_DIR --config_file CONFIG_FILE --paseo_repo_dir PASEO_REPO_DIR --polkadot_cargo POLKADOT_CARGO --paseo_cargo PASEO_CARGO`

This script facilitates the process of upgrading the Paseo testnet runtime by cloning a specific version of the Polkadot runtime from a GitHub repository. It creates a new branch in the local Paseo repository, copies the specified Polkadot runtime subdirectory and the Cargo.toml configuration file into the Paseo runtime,
applies predefined text replacements to accommodate Paseo's specific configurations, and performs cleanup after the operations.

optional arguments:
  -h, --help            show this help message and exit
  --repo_url REPO_URL   The GitHub URL of the Polkadot runtime repository to clone. Example: https://github.com/polkadot-fellows/runtimes.git
  --tag TAG             The tag or release of the Polkadot Runtime repository to clone. This specifies the exact snapshot of the Polkadot runtime to use for the upgrade.
  --source_subdir SOURCE_SUBDIR
                        The subdirectory within the cloned Polkadot repository containing the runtime source code. Path is relative to the repository root. Example: 'src/runtime'
  --destination_dir DESTINATION_DIR
                        The destination directory in the local Paseo repository where the Polkadot runtime source will be copied. This should be the path to the Paseo runtime directory.
  --config_file CONFIG_FILE
                        Path to the JSON configuration file that contains text replacements and configurations specific to Paseo. These replacements are applied to the copied Polkadot runtime source files to ensure compatibility.
  --paseo_repo_dir PASEO_REPO_DIR
                        The root directory of the local Paseo repository. A new branch for the runtime upgrade will be created here.
  --polkadot_cargo POLKADOT_CARGO
                        Relative path to the Polkadot runtime's Cargo.toml file in the cloned repository. This file contains dependencies and configurations for the runtime.
  --paseo_cargo PASEO_CARGO
                        The destination path for the Polkadot runtime's Cargo.toml file within the Paseo repository. This replaces Paseo's existing Cargo.toml to integrate the new runtime configurations.

## Example

```
 python upgrader.py --repo_url https://github.com/polkadot-fellows/runtimes.git --tag v1.1.2 --source_subdir relay/polkadot/src --destination_dir /local/paseo/runtimes/relay/paseo/src --polkadot_cargo relay/polkadot/Cargo.toml --paseo_cargo /local/paseo/runtimes/relay/paseo/Cargo.toml --config_file replacements_config.json --paseo_repo_dir /local/paseo/runtimes
```