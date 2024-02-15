# Slic3r-Post-processing-script
A gcode post-processing script that allows for dynamic speed control of the side fan.

### How to use
In your slicer of choice go to

`Print settings > Output options > Post-processing script`

and enter the following:

`"A:\bsolute\path\to\python.exe" "A:\bsolute\path\to\post\processing\script.py" "SlicerAbbreviation"`,

where `"SlicerAbbreviation"` is
- `"SS"` for SuperSlicer
- `"PS"` for PrusaSlicer
- `"OS"` for OrcaSlicer

Slicer abbreviations are necessary for the script to work and are not interchangeable, due to different slicers naming the same feature/parameter differently.

For additional customisation you can add custom variables in either printer_notes, notes or filament_notes as follows:

`pps_custom_variable=[value]`,

no spaces, each new variable on a new line. All variables are non-negative float values. Default values are either set in the script or taken from your printer/print/filament profiles. Variables set in printer_notes override default values, variables in notes override those set in printer_notes and default values, variables set in filament_notes override all other values.

### Current limitations
- works in SuperSlicer, not PrusaSlicer nor OrcaSlicer
- single extruder setup
- absolute E distances
- non-volumetric E
