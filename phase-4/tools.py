from pathlib import Path
import json
from error import ToolError
import csv, io
from decimal import Decimal, InvalidOperation


ROOT = (Path(__file__).parent / "workdir").resolve()
confine = True
MAX_CHUNKS=8000


def _is_safe(path : str) -> Path:
    p = (ROOT/path).resolve()
    if confine and not p.is_relative_to(ROOT) :
        raise ToolError(f"refused: '{path}' resolves outside the sandbox")
    return p


def read_file(path : str):
    p = _is_safe(path)

    if not p.is_file():
        raise ToolError(f"no such file: '{path}'")

    text = p.read_text(encoding="utf-8", errors="replace")
    if len(text) > MAX_CHUNKS:
         return text[:MAX_CHUNKS] + f"\n[truncated - {len(text)} chars total]"

    return text


def list_files(directory : str):
    names = []

    p = _is_safe(directory)
    if not p.is_dir():
        raise ToolError("it is not a directory")

    for d in p.iterdir():
        name = d.name
        if d.is_dir():
            name = name + "/"
        names.append(name)

    names = sorted(names)

    text = "\n".join(names)
    if text == "":                    
        text = "(empty)"
    
    return text


def write_file(content : str, path : str):
   p = _is_safe(path)
   existed = p.is_file()
   p.write_text(content,encoding="utf-8")

   return f"{'overwrote' if existed else 'wrote'}"


def sum_column(path : str, filter_column : str, filter_value : str, amount_column : str) -> str:
    """Exact arithmetic in Python. The model picks the file and the filter;
    it never adds the numbers itself."""
    p = _is_safe(path)
    if not p.is_file():
        raise ToolError(f"no such file: '{path}'")

    reader = csv.DictReader(io.StringIO(p.read_text(encoding="utf-8")))
    header = reader.fieldnames or []
    for col in (filter_column, amount_column):
        if col not in header:
            raise ToolError(f"no column '{col}' in {path}. columns are: {', '.join(header)}")

    total, matched, seen = Decimal("0"), 0, 0
    for i, r in enumerate(reader, start=2):
        seen += 1
        if r[filter_column] != filter_value:
            continue
        try:
            total += Decimal(r[amount_column])
        except InvalidOperation:
            raise ToolError(f"row {i}: '{r[amount_column]}' in column '{amount_column}' is not a number")
        matched += 1

    return (f"{path}: sum of '{amount_column}' where {filter_column} == '{filter_value}' "
            f"= {total} ({matched} of {seen} rows matched)")


TOOLS = {"read_file" : read_file, "write_file" : write_file, "list_files" : list_files, "sum_column" : sum_column}



