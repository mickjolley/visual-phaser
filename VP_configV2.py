# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
VP_configV2.py is the configuration file for Visual_Phaser.V2.0.py.

The ability to process ,vcf files has been added to V1.1. Add the .vcf file to
the FILES_PATH. Add individuals to SIBLINGS.

FILES_PATH: Path to folder where the DNA files are stored. If .vcf files are to
processed add the .vcf file to the end. Example FILES_PATH = r"c:/dna.xyx.vcf".

WORKING_DIRECTORY: Folder where the .xlsx and .py files will be stored.

MAP_PATH: Path to folder containing min_map.txt.

SIBLINGS: Two minimum. Make sure that the DNA files are in the
PixelChromosomeView (PCV) format. Examples are 'Ancestry_Fred_raw_dna.txt' and
'23andMe_Susan_raw_dna.txt'. These files must tab delimited .txt files. Use
ancestry_csv_to_tab_converter.py or not_ancestry_csv_to_tab_converter.py to
convert .csv files to the correct format.

PHASED_FILES: Enter comma-separated names of the individuals in phased files to
be compared to each other. They will not be compared to siblings. The default
assignment for no calls is "X".

EVIL_TWINS: Enter comma-separated names of the individuals in evil-twin files
to be compared to SIBLINGS.

COUSINS: Enter comma-separated names of the individuals to be compared with all SIBLINGS in a
pre-existing file. Leave blank ([]) when creating a new file.

CHROMOSOMES: Chromosome selected (1-23). More than one chromosome may be entered.
Leave empty for all chromosomes.

EXCEL_FILE_NAME: Name of the .xlsx file. Do not include the ".xlsx", This is
added automatically.

SHOW_NO_MATCHES: Set to False if the display of match pairs with no matching
segments is not desired. This is the recommended default value for cousin
matches. If only siblings are being compared set this to True.

CHROM_TRUE_SIZE: Set to True for true size. Set to False for normalized size.

LINEAR_CHROMOSOME: Set to True if you want to see linearized chromosomes.
In linear mode the display is mapped to a fixed grid: RESOLUTION=10 uses
10000 bins, all other values use 1000 bins. CHROM_TRUE_SIZE is automatically
set to False.

MERGE_FILES: Set to True if merging of DNA files is desired. If it is desired
to treat match pairs separately, set to False. This is useful if one of the
files is missing a lot of SNPs or if LINEAR_CHROMOSOME is set to True. Missing
SNPs are shown in gray. Default = True.

RESOLUTION: Default value = 1. Valid user range is 1..100.
For non-linear chromosomes, effective bins are approximately RESOLUTION * 1000,
up to full data length; RESOLUTION=100 typically gives full detail.
For LINEAR_CHROMOSOME mode, RESOLUTION=10 uses 10000 bins; all other values use
1000 bins.
At RESOLUTION=100 with typical SNP counts, div becomes 1 so dplot pixel width is
approximately source_rows + 1.

AUTO_REC_PNTS: Set AUTO_REC_PNTS to True if calculation of RPs is desired. ARP
is not activated in LINEAR_CHROMOSOME mode or when cousins are being added.
The first time the program is run, if AUTO_ REC_PNTS is set to True, it is
recommended that it is run with two siblings and chromosome 1 only. If the RPs
do not line up correctly, the SCALE_FACTOR needs to be adjusted (see below).

ARP_TOLERANCE: When AUTO_REC_PNTS is activated, columns with pixel size
less than this value will be deleted. Set to minimum desired column width
(pixels). Default = 5.

AUTO_RP_ASSIGN: Set AUTO_RP_ASSIGN to True if automatic assignment of
recombination points is desired.

REPAIR_FILES: Converts isolated NIR and HIR SNPs to FIR. Converts isolated
NIR SNPs to HIR. Default = True.

SCALE_FACTOR: The column width per pixel factor. Default value = 0.1355. This may
require adjustment to correctly position the recombination points. If the RPs
are to the right of where they should be, decrease SCALE_FACTOR (try 0.13 to
start), and vice versa (try 0.14 to start). Repeat until the RPs line up
correctly. It is suggested that this procedure is performed using two siblings
and chromosome 1 only. This only has to be performed once.
If near 1 pixel per source row is desired in non-linear mode, use
RESOLUTION = 1

HIR_CUTOFF: Default value = 7 cM

FIR_CUTOFF: Default value = 1 cM.

X_HIR_CUTOFF: X chromosome cutoff (cM). The default is 15.

X_FIR_CUTOFF: X chromosome FIR cutoff (cM). The default 15.

FIR_TABLES: Set to True if display of FIR tables is desired.

SCALE_ON: Turn scale on and off. Set to False if not required. Default = True

FREEZE_COLUMN: Set to "A" if freezing not desired. Default = "A".

LINUX_FONT_STRING: Linux users only. Enter the path to your font. If you don't
know it, set SCALE_ON to False.

SHOW_TIMES: Elapsed times are shown for each step. Default =True

SHOW_MATCH_PAIR_PROGRESS: Notifies the completion of each step. Set to
False if you don't want to see this. Default = True

HIR_SNP_MIN: Minimum number of HIR SNPs. Default value = 200

FIR_SNP_MIN: Minimum number of FIR SNPs. Default value = 75

MM_DIST: Number of Kbs between mismatches to end segment. Default = 1000.

NO_CALL: Character assigned to a no-call IN PHASED FILES.

© 2026 Mick Jolley (mickj1948@gmail.com)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Path to DNA files. Add .vcf file to the end if .vcf file is to be processed.
FILES_PATH = 'C:\\Users\\rjs\\AppData\\Local\\DNA_phasing\\DNA_files'

# Path to .xlsx file.
WORKING_DIRECTORY = 'C:\\Users\\rjs\\AppData\\Local\\DNA_phasing\\DNA_files\\tmp'

# Path to min_map.txt file.
MAP_PATH = 'C:\\Users\\rjs\\AppData\\Local\\DNA_phasing\\DNA_files'

# SIBLINGS to be compared. Make sure that no two files share the same name.
SIBLINGS = ['Diane', 'Tom', 'Ray']

# Phased files to be compared to each other.
PHASED_FILES = []

# Evil Twin files to be compared to SIBLINGS.
EVIL_TWINS = []

# COUSINS to be compared with SIBLINGS in a pre-existing file.
COUSINS = []

# Chromosome selected. Leave empty to select all the chromosomes.
CHROMOSOMES = []

# Excel file name. Leave ".xlsx" out.
EXCEL_FILE_NAME = 'RP_test'

# Suppress no-matches. Set to True if display of no-matches is desired.
SHOW_NO_MATCHES = True

# Chromosome true size. Set to False for normalized size.
CHROM_TRUE_SIZE = False

# Linearize the chromosome.
LINEAR_CHROMOSOME = False

# Select merging of DNA files. Default = True
MERGE_FILES = True

# Resolution. Default = 1. Valid range = 1..100.
# Non-linear mode: effective bins are approximately RESOLUTION * 1000 up to full
# data length (RESOLUTION=100 is typically full detail).
# Linear mode: RESOLUTION=10 uses 10000 bins; all other values use 1000 bins.
# At RESOLUTION=100 with typical SNP counts, dplot width is approximately
# source_rows + 1 (div usually resolves to 1).
RESOLUTION = 1

# Set AUTO_REC_PNTS to True if calculation of RPs is desired. ARP is not
# activated in LINEAR_CHROMOSOME mode or when COUSINS is not empty.
AUTO_REC_PNTS = True

# When AUTO_REC_PNTS is activated, Columns with pixel numbers less than this
# value will be deleted. Set to minimum desired column width (pixels).
# Default = 5.
ARP_TOLERANCE = 5

# Set AUTO_RP_ASSIGN to True if automatic assignment of recombination points is
# desired.
AUTO_RP_ASSIGN = True

# Repair files. Converts isolated NIR and HIR SNPs to FIR. Converts isolated
# NIR SNPs to HIR.
REPAIR_FILES = True

# The column width per pixel factor. This may need adjustment depending on
# the display resolution.
# For near 1 pixel per source row in non-linear mode, use RESOLUTION=100 and
# SCALE_FACTOR approximately 0.3483.
SCALE_FACTOR = 0.1355

# HIR Minimum segment length (cM). The default is 7.
HIR_CUTOFF = 6

# FIR cutoff. FIRs less than 1cM in length are probably not significant.
FIR_CUTOFF = 1

# X chromosome HIR Minimum segment length (cM). The default is 15.
X_HIR_CUTOFF = 15

# X chromosome FIR cutoff. FIRs less than 15cM in length are probably not significant.
X_FIR_CUTOFF = 15

# Display Fir tables.
FIR_TABLES = True

# Turn scale on and off. Set to False if not required.
SCALE_ON = True

# Column to freeze. Set to "A" if freezing not required.
FREEZE_COLUMN = 'A'

# Linux font string. An alternative is:
# "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
LINUX_FONT_STRING = '*/fonts/truetype/family/DejaVuSerif-Bold.ttf'

# Elapsed times are shown for each step.
SHOW_TIMES = True

# Notifies the completion of each step. Set to False if you don't want to see
# this.
SHOW_MATCH_PAIR_PROGRESS = True

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
You shouldn't have to change the parameters below.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Minimum number of HIR SNPs.
HIR_SNP_MIN = 150

# Minimum number of FIR SNPs.
FIR_SNP_MIN = 50

# Number of Kbs between mismatches to end segment.
MM_DIST = 1000

# Character assigned to no calls in phased files.
NO_CALL = 'X'

