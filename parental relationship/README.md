Parental Relationship

Parental_Relationship_V4.py estimates the relationsip between an individual's 
parents by calculating runs of homozygosity (ROHs) for that individual. 
Default values of 1% error rate, 50 SNPs minimum, a SNP density of a least 20 
SNPs per Mb and a ROH cutoff of 5 Mb are used. The result is a .xlsx file of 
the ROHs per chromosome (if found) and a summary .csv file. 

Multiply the total ROH cMs by four to approximate sibling comparison cMs.
For example, if the total cM of the ROHs is 200, then 4 times this is 800 cM,
which approximates to first cousins. 

An example of an individual from an endogamous population is Ancestry_Samaritan
_raw_dan.txt'. The total cMs of ROHs for this individual is 289.7 cM, which 
means that this individual's parents were probably first cousins.

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

SHOW_NO_MATCHES: Set to False if the display of individuals with no matching
segments is not desired. This is the recommended default value. 

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
