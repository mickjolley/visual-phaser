# -*- coding: utf-8 -*-
"""
PKMconfig_V6.py is the configuration file for Phased_Kit_Maker_V6.py.

DNA file names must have _raw_dna immediately after name. Both ,csv and .txt
files from all testing companies may be used.

@author: mickjolley (mickj1948@gmail.com)   © 2026
"""

# Path to folder where DNA files are stored.
DNA_FOLDER = r"**********"

# Names of sibs.
SIB_NAMES = ['****', '****','****']

# Name of parent.
PARENT = '****'

# Relationship of parent to sibs. Enter "Mother" or "Father".
RELATIONSHIP = 'Mother'

# Select output mode.
"""
Enter "Opposite", 'Same" or "ET". "Opposite" generates a paternal phased
kit using a maternal kit as reference (suffix "mp") and vice versa (suffix
"pm"). Enter "Same" to generate a paternal phased kit using a paternal kit 
as reference (suffix "pp") and a maternal phased kit using a maternal kit as
reference (suffix "mm"). "ET" generates an Evil Twin phased kit. The 
suffix will be "etm" or "etp" depending on whether a maternal or paternal 
kit is used as reference.
"""
MODE = 'Opposite'

# Select character to be used to designate no calls
NO_CALLS = 'X'

