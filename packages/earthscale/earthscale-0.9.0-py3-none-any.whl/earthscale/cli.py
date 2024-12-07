import importlib
import inspect
import os
import sys
from types import ModuleType
from typing import Any, cast

import click
import requests
from loguru import logger

from earthscale.auth import authenticate as run_auth
from earthscale.auth import get_supabase_client
from earthscale.constants import BACKEND_URL_ENV_VAR, DEFAULT_BACKEND_URL
from earthscale.datasets.dataset import Dataset
from earthscale.ingest import (
    ingest_dataset_to_earthscale,
    is_dataset_readable_by_earthscale,
    validate_if_dataset_is_ingestable,
)
from earthscale.repositories.dataset import DatasetRepository


@click.group()
def cli() -> None:
    """Earthscale command line tool."""
    pass


def _find_datasets_for_module(
    module: ModuleType,
) -> list[Dataset[Any]]:
    datasets = []
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, Dataset):
            datasets.append(obj)
    return datasets


def _register_dataset(
    dataset: Dataset[Any],
    dataset_repo: DatasetRepository,
    ingest: bool,
) -> None:
    if not is_dataset_readable_by_earthscale(dataset):
        logger.warning(
            f"Dataset {dataset.name} is not readable by Earthscale backend."
            + (
                "Not ingesting dataset as --ingest flag was not provided."
                if not ingest
                else "Ingesting dataset to Earthscale's shared storage..."
            )
        )
        if not ingest:
            return
        validate_if_dataset_is_ingestable(dataset)
        dataset = ingest_dataset_to_earthscale(dataset)
        logger.info("Dataset ingested successfully.")
    dataset_repo.add(dataset)


@cli.command(help="Register datasets from a Python module.")
@click.argument("module")
@click.option(
    "--ingest",
    is_flag=True,
    help="Ingest any datasets that are not already in Earthscale's shared storage.",
)
def register(
    module: str,
    ingest: bool,
) -> None:
    # Add cwd to sys.path
    sys.path.insert(0, os.getcwd())

    # Look for all Dataset instances in the module
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        logger.error(f"Error importing module {module}: {e}")
        return
    datasets = _find_datasets_for_module(mod)

    client = get_supabase_client()

    dataset_repo = DatasetRepository(
        client,
    )
    registered_datasets = []
    logger.info("Registering datasets...")
    for dataset in datasets:
        if not dataset._explicit_name:
            continue
        logger.info(f"     {dataset.name}")

        if dataset_repo.exists(dataset.name):
            logger.warning(f"Dataset {dataset.name} already exist, overwriting...")

        # TODO: for now the vector data processing POST is blocking, so we
        try:
            _register_dataset(dataset, dataset_repo, ingest)
            registered_datasets.append(dataset)
        except Exception as e:
            logger.error(f"Error registering dataset {dataset.name}: {e}")
            continue

    dset_strs = []
    for i, dataset in enumerate(registered_datasets):
        dset_strs.append(f"     {i + 1}. {dataset.name} | {type(dataset).__name__}")

    deploy_summary_msg = (
        f"Registered {len(registered_datasets)} dataset(s) from module `{module}`"
    )
    if len(registered_datasets) == 0:
        logger.info("(Hint: did you remember to add a `name` to each dataset?)")
    else:
        logger.info(deploy_summary_msg)
        logger.info("Datasets:")
    for dset in dset_strs:
        logger.info(dset)


def _earthscale_has_access(
    url: str,
    backend_url: str,
    session: requests.Session,
) -> bool:
    query_params = {"path": url}
    response = session.get(
        f"{backend_url}/ingest/has-read-access",
        params=query_params,
    )
    response.raise_for_status()
    return cast(bool, response.json())


def _add_url(url: str, name: str, backend_url: str, session: requests.Session) -> None:
    request_data = {
        "url": url,
        "name": name,
    }
    response = session.post(
        f"{backend_url}/datasets/add",
        json=request_data,
    )
    match response.status_code:
        case 500:
            response_json = response.json()
            error_message = response_json["detail"]["message"]
            logger.error(error_message)
        case 200:
            logger.info(
                f"Dataset from url '{url}' added successfully to Earthscale. It will "
                f"be available as '{name}' in the Catalog on "
                f"https://app.earthscale.ai."
            )
        case _:
            response.raise_for_status()


@cli.command(help="Add a dataset to Earthscale using only a name and a URL.")
@click.argument("url")
@click.option(
    "-n",
    "--name",
    required=True,
    help="Name of the dataset as it will appear in Earthscale.",
)
def add(
    url: str,
    name: str,
) -> None:
    backend_url = os.getenv(BACKEND_URL_ENV_VAR, DEFAULT_BACKEND_URL).rstrip("/")
    client = get_supabase_client()
    dataset_repo = DatasetRepository(client)

    session = requests.Session()
    request_headers = {
        "Authorization": f"Bearer {client.auth.get_session().access_token}"
    }
    session.headers = request_headers  # type: ignore

    if not _earthscale_has_access(url, backend_url, session):
        logger.error(
            f"Earthscale does not have access to '{url}'. Please ensure that the "
            f"dataset publicly accessible, on a shared bucket or shared with "
            f"`backend-services@earthscale.ai`."
        )
        return

    if dataset_repo.exists(name):
        logger.warning(f"Dataset '{name}' already exist. It will be overwritten.")

    _add_url(url, name, backend_url, session)


@cli.command(help="Authenticate with Earthscale.")
def authenticate() -> None:
    run_auth()


if __name__ == "__main__":
    cli()
