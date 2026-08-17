# -*- coding: utf-8 -*-
"""
Issue 2 — genome build / coordinate-system assumptions.

The engine is hard-wired to GRCh37: the bundled `min_map.txt` and the
`chr_lens` table are both build 37, and nothing validates that the input files
use the same coordinate system. Two silent failure modes follow.

  (a) Two files on different builds carry the same rsIDs at different
      positions. `position` is part of the pair merge key, so almost nothing
      joins and the tool reports that two people share no DNA.

  (b) `np.interp` clamps out-of-range positions instead of raising, so a
      segment reaching past the mapped region gets a silently truncated cM
      length -- or a fabricated 0.0.

See SCIENTIFIC_AUDIT.md, Issue 2.
"""
import numpy as np
import pytest

from conftest import make_individual, merge_pair

# A GRCh37 -> GRCh38 lift shifts coordinates by a locus-dependent amount. The
# exact value is irrelevant here; what matters is that the same marker sits at
# a different position, which is what a build difference looks like in the data.
BUILD_SHIFT = 64_620


def _same_person_two_builds(n_snps=500, chromosome=1):
    """
    One individual's genotypes, expressed on two different coordinate systems.

    Same rsIDs, same alleles, shifted positions. Compared against itself this
    must look like a perfect match; anything less is an artefact of the
    coordinate mismatch rather than biology.
    """
    genotypes = ["AG"] * n_snps
    rsids = [f"rs{i}" for i in range(n_snps)]
    build37 = make_individual(
        genotypes, chromosome, start=100_000_000, step=20_000, rsids=rsids
    )
    build38 = make_individual(
        genotypes,
        chromosome,
        start=100_000_000 + BUILD_SHIFT,
        step=20_000,
        rsids=rsids,
    )
    return build37, build38


class TestCrossBuildComparison:
    def test_build_mismatch_is_detected_rather_than_silently_dropping_snps(self, vp):
        """
        The same person on two builds must not be reportable as sharing
        nothing. The engine has to notice the coordinate systems disagree.
        """
        build37, build38 = _same_person_two_builds()

        # Demonstrate the silent failure this guards against: the merge that
        # drives every downstream comparison collapses to nothing.
        merged = merge_pair(build37, build38)
        assert len(merged) == 0, (
            "test fixture is not exercising the defect -- the two coordinate "
            "systems still overlap"
        )
        assert len(merge_pair(build37, build37)) == 500, (
            "sanity check: on a common build these same markers all join"
        )

        problems = vp.check_coordinate_consistency(
            {"Alice_b37": build37, "Alice_b38": build38}
        )
        assert problems, (
            "two files on different coordinate systems produced no warning; "
            "every downstream comparison between them silently reports no "
            "shared DNA"
        )
        joined = " ".join(problems)
        assert "Alice_b37" in joined and "Alice_b38" in joined, (
            f"the report must name the individuals involved, got: {problems}"
        )

    def test_consistent_coordinates_are_not_flagged(self, vp):
        """Guard against a detector that cries wolf on well-formed input."""
        build37, _ = _same_person_two_builds()
        sibling = make_individual(
            ["AC"] * 500,
            chromosome=1,
            start=100_000_000,
            step=20_000,
            rsids=[f"rs{i}" for i in range(500)],
        )
        problems = vp.check_coordinate_consistency(
            {"Alice": build37, "Bob": sibling}
        )
        assert not problems, (
            f"two files on the same coordinate system were flagged as a build "
            f"mismatch: {problems}"
        )

    def test_partial_overlap_is_tolerated(self, vp):
        """
        Different chip versions legitimately share only some markers at
        identical positions. That is not a build mismatch and must not be
        reported as one.
        """
        rsids = [f"rs{i}" for i in range(500)]
        alice = make_individual(
            ["AG"] * 500, 1, start=100_000_000, step=20_000, rsids=rsids
        )
        # Bob is tested on a chip carrying only every other marker.
        bob = alice.iloc[::2].reset_index(drop=True)
        problems = vp.check_coordinate_consistency({"Alice": alice, "Bob": bob})
        assert not problems, (
            f"partial marker overlap on a common build was misreported as a "
            f"coordinate mismatch: {problems}"
        )


class TestGeneticMapCoverage:
    def test_snps_outside_the_mapped_region_are_reported(self, vp, genetic_map):
        """
        chr21's map starts at 10,865,933. SNPs below that are silently clamped
        to the first mapped cM, so a real segment there measures 0.000 cM and
        vanishes. The user must be told the map does not cover their data.
        """
        chromosome = 21
        map_positions, _ = genetic_map[chromosome]
        positions = np.arange(1_000_000, 9_000_000, 20_000)
        assert positions.max() < map_positions.min(), (
            "test fixture must sit entirely below the mapped region"
        )

        warning = vp.check_map_coverage(chromosome, positions, map_positions)
        assert warning, (
            "SNPs falling entirely outside the genetic map produced no "
            "warning; every segment there is measured against a clamped "
            "boundary value"
        )
        assert "21" in str(warning), (
            f"the warning must name the chromosome, got: {warning}"
        )

    def test_fully_covered_chromosome_is_not_flagged(self, vp, genetic_map):
        chromosome = 1
        map_positions, _ = genetic_map[chromosome]
        positions = np.arange(100_000_000, 110_000_000, 20_000)
        warning = vp.check_map_coverage(chromosome, positions, map_positions)
        assert not warning, (
            f"SNPs well inside the mapped region were flagged: {warning}"
        )

    def test_segment_entirely_off_the_map_is_not_measured_as_zero(
        self, vp, genetic_map
    ):
        """
        `np.interp` clamps, so both endpoints of an off-map segment collapse to
        the same boundary cM and the length comes out as exactly 0.0. Zero is a
        measurement; this length is unknown. It must not be reported as a number.
        """
        chromosome = 21
        map_positions, map_cms = genetic_map[chromosome]
        genotypes = ["AG"] * 300
        dna = make_individual(genotypes, chromosome, start=1_000_000, step=20_000)
        dm = merge_pair(dna, dna, chromosome)
        assert dm["position"].max() < map_positions.min()

        dm["match"] = vp.apply_conditions_vectorized(
            dm["allele1_1"].values,
            dm["allele2_1"].values,
            dm["allele1_2"].values,
            dm["allele2_2"].values,
            "X",
        )
        hirs, firs = vp.scan_genomes_optimized(
            dm, chromosome, 7, 1, 200, 75, 1000, map_positions, map_cms
        )

        for name, table in (("HIR", hirs), ("FIR", firs)):
            if table.empty:
                continue
            assert not (table["Length (cM)"] == 0.0).any(), (
                f"a {name} segment lying entirely outside the genetic map was "
                f"reported with a fabricated length of 0.0 cM"
            )
