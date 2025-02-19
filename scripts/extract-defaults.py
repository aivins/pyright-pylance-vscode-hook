#!/usr/bin/env python

import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = PROJECT_ROOT / "src/pyright_pylance_vscode/defaults.json"

parser = argparse.ArgumentParser(
    description="Extract Pyright defaults from Pylance VSCode extension and write to source"
)
parser.add_argument(
    "pyright_config_schema", type=Path, help="Path to pyrightconfig.schema.json"
)
options = parser.parse_args()


with open(options.pyright_config_schema, "r") as fh:
    config_schema = json.load(fh)

definitions = config_schema["definitions"]


def extract_value(entry):
    value = entry.get("default", None) or entry.get("items", {}).get("default", None)
    entry_type = entry.get("type", "string")
    if entry_type == "array":
        if not isinstance(value, list):
            value = [value] if value is not None and value != "" else []
    elif entry_type == "boolean":
        if value is None:
            value = False
    return value


defaults = {key: extract_value(entry) for key, entry in definitions.items()}


with open(OUTPUT_FILE, "w") as fh:
    json.dump(defaults, fh, indent=2)
