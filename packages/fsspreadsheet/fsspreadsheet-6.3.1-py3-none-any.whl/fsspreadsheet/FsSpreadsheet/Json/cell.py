from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.util import to_enumerable
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, int_1, IGetters)
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..Cells.fs_cell import (FsCell, DataType)
from ..fs_address import FsAddress__ctor_Z37302880
from .value import (encode, decode)

def encode_no_number(cell: FsCell) -> Json:
    return Json(5, to_enumerable([("value", encode(cell.Value))]))


def encode_rows(cell: FsCell) -> Json:
    def _arrow218(__unit: None=None, cell: Any=cell) -> Json:
        value_1: int = cell.ColumnNumber or 0
        return Json(7, int(value_1+0x100000000 if value_1 < 0 else value_1))

    return Json(5, to_enumerable([("column", _arrow218()), ("value", encode(cell.Value))]))


def decode_rows(row_number: int | None=None) -> Decoder_1[FsCell]:
    def _arrow221(builder: IGetters, row_number: Any=row_number) -> FsCell:
        def _arrow219(__unit: None=None) -> tuple[Any, DataType] | None:
            object_arg: IOptionalGetter = builder.Optional
            return object_arg.Field("value", decode)

        pattern_input: tuple[Any, DataType] = default_arg(_arrow219(), ("", DataType(4)))
        def _arrow220(__unit: None=None) -> int | None:
            object_arg_1: IOptionalGetter = builder.Optional
            return object_arg_1.Field("column", int_1)

        c: int = default_arg(_arrow220(), 0) or 0
        return FsCell(pattern_input[0], pattern_input[1], FsAddress__ctor_Z37302880(default_arg(row_number, 0), c))

    return object(_arrow221)


def encode_cols(cell: FsCell) -> Json:
    def _arrow222(__unit: None=None, cell: Any=cell) -> Json:
        value_1: int = cell.RowNumber or 0
        return Json(7, int(value_1+0x100000000 if value_1 < 0 else value_1))

    return Json(5, to_enumerable([("row", _arrow222()), ("value", encode(cell.Value))]))


def decode_cols(col_number: int | None=None) -> Decoder_1[FsCell]:
    def _arrow225(builder: IGetters, col_number: Any=col_number) -> FsCell:
        def _arrow223(__unit: None=None) -> tuple[Any, DataType] | None:
            object_arg: IOptionalGetter = builder.Optional
            return object_arg.Field("value", decode)

        pattern_input: tuple[Any, DataType] = default_arg(_arrow223(), ("", DataType(4)))
        def _arrow224(__unit: None=None) -> int | None:
            object_arg_1: IOptionalGetter = builder.Optional
            return object_arg_1.Field("row", int_1)

        return FsCell(pattern_input[0], pattern_input[1], FsAddress__ctor_Z37302880(default_arg(_arrow224(), 0), default_arg(col_number, 0)))

    return object(_arrow225)


__all__ = ["encode_no_number", "encode_rows", "decode_rows", "encode_cols", "decode_cols"]

