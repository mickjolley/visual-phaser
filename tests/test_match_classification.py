# -*- coding: utf-8 -*-
"""
Issue 3 — exclusions are only detected when both individuals are homozygous.

`crimson` is the no-match (NIR) class. Its condition requires *both*
individuals to be homozygous:

    cond_crimson = (al1x == al2x) & (al1y == al2y) & (al1x != al1y)

So any genotype pair that shares no allele but has a heterozygote on either
side falls through to the `yellow` default, which is the *half-identical*
class. Those SNPs then count toward `nsnps` and keep the HIR run alive in
`scan_genomes_optimized`, actively extending a shared segment through a region
where the two people demonstrably do not match.

See SCIENTIFIC_AUDIT.md, Issue 3.
"""
import numpy as np
import pytest

from conftest import NO_CALL, classify, classify_one, make_individual, merge_pair

HIR_CUTOFF = 7
HIR_SNP_MIN = 200
FIR_CUTOFF = 1
FIR_SNP_MIN = 75
MM_DIST = 1000


class TestExclusionDetection:
    @pytest.mark.parametrize(
        "geno_x, geno_y, description",
        [
            ("AA", "GG", "opposite homozygotes"),
            ("AG", "CC", "heterozygote vs homozygote, no shared allele"),
            ("CC", "AG", "homozygote vs heterozygote, no shared allele"),
            ("AG", "CT", "two heterozygotes, no shared allele"),
            ("AT", "CG", "two heterozygotes, no shared allele"),
        ],
    )
    def test_genotypes_sharing_no_allele_are_no_match(
        self, vp, geno_x, geno_y, description
    ):
        """
        Sharing no allele is an exclusion, whatever the zygosity. Classifying
        it 'yellow' does not merely lose the exclusion -- it converts the
        strongest available negative evidence into segment support.
        """
        result = classify_one(vp, geno_x, geno_y)
        assert result == "crimson", (
            f"{description}: X={geno_x} Y={geno_y} share no allele but were "
            f"classified '{result}' instead of 'crimson' (no match)"
        )

    @pytest.mark.parametrize(
        "geno_x, geno_y, expected, description",
        [
            ("AG", "AC", "yellow", "shares one allele (A)"),
            ("AA", "AG", "yellow", "shares one allele (A)"),
            ("AG", "GT", "yellow", "shares one allele (G)"),
            ("AG", "AG", "limegreen", "both alleles shared"),
            ("AG", "GA", "limegreen", "both alleles shared, order reversed"),
            ("AA", "AA", "limegreen", "identical homozygotes"),
        ],
    )
    def test_genuine_matches_are_unchanged(
        self, vp, geno_x, geno_y, expected, description
    ):
        """Guard against an exclusion rule that swallows real matches."""
        result = classify_one(vp, geno_x, geno_y)
        assert result == expected, (
            f"{description}: X={geno_x} Y={geno_y} expected '{expected}', "
            f"got '{result}'"
        )

    @pytest.mark.parametrize(
        "geno_x, geno_y",
        [
            (f"A{NO_CALL}", "GG"),
            (f"{NO_CALL}{NO_CALL}", "GG"),
            ("CC", f"A{NO_CALL}"),
        ],
    )
    def test_no_call_never_produces_an_exclusion(self, vp, geno_x, geno_y):
        """
        Unknown alleles cannot exclude. The no-call rule is applied after the
        exclusion rule and must still win.
        """
        result = classify_one(vp, geno_x, geno_y)
        assert result != "crimson", (
            f"X={geno_x} Y={geno_y} contains a no-call but was reported as a "
            f"definite exclusion"
        )


class TestExclusionsDoNotExtendSegments:
    def test_non_sharing_region_produces_no_hir_segment(self, vp, genetic_map):
        """
        Two individuals who share no allele anywhere across a wide region must
        not be reported as half-identical across it.
        """
        chromosome = 1
        map_positions, map_cms = genetic_map[chromosome]
        n_snps = 500

        # X is heterozygous A/G throughout; Y is homozygous C/C throughout.
        # They share nothing at any SNP.
        dna_x = make_individual(["AG"] * n_snps, chromosome, 100_000_000, 30_000)
        dna_y = make_individual(["CC"] * n_snps, chromosome, 100_000_000, 30_000)
        dm = merge_pair(dna_x, dna_y, chromosome)

        # Precondition: a fabricated segment here would clear both gates, so a
        # pass cannot be an artefact of the region being too small to report.
        span_cm = np.interp(dm["position"].max(), map_positions, map_cms) - np.interp(
            dm["position"].min(), map_positions, map_cms
        )
        assert len(dm) > HIR_SNP_MIN, "test region too short to clear HIR_SNP_MIN"
        assert span_cm > HIR_CUTOFF, "test region too narrow to clear HIR_CUTOFF"

        dm["match"] = classify(vp, dm)
        hirs, firs = vp.scan_genomes_optimized(
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

        assert hirs.empty, (
            f"{len(hirs)} half-identical segment(s) totalling "
            f"{hirs['Length (cM)'].sum() if not hirs.empty else 0} cM were "
            f"reported between two individuals who share no allele at any of "
            f"the {len(dm)} SNPs in the region"
        )
        assert firs.empty, "a fully-identical segment was reported across an exclusion"

    def test_genuine_hir_is_still_detected(self, vp, genetic_map):
        """Guard: a real half-identical region must survive the change."""
        chromosome = 1
        map_positions, map_cms = genetic_map[chromosome]
        n_snps = 500
        dna_x = make_individual(["AG"] * n_snps, chromosome, 100_000_000, 30_000)
        dna_y = make_individual(["AC"] * n_snps, chromosome, 100_000_000, 30_000)
        dm = merge_pair(dna_x, dna_y, chromosome)
        dm["match"] = classify(vp, dm)

        hirs, _ = vp.scan_genomes_optimized(
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
        assert not hirs.empty, (
            "a region where both individuals carry a shared A allele produced "
            "no HIR segment -- the exclusion fix has suppressed real matches"
        )
