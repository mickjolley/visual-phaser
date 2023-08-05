# -*- coding: utf-8 -*-
"""
VPconfig.py.

Visual Phaser configuration file. To be used with Visual_Phaser.

@author: mick jolley (email: mickj1948@gmail.com)

Make sure that all items are entered correctly. Any errors will cause the 
program to crash.

Folders should be a single word. Words can be combined with the underscore 
character ("_"). Also, use forward slashes ("\") at the end of folder names.
Python can get confused with back slashes. It uses it as an escape character. 

Do not use special characters in Excel file names.

The length of time that you are allowed to respond to reCAPTCHA messages is 
set by the "RECAPTCHA_TIMEOUT" variable.

When entering the Excel file name, leave the '.xlsx' out. The program adds it
automatically.

It is very important that you select a cutoff that is between 3 and 50. If you
select one outside of this range, the program will crash.

For automatic recombination points determination, set AUTO_REC_PNTS to "True".

Run ARP_Scale_Factor.py to determine SCALE_FACTOR. 

Set CROMOSOME_LENGTH_SCALE_FACTOR to 1.

End phased kits names with "PP" for paternal phased kits and "MP" for maternal
phased kits.

If using phased kits, make sure that a phased kit is last in the list.

Set CHROMOSOME_X to "True" to add chromosome 23 to the list of selected 
chromosomes. Enter "0" in CHROMOSOMES_SELECTED to deselect all autosomal
chromosomes. By setting CHROMOSOME_X to "True" and entering "0" in CHROMOSOMES_
SELECTED, only chromosome 23 will be compared. 

© 2023 Michael E. Jolley

"""


# Login Variables
BROWSER = 'Firefox' # Chrome can also be used, but not recommended.
WORKING_DIRECTORY = 'c:/********/' 
EMAIL = '*************'
PASSWORD = '*********'

# If using phased kits set to "True". If set to "False", all kits will be 
# treated normally. Chromosome maps will still be generated if AUTO_REC_PNTS 
# is set to "True".  
PHASED_KITS = False

# Miscellaneous Variables
# Names and GEDmatches ID of the individuals
"""
Example :- "Fred_AA1234567"
If using phased kits end names with "PP" for paternal phased kits and "MP"
for maternal phased kits. 
Make sure that a phased kit is last in the list. 
Do not mix maternal and paternal phased kits.
Make paternal kits using the mother's kit. 
Make maternal kits using the father's kit.
Do not use maternal kits made using the mother's kit.
Do not use paternal kits made using the father's kit. 

"""
INDIVS = [
          'A***_*********',  
          'B***_*********',  
          'C***_*********',  
          'D***_*********'  
          ] 

# Chromosome 23 will be added to chromosomes selected list.
CHROMOSOME_X = True

# Chromosome 23 cutoff.
CHROM_X_CUTOFF = 15

CHROMOSOMES_SELECTED = [] # Empty list for all chromosmes.Enter numbers, separated
                          # by a comma for individual chromosomes eg, [1,2,3].
                          # Enter "0" to deselect all autosomal chromosomes.
                          
CM_CUTOFF = 7 # Cutoff has to between 3 and 50

EXCEL_FILE_NAME = '*******' # .xlsx file


# Auto RP Option. If set to "True", the recombination points will be automatically
# calculated and Chromosomes will be generated.
AUTO_REC_PNTS = True

# This is the default value. Your's might be different.
SCALE_FACTOR = .1357

# Gap defining beginning and end of NIR.
NIR_GAP = 20

# Merge RPs within this distance.
RP_GAP = 6

# Merge double RPs within this distance.
DUP_DIST = 3


# Program Variables
RECAPTCHA_TIMEOUT = 30 # seconds
BEEP_TONE = 400 # Tone (Hz)
BEEP_TIME = 500 # milliseconds
IMAGE_GATHERING_TIMEOUT = 30 # seconds
CROMOSOME_LENGTH_SCALE_FACTOR = 1 # Determines chromosome length
FINISHED_WARNING = True # Enter "True" to turn on, "False" to turn off (case sensitive)
WARNING_BEEPS = 5 # Number of beeps
BEEP_SPACING = 1 # Time (seconds) between beeps
INTERNET_WAIT = 0 # Time to wait for internet connection.