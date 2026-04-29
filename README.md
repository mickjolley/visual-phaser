# visual-phaser

1. Introduction

  Visual_Phaser_New_V21superplus.py is a specialized bioinformatics application designed for
  genetic genealogy. It analyzes raw autosomal DNA files to identify and visualize 
  shared segments (Half-Identical Regions (HIRs), Fully-Identical Regions
  (FIRs) and Non-Identical regions (NIRs)) between siblings, cousins, and other relatives.

  The software produces a comprehensive Excel (.xlsx) workbook featuring color-coded
  chromosomal maps and detailed segment data tables.

  ---

2. System Requirements & Installation

  Prerequisites
   - Python >=3.8, <3.14
   - Required Libraries:
           numpy pandas pillow openpyxl

  Project Structure 
   - Visual_Phaser_New_V21superplus.py: The main execution engine.
   - VPnew_config_V21super.py: The configuration and parameter file.
   - min_map.txt: (Required) A genetic map file mapping physical positions (Mb) to
     genetic distances (cM).

  ---

3. Data Preparation

  DNA File Format (PCV)
  The software expects tab-delimited .txt files in a format often referred to as
  "PixelChromosomeView" (PCV).
   - Naming Convention: Files must contain the person's name followed by _raw_dna
     - Example: Barb_raw_dna.txt, Jan_raw_dna.txt.
     - .csv files can be converted to .txt files with ancestry_to_tab_converter.py
       or non_ancestry_to_tab_converter.py as the case may be.
   - Supported Sources: Specifically optimized for AncestryDNA , 23andMe and other            
      non- Ancestry exports.

  Genetic Map (min_map.txt)
  Place this file in your designated MAP_PATH. This is used to accurately calculate 
  the length of shared segments in centiMorgans.

  ---

4. Configuration Guide

  All settings are managed within VPnew_config_V21super.py.

  Primary Paths
   - FILES_PATH: The folder containing your raw DNA .txt files.
   - WORKING_DIRECTORY: The folder where the Excel report and temporary images will be
     saved.
   - MAP_PATH: The folder containing min_map.txt.

  Comparison Lists
   - SIBLINGS: A list of individuals to be compared against one another.
   - PHASED_FILES: Names of phased files (usually derived from parent/child
     comparisons).
   - COUSINS: Individuals to be compared against the sibling list in an existing
     project.
   - EVIL_TWINS: Specialized files representing the non-matching side of a phased
     individual.

  Genetic Cutoffs
   - HIR_CUTOFF: Minimum segment length (in cM) for Half-Identical segments (Default:
     7 cM).
   - FIR_CUTOFF: Minimum segment length (in cM) for Fully-Identical segments (Default:
     1 cM).
   - REPAIR_FILES: (True/False) Enables smoothing logic to bridge small gaps caused by
     bad SNPs.

  Display & Scaling
   - RESOLUTION: Scaling factor for the visual plot. 1 is default; 10 provides 10x
     detail.
   - SCALE_FACTOR: This depends on the display reso;ution. Adjusts the column width
     in Excel to ensure visual blocks align with data. Manual adjust to line up
     recombination points correctly. This only has to be done once.
   - CHROM_TRUE_SIZE: If True, visual blocks are proportional to the physical length
     of the chromosome.
   - LINEAR_CHROMOSOME: If True, a linear chromosome is displayed. Regions where   
     there is no data are shown in grey.
  ---

5. Software Operation

  Execution Phases
   1. DNA Loading: The system scans your FILES_PATH and loads data for all listed
      individuals using multithreading.
   2. Genetic Analysis: Chromosomes are distributed across CPU cores
      (multiprocessing). The system identifies matches and calculates cM lengths.
   3. Image Generation: PNG images are created for each match pair.
   4. Excel Merging: Data and images are compiled into a final workbook.

  ---

6. Understanding the Output

  The output is an Excel file named according to your EXCEL_FILE_NAME setting. Each
  chromosome (1–23/X) has its own tab.

   Graphical Plot (The Image)
   - Top Half (SNP Details):
       - Yellow: Half-match (One chromosome matches).
       - Limegreen: Full-match (Both chromosomes match).
       - Crimson: No match.
       - Grey: No data.
   - Bottom Half (Segment Blocks):
       - Blue Bar: Confirmed HIR segment.
       - Orange Bar: Confirmed FIR segment.

  Data Tables
  Tables list each segment's start and end positions (Mb), the number of SNPs in the
  segment, and the genetic length (cM).

  Recombination Points (ARP)
  If AUTO_REC_PNTS is enabled, the bottom of each sheet will display Column Width
  data. These represent segments of DNA between crossover points. The AUTO_RP_ASSIGN
  feature attempts to attribute these segments to specific siblings based on matching
  patterns.

  ---

7. Technical Architecture

  For developers and power users:
   - Hybrid Concurrent Architecture:
     - multiprocessing: Used for heavy genetic number-crunching on a
       per-chromosome basis.
     - ThreadPoolExecutor: Used for I/O operations (reading files from disk) and
       concurrent image generation using the Pillow library.
   - Vectorization: Uses NumPy and Pandas for rapid allele comparison across millions
     of rows, significantly outperforming standard Python loops.

  ---
  © 2026 Mick Jolley | Support: mickj1948@gmail.com














