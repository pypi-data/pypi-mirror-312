import logging

import click

from deltalake_tools.__version__ import version
from deltalake_tools.core.core import (
    delta_compact,
    delta_create_checkpoint,
    delta_vacuum,
)
from deltalake_tools.core.core import table_version as delta_table_version
from deltalake_tools.core.convert import convert_parquet_to_delta
from deltalake_tools.models.models import (
    S3ClientDetails,
    S3KeyPairWrite,
    S3Scheme,
    TableType,
    VirtualAddressingStyle,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=version)
def cli() -> None:
    pass


@cli.command()
@click.argument("delta-table-path")
@click.option("--bucket", required=False, type=str)
@click.option("--access-key-id", required=False, type=str)
@click.option("--secret-access-key", required=False, type=str)
@click.option("--region", required=False, type=str)
@click.option("--endpoint-host", required=False, type=str)
@click.option("--port", type=int, required=False)
@click.option("--scheme", type=click.Choice(["http", "https"]), required=False)
@click.option("--allow-unsafe-https", is_flag=True)
@click.option("--path-addressing-style", is_flag=True)
def compact(delta_table_path: str, **kwargs) -> None:
    client_details = parse_cli_kwargs(delta_table_path, **kwargs)

    result = delta_compact(delta_table_path, client_details=client_details)

    if result.is_err():
        print(result.unwrap_err())
    else:
        print(result.unwrap())


@cli.command()
@click.argument("delta-table-path")
@click.option("--retention-hours", default=168, type=int)
@click.option("--disable-retention-duration", is_flag=True)
@click.option("--force", is_flag=True)
@click.option("--bucket", required=False, type=str)
@click.option("--access-key-id", required=False, type=str)
@click.option("--secret-access-key", required=False, type=str)
@click.option("--region", required=False, type=str)
@click.option("--endpoint-host", required=False, type=str)
@click.option("--port", type=int, required=False)
@click.option("--scheme", type=click.Choice(["http", "https"]), required=False)
@click.option("--allow-unsafe-https", is_flag=True)
@click.option("--path-addressing-style", is_flag=True)
def vacuum(
    delta_table_path: str,
    *,
    retention_hours: int,
    disable_retention_duration: bool = False,
    force: bool = False,
    **kwargs,
) -> None:
    client_details = parse_cli_kwargs(delta_table_path, **kwargs)
    result = delta_vacuum(
        delta_table_path,
        client_details=client_details,
        retention_hours=retention_hours,
        enforce_retention_duration=not disable_retention_duration,
        dry_run=not force,
    )

    if result.is_err():
        print(result.unwrap_err())
    else:
        print(result.unwrap())


@cli.command()
@click.argument("delta-table-path")
@click.option("--bucket", required=False, type=str)
@click.option("--access-key-id", required=False, type=str)
@click.option("--secret-access-key", required=False, type=str)
@click.option("--region", required=False, type=str)
@click.option("--endpoint-host", required=False, type=str)
@click.option("--port", type=int, required=False)
@click.option("--scheme", type=click.Choice(["http", "https"]), required=False)
@click.option("--allow-unsafe-https", is_flag=True)
@click.option("--path-addressing-style", is_flag=True)
def create_checkpoint(delta_table_path: str, **kwargs) -> None:
    client_details = parse_cli_kwargs(delta_table_path, **kwargs)

    result = delta_create_checkpoint(delta_table_path, client_details=client_details)

    if result.is_err():
        print(result.unwrap_err())
    else:
        print(result.unwrap())


@cli.command()
@click.argument("delta-table-path")
@click.option("--bucket", required=False, type=str)
@click.option("--access-key-id", required=False, type=str)
@click.option("--secret-access-key", required=False, type=str)
@click.option("--region", required=False, type=str)
@click.option("--endpoint-host", required=False, type=str)
@click.option("--port", type=int, required=False)
@click.option("--scheme", type=click.Choice(["http", "https"]), required=False)
@click.option("--allow-unsafe-https", is_flag=True)
@click.option("--path-addressing-style", is_flag=True)
def table_version(delta_table_path: str, **kwargs) -> None:
    client_details = parse_cli_kwargs(delta_table_path, **kwargs)

    result = delta_table_version(delta_table_path, client_details=client_details)

    if result.is_err():
        print(result.unwrap_err())
    else:
        print(result.unwrap())


def check_delta_table_type(delta_table_path: str) -> TableType:
    if delta_table_path.startswith("s3://"):
        return TableType.S3
    else:
        return TableType.Local


@cli.command()
@click.argument("table-path")
@click.option("--inplace", is_flag=True, help="currently only supports inplace conversion")
@click.option("--infer-partitioning", is_flag=True)
@click.option("--aws-profile", required=False, type=str, help="AWS profile name. Leave blank to use environment variables.")
def parquet_to_delta(
    table_path: str, inplace: bool = False, infer_partitioning: bool = False,
    aws_profile: str = None,
) -> None:

    # logger.warning(f"{table_path=}")
    # logger.warning(f"{inplace=}")
    # logger.warning(f"{infer_partitioning=}")

    if aws_profile is not None:
        storage_options = {"aws_profile": aws_profile}
    else:
        storage_options = None

    result = convert_parquet_to_delta(
        table_path, inplace=inplace, infer_partitioning=infer_partitioning, 
        storage_options=storage_options
    )

    if result.is_err():
        print(result.unwrap_err())
    else:
        print(result.unwrap())


def parse_cli_kwargs(
    delta_table_path,
    *,
    bucket: str,
    access_key_id: str,
    secret_access_key: str,
    region: str = "us-east-1",
    endpoint_host: str,
    port: int = 443,
    scheme: str = "https",
    allow_unsafe_https: bool = False,
    path_addressing_style: bool = VirtualAddressingStyle.Path,
) -> S3ClientDetails:
    client_details: S3ClientDetails = None
    # logger.error("in the table version command")
    table_type = check_delta_table_type(delta_table_path)
    if table_type == TableType.S3:
        if bucket is None:
            raise click.BadParameter(
                "Bucket must be provided, along with storage options (see -h), when using S3 table type."
            )
        # logger.error(f"Bucket: {bucket}")
        client_details_result = S3ClientDetails.default()
        if client_details_result.is_err():
            click.echo(client_details_result.unwrap_err())

        client_details = client_details_result.unwrap()

        if bucket is not None:
            client_details.bucket = bucket

        if access_key_id is not None and secret_access_key is not None:
            client_details.hmac_keys = S3KeyPairWrite(
                access_key_id=access_key_id, secret_access_key=secret_access_key
            )

        if region is not None:
            client_details.region = region

        if endpoint_host is not None:
            client_details.endpoint_host = endpoint_host

        if port is not None:
            client_details.port = port

        if scheme is not None:
            client_details.scheme = S3Scheme(scheme)

        if allow_unsafe_https:
            client_details.allow_unsafe_https = True

        if path_addressing_style:
            client_details.virtual_addressing_style = VirtualAddressingStyle.Path

    return client_details
