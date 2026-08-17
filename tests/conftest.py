# -*- coding: utf-8 -*-
"""
Shared fixtures for the Visual Phaser correctness tests.

The engine ships as `Visual_Phaser.V<version>.py` — a filename with dots in it,
so it cannot be imported by name. It is loaded here via importlib instead.
Loading is safe: the module body only reads config and defines functions, and
the executable entry point sits behind `if __name__ == "__main__"`.

The version is discovered rather than hardcoded. A pinned filename is what made
an earlier branch of these tests unmergeable the moment the shipped engine was
renamed, and the point of a regression test is to survive that.
"""
import importlib.util
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
def _newest_engine():
    """Highest-versioned Visual_Phaser.V*.py in the repo root."""
    def version_key(path):
        return [int(n) for n in re.findall(r"\d+", path.name.split("Visual_Phaser.V")[-1])]

    candidates = sorted(REPO_ROOT.glob("Visual_Phaser.V*.py"), key=version_key)
    if not candidates:
        raise RuntimeError(f"No Visual_Phaser.V*.py found in {REPO_ROOT}")
    return candidates[-1]


ENGINE_PATH = _newest_engine()
MAP_PATH = REPO_ROOT / "minmap" / "min_map.txt"


def _load_engine():
    # VP_configV1 is imported by the engine at module load time.
    sys.path.insert(0, str(REPO_ROOT))

    # `_load_runtime_config_module` treats any argv[1] ending in `.py` as a
    # config override. Under pytest that is the test file, so argv and the
    # VP_CONFIG_PATH environment variable are both neutralised for the load.
    saved_argv, saved_env = sys.argv, os.environ.get("VP_CONFIG_PATH")
    sys.argv = [saved_argv[0]]
    os.environ.pop("VP_CONFIG_PATH", None)
    try:
        spec = importlib.util.spec_from_file_location("visual_phaser_engine", ENGINE_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load engine from {ENGINE_PATH}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.argv = saved_argv
        if saved_env is not None:
            os.environ["VP_CONFIG_PATH"] = saved_env


@pytest.fixture(scope="session")
def vp():
    """The Visual Phaser engine module."""
    return _load_engine()


@pytest.fixture(scope="session")
def genetic_map():
    """The shipped GRCh37 genetic map, as {chromosome: (positions, cMs)}."""
    raw = pd.read_csv(MAP_PATH, sep="\t", header=0)
    by_chrom = {}
    for chrom, group in raw.groupby("Chromosome"):
        ordered = group.sort_values("Position")
        by_chrom[int(chrom)] = (ordered["Position"].values, ordered["cM"].values)
    return by_chrom


# --------------------------------------------------------------------------
# Synthetic DNA construction
#
# Everything below builds raw-DNA-shaped data in memory. No real genotypes are
# used anywhere in this suite: the tests assert on logic, so the inputs are
# constructed to isolate one behaviour at a time.
# --------------------------------------------------------------------------

NO_CALL = "X"


def make_individual(genotypes, chromosome=1, start=1_000_000, step=10_000, rsids=None):
    """
    Build a loaded-DNA frame in the shape `agnostic_load_individual_dna` returns.

    `genotypes` is a sequence of 2-character strings, e.g. ["AA", "AG", "XX"].
    Positions are laid out on a regular grid unless `rsids` is supplied.
    """
    n = len(genotypes)
    positions = [start + i * step for i in range(n)]
    if rsids is None:
        rsids = [f"rs{i}" for i in range(n)]
    return pd.DataFrame(
        {
            "rsid": rsids,
            "chromosome": [chromosome] * n,
            "position": positions,
            "allele1": [g[0] for g in genotypes],
            "allele2": [g[1] for g in genotypes],
        }
    )


def merge_pair(dna1, dna2, chromosome=1):
    """Reproduce the engine's pair merge exactly as `thread_chromosome` does it."""
    return pd.merge(
        dna1[dna1["chromosome"] == chromosome],
        dna2[dna2["chromosome"] == chromosome],
        on=("rsid", "chromosome", "position"),
        suffixes=("_1", "_2"),
    )


def classify(vp, dm, no_call=NO_CALL):
    """Run the engine's classifier over a merged pair frame."""
    return vp.apply_conditions_vectorized(
        dm["allele1_1"].values,
        dm["allele2_1"].values,
        dm["allele1_2"].values,
        dm["allele2_2"].values,
        no_call,
    )


def classify_one(vp, geno_x, geno_y, no_call=NO_CALL):
    """Classify a single genotype pair, e.g. classify_one(vp, "AG", "CC")."""
    return vp.apply_conditions_vectorized(
        np.array([geno_x[0]]),
        np.array([geno_x[1]]),
        np.array([geno_y[0]]),
        np.array([geno_y[1]]),
        no_call,
    )[0]
