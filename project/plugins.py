#!/usr/bin/env python3
# coding: utf-8

from pathlib import Path
from importlib import import_module
from os.path import splitext


def load_plugins(plugins_dirs, class_name):
    """ Liste tous les modules python du dossier 'plugins_dirs' """
    for p in Path(plugins_dirs).glob("*.py"):
        if str(p.stem) not in ("__init__", "base"):
            try:
                yield (
                    p.stem,
                    import_module(str(p.with_suffix("")).replace("/", "."), class_name),
                )
            except:
                print(f"error {p}")
