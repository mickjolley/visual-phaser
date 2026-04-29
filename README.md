# visual-phaser

1. Overview

  Visual Phaser is a specialized Python-based tool that automates the process of "phasing" 
  and comparing genetic markers  across multiple individuals. It identifies HIR (Half Identical
  Regions), FIR (Fully Identical Regions) and NIRs (Non Identical Regions), generating
  detailed Excel reports and visual chromosome maps.

  Key Features:
   * Hybrid Architecture: Uses Multiprocessing for heavy genetic calculations and
     Multithreading for fast file I/O and image generation.
   * Broad Compatibility: Supports raw DNA data from AncestryDNA, 23andMe, and other
     major providers.
   * Visual Output: Automatically generates and embeds chromosome visualizations directly
     into Excel worksheets.

  ---

2. Data Requirements

   Raw DNA Files:
      Must be placed in a single directory. Files must tab-delimited .txt files
      following the naming convention:
                                          Company_Name_raw_dna.txt.
      Examples: Ancestry_John_raw_dna.txt, FTDNA_Sue_raw_dna.txt
      Either rename your ,txt files or, if they are in .csv format use either
                                        ancestry_csv_to_tab_converter_V1.exe or
                                        non_ancestry_csv_to_tab_converter_V1.exe 
     to convert them. Make sure to fill in the blanks in the appropriate configuration files 
     (ACTTC_config_V1exe.json or  NACTTC_config_V1exe.json respectively).

  Genetic Map:
     A file named min_map.txt containing Centimorgan (cM) mapping data for
     chromosomes.

  ---

  Configuration (VPnew_config_V21super.json)
     The behavior of the script is entirely controlled by the .json configuration file. Note that 
     double quotation marks only can be used. In addition “true” and “false” must be lower 
     case. The congiguration file MUST be in the same folder as the .exe file.

      Path Settings
      * FILES_PATH: The directory containing your raw DNA .txt files.
      * WORKING_DIRECTORY: The folder where the output Excel file and temporary images
        will be stored.
      * MAP_PATH: The directory containing min_map.txt.

  Analysis Groups
    * SIBLINGS: A list of names for sibling comparison (e.g., ["Barb", "Jan", "Pat"]).
    * COUSINS: A list of names for cousin comparison. If populated, the tool looks for an
       existing Excel file to update.
    * PHASED_FILES / EVIL_TWINS: Advanced files for phased data comparisons. These are
      created by “Phased_Kit_Maker_V5.exe” and its configuration file “PKMconfig_V5exe.json”. 
      The default character is “X”, but anything can be used. Make sure the same character is
      entered in the Visual Phaser configuration file NO_CALL option.

  Technical Thresholds
    * HIR_CUTOFF / FIR_CUTOFF: The minimum cM length required to qualify as a match
      (default: 7 for HIR, 1 for FIR).
    * HIR_SNP_MIN / FIR_SNP_MIN: The minimum number of SNPs required for a valid
      segment (defaults 200 and 75 respectively).
    * RESOLUTION: The level of detail in the visual bars (default = 1).
    * NO_CALL: The character used for missing data in your phased and evil twin files. 

  ---

3. Operation

   1. Prepare your data: Ensure your raw DNA files are named correctly.
   2. Configure: Update VPnew_config_V21super.json with your file paths and names.
   3. Run the script by double clicking on it.
   4. Monitor Output: The CLI will display progress for each chromosome.
   5. Finalize: Once finished, the script will prompt you to enter “q” to exit. Your Excel file will
       be  ready in the WORKING_DIRECTORY.

  ---

4. Understanding the Results

  The tool produces an Excel workbook (.xlsx) with a sheet for each chromosome (Chr1–
  Chr23).

  The Visualization Area
   * Limegreen (Fully Identical): Indicates both chromosomes match (FIR).
   * Yellow (Half Identical): Indicates one chromosome matches (HIR).
   * Crimson (No Match): Indicates no matching alleles.
   * Blue Bar (Underneath): Represents the identified HIR segment.
   * Orange Bar (Underneath): Represents the identified FIR segment.

  Tables & Data
   * Segment Tables: Columns B–F contain the Start/Finish positions (Mb), Start/Finish cM,
     and total cM/SNP counts for every detected match.
   * Recombination Points: If AUTO_REC_PNTS is enabled, the tool will mark the exact
     positions where genetic crossovers occurred.

  ---
  © 2026 Mick Jolley. Optimized for high-speed genetic analysis.























