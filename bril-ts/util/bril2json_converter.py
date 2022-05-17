import json

from pybril import PyBril


def convert(bril_files):
    BRIL_BINARIES = "/Users/victorgiannakouris/Dev/bril/.venv/bin"

    for bril in bril_files:
        brilpy = PyBril(bril_binaries_path=BRIL_BINARIES)
        code = brilpy.bril2json(bril)

        json.dump(code, open(bril.replace(".bril", ".json"), "w+"), indent=2)



