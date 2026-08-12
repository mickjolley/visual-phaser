# -*- coding: utf-8 -*-
"""
Issue 1 — no-call handling in `apply_conditions_vectorized`.

A no-call means "we do not know the alleles here". The engine must never treat
absence of data as positive evidence of a fully-identical region (FIR), and it
must recognise a no-call wherever it appears in the genotype — not only in the
first allele.

See SCIENTIFIC_AUDIT.md, Issue 1.
"""
import numpy as np
import pytest

from conftest import NO_CALL, classify, classify_one, make_individual, merge_pair

# The engine's own defaults, from VP_configV1.py.
FIR_CUTOFF = 1
FIR_SNP_MIN = 75
HIR_CUTOFF = 7
HIR_SNP_MIN = 200
MM_DIST = 1000


class TestNoCallDetection:
    """A no-call must be recognised in either allele, for either individual."""

    @pytest.mark.parametrize(
        "geno_x, geno_y, description",
        [
            (f"A{NO_CALL}", f"A{NO_CALL}", "both individuals half-called"),
            (f"A{NO_CALL}", "AA", "individual X half-called"),
            ("AA", f"A{NO_CALL}", "individual Y half-called"),
            (f"{NO_CALL}A", f"{NO_CALL}A", "no-call in the first allele of both"),
            (f"{NO_CALL}{NO_CALL}", "AA", "individual X entirely no-call"),
        ],
    )
    def test_no_call_is_never_classified_as_fully_identical(
        self, vp, geno_x, geno_y, description
    ):
        """
        `limegreen` is the FIR class — it is what increments `fsnps` and drives
        FIR segment emission in `scan_genomes_optimized`. Missing data must not
        reach it.
        """
        result = classify_one(vp, geno_x, geno_y)
        assert result != "limegreen", (
            f"{description}: X={geno_x} Y={geno_y} was classified as "
            f"'limegreen' (fully identical), but at least one allele is unknown"
        )

    def test_no_call_token_is_not_compared_as_a_base(self, vp):
        """
        With the no-call guard only covering allele 1, the token leaks into the
        allele comparison and is matched against itself as though it were a real
        base. Two individuals whose second allele is unknown must not be called
        fully identical on the strength of `X == X`.
        """
        result = classify_one(vp, f"A{NO_CALL}", f"A{NO_CALL}")
        assert result != "limegreen", (
            "the no-call token matched itself and produced a fully-identical "
            "call from two unknown alleles"
        )

    def test_no_call_still_preserves_hir_continuity(self, vp):
        """
        The author's stated intent is that no-calls do not shatter segments.
        That must be preserved: a no-call has to remain a class that
        `scan_genomes_optimized` counts as continuing an HIR run, i.e. one of
        ('yellow', 'limegreen') — never 'crimson'.
        """
        result = classify_one(vp, f"A{NO_CALL}", f"G{NO_CALL}")
        assert result in ("yellow", "limegreen"), (
            f"a no-call was classified as '{result}', which terminates the "
            f"enclosing HIR segment instead of bridging it"
        )


class TestNoCallDoesNotFabricateSegments:
    """End-to-end: a run of no-calls must not manufacture an FIR segment."""

    @staticmethod
    def _no_call_run(n_snps=250, chromosome=1, start=100_000_000, step=20_000):
        """
        Two individuals, both half-called across a contiguous block. Every
        second allele is unknown, so nothing here supports a fully-identical
        call anywhere in the block.
        """
        genotypes = [f"A{NO_CALL}"] * n_snps
        dna1 = make_individual(genotypes, chromosome, start, step)
        dna2 = make_individual(genotypes, chromosome, start, step)
        return merge_pair(dna1, dna2, chromosome)

    def test_run_of_no_calls_produces_no_fir_segment(self, vp, genetic_map):
        chromosome = 1
        map_positions, map_cms = genetic_map[chromosome]
        dm = self._no_call_run(chromosome=chromosome)

        # Precondition: the block is long enough and wide enough that a
        # fabricated FIR would clear both the SNP-count and cM gates. Without
        # this the test could pass for the wrong reason.
        span_cm = np.interp(dm["position"].max(), map_positions, map_cms) - np.interp(
            dm["position"].min(), map_positions, map_cms
        )
        assert len(dm) > FIR_SNP_MIN, "test block too short to clear FIR_SNP_MIN"
        assert span_cm > FIR_CUTOFF, "test block too narrow to clear FIR_CUTOFF"

        dm["match"] = classify(vp, dm)
        _, firs = vp.scan_genomes_optimized(
            dm,
            chromosome,
            HIR_CUTOFF,
            FIR_CUTOFF,
            HIR_SNP_MIN,
            FIR_SNP_MIN,
            MM_DIST,
            map_positions,
            map_cms,
        )

        assert firs.empty, (
            f"{len(firs)} fully-identical segment(s) totalling "
            f"{firs['Length (cM)'].sum() if not firs.empty else 0} cM were "
            f"reported across a region where every genotype is half no-call — "
            f"missing data was counted as FIR evidence"
        )

    def test_genuine_fir_is_still_detected(self, vp, genetic_map):
        """
        Guard against over-correcting: real fully-identical genotypes must
        still produce an FIR segment.
        """
        chromosome = 1
        map_positions, map_cms = genetic_map[chromosome]
        genotypes = ["AG"] * 250
        dna1 = make_individual(genotypes, chromosome, 100_000_000, 20_000)
        dna2 = make_individual(genotypes, chromosome, 100_000_000, 20_000)
        dm = merge_pair(dna1, dna2, chromosome)
        dm["match"] = classify(vp, dm)

        _, firs = vp.scan_genomes_optimized(
            dm,
            chromosome,
            HIR_CUTOFF,
            FIR_CUTOFF,
            HIR_SNP_MIN,
            FIR_SNP_MIN,
            MM_DIST,
            map_positions,
            map_cms,
        )

        assert not firs.empty, (
            "a block of identical heterozygous genotypes produced no FIR "
            "segment — the no-call fix has suppressed genuine FIR detection"
        )
