import argparse
import base64
import json
import requests
from .util import extract_public_key, verify_artifact_signature
from .merkle_proof import (
    DefaultHasher,
    verify_consistency,
    verify_inclusion,
    compute_leaf_hash,
)

L_QUERY_EP = "https://rekor.sigstore.dev/api/v1/log/entries?logIndex="
L_P_EP = "https://rekor.sigstore.dev/api/v1/log/proof?"
L_C_EP = "https://rekor.sigstore.dev/api/v1/log"


def get_log_entry(log_index, debug=False):
    http_res = requests.get(L_QUERY_EP + str(log_index),timeout=10)
    if http_res.status_code != 200:
        print("Error: Unable to fetch log entry")
        return None

    http_res = http_res.json()

    first_key = next(iter(http_res))

    log_entry = http_res[first_key]
    if debug:
        print(json.dumps(log_entry, indent=4))
    return log_entry


def get_verification_proof(log_index, debug=False):
    if debug:
        print("Fetching verification proof")

    # check if log_index is a valid integer and non negative
    if log_index < 0:
        raise ValueError("Invalid log index value")

    if not isinstance(log_index, int):
        raise TypeError("Log index value must be an integer")

    http_res = requests.get(L_QUERY_EP + str(log_index),timeout=10)
    if http_res.status_code != 200:
        print("Error: Unable to fetch log entry")
        return None

    http_res = http_res.json()
    first_key = next(iter(http_res))

    log_entry = http_res[first_key]
    verification = log_entry["verification"]
    inclusion_proof = verification["inclusionProof"]

    index = inclusion_proof["logIndex"]
    root_hash = inclusion_proof["rootHash"]
    tree_size = inclusion_proof["treeSize"]
    hashes = inclusion_proof["hashes"]

    leaf_hash = compute_leaf_hash(log_entry["body"])

    # index, tree_size, leaf_hash, hashes, root_hash
    return index, tree_size, leaf_hash, hashes, root_hash


def inclusion(log_index, artifact_filepath, debug=False):
 
    if not artifact_filepath:
        print("Error: artifact filepath is missing")
        return

    # get log entry
    log_entry = get_log_entry(log_index, debug)

    body_from_log_b64 = log_entry["body"]
    body_from_log = base64.b64decode(body_from_log_b64)
    body_from_log = json.loads(body_from_log)

    signature_b64 = body_from_log["spec"]["signature"]["content"]
    signature = base64.b64decode(signature_b64)
    print("Signature Decoded")

    cert_b64 = body_from_log["spec"]["signature"]["publicKey"]["content"]
    certificate = base64.b64decode(cert_b64)
    print("Certificate Decoded") 

    # extract_public_key(certificate)
    public_key = extract_public_key(certificate)
    print("Extracted Public Key")
    if not public_key:
        print("Error: Unable to extract public key, Verification Failed")
        return

    print("Artifact Signature Verification Started")
    is_verified = verify_artifact_signature(signature, public_key, artifact_filepath)
    if not is_verified:
        print("Artifact Signature Verification Failed")
        return
    print("Artifact Signature Verified")

    # get verification proof
    print("Verification Proof Started")
    index, tree_size, leaf_hash, hashes, root_hash = get_verification_proof(log_index)
    print("Verification Proof Obtained")

    # verify inclusion
    print("Inclusion Verification Started")

    v_i_res = verify_inclusion(
        DefaultHasher, index, tree_size, leaf_hash, hashes, root_hash, debug
    )

    if v_i_res:
        print("Inclusion Verified")
    else:
        print("Inclusion Verification Failed")


def get_certificate(artifact_filepath):

    #  Missing function or method docstring (missing-function-docstring)
    """
    Get certificate from artifact filepath

    Parameters:
    artifact_filepath (str): The filepath to the artifact.

    Returns:
    str: The certificate extracted from the artifact.
    """
    # get certificate from artifact filepath
    with open(artifact_filepath, "rb") as cert_file:
        cert_data = cert_file.read()

    # get cert data from json
    cert_data = json.loads(cert_data)
    cert = cert_data["cert"]
    return cert


def get_signature(artifact_filepath):
    """
    Get signature from artifact filepath

    Parameters:
    artifact_filepath (str): The filepath to the artifact.

    Returns:
    str: The signature extracted from the artifact.


    """

    # get signature from artifact filepath
    with open(artifact_filepath, "rb") as signature_file:
        signature_data = signature_file.read()

    # get signature data from json
    signature_data = json.loads(signature_data)
    signature = signature_data["base64Signature"]
    print("signature : ", signature)
    return signature


def get_latest_checkpoint(debug=False):
    http_res = requests.get(L_C_EP,timeout=10)
    if http_res.status_code != 200:
        print("Error: Unable to fetch log entry")
        return None

    log_entry = http_res.json()
    if debug:
        print(json.dumps(log_entry, indent=4))
    return log_entry


def consistency(prev_checkpoint, debug=False):
    """
    Verifies the consistency between the previous checkpoint and the latest checkpoint.

    Parameters:
    prev_checkpoint (dict): The previous checkpoint containing the tree size and root hash.
    debug (bool, optional): Whether to print additional debug information. Defaults to False.

    Returns:
    None. Prints "Consistency Verified" if the consistency check passes.
    """

    if debug:
        print("Previous Checkpoint: ", prev_checkpoint)
    l_checkpoint = get_latest_checkpoint()

    size1 = prev_checkpoint["treeSize"]
    size2 = l_checkpoint["treeSize"]

    root1 = prev_checkpoint["rootHash"]
    root2 = l_checkpoint["rootHash"]

    proof = requests.get(f"{L_P_EP}firstSize={size1}&lastSize={size2}",timeout=10)
    proof = proof.json()["hashes"]

    vc_res = verify_consistency(DefaultHasher, size1, size2, proof, root1, root2)
    if vc_res:
        print("Consistency Verified")
    else:
        print("Consistency Verification Failed")


def main():
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
