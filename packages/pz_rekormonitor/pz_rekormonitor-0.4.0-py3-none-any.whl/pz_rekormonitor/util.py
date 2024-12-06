"""
Utilities for working with certificates and signatures.
"""

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature


# extracts and returns public key from a given cert (in pem format)
def extract_public_key(cert):
    """Extracts and returns the public key from the given certificate.

    Args:
        cert (str): The certificate, in PEM format.

    Returns:
        str: The public key.
    """
    # load the certificate
    certificate = x509.load_pem_x509_certificate(cert, default_backend())

    # extract the public key
    public_key = certificate.public_key()

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return pem_public_key


def verify_artifact_signature(signature, public_key, artifact_filename):
    """Verifies the signature of the provided artifact.

    Args:
        signature (str): The signature to verify.
        public_key (str): The public key to verify the signature against.
        artifact_filename (str): The artifact to verify.
    """
    public_key = load_pem_public_key(public_key)
    # load the data to be verified
    with open(artifact_filename, "rb") as data_file:
        data = data_file.read()

    # verify the signature
    # Only returns one type of exception as per
    # https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dsa/#cryptography.hazmat.primitives.asymmetric.dsa.DSAPublicKey.verify
    try:
        public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        print("Signature is invalid.")
        return False
    # except Exception as e:
    #     print("Exception in verifying artifact signature:", e)
