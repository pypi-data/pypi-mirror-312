from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.seq import (map, empty)
from ...fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, int_1, seq as seq_1, IGetters)
from ...fable_modules.thoth_json_core.encode import seq
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..Cells.fs_cell import FsCell
from ..fs_column import FsColumn
from .cell import (encode_cols, encode_no_number, decode_cols)

def encode(col: FsColumn) -> Json:
    def _arrow229(__unit: None=None, col: Any=col) -> Json:
        value: int = col.Index or 0
        return Json(7, int(value+0x100000000 if value < 0 else value))

    def mapping(cell: FsCell, col: Any=col) -> Json:
        return encode_cols(cell)

    return Json(5, to_enumerable([("number", _arrow229()), ("cells", seq(map(mapping, col.Cells)))]))


def encode_no_numbers(col: IEnumerable_1[FsCell]) -> Json:
    def mapping(cell: FsCell, col: Any=col) -> Json:
        return encode_no_number(cell)

    return Json(5, to_enumerable([("cells", seq(map(mapping, col)))]))


def _arrow231(builder: IGetters) -> tuple[int | None, IEnumerable_1[FsCell]]:
    n: int | None
    object_arg: IOptionalGetter = builder.Optional
    n = object_arg.Field("number", int_1)
    def _arrow230(__unit: None=None) -> IEnumerable_1[FsCell] | None:
        arg_3: Decoder_1[IEnumerable_1[FsCell]] = seq_1(decode_cols(n))
        object_arg_1: IOptionalGetter = builder.Optional
        return object_arg_1.Field("cells", arg_3)

    return (n, default_arg(_arrow230(), empty()))


decode: Decoder_1[tuple[int | None, IEnumerable_1[FsCell]]] = object(_arrow231)

__all__ = ["encode", "encode_no_numbers", "decode"]

