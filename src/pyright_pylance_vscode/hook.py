import json
import platform
import sys
import tempfile
from pathlib import Path
from pprint import pprint

import pyright.cli


def entrypoint():
    sys.exit(main().returncode)


def main():
    config_overrides = {}
    files = []
    args = sys.argv[1:]

    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            config_overrides[args[i][2:]] = args[i + 1]
            i += 2
            continue
        files.append(args[i])
        i += 1

    source_config_file = Path(__file__).parent / "defaults.json"
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_config_file = Path(temp_dir) / "defaults.json"
        with open(source_config_file, "r") as fh:
            config = json.load(fh)
            config["pythonVersion"] = platform.python_version()
            config["pythonPlatform"] = platform.platform()

        merged_config = {**config, **config_overrides}

        with open(temp_config_file, "w") as fh:
            json.dump(merged_config, fh, indent=2)

        return pyright.cli.run("--project", str(temp_config_file), *files)
