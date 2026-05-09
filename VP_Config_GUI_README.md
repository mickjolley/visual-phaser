# Visual Phaser Configuration GUI

A wxPython-based graphical user interface for editing the Visual Phaser `VP_configV1.py` configuration file.

## Features

- **Path Selection**: Browse and select directories using file dialogs for:
  - `FILES_PATH` - DNA files directory
  - `WORKING_DIRECTORY` - Output directory
  - `MAP_PATH` - Map file directory

- **File Management**:
  - Edit `SIBLINGS`, `PHASED_FILES`, `EVIL_TWINS`, `COUSINS`, and `CHROMOSOMES` as comma-separated lists
  - Set `EXCEL_FILE_NAME` for output

- **Configuration Options**:
  - **Boolean Settings**: True/False dropdowns for all boolean parameters
  - **Numeric Parameters**: Spin controls for integer values (RESOLUTION, ARP_TOLERANCE, etc.)
  - **Float Parameters**: Text input for SCALE_FACTOR
  - **Text Fields**: Direct text entry for other configuration values

- **Tooltips**: Context-sensitive help from the original configuration file comments displayed on mouseover

- **Load/Save**:
  - Load configuration from any VP_configV1.py file
  - Save configuration back to file
  - Reset to defaults

## Installation

### Prerequisites

- Python 3.7 or higher
- wxPython 4.0 or higher

### Setup

1. Install wxPython:
```bash
pip install wxPython>=4.0.0
```

2. Navigate to the visual-phaser directory:
```bash
cd path/to/visual-phaser
```

## Usage

### Launch the GUI

From command line:
```bash
python VP_Config_GUI.py
```

With an optional config file path:
```bash
python VP_Config_GUI.py path/to/VP_configV1.py
```

### Using the GUI

1. **Load Configuration**:
   - Click menu: File → Load Config, or
   - Click "Load Configuration" button at bottom
   - Select your VP_configV1.py file

2. **Edit Settings**:
   - Use appropriate controls for each field type:
     - **Browse buttons**: Navigate folders for paths
     - **Text fields**: Enter text values
     - **Dropdowns**: Select True/False for boolean options
     - **Spin controls**: Adjust numeric values
    - **Text fields**: Enter comma-separated list values for `SIBLINGS`, `PHASED_FILES`, `EVIL_TWINS`, `COUSINS`, and `CHROMOSOMES`

3. **Get Help**:
   - Hover over any field to see its tooltip
   - Tooltips are taken from the original configuration file comments

4. **Save Configuration**:
   - Click "Save Configuration" button, or
   - Use menu: File → Save Config
   - Configuration will be saved to VP_configV1.py

5. **Reset Values**:
   - Click "Reset to Defaults" to reload original values
   - Your edits must be saved first to see the saved values

6. Run
   - Click "Save Configuration" button if modifications have been made
  - Click the "Run" button to run the main program
  - The app switches to the Paths tab and streams STDIO into Program output
  - Use the Program output "Clear" button to clear the output box

## File Structure

- **VP_Config_GUI.py** - Main GUI application and entry point script
- **VP_configV1.py** - Configuration file edited by the GUI
- **VP_Config_Resources.py** - Additional project resources

## Notes

- The current GUI implementation is in `VP_Config_GUI.py`.
- It supports loading a local `VP_configV1.py` at startup, or a custom path via CLI argument.

## Configuration Parameters Reference

### Paths
- **FILES_PATH**: Directory containing DNA files
- **WORKING_DIRECTORY**: Where output files (.xlsx, .py) are saved
- **MAP_PATH**: Directory containing min_map.txt

### File Lists
- **SIBLINGS**: Comma-separated names of the individuals to compare (minimum 2)
- **PHASED_FILES**: Comma-separated names of the individuals in phased files to compare
- **EVIL_TWINS**: Comma-separated names of the individuals in evil-twin files to compare with siblings
- **COUSINS**: Comma-separated names of the individuals to compare with siblings
- **CHROMOSOMES**: Which chromosomes to process (1-23, or empty for all)

### Output
- **EXCEL_FILE_NAME**: Name for output Excel file (without .xlsx extension)

### Display Options
- **CHROM_TRUE_SIZE**: Use true chromosome sizes vs. normalized
- **LINEAR_CHROMOSOME**: Show chromosomes in linearized format
- **SHOW_NO_MATCHES**: Include pairs with no matching segments
- **SHOW_TIMES**: Display elapsed time for each step
- **SHOW_MATCH_PAIR_PROGRESS**: Show progress notifications

### Processing
- **MERGE_FILES**: Combine DNA file data
- **AUTO_REC_PNTS**: Automatically calculate recombination points
- **AUTO_RP_ASSIGN**: Automatically assign recombination points
- **REPAIR_FILES**: Fix isolated SNPs

### Quality Settings
- **RESOLUTION**: Display resolution (1-100)
- **ARP_TOLERANCE**: Minimum column width for recombination points
- **HIR_CUTOFF**: Minimum HIR segment length (cM)
- **FIR_CUTOFF**: Minimum FIR segment length (cM)
- **X_HIR_CUTOFF**: X chromosome HIR cutoff
- **X_FIR_CUTOFF**: X chromosome FIR cutoff
- **HIR_SNP_MIN**: Minimum HIR SNPs
- **FIR_SNP_MIN**: Minimum FIR SNPs
- **MM_DIST**: Distance between mismatches to end segment (Kbs)

### Advanced
- **SCALE_FACTOR**: Column width per pixel factor
- **SCALE_ON**: Enable/disable scale display
- **FREEZE_COLUMN**: Column to freeze in display
- **LINUX_FONT_STRING**: Font path for Linux systems
- **NO_CALL**: Character for no-call markers
- **FIR_TABLES**: Display FIR analysis tables

## Troubleshooting

### wxPython Installation Issues

On Windows, if wxPython installation fails:
```bash
pip install --upgrade wxPython>=4.0.0
```

On macOS, you may need to install from source:
```bash
pip install wxPython --no-binary wxPython
```

On Linux, ensure you have the required development packages:
```bash
# Ubuntu/Debian
sudo apt-get install python3-wxgtk4.0

# Fedora
sudo dnf install python3-wxpython
```

### File Not Found Errors

- Ensure VP_configV1.py exists in the application directory
- When loading a custom config file, use the "Load Configuration" button to browse

### Changes Not Saving

- Check that you have write permissions to the VP_configV1.py file
- Verify the file is not open in another editor or locked by antivirus software

## Development Notes

### Customizing UI

- Update layout/control code directly in `VP_Config_GUI.py`
- Update tooltips and config mapping in `VP_Config_GUI.py`

## License

© 2026 Mick Jolley (mickj1948@gmail.com)

## Support

For issues or suggestions, visit: https://github.com/mickjolley/visual-phaser
