# -*- coding: utf-8 -*-
"""
VP_Config_Resources.py - Resource definitions for Visual Phaser Config GUI

This module contains all static resource definitions for the VP Config GUI,
following boa-constructor methodology for modular resource management.

Boa Constructor Pattern:
- Separates resource definitions from UI logic
- Centralizes configuration tooltips, labels, and field definitions
- Enables easy localization and maintenance
"""

# Field definitions with metadata
FIELD_DEFINITIONS = {
    # Path Fields
    'FILES_PATH': {
        'type': 'path_directory',
        'label': 'DNA Files Path',
        'tooltip': 'Path to folder where the DNA files are stored.',
        'required': True,
    },
    'WORKING_DIRECTORY': {
        'type': 'path_directory',
        'label': 'Working Directory',
        'tooltip': 'Folder where the .xlsx and .py files will be stored.',
        'required': True,
    },
    'MAP_PATH': {
        'type': 'path_directory',
        'label': 'Map File Path (min_map.txt)',
        'tooltip': 'Path to folder containing min_map.txt.',
        'required': True,
    },

    # File Lists
    'SIBLINGS': {
        'type': 'list_text',
        'label': 'DNA Siblings (comma-separated filenames)',
        'tooltip': 'Two minimum. Make sure that the DNA files are in the PixelChromosomeView (PCV) format.',
        'required': True,
    },
    'PHASED_FILES': {
        'type': 'list_files',
        'label': 'Phased Files (select files)',
        'tooltip': 'Enter names of phased files to be compared to each other.',
        'required': False,
    },
    'EVIL_TWINS': {
        'type': 'list_files',
        'label': 'Evil Twin Files (select files)',
        'tooltip': 'Evil Twin files to be compared to SIBLINGS.',
        'required': False,
    },
    'COUSINS': {
        'type': 'list_text',
        'label': 'Cousins (comma-separated names)',
        'tooltip': 'Enter names of individuals to be compared with all SIBLINGS in a pre-existing file.',
        'required': False,
    },
    'CHROMOSOMES': {
        'type': 'list_text',
        'label': 'Chromosomes (1-23, comma-separated or empty for all)',
        'tooltip': 'Chromosome selected (1-23). Leave empty for all chromosomes.',
        'required': False,
    },

    # Text Fields
    'EXCEL_FILE_NAME': {
        'type': 'text',
        'label': 'Excel Output File Name',
        'tooltip': 'Name of the .xlsx file. Do not include the ".xlsx".',
        'required': True,
    },
    'LINUX_FONT_STRING': {
        'type': 'text',
        'label': 'Linux Font Path',
        'tooltip': 'Linux users only. Enter the path to your font.',
        'required': False,
        'default': '*/fonts/truetype/family/DejaVuSerif-Bold.ttf',
    },
    'FREEZE_COLUMN': {
        'type': 'text',
        'label': 'Freeze Column (e.g., "A" for no freeze)',
        'tooltip': 'Set to "A" if freezing not desired.',
        'required': False,
        'default': "A",
    },
    'NO_CALL': {
        'type': 'text',
        'label': 'No-Call Character',
        'tooltip': 'Character assigned to a no-call IN PHASED FILES.',
        'required': False,
        'default': "X",
    },

    # Boolean Fields
    'SHOW_NO_MATCHES': {
        'type': 'boolean',
        'label': 'SHOW_NO_MATCHES',
        'tooltip': 'Set to False if display of match pairs with no matching segments is not desired.',
        'default': True,
    },
    'CHROM_TRUE_SIZE': {
        'type': 'boolean',
        'label': 'CHROM_TRUE_SIZE',
        'tooltip': 'Set to True for true size. Set to False for normalized size.',
        'default': False,
    },
    'LINEAR_CHROMOSOME': {
        'type': 'boolean',
        'label': 'LINEAR_CHROMOSOME',
        'tooltip': 'Set to True if you want to see the linearized chromosomes.',
        'default': False,
    },
    'MERGE_FILES': {
        'type': 'boolean',
        'label': 'MERGE_FILES',
        'tooltip': 'Set to True if merging of DNA files is desired.',
        'default': True,
    },
    'AUTO_REC_PNTS': {
        'type': 'boolean',
        'label': 'AUTO_REC_PNTS',
        'tooltip': 'Set to True if calculation of RPs is desired.',
        'default': True,
    },
    'AUTO_RP_ASSIGN': {
        'type': 'boolean',
        'label': 'AUTO_RP_ASSIGN',
        'tooltip': 'Set to True if automatic assignment of recombination points is desired.',
        'default': True,
    },
    'REPAIR_FILES': {
        'type': 'boolean',
        'label': 'REPAIR_FILES',
        'tooltip': 'Converts isolated NIR and HIR SNPs to FIR.',
        'default': True,
    },
    'FIR_TABLES': {
        'type': 'boolean',
        'label': 'FIR_TABLES',
        'tooltip': 'Set to True if display of FIR tables is desired.',
        'default': True,
    },
    'SCALE_ON': {
        'type': 'boolean',
        'label': 'SCALE_ON',
        'tooltip': 'Turn scale on and off.',
        'default': True,
    },
    'SHOW_TIMES': {
        'type': 'boolean',
        'label': 'SHOW_TIMES',
        'tooltip': 'Elapsed times are shown for each step.',
        'default': True,
    },
    'SHOW_MATCH_PAIR_PROGRESS': {
        'type': 'boolean',
        'label': 'SHOW_MATCH_PAIR_PROGRESS',
        'tooltip': 'Notifies the completion of each step.',
        'default': True,
    },

    # Numeric Integer Fields
    'RESOLUTION': {
        'type': 'int_spin',
        'label': 'Resolution',
        'tooltip': 'Default value = 1. Keep under 10. Set to 100 for full resolution.',
        'min': 1,
        'max': 100,
        'default': 1,
    },
    'ARP_TOLERANCE': {
        'type': 'int_spin',
        'label': 'ARP Tolerance (pixels)',
        'tooltip': 'When AUTO_REC_PNTS is activated, columns with pixel size less than this value will be deleted.',
        'min': 1,
        'max': 100,
        'default': 5,
    },
    'HIR_CUTOFF': {
        'type': 'int_spin',
        'label': 'HIR Cutoff (cM)',
        'tooltip': 'HIR Minimum segment length (cM). The default is 7.',
        'min': 1,
        'max': 100,
        'default': 7,
    },
    'FIR_CUTOFF': {
        'type': 'int_spin',
        'label': 'FIR Cutoff (cM)',
        'tooltip': 'FIR cutoff. FIRs less than 1cM in length are probably not significant.',
        'min': 1,
        'max': 100,
        'default': 1,
    },
    'X_HIR_CUTOFF': {
        'type': 'int_spin',
        'label': 'X Chromosome HIR Cutoff (cM)',
        'tooltip': 'X chromosome cutoff (cM). The default is 15.',
        'min': 1,
        'max': 100,
        'default': 15,
    },
    'X_FIR_CUTOFF': {
        'type': 'int_spin',
        'label': 'X Chromosome FIR Cutoff (cM)',
        'tooltip': 'X chromosome FIR cutoff (cM). The default is 15.',
        'min': 1,
        'max': 100,
        'default': 15,
    },
    'HIR_SNP_MIN': {
        'type': 'int_spin',
        'label': 'HIR SNP Minimum',
        'tooltip': 'Minimum number of HIR SNPs. Default value = 200.',
        'min': 1,
        'max': 10000,
        'default': 200,
    },
    'FIR_SNP_MIN': {
        'type': 'int_spin',
        'label': 'FIR SNP Minimum',
        'tooltip': 'Minimum number of FIR SNPs. Default value = 75.',
        'min': 1,
        'max': 10000,
        'default': 75,
    },
    'MM_DIST': {
        'type': 'int_spin',
        'label': 'Mismatch Distance (Kbs)',
        'tooltip': 'Number of Kbs between mismatches to end segment. Default = 1000.',
        'min': 1,
        'max': 10000,
        'default': 1000,
    },

    # Float Fields
    'SCALE_FACTOR': {
        'type': 'float',
        'label': 'Scale Factor',
        'tooltip': 'The column width per pixel factor. Default value = 0.1351.',
        'default': 0.1355,
    },
}

# Section groupings for UI organization
FIELD_SECTIONS = {
    'Paths and Directories': [
        'FILES_PATH',
        'WORKING_DIRECTORY',
        'MAP_PATH',
    ],
    'File Management': [
        'SIBLINGS',
        'PHASED_FILES',
        'EVIL_TWINS',
        'COUSINS',
        'CHROMOSOMES',
        'EXCEL_FILE_NAME',
    ],
    'Display and Processing Options': [
        'SHOW_NO_MATCHES',
        'CHROM_TRUE_SIZE',
        'LINEAR_CHROMOSOME',
        'MERGE_FILES',
        'AUTO_REC_PNTS',
        'AUTO_RP_ASSIGN',
        'REPAIR_FILES',
        'FIR_TABLES',
        'SCALE_ON',
        'SHOW_TIMES',
        'SHOW_MATCH_PAIR_PROGRESS',
    ],
    'Numeric Parameters': [
        'RESOLUTION',
        'ARP_TOLERANCE',
        'HIR_CUTOFF',
        'FIR_CUTOFF',
        'X_HIR_CUTOFF',
        'X_FIR_CUTOFF',
        'HIR_SNP_MIN',
        'FIR_SNP_MIN',
        'MM_DIST',
        'SCALE_FACTOR',
    ],
    'Other Settings': [
        'FREEZE_COLUMN',
        'NO_CALL',
        'LINUX_FONT_STRING',
    ],
}

# Application strings
APP_TITLE = 'Visual Phaser Configuration Editor'
APP_VERSION = '1.0'
APP_DESCRIPTION = 'GUI Configuration Editor for Visual Phaser VP_configV1.py'
APP_AUTHOR = 'Ray Schumacher, Mick Jolley'
APP_EMAIL = 'mickj1948@gmail.com'
APP_COPYRIGHT = '© 2026 Mick Jolley'
APP_WEBSITE = 'https://github.com/mickjolley/visual-phaser'

# Messages
MSG_LOAD_SUCCESS = 'Configuration loaded successfully'
MSG_SAVE_SUCCESS = 'Configuration saved successfully!'
MSG_LOAD_ERROR = 'Error loading configuration: {}'
MSG_SAVE_ERROR = 'Error saving configuration: {}'
MSG_RESET_CONFIRM = 'Reset all values to defaults?'
MSG_INVALID_FLOAT = 'Invalid float value for {}: {}'

# UI Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800
CONTROL_HEIGHT = 60
PADDING = 5
SECTION_FONT_SIZE = 12
TITLE_FONT_SIZE = 14

# File dialog wildcards
WILDCARD_PYTHON = 'Python files (*.py)|*.py|All files (*.*)|*.*'
WILDCARD_ALL = 'All files (*.*)|*.*'
WILDCARD_TXT = 'Text files (*.txt)|*.txt|All files (*.*)|*.*'


def get_field_definition(field_name):
    """Get field definition by name"""
    return FIELD_DEFINITIONS.get(field_name, {})


def get_field_section(field_name):
    """Get the section that contains the field"""
    for section, fields in FIELD_SECTIONS.items():
        if field_name in fields:
            return section
    return 'Other Settings'


def get_all_sections():
    """Get all section names in order"""
    return list(FIELD_SECTIONS.keys())


def get_fields_in_section(section_name):
    """Get all fields in a section"""
    return FIELD_SECTIONS.get(section_name, [])
