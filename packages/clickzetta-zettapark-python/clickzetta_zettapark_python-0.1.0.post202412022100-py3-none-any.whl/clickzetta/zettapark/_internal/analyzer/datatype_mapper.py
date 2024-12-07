#!/usr/bin/env python3
#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import binascii
import json
import math
from array import array
from collections.abc import Iterable
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from typing import Any

import clickzetta.zettapark._internal.analyzer.analyzer_utils as analyzer_utils
from clickzetta.zettapark._internal.type_utils import convert_sp_to_cz_type
from clickzetta.zettapark._internal.utils import PythonObjJSONEncoder
from clickzetta.zettapark.types import (
    ArrayType,
    BinaryType,
    BooleanType,
    DataType,
    DateType,
    DecimalType,
    GeographyType,
    GeometryType,
    MapType,
    NullType,
    StringType,
    StructType,
    TimestampTimeZone,
    TimestampType,
    TimeType,
    VariantType,
    VectorType,
    _FractionalType,
    _IntegralType,
    _NumericType,
)

MILLIS_PER_DAY = 24 * 3600 * 1000
MICROS_PER_MILLIS = 1000


def str_to_sql(value: str) -> str:
    sql_str = str(value).replace("\\", "\\\\").replace("'", "''").replace("\n", "\\n")
    return f"'{sql_str}'"


def _to_vector_literal(value: Iterable, datatype: VectorType) -> str:
    if datatype.element_type == "tinyint":
        return "VECTOR(" + ", ".join(str(int(i)) + "Y" for i in value) + ")"
    elif datatype.element_type == "int":
        return "VECTOR(" + ", ".join(str(int(i)) for i in value) + ")"
    elif datatype.element_type == "float":
        return "VECTOR(" + ", ".join(str(float(i)) + "F" for i in value) + ")"
    raise TypeError(f"Unsupported VectorType: {datatype}")


def to_sql(value: Any, datatype: DataType, from_values_statement: bool = False) -> str:
    """Convert a value with DataType to a snowflake compatible sql"""

    # Handle null values
    if isinstance(
        datatype,
        (NullType, ArrayType, MapType, StructType, GeographyType, GeometryType),
    ):
        if value is None:
            return "NULL"
    if isinstance(
        datatype,
        (
            BinaryType,
            _IntegralType,
            _FractionalType,
            TimestampType,
            StringType,
            BooleanType,
            VariantType,
            VectorType,
        ),
    ):
        if value is None:
            return f"CAST(NULL AS {convert_sp_to_cz_type(datatype)})"
    if value is None:
        return "NULL"

    # Not nulls
    if isinstance(value, str) and isinstance(datatype, StringType):
        # If this is used in a values statement (e.g., create_dataframe),
        # the sql value has to be casted to make sure the varchar length
        # will not be limited.
        return (
            f"CAST({str_to_sql(value)} AS {analyzer_utils.string(datatype.length)})"
            if from_values_statement
            else str_to_sql(value)
        )

    if isinstance(datatype, _IntegralType):
        return f"CAST({value} AS {convert_sp_to_cz_type(datatype)})"

    if isinstance(datatype, BooleanType):
        return f"CAST({value} AS BOOLEAN)"

    if isinstance(value, float) and isinstance(datatype, _FractionalType):
        if math.isnan(value):
            cast_value = "'NAN'"
        elif math.isinf(value) and value > 0:
            cast_value = "'INF'"
        elif math.isinf(value) and value < 0:
            cast_value = "'-INF'"
        else:
            cast_value = f"'{value}'"
        return f"CAST({cast_value} AS {convert_sp_to_cz_type(datatype)})"

    if isinstance(value, Decimal) and isinstance(datatype, DecimalType):
        format_ = f"{{:.{datatype.scale}f}}"
        value = format_.format(value, datatype=datatype)
        return f"CAST({value} AS DECIMAL({datatype.precision}, {datatype.scale}))"

    if isinstance(datatype, DateType):
        if isinstance(value, int):
            # add value as number of days to 1970-01-01
            target_date = date(1970, 1, 1) + timedelta(days=value)
            return f"DATE '{target_date.isoformat()}'"
        elif isinstance(value, date):
            return f"DATE '{value.isoformat()}'"
        elif isinstance(value, str):
            return f"DATE '{value}'"

    if isinstance(datatype, TimestampType):
        if isinstance(value, (int, str, datetime)):
            if isinstance(value, int):
                # add value as microseconds to 1970-01-01 00:00:00.00.
                value = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(
                    microseconds=value
                )
            if datatype.tz == TimestampTimeZone.NTZ:
                return f"TIMESTAMP_NTZ '{value}'"
            elif datatype.tz == TimestampTimeZone.LTZ:
                return f"TIMESTAMP_LTZ '{value}'"
            # NOTE: we dont support TIMESTAMP_TZ yet.
            # elif datatype.tz == TimestampTimeZone.TZ:
            #     return f"CAST('{value}' AS TIMESTAMP_TZ)"
            else:
                return f"TIMESTAMP '{value}'"

    if isinstance(datatype, TimeType):
        if isinstance(value, time):
            trimmed_ms = value.strftime("%H:%M:%S.%f")[:-3]
            return f"TIME('{trimmed_ms}')"
        if isinstance(value, str):
            return f"TIME('{value}')"

    if isinstance(value, (list, bytes, bytearray)) and isinstance(datatype, BinaryType):
        if isinstance(value, (list, bytearray)):
            return f"CAST('{binascii.hexlify(bytes(value)).decode()}' AS BINARY)"
        else:
            return f"CAST('{bytes(value).decode('utf-8')}' AS BINARY)"

    if isinstance(value, (list, tuple, array)) and isinstance(datatype, ArrayType):
        return f"CAST(JSON {str_to_sql(json.dumps(value, cls=PythonObjJSONEncoder))} AS {convert_sp_to_cz_type(datatype)})"

    if isinstance(value, dict) and isinstance(datatype, MapType):
        return f"CAST(JSON {str_to_sql(json.dumps(value, cls=PythonObjJSONEncoder))} AS {convert_sp_to_cz_type(datatype)})"

    # NOTE: We dont support variant type yet.
    # if isinstance(datatype, VariantType):
    #     # PARSE_JSON returns VARIANT, so no need to append :: VARIANT here explicitly.
    #     return f"PARSE_JSON({str_to_sql(json.dumps(value, cls=PythonObjJSONEncoder))})"

    if isinstance(datatype, VectorType) and isinstance(value, Iterable):
        return _to_vector_literal(value, datatype)

    raise TypeError(f"Unsupported datatype {datatype}, value {value} by to_sql()")


def schema_expression(data_type: DataType, is_nullable: bool) -> str:
    if is_nullable:
        return "CAST(NULL AS " + convert_sp_to_cz_type(data_type) + ")"

    if isinstance(data_type, _NumericType):
        return f"CAST(0 AS {convert_sp_to_cz_type(data_type)})"
    if isinstance(data_type, StringType):
        return f"CAST('a' AS {analyzer_utils.varchar(data_type.length)})"
    if isinstance(data_type, BinaryType):
        return "CAST('01' AS BINARY)"
    if isinstance(data_type, DateType):
        return "DATE '2020-9-16'"
    if isinstance(data_type, BooleanType):
        return "true"
    # if isinstance(data_type, TimeType): # not supported
    #     return "to_time('04:15:29.999')"
    if isinstance(data_type, TimestampType):
        if data_type.tz == TimestampTimeZone.NTZ:
            return "TIMESTAMP_NTZ '2020-09-16 06:30:00'"
        elif data_type.tz == TimestampTimeZone.LTZ:
            return "TIMESTAMP_LTZ '2020-09-16 06:30:00'"
        # elif data_type.tz == TimestampTimeZone.TZ: # not supported
        #     return "to_timestamp_tz('2020-09-16 06:30:00')"
        else:
            return "TIMESTAMP '2020-09-16 06:30:00'"
    if isinstance(data_type, ArrayType):
        return f"ARRAY({schema_expression(data_type.element_type, False)})"
    if isinstance(data_type, MapType):
        key_expr = schema_expression(data_type.key_type, False)
        value_expr = schema_expression(data_type.value_type, False)
        return f"MAP({key_expr}, {value_expr})"
    # if isinstance(data_type, VariantType): # not supported
    #     return "to_variant(0)"
    # if isinstance(data_type, GeographyType): # not supported
    #     return "to_geography('POINT(-122.35 37.55)')"
    # if isinstance(data_type, GeometryType): # not supported
    #     return "to_geometry('POINT(-122.35 37.55)')"
    if isinstance(data_type, VectorType):

        def zero_gen(count: int, suffix: str):
            for _ in range(count):
                yield str(0) + suffix

        if data_type.element_type == "tinyint":
            return "VECTOR(" + ", ".join(zero_gen(data_type.dimension, "Y")) + ")"
        if data_type.element_type == "int":
            return "VECTOR(" + ", ".join(zero_gen(data_type.dimension, "")) + ")"
        elif data_type.element_type == "float":
            return "VECTOR(" + ", ".join(zero_gen(data_type.dimension, "F")) + ")"
        else:
            raise TypeError(f"Invalid vector element type: {data_type.element_type}")

    raise Exception(f"Unsupported data type: {data_type.__class__.__name__}")


def to_sql_without_cast(value: Any, datatype: DataType) -> str:
    if value is None:
        return "NULL"
    if isinstance(datatype, StringType):
        return f"'{value}'"
    return str(value)
