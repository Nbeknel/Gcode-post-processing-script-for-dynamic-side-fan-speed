# Gcode-post-processing-script-for-dynamic-side-fan-speed
A gcode post-processing script that allows for dynamic speed control of the side fan.

Additionaly it can calculate material cost based on extrusion role (e.g. you want to charge more for supports).

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

`pps_custom_variable=[value];`,

no spaces, semicolon at the end is required. All variables are non-negative float values. Default values are either set in the script or taken from your printer/print/filament profiles. Variables set in printer_notes override default values, variables in notes override those set in printer_notes and default values, variables set in filament_notes override all other values. A list of all available variables can be found [here](https://github.com/Nbeknel/Slic3r-Post-processing-scripts/wiki).

Instead of using the in slicer variable full_fan_speed_layer this script implements two new variables `fan_max_positive_step` and `fan_max_negative_step`. `fan_max_positive_step` defines the maximum increase in percentages for the fan speed between layers, `fan_max_negative_step` defines the maximum decrease in percentages. E.g. if `fan_max_positive_step` is set to 25, `fan_max_negative_step` is set to 10, fan speed for the layer with number n is 49, then the fan speed for the layer with number n+1 will lie between 39 and 74.

### Current limitations
- single extruder setup

## v1.0 improvements
- Fixed recognition of declared variables in notes, now are required to end with a semicolon ';'.
- Added support for relative extrusion and volumetric.
- Changed time estimation, introduced a new variable 'theta' and calculate time as 'theta' * pessimistic + (1 - 'theta') * optimistic, default value for 'theta' is 1/3.
- Account for acceleration for retraction moves.
- Disabling fan for the first few layers is now height dependant. Introduced a new variable `disable_fan_initial_height` which can be manually set, or is calculated from layer height. Its actual value will be the maximum of the two.

## v0.3 improvements
- Added OrcaSlicer support.
- Reworked time calculation, previously it was calculated without taking acceleration into consideration (optimistic). Current implementation calculates the time for each movement from standstill to standstill (0 to target speed and target speed to 0) (pesimistic) and takes the arithmetic average of the optimistic and pessimistic estimations.
- Some minor corrections.

## v0.2 improvements
- added PrusaSlicer Support
- removed pps_wipe_tower_cost_multiplier for SuperSlicer
- removed the ability to change the values of `pps_fill_density`, `pps_filament_diameter`, `pps_filament_cost` and `pps_filament_density` as they're only used for cost calculation and do not have an influence on the speed of the side fan

## v0.1
Initial gcode post-processing script.
- works in SuperSlicer, not PrusaSlicer nor OrcaSlicer
- single extruder setup
- absolute E distances
- non-volumetric E
