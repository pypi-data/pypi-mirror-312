"""
Tools for working with Merkle trees.
"""

import hashlib
import binascii
import base64

# domain separation prefixes according to the RFC
RFC6962_LEAF_HASH_PREFIX = 0
RFC6962_NODE_HASH_PREFIX = 1


class Hasher:
    """
    A representation of a Hasher.
    """

    def __init__(self, hash_func=hashlib.sha256):
        self.hash_func = hash_func

    def new(self):
        """Returns a new instance of the Hasher"""
        return self.hash_func()

    def empty_root(self):
        """Returns the digest of an empty root"""
        return self.new().digest()

    def hash_leaf(self, leaf):
        """Hashes the provided leaf"""
        h = self.new()
        h.update(bytes([RFC6962_LEAF_HASH_PREFIX]))
        h.update(leaf)
        return h.digest()

    def hash_children(self, le, r):
        """Hashes the provided leaf + root"""
        h = self.new()
        b = bytes([RFC6962_NODE_HASH_PREFIX]) + le + r
        h.update(b)
        return h.digest()

    def size(self):
        """Returns the size of the digest"""
        return self.new().digest_size


# DefaultHasher is a SHA256 based LogHasher
DefaultHasher = Hasher(hashlib.sha256)


def verify_consistency(hasher, size1, size2, proof, roots):
    """Verifies the consistency of the tree.

    Args:
        hasher (Hasher): The hasher to use.
        size1 (int): The size of the 1st tree.
        size2 (int): The size of the 2nd tree.
        proof (str[]): The data containing the proof for the tree.
        roots (str[]): The roots of the 1st and 2nd tree.

    Raises:
        ValueError: Raised if size2 < size1.
        ValueError: Raised if size1 == size2, but there is proof data in proof.
        ValueError: Raised if an empty proof array was expected, but was not.
        ValueError: Raised if proof is empty when it should not have been.
        ValueError: Raised if proof is of the wrong size for the computed trees.
    """
    # change format of args to be bytearray instead of hex strings
    root1 = bytes.fromhex(roots[0])
    root2 = bytes.fromhex(roots[1])
    bytearray_proof = [bytes.fromhex(elem) for elem in proof]

    if size2 < size1:
        raise ValueError(f"size2 ({size2}) < size1 ({size1})")
    if size1 == size2:
        if bytearray_proof:
            raise ValueError("size1=size2, but bytearray_proof is not empty")
        verify_match(root1, root2)
        return
    if size1 == 0:
        if bytearray_proof:
            raise ValueError(
                f"expected empty bytearray_proof, but got {len(bytearray_proof)} components"
            )
        return
    if not bytearray_proof:
        raise ValueError("empty bytearray_proof")

    inner, border = decomp_incl_proof(size1 - 1, size2)
    shift = (size1 & -size1).bit_length() - 1
    inner -= shift

    if size1 == 1 << shift:
        seed, start = root1, 0
    else:
        seed, start = bytearray_proof[0], 1

    if len(bytearray_proof) != start + inner + border:
        raise ValueError(
            f"wrong bytearray_proof size {len(bytearray_proof)}, want {start + inner + border}"
        )

    bytearray_proof = bytearray_proof[start:]

    hash1 = chain_inner_right(
        hasher, seed, bytearray_proof[:inner], (size1 - 1) >> shift
    )
    hash1 = chain_border_right(hasher, hash1, bytearray_proof[inner:])
    verify_match(hash1, root1)

    hash2 = chain_inner(hasher, seed, bytearray_proof[:inner], (size1 - 1) >> shift)
    hash2 = chain_border_right(hasher, hash2, bytearray_proof[inner:])
    verify_match(hash2, root2)


def verify_match(calculated, expected):
    """Checks if the calculated root == the expected root.

    Args:
        calculated (str): The calculated root hash.
        expected (str): The expected root hash.

    Raises:
        RootMismatchError: Raised if the hashes do not match.
    """
    if calculated != expected:
        raise RootMismatchError(expected, calculated)


def decomp_incl_proof(index, size):
    """Decomposes an inclusion proof.

    Args:
        index (int): The index of the proof.
        size (int): The size of the proof.
    Returns:
        (int, int): The decomposed proof.
    """
    inner = inner_proof_size(index, size)
    border = bin(index >> inner).count("1")
    return inner, border


def inner_proof_size(index, size):
    """Returns the size of the inner proof.

    Args:
        index (int): The index of the proof.
        size (int): The size of the proof.

    Returns:
        int: The size of the proof.
    """
    return (index ^ (size - 1)).bit_length()


def chain_inner(hasher, seed, proof, index):
    """Chains inner proofs together."""
    for i, h in enumerate(proof):
        if (index >> i) & 1 == 0:
            seed = hasher.hash_children(seed, h)
        else:
            seed = hasher.hash_children(h, seed)
    return seed


def chain_inner_right(hasher, seed, proof, index):
    """Chain inner proofs together."""
    for i, h in enumerate(proof):
        if (index >> i) & 1 == 1:
            seed = hasher.hash_children(h, seed)
    return seed


def chain_border_right(hasher, seed, proof):
    """Chain proofs together."""
    for h in proof:
        seed = hasher.hash_children(h, seed)
    return seed


class RootMismatchError(Exception):
    """An exception for the mismatch of roots"""

    def __init__(self, expected_root, calculated_root):
        self.expected_root = binascii.hexlify(bytearray(expected_root))
        self.calculated_root = binascii.hexlify(bytearray(calculated_root))

    def __str__(self):
        return (
            f"calculated root:\n{self.calculated_root}\n"
            + f"does not match expected root:\n{self.expected_root}"
        )


def root_from_inclusion_proof(hasher, index, size, leaf_hash, proof):
    """Compute the root from an inclusion proof.

    Args:
        hasher (Hasher): The hasher to use.
        index (int): The index to use.
        size (int): The size to use.
        leaf_hash (str): The leaf hash.
        proof (str): The proof to use.

    Raises:
        ValueError: Raised if the index is greater than the size.
        ValueError: Raised if the leaf_hash has an unexpected size.
        ValueError: Raised if the proof is of the wrong size.

    Returns:
        str: The root hash.
    """
    if index >= size:
        raise ValueError(f"index is beyond size: {index} >= {size}")

    if len(leaf_hash) != hasher.size():
        raise ValueError(
            f"leaf_hash has unexpected size {len(leaf_hash)}, want {hasher.size()}"
        )

    inner, border = decomp_incl_proof(index, size)
    if len(proof) != inner + border:
        raise ValueError(f"wrong proof size {len(proof)}, want {inner + border}")

    res = chain_inner(hasher, leaf_hash, proof[:inner], index)
    res = chain_border_right(hasher, res, proof[inner:])
    return res


# def verify_inclusion(hasher, index, size, leaf_hash, proof, root, debug=False):
def verify_inclusion(hasher, proof_components, debug=False):
    """Verify inclusion of an entry.

    Args:
        hasher (Hasher): The hasher to use.
        index (int): The index to use.
        size (int): The size to use.
        leaf_hash (str): The leaf hash.
        proof (str[]): The proof to use.
        root (str): The hash of the root.
        debug (bool, optional): Print out debugging information. Defaults to False.
    """
    bytearray_proof = [bytes.fromhex(elem) for elem in proof_components["proof"]]

    bytearray_root = bytes.fromhex(proof_components["root"])
    bytearray_leaf = bytes.fromhex(proof_components["leaf_hash"])
    calc_root = root_from_inclusion_proof(
        hasher,
        proof_components["index"],
        proof_components["size"],
        bytearray_leaf,
        bytearray_proof,
    )
    verify_match(calc_root, bytearray_root)
    if debug:
        print("Calculated root hash", calc_root.hex())
        print("Given root hash", bytearray_root.hex())


# requires entry["body"] output for a log entry
# returns the leaf hash according to the rfc 6962 spec
def compute_leaf_hash(body):
    """Computes the hash of a leaf.

    Args:
        body (str): The data to be hashed.

    Returns:
        str: The computed hash.
    """
    entry_bytes = base64.b64decode(body)

    # create a new sha256 hash object
    h = hashlib.sha256()
    # write the leaf hash prefix
    h.update(bytes([RFC6962_LEAF_HASH_PREFIX]))

    # write the actual leaf data
    h.update(entry_bytes)

    # return the computed hash
    return h.hexdigest()
