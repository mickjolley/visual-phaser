# -*- coding: utf-8 -*-
"""
VPHC_config_V2.py.

VP_html_Cousins_V1.py configuration file.

When entering the Excel file name, leave the '.xlsx' out. The program adds it
automatically. The .xlsx file must already exist.

Create .html files by right clicking on the GEDmatch comparison page and selecting 
"Save as..". Name the file (see below) and save (Webpage,complete) to a dedicated
folder.

.html Files should be named "Sibling-Cousin.html". Autosomal matches only. It is
important that all Sibling-Cousin matches are included.

LINEAR_CHROMOSOME files cannot be used.

Sibling names must not contain a hyphen ("-").

Siblings, chromosomes and resolution are automatically extracted from the .xlsx 
file. The resolution of the GEDmatch comparison must match that of the .xlsx file.
A VP RESOLUTION of 1 (default) is equivalent to GEDmatch 1000 pixels (default).

@author: Mick Jolley (email: mickj1948@gmail.com)

© 2026 Michael E. Jolley

"""
# Working directory.
WORKING_DIRECTORY = r"*********"

# Folder where html files are stored.
HTML_FOLDER = r'********'

# Cousins with .html files. 
COUSINS = ['****', '****']

# Pre-existing Excel file name.
EXCEL_FILE_NAME = "****"  # .xlsx file

# Make backup file.
MAKE_BACKUP = True

# Show no matches.Set to "False" if suppression of the display of no-matches is
# desired.
SHOW_NO_MATCHES = True

