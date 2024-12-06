# arsa_pipeline_tools/utils.py

import os
import logging
import importlib.util
from google.cloud import storage

def download_files_from_gcs(code_bucket_path: str, code_dir: str, allowed_extensions=None):
    """
    Downloads files from a GCS bucket and saves them to a specified local directory.

    Args:
        code_bucket_path (str): The GCS bucket path (e.g., gs://bucket-name/folder).
        code_dir (str): The local directory where files will be downloaded.
        allowed_extensions (set): A set of allowed file extensions to filter downloads.

    Returns:
        None
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Parse bucket name and prefix from the GCS path
    bucket_name = code_bucket_path.split('/')[2]
    prefix = '/'.join(code_bucket_path.split('/')[3:])

    # Initialize the GCS client
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = client.list_blobs(bucket, prefix=prefix)

    # Create the target directory
    os.makedirs(code_dir, exist_ok=True)

    # Set default allowed extensions
    if allowed_extensions is None:
        allowed_extensions = {".py", ".json", ".yaml", ".csv", ".pkl"}

    # Download files
    for blob in blobs:
        if any(blob.name.endswith(ext) for ext in allowed_extensions):
            relative_path = blob.name[len(prefix):].lstrip("/")
            file_path = os.path.join(code_dir, relative_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            blob.download_to_filename(file_path)
            logger.info(f"Downloaded {blob.name} to {file_path}")

    logger.info(f"All files downloaded to {code_dir}")


def load_module_from_file(file_path):
    """
    Loads a Python module dynamically from a file path.

    Args:
        file_path (str): The file path to the Python module.

    Returns:
        module: The loaded module object.
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
