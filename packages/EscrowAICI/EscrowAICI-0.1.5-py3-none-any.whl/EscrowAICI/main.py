# EscrowAI Python script
# for Algorithm Owner
# Copyright 2023 BeeKeeperAI(r)
# Last updated: 2023-12-01


# Import BeeKeeperAI EscrowAI Python library
from EscrowAICI.EscrowAI import EscrowAI
import os
import argparse
import base64
from git import Repo
import re


def main():
    # Example usage:
    # You would call `encrypt_algo` here with the appropriate arguments.
    # This would be done when you run this script from the command line or a GitHub Action step.

    # Retrieve the encryption key from an environment variable or command line argument
    # encryption_key = os.getenv('ENCRYPTION_KEY') or b'some-default-key'

    # username = os.getenv('BEEKEEPER_USERNAME')
    # password = os.getenv('BEEKEEPER_PASSWORD')
    repo = Repo(".")
    auth_key = os.getenv("PROJECT_PRIVATE_KEY")
    project_id = os.getenv("BEEKEEPER_PROJECT_ID")
    environment = os.getenv(
        "BEEKEEPER_ENVIRONMENT", "prod"
    )  # Default to 'prod' if not specified
    # We might need to check organization participation on project..
    organization_id = os.getenv("BEEKEEPER_ORGANIZATION_ID")

    parser = argparse.ArgumentParser(
        description="Encrypt files and package them into a zip archive."
    )
    parser.add_argument(
        "folder", type=str, help="The folder path containing the files to encrypt"
    )
    parser.add_argument(
        "--algorithm_type",
        type=str,
        help="Algorithm type can be either validation or training",
    )
    parser.add_argument("--algorithm_name", type=str, help="Algorithm name")
    parser.add_argument(
        "--algorithm_description", type=str, help="Description for the algorithm"
    )
    parser.add_argument("--version_tag", type=str, help="Algorithm version tag")
    parser.add_argument(
        "--version_description", type=str, help="Algorithm version description"
    )
    parser.add_argument(
        "--key", type=str, help="The encryption key (base64 encoded)", required=False
    )
    args = parser.parse_args()

    if not project_id:
        raise Exception("Project id not provided")

    if not organization_id:
        raise Exception("Organization Id not provided")

    if not auth_key:
        raise Exception("Private key not provided")

    escrow = EscrowAI(
        authKey=auth_key,
        project_id=project_id,
        environment=environment,
        organization_id=organization_id,
    )

    # Get Commit message
    commit_message = ""
    try:
        commit_message = repo.head.commit.message
        pattern = r"[\'\";`/&<>]"
        commit_message = re.sub(pattern, "", commit_message)
    except Exception:
        pass

    print("commit_message: " + commit_message)

    # Determine the path for the secret.key file
    # key_file_path = os.path.join(os.path.dirname(__file__), 'secret.key')
    # print(key_file_path)

    # Convert base64 key if provided, otherwise generate a random key
    if args.key:
        key = base64.b64decode(args.key)

    if args.key:
        escrow.encrypt_algo(args.folder, key_from_file=True, secret=key)
    else:
        # Call the function with the path to the folder and the encryption key
        escrow.encrypt_algo(args.folder)

    # Example of using a method
    escrow.upload_algorithm(
        filename=args.folder + ".zip",
        name=args.algorithm_name
        if args.algorithm_name
        else os.path.basename(os.path.normpath(args.folder)),
        algo_type=args.algorithm_type if args.algorithm_type else "validation",
        version=args.version_tag if args.version_tag else "V2",
        description=args.version_description
        if args.version_description
        else commit_message,
        algo_description=args.algorithm_description
        if args.algorithm_description
        else "",
    )


if __name__ == "__main__":
    main()
