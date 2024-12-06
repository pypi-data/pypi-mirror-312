# ARSA Pipeline Tools

`arsa-pipeline-tools` is a utility package designed for MLOps pipelines in Vertex AI. It provides functions for:
- Downloading files from Google Cloud Storage (GCS) buckets.
- Dynamically loading Python modules from local files.

## Features
- **`download_files_from_gcs`**: Downloads files from a GCS bucket into a specified local directory, with optional filtering by file extensions.
- **`load_module_from_file`**: Dynamically loads a Python module from a local file.

## Installation

Install the package via pip:

```bash
pip install arsa-pipeline-tools
