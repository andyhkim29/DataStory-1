#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: run_notebook_cells.py <notebook.ipynb>", file=sys.stderr)
        return 1

    notebook_path = Path(sys.argv[1]).resolve()
    notebook = json.loads(notebook_path.read_text())
    globals_dict = {"__name__": "__main__", "__file__": str(notebook_path)}

    for index, cell in enumerate(notebook.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        print(f"[run_notebook_cells] executing cell {index}")
        exec(compile(source, f"{notebook_path}#cell-{index}", "exec"), globals_dict)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
