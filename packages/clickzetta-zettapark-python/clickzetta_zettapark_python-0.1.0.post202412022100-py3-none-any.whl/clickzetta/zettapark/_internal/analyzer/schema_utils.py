#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
import re
from typing import TYPE_CHECKING, List, Union

import clickzetta.zettapark
from clickzetta.zettapark._adaptor import ClickzettaCursor
from clickzetta.zettapark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from clickzetta.zettapark._internal.analyzer.expression import Attribute
from clickzetta.zettapark._internal.type_utils import convert_metadata_to_sp_type
from clickzetta.zettapark.exceptions import ZettaparkSQLException
from clickzetta.zettapark.types import DecimalType, LongType, StringType, BooleanType
from snowflake.connector.cursor import ResultMetadata, SnowflakeCursor

if TYPE_CHECKING:
    import clickzetta.zettapark.session

    # Refer to the docstring for ResultMetadataV2 (in cursor.py) for more information about
    # how it differs from ResultMetadata
    try:
        from snowflake.connector.cursor import ResultMetadataV2
    except ImportError:
        ResultMetadataV2 = ResultMetadata


def command_attributes() -> List[Attribute]:
    return [Attribute('"status"', StringType())]


def show_tables_attributes() -> List[Attribute]:
    # schema_name,table_name,is_view,is_materialized_view
    return [Attribute('"schema_name"', StringType(), nullable=False),
            Attribute('"table_name"', StringType(), nullable=False),
            Attribute('"is_view"', BooleanType(), nullable=False),
            Attribute('"is_materialized_view"', BooleanType(), nullable=False),
            Attribute('"is_external"', BooleanType(), nullable=False),
            Attribute('"is_dynamic"', BooleanType(), nullable=False)]


def show_volume_attributes() -> List[Attribute]:
    # relative_path,url,size,last_modified_time
    return [Attribute('"relative_path"', StringType()), Attribute('"url"', StringType()),
            Attribute('"size"', LongType()), Attribute('"last_modified_time"', StringType())]


def list_stage_attributes() -> List[Attribute]:
    return [
        Attribute('"name"', StringType()),
        Attribute('"size"', LongType()),
        Attribute('"md5"', StringType()),
        Attribute('"last_modified"', StringType()),
    ]


def remove_state_file_attributes() -> List[Attribute]:
    return [Attribute('"name"', StringType()), Attribute('"result"', StringType())]


def put_attributes() -> List[Attribute]:
    return [
        Attribute('"source"', StringType(), nullable=False),
        Attribute('"target"', StringType(), nullable=False),
        Attribute('"source_size"', DecimalType(10, 0), nullable=False),
        Attribute('"target_size"', DecimalType(10, 0), nullable=False),
        Attribute('"source_compression"', StringType(), nullable=False),
        Attribute('"target_compression"', StringType(), nullable=False),
        Attribute('"status"', StringType(), nullable=False),
        Attribute('"encryption"', StringType(), nullable=False),
        Attribute('"message"', StringType(), nullable=False),
    ]


def get_attributes() -> List[Attribute]:
    return [
        Attribute('"file"', StringType(), nullable=False),
        Attribute('"size"', DecimalType(10, 0), nullable=False),
        Attribute('"status"', StringType(), nullable=False),
        Attribute('"encryption"', StringType(), nullable=False),
        Attribute('"message"', StringType(), nullable=False),
    ]


def analyze_attributes(
    sql: str, session: "clickzetta.zettapark.session.Session"
) -> List[Attribute]:
    lowercase = sql.strip().lower()

    # SQL commands which cannot be prepared
    # https://docs.snowflake.com/en/user-guide/sql-prepare.html
    if lowercase.startswith(
        ("alter", "drop", "use", "create", "grant", "revoke", "comment")
    ):
        return command_attributes()
    if lowercase.startswith(("ls", "list")):
        return list_stage_attributes()
    if lowercase.startswith(("rm", "remove")):
        return remove_state_file_attributes()
    if lowercase.startswith("put"):
        return put_attributes()
    if lowercase.startswith("get"):
        return get_attributes()
    if lowercase.startswith("show"):
        if re.match(r"^show\s+(user\s+|table\s+)?volume", lowercase):
            return show_volume_attributes()
        if re.match(r"^show\s+tables\s*[ ;]?$", lowercase):
            return show_tables_attributes()
        else:
            raise ZettaparkSQLException(f"not support cmd {sql}.")
    if lowercase.startswith("describe"):
        session._run_query(sql)
        return convert_result_meta_to_attribute(
            session._conn._cursor.description  # pyright: ignore
        )

    return session._get_result_attributes(sql)


def convert_result_meta_to_attribute(
    meta: Union[List[ResultMetadata], List["ResultMetadataV2"]],  # pyright: ignore
) -> List[Attribute]:
    # ResultMetadataV2 may not currently be a type, depending on the connector
    # version, so the argument types are pyright ignored

    attributes = []
    for column_metadata in meta:
        quoted_name = quote_name_without_upper_casing(column_metadata.name)
        attributes.append(
            Attribute(
                quoted_name,
                convert_metadata_to_sp_type(column_metadata),
                column_metadata.null_ok,  # pyright: ignore
            )
        )
    return attributes


def get_new_description(
    cursor: SnowflakeCursor,
) -> Union[List[ResultMetadata], List["ResultMetadataV2"]]:  # pyright: ignore
    """Return the description of a cursor using the new metadata format, if possible.

    If an older connector is in use, this function falls back to the old metadata format.
    """

    # ResultMetadataV2 may not currently be a type, depending on the connector
    # version, so the argument types are pyright ignored

    if hasattr(cursor, "_description_internal"):
        # Pyright does not perform narrowing here
        return cursor._description_internal  # pyright: ignore
    else:
        return cursor.description


def run_new_describe(
    cursor: ClickzettaCursor, query: str
) -> Union[List[ResultMetadata], List["ResultMetadataV2"]]:  # pyright: ignore
    """Execute describe() on a cursor, returning the new metadata format if possible.

    If an older connector is in use, this function falls back to the old metadata format.
    """

    # ResultMetadataV2 may not currently be a type, depending on the connector
    # version, so the argument types are pyright ignored

    if hasattr(cursor, "_describe_internal"):
        # Pyright does not perform narrowing here
        return cursor._describe_internal(query)  # pyright: ignore
    else:
        query = f"select * from ({query}) limit 0"
        cursor.execute(query)
        return cursor.description  # pyright: ignore
