## About
This project implements a signing and verification process using Sigstore’s tools for Software Supply Chain Security. We use `cosign` to sign an artifact and store it in a transparency log, and Python code to verify the artifact's inclusion, signature, and consistency.

## Usage Instructions
- **Artifact Creation**: Add your content to `artifact.md`.
- **Signing and Uploading**: Use `cosign` to sign `artifact.md` and upload it to Rekor's transparency log.
- **Verification**: Run the Python script to verify inclusion, signature, and consistency with Rekor log checkpoints.

## Installation
1. Install `cosign`: [Installation Guide](https://docs.sigstore.dev/cosign/system_config/installation/)
2. Clone this repository.
3. Install dependencies using `pip install -r requirements.txt`.
 
