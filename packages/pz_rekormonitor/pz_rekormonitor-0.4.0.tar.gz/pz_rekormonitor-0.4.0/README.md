# Python Rekor Monitor

This tool allows one to validate entries in the Sigstore Rekor transparency log.

## Usage

The tool has three distinct flows.

1. **Checkpoint retreival**: Run `python-rekor-monitor` with the `-c` argument to
   obtain the latest checkpoint information from the server.

2. **Inclusion verification**: Run`python-rekor-monitor` with the following
   arguments:
     - `--inclusion <log_index>` with the specified Rekor log index to verify
       inclusion at.
     - `--artifact <artifact_filepath>` with the filepath to the artifact to
       verify inclusion of.

3. **Consistency verification**: Run `python-rekor-monitor` with the following
   arguments:
     - `--consistency` to enable this mode.
     - `--tree-id <tree_id>` with the specified Rekor tree ID to check.
     - `--tree-size <tree_size>` with the specified Rekor tree size to check.
     - `--root-hash <root_hash>` with the specified Rekor root hash to check.

The `--debug` flag may be added to any flow to view additional output useful for
debugging the monitor tool.
