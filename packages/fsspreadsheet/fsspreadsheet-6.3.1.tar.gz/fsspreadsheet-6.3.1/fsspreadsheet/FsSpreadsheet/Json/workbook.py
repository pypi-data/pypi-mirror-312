from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.seq import map
from ...fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ...fable_modules.thoth_json_core.decode import (object, seq as seq_1, IRequiredGetter, IGetters)
from ...fable_modules.thoth_json_core.encode import seq
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fs_workbook import FsWorkbook
from ..fs_worksheet import FsWorksheet
from .worksheet import (encode_rows as encode_rows_1, decode_rows as decode_rows_1, encode_columns as encode_columns_1, decode_columns as decode_columns_1)

def encode_rows(no_numbering: bool, wb: FsWorkbook) -> Json:
    def mapping(sheet: FsWorksheet, no_numbering: Any=no_numbering, wb: Any=wb) -> Json:
        return encode_rows_1(no_numbering, sheet)

    return Json(5, to_enumerable([("sheets", seq(map(mapping, wb.GetWorksheets())))]))


def _arrow235(builder: IGetters) -> FsWorkbook:
    wb: FsWorkbook = FsWorkbook()
    ws: IEnumerable_1[FsWorksheet]
    arg_1: Decoder_1[IEnumerable_1[FsWorksheet]] = seq_1(decode_rows_1)
    object_arg: IRequiredGetter = builder.Required
    ws = object_arg.Field("sheets", arg_1)
    wb.AddWorksheets(ws)
    return wb


decode_rows: Decoder_1[FsWorkbook] = object(_arrow235)

def encode_columns(no_numbering: bool, wb: FsWorkbook) -> Json:
    def mapping(sheet: FsWorksheet, no_numbering: Any=no_numbering, wb: Any=wb) -> Json:
        return encode_columns_1(no_numbering, sheet)

    return Json(5, to_enumerable([("sheets", seq(map(mapping, wb.GetWorksheets())))]))


def _arrow236(builder: IGetters) -> FsWorkbook:
    wb: FsWorkbook = FsWorkbook()
    ws: IEnumerable_1[FsWorksheet]
    arg_1: Decoder_1[IEnumerable_1[FsWorksheet]] = seq_1(decode_columns_1)
    object_arg: IRequiredGetter = builder.Required
    ws = object_arg.Field("sheets", arg_1)
    wb.AddWorksheets(ws)
    return wb


decode_columns: Decoder_1[FsWorkbook] = object(_arrow236)

__all__ = ["encode_rows", "decode_rows", "encode_columns", "decode_columns"]

