# Visual Phaser Configuration GUI

A wxPython-based graphical user interface for editing the Visual Phaser `VP_configV1.py` configuration file.

## Features

- **Path Selection**: Browse and select directories using file dialogs for:
  - `FILES_PATH` - DNA files directory
  - `WORKING_DIRECTORY` - Output directory
  - `MAP_PATH` - Map file directory

- **File Management**:
  - Add/remove `PHASED_FILES` and `EVIL_TWINS` using file selectors
  - Edit `SIBLINGS`, `COUSINS`, and `CHROMOSOMES` as comma-separated lists
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
pip install wxPython
```

2. Navigate to the visual-phaser directory:
```bash
cd path/to/visual-phaser
```

## Usage

### Launch the GUI

From command line:
```bash
python VP_Config_GUI_Launcher.py
```

Or directly:
```bash
python VP_Config_GUI.py
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
     - **File selectors**: Choose multiple files for lists

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

## File Structure

- **VP_Config_GUI.py** - Main GUI application (uses wxPython ScrolledPanel)
- **VP_Config_GUI_Launcher.py** - Entry point script for launching the application
- **VP_Config_Resources.py** - Resource definitions, field metadata, and tooltips (boa-constructor pattern)
- **VP_configV1.py** - Original configuration file (edited by the GUI)

## Boa Constructor Methodology

This GUI follows the boa-constructor pattern for modular wxPython development:

- **Separation of Concerns**:
  - GUI logic in VP_Config_GUI.py
  - Resource definitions in VP_Config_Resources.py
  - Launcher script for application entry

- **Resource Management**:
  - All tooltips, labels, and field definitions centralized in Resources
  - Easy to maintain, localize, or modify without changing GUI code
  - Field metadata includes type, constraints, and defaults

- **Extensibility**:
  - Add new fields by updating FIELD_DEFINITIONS and FIELD_SECTIONS in Resources
  - New field types can be added by creating corresponding Create*Control methods

## Configuration Parameters Reference

### Paths
- **FILES_PATH**: Directory containing DNA files
- **WORKING_DIRECTORY**: Where output files (.xlsx, .py) are saved
- **MAP_PATH**: Directory containing min_map.txt

### File Lists
- **SIBLINGS**: DNA sample files to compare (minimum 2)
- **PHASED_FILES**: Pre-phased files to compare
- **EVIL_TWINS**: Files to compare with siblings
- **COUSINS**: Cousin relationships to track
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
pip install --upgrade wxPython
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

### Adding New Configuration Fields

1. Add field definition to `FIELD_DEFINITIONS` in VP_Config_Resources.py
2. Add field to appropriate section in `FIELD_SECTIONS`
3. (Optional) Add Create*Control method in VP_Config_GUI.py if using new control type
4. Update LoadConfig and OnSaveConfig methods if using new control type

### Customizing UI

- Modify WINDOW_WIDTH and WINDOW_HEIGHT in VP_Config_Resources.py
- Change PADDING and font sizes for UI layout
- Update APP_TITLE, APP_VERSION in Resources for branding

## License

© 2026 Mick Jolley (mickj1948@gmail.com)

## Support

For issues or suggestions, visit: https://github.com/Daverz/visual-phaser
