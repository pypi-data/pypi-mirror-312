"""
A set of tools to interact with the Sigstore Rekor transparency log.
"""

import argparse
import base64
import json
import os
import requests
from pz_rekormonitor.util import extract_public_key, verify_artifact_signature
from pz_rekormonitor.merkle_proof import (
    DefaultHasher,
    verify_consistency,
    verify_inclusion,
    compute_leaf_hash,
)

LOG_QUERY_ENDPOINT = "https://rekor.sigstore.dev/api/v1/log/entries?logIndex="
LOG_PROOF_ENDPOINT = "https://rekor.sigstore.dev/api/v1/log/proof?"
LOG_CHECKPOINT_ENDPOINT = "https://rekor.sigstore.dev/api/v1/log"


def get_log_entry(log_index, debug=False):
    """Obtain the specified entry from Rekor.

    Args:
        log_index (int): The index of the entry to obtain. Must be a positive int.
        debug (bool, optional): Print out debugging information. Defaults to False.

    Raises:
        TypeError: Raised on an invalid type for log_index.
        ValueError: Raised on a negative value for log_index.
        SystemExit: Raised on an exception when sending the HTTP request to Rekor.
        SystemExit: Raised on an unexpected HTTP status code from Rekor.

    Returns:
        str: The JSON payload from Rekor about the entry.
    """
    # verify that log index value is sane
    if not isinstance(log_index, int):
        raise TypeError("Invalid type for log index.")
    if log_index < 0:
        raise ValueError("Index value must be nonnegative.")

    log_query = LOG_QUERY_ENDPOINT + str(log_index)

    # Query Rekor, and exit upon an exception
    try:
        http_response = requests.get(log_query, timeout=10)
    except requests.exceptions.RequestException as exception:
        raise SystemExit(exception) from exception

    # Validate return code; only valid one is 200 as per
    # https://www.sigstore.dev/swagger/index.html?urls.primaryName=Rekor#/entries/getLogEntryByIndex

    if http_response.status_code != 200:
        raise SystemExit("An error was encountered when querying the Rekor API")

    if debug:
        print(json.dumps(http_response.json(), indent=4))

    return http_response.json()


def get_verification_proof(log_index, debug=False):
    """Get a verification proof for the specified entry in Rekor.

    Args:
        log_index (int): The index of the entry to obtain. Must be a positive int.
        debug (bool, optional): Print out debugging information. Defaults to False.

    Raises:
        TypeError: Raised on an invalid type for log_index.
        ValueError: Raised on a negative value for log_index.

    Returns:
        (int, int, str, str[], str): The tuple containing the data needed for a proof.
    """
    # verify that log index value is sane
    if not isinstance(log_index, int):
        raise TypeError("Invalid type for log index.")
    if log_index < 0:
        raise ValueError("Index value must be nonnegative.")

    # Pull the record from the log
    log_entry = get_log_entry(log_index, debug)

    # Select the first key in the JSON record
    intermediate_data = log_entry[list(dict(log_entry).keys())[0]]

    # print(json.dumps(intermediate_data['body'], indent=4))

    # Get the leaf hash from the body entry
    leaf_hash = compute_leaf_hash(intermediate_data["body"])

    # Select the verification.inclusionProof
    intermediate_data = intermediate_data["verification"]["inclusionProof"]

    # Extract the hashes, log index, root hash, and tree size
    hashes = intermediate_data["hashes"]
    index = intermediate_data["logIndex"]
    root_hash = intermediate_data["rootHash"]
    tree_size = intermediate_data["treeSize"]

    return (index, tree_size, leaf_hash, hashes, root_hash)


def inclusion(log_index, artifact_filepath, debug=False):
    """Checks if the specified artifact is included in Rekor.

    Args:
        log_index (int): The index of the checkpoint to check for inclusion against. Must be a
                            positive int.
        artifact_filepath (str): The path to the artifact to check.
        debug (bool, optional): Print out debugging information. Defaults to False.

    Raises:
        TypeError: Raised on an invalid type for log_index.
        ValueError: Raised on a negative value for log_index.
        TypeError: Raised on an invalid type for artifact_filepath.
        SystemExit: Raised on being unable to open the artifact file.
    """
    # verify that log index and artifact filepath values are sane
    if not isinstance(log_index, int):
        raise TypeError("Invalid type for log index.")
    if log_index < 0:
        raise ValueError("Index value must be nonnegative.")

    if not artifact_filepath:
        raise TypeError("Invalid type for artifact filepath.")

    if not os.path.isfile(artifact_filepath):
        raise SystemExit("Encountered an error when attempting to open the artifact")

    log_entry = get_log_entry(log_index, debug)

    # Select the first key in the JSON record
    intermediate_data = log_entry[list(dict(log_entry).keys())[0]]

    # Select its body key
    intermediate_data = intermediate_data["body"]

    # b64 + utf-8 decode + json reload
    intermediate_data = json.loads(base64.b64decode(intermediate_data).decode("utf-8"))

    # Select the spec.body key as the signature data
    intermediate_data = dict(intermediate_data)["spec"]["signature"]

    # Extract signature + b64 decode (again...)
    signature = base64.b64decode(dict(intermediate_data)["content"])

    # Extract public key + b64 decode (again...)
    certificate = base64.b64decode(
        dict(intermediate_data)["publicKey"]["content"]
    ).decode("utf-8")

    # Process the public key
    public_key = extract_public_key(bytes(certificate, "utf-8"))

    # Verify the artifact's signature
    retval = verify_artifact_signature(signature, public_key, artifact_filepath)

    if retval is False:
        return

    print("Signature is valid.")

    # Get the values needed for the verification proof
    index, tree_size, leaf_hash, hashes, root_hash = get_verification_proof(log_index)

    # Finally, verify inclusion of the entry
    inclusion_args = {}
    inclusion_args["index"] = index
    inclusion_args["size"] = tree_size
    inclusion_args["leaf_hash"] = leaf_hash
    inclusion_args["proof"] = hashes
    inclusion_args["root"] = root_hash
    verify_inclusion(DefaultHasher, inclusion_args, debug)

    print("Offline root hash calculation for inclusion verified.")


def get_latest_checkpoint(debug=False):
    """Obtain the latest checkpoint from Rekor.

    Args:
        debug (bool, optional): Print out debugging information. Defaults to False.

    Raises:
        SystemExit: Raised on an exception when sending the HTTP request to Rekor.
        SystemExit: Raised on an unexpected HTTP status code from Rekor.

    Returns:
        _type_: _description_
    """
    # Execute the query to get the latest log checkpoint
    try:
        http_response = requests.get(LOG_CHECKPOINT_ENDPOINT, timeout=10)
    except requests.exceptions.RequestException as exception:
        raise SystemExit(exception) from exception

    # Validate return code; only valid one is 200 as per
    # https://www.sigstore.dev/swagger/index.html?urls.primaryName=Rekor#/tlog/getLogProof

    if http_response.status_code != 200:
        raise SystemExit("An error was encountered when querying the Rekor API")

    if debug:
        print(json.dumps(http_response.json(), indent=4))

    return http_response.json()


def consistency(prev_checkpoint, debug=False):
    """_summary_

    Args:
        prev_checkpoint (dict): The previous checkpoint to verify against.
        debug (bool, optional): Print out debugging information. Defaults to False.

    Raises:
        ValueError: Raised on an invalid value for prev_checkpoint.
        SystemExit: Raised on an exception when sending the HTTP request to Rekor.
        SystemExit: Raised on an unexpected HTTP status code from Rekor.
    """
    # verify that previous checkpoint is not empty
    if not prev_checkpoint:
        raise ValueError("Previous checkpoint is invalid.")

    # Get the latest checkpoint from the server
    latest_checkpoint = get_latest_checkpoint(debug)

    # Contruct + execute the query to get the previous checkpoint proof
    proof_query = (
        LOG_PROOF_ENDPOINT
        + "firstSize="
        + str(prev_checkpoint["treeSize"])
        + "&lastSize="
        + str(latest_checkpoint["treeSize"])
        + "&treeID="
        + str(prev_checkpoint["treeID"])
    )

    try:
        http_response = requests.get(proof_query, timeout=10)
    except requests.exceptions.RequestException as exception:
        raise SystemExit(exception) from exception

    # Validate return code; only valid one is 200 as per
    # https://www.sigstore.dev/swagger/index.html?urls.primaryName=Rekor#/entries/getLogEntryByIndex

    if http_response.status_code != 200:
        raise SystemExit("An error was encountered when querying the Rekor API")

    # Assign variables as needed
    size1 = prev_checkpoint["treeSize"]
    size2 = latest_checkpoint["treeSize"]
    proof = http_response.json()["hashes"]
    root1 = prev_checkpoint["rootHash"]
    root2 = latest_checkpoint["rootHash"]

    # Hand off to consistency verifier
    verify_consistency(DefaultHasher, size1, size2, proof, [root1, root2])

    print("Consistency verification successful.")


def main():
    """The main code for the tool that parses args and calls out to other functions"""
    debug = False
    parser = argparse.ArgumentParser(description="Rekor Verifier")
    parser.add_argument(
        "-d", "--debug", help="Debug mode", required=False, action="store_true"
    )  # Default false
    parser.add_argument(
        "-c",
        "--checkpoint",
        help="Obtain latest checkpoint\
                        from Rekor Server public instance",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--inclusion",
        help="Verify inclusion of an\
                        entry in the Rekor Transparency Log using log index\
                        and artifact filename.\
                        Usage: --inclusion 126574567",
        required=False,
        type=int,
    )
    parser.add_argument(
        "--artifact",
        help="Artifact filepath for verifying\
                        signature",
        required=False,
    )
    parser.add_argument(
        "--consistency",
        help="Verify consistency of a given\
                        checkpoint with the latest checkpoint.",
        action="store_true",
    )
    parser.add_argument(
        "--tree-id", help="Tree ID for consistency proof", required=False
    )
    parser.add_argument(
        "--tree-size", help="Tree size for consistency proof", required=False, type=int
    )
    parser.add_argument(
        "--root-hash", help="Root hash for consistency proof", required=False
    )
    args = parser.parse_args()
    if args.debug:
        debug = True
        print("enabled debug mode")
    if args.checkpoint:
        # get and print latest checkpoint from server
        # if debug is enabled, store it in a file checkpoint.json
        checkpoint = get_latest_checkpoint(debug)
        print(json.dumps(checkpoint, indent=4))

        if debug:
            with open("checkpoint.json", "w", encoding="utf-8") as json_file:
                json_file.write(json.dumps(checkpoint, indent=4))
                json_file.write("\n")

    if args.inclusion:
        inclusion(args.inclusion, args.artifact, debug)
    if args.consistency:
        if not args.tree_id:
            print("please specify tree id for prev checkpoint")
            return
        if not args.tree_size:
            print("please specify tree size for prev checkpoint")
            return
        if not args.root_hash:
            print("please specify root hash for prev checkpoint")
            return

        prev_checkpoint = {}
        prev_checkpoint["treeID"] = args.tree_id
        prev_checkpoint["treeSize"] = args.tree_size
        prev_checkpoint["rootHash"] = args.root_hash

        consistency(prev_checkpoint, debug)


if __name__ == "__main__":
    main()
