from pathlib import Path
import json
from error import ToolError


ROOT = (Path(__file__).parent / "workdir").resolve()
confine = True
MAX_CHUNKS=300


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
        return text[:MAX_CHUNKS]

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


TOOLS = {"read_file" : read_file, "write_file" : write_file, "list_files" : list_files}



