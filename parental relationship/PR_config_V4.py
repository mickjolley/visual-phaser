# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PR_config_V4.py is the configuration file for Parental_Relationship_V4.py.

DNA_FILES_PATH: Path to DNA files.

WORKING_DIRECTORY: Folder where the .xlsx and .csv files will be stored.

MAP_PATH: Path to folder containing min_map.txt.

SUBJECTS: List of individuals to be analyzed from DNA_FILES_PATH. Enter ['*'] 
to load all subjects. SUBJECT file names must contain '_raw_dna' after the 
name.

CHROMOSOMES: Chromosome selected (1-22). More than one chromosome may be entered.
Leave empty for all chromosomes.

EXCEL_FILE_NAME: Name of the .xlsx file. Do not include the ".xlsx", This is
added automatically.

SHOW_NO_ROHS: Set to False if the display of individuals with no ROHs is not
desired. This is the default value. 

CHROM_TRUE_SIZE: Set to True for true size. Set to False for normalized size.

LINEAR_CHROMOSOME: Set to True if you want to see the linearized chromosomes.
RESOLUTION will be ignored unless it is 10 (10x resolution). CHROM_TRUE_SIZE is
automatically set to False.

RESOLUTION: Default value = 1. For normalized size it is advised to keep it
under 10. Set to 100 for full length chromosomes. If LINEAR_CHROMOSOME is set
to "True", RESOLUTION is automatically set to 1, unless it is set to 10.

FREEZE_COLUMN: Set to "A" if freezing not desired. Default = "A".

LINUX_FONT_STRING: Linux users only. Enter the path to your font. 

ROH_CUTOFF: ROH cutoff (Mbs). Default = 5.

ERR_RATE: Error rate tolerated (%). Default = 1.

SNP_MIN: Minimum number of SNPs in ROH. Default = 50.

SNP_DENS_MIN: Min SNP densiy (SNPs/Mb). Default = 20.


© 2026 Mick Jolley (mickj1948@gmail.com)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Path to DNA files.
DNA_FILES_PATH = r'c:/dna files' 

# Path to .xlsx file.
WORKING_DIRECTORY = r'c:/vpphaser'

# Path to min_map.txt file.
MAP_PATH = r'c:/minmap'

# SUBJECTS to be compared from DNA_FILES_PATH. 
# Enter ['*'] to load all subjects. Leave empty ([]) to load none.
SUBJECTS = ['High']

# Chromosome selected. Leave empty to select all the chromosomes.
CHROMOSOMES = []

# Excel file name. Leave ".xlsx" out.
EXCEL_FILE_NAME = 'roh'

# Suppress no-matches. Set to True if display of no-matches is desired.
SHOW_NO_ROHS = False

# Chromosome true size. Set to False for normalized size.
CHROM_TRUE_SIZE = False

# Linearize the chromosome.
LINEAR_CHROMOSOME = False

# Resolution. Default = 1. Keep under 10. Set to 100 if full resolution is
# desired. If LINEAR_CHROMOSOME is set to True, RESOLUTION will be automatically
# set to 1, unless it is set to 10 (10x resolution).
RESOLUTION = 1

# Column to freeze. Set to "A" if freezing not required.
FREEZE_COLUMN = 'A'

# Linux font string. An alternative is:
# "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
LINUX_FONT_STRING = '*/fonts/truetype/family/DejaVuSerif-Bold.ttf'

""" You shouldn't need to change these' """

# ROH cutoff (Mb).
ROH_CUTOFF = 5

#Error rate tolerated (%).
ERR_RATE = 1

#Minimum number of SNPs in ROH.
SNP_MIN = 50

#Min SNP densiy (SNPs/Mb).
SNP_DENS_MIN = 20




