#!/usr/bin/python

import re
import sys
import math
import os

filename = sys.argv[-1]

slicer = sys.argv[-2]

# Reading file and storing in memory
with open(filename, "r") as file:
    lines = file.readlines()

print(f"Original file: {len(lines)} lines\n")

# Preprocessing
#START

feature_types = {
    "Unknown": {
        "OS": "",
        "PS": "Unknown",
        "SS": "Unknown",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Internal perimeter": {
        "OS": "Inner wall",
        "PS": "Perimeter",
        "SS": "Internal perimeter",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "External perimeter": {
        "OS": "Outer wall",
        "PS": "External perimeter",
        "SS": "External perimeter",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Overhang perimeter": {
        "OS": "Overhang wall",
        "PS": "Overhang perimeter",
        "SS": "Overhang perimeter",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Internal infill": {
        "OS": "Sparse infill",
        "PS": "Internal infill",
        "SS": "Internal infill",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Solid infill": {
        "OS": "Internal solid infill",
        "PS": "Solid infill",
        "SS": "Solid infill",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Top solid infill": {
        "OS": "Top surface",
        "PS": "Top solid infill",
        "SS": "Top solid infill",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Ironing": {
        "OS": "",
        "PS": "Ironing",
        "SS": "Ironing",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Bridge infill": {
        "OS": "Bridge",
        "PS": "Bridge infill",
        "SS": "Bridge infill",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Internal bridge infill": {
        "OS": "Internal Bridge",
        "PS": "Bridge infill",
        "SS": "Internal bridge infill",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Thin wall": {
        "OS": "",
        "PS": "External perimeter",
        "SS": "Thin wall",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Gap fill": {
        "OS": "Gap infill",
        "PS": "Gap fill",
        "SS": "Gap fill",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Skirt": {
        "OS": "Skirt",
        "PS": "Skirt/Brim",
        "SS": "Skirt",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Support material": {
        "OS": "",
        "PS": "Support material",
        "SS": "Support material",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Support material interface": {
        "OS": "",
        "PS": "Support material interface",
        "SS": "Support material interface",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Custom": {
        "OS": "Custom",
        "PS": "Custom",
        "SS": "Custom",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Bottom surface": {
        "OS": "Bottom surface",
        "PS": "Solid infill",
        "SS": "Solid infill",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        },
    "Brim": {
        "OS": "Brim",
        "PS": "Skirt/Brim",
        "SS": "Skirt",
        "Length": 0,
        "Cost_multiplier" : 1,
        "Cost": 0
        }
    }

value = 0

dtype = 1

slicer_variables = {
    "fill_density": {
        "PS": "SLIC3R_FILL_DENSITY",
        "SS": "SLIC3R_FILL_DENSITY",
        value: 0,
        dtype: float
        },
    "filament_diameter": {
        "PS": "SLIC3R_FILAMENT_DIAMETER",
        "SS": "SLIC3R_FILAMENT_DIAMETER",
        value: 1.75,
        dtype: float
        },
    "filament_cost": {
        "PS": "SLIC3R_FILAMENT_COST",
        "SS": "SLIC3R_FILAMENT_COST",
        value: 0,
        dtype: float
        },
    "filament_density": {
        "PS": "SLIC3R_FILAMENT_DENSITY",
        "SS": "SLIC3R_FILAMENT_DENSITY",
        value: 1,
        dtype: float
        },
    "printer_notes": {
        "PS": "SLIC3R_PRINTER_NOTES",
        "SS": "SLIC3R_PRINTER_NOTES",
        value: "",
        dtype: str
        },
    "notes": {
        "PS": "SLIC3R_NOTES",
        "SS": "SLIC3R_NOTES",
        value: "",
        dtype: str
        },
    "filament_notes": {
        "PS": "SLIC3R_FILAMENT_NOTES",
        "SS": "SLIC3R_FILAMENT_NOTES",
        value: "",
        dtype: str
        }
    }

variables = {
    "time_estimation_compensation": {
        "PS": "",
        "SS": "SLIC3R_TIME_ESTIMATION_COMPENSATION",
        value: 100,
        dtype: float
        },
    "time_start_gcode": {
        "PS": "",
        "SS": "SLIC3R_TIME_START_GCODE",
        value: 0,
        dtype: float
        },
    "time_cost": {
        "PS": "",
        "SS": "SLIC3R_TIME_COST",
        value: 0,
        dtype: float
        },
    "fan_printer_min_speed": {
        "PS": "SLIC3R_MIN_FAN_SPEED",
        "SS": "SLIC3R_FAN_PRINTER_MIN_SPEED",
        value: 0,
        dtype: float
        },
    "default_fan_speed": {
        "PS": "",
        "SS": "SLIC3R_DEFAULT_FAN_SPEED",
        value: -1,
        dtype: float
        },
    "disable_fan_first_layers": {
        "PS": "SLIC3R_DISABLE_FAN_FIRST_LAYERS",
        "SS": "SLIC3R_DISABLE_FAN_FIRST_LAYERS",
        value: 1,
        dtype: int
        },
    "fan_below_layer_time": {
        "PS": "SLIC3R_FAN_BELOW_LAYER_TIME",
        "SS": "SLIC3R_FAN_BELOW_LAYER_TIME",
        value: 60,
        dtype: float
        },
    "max_fan_speed": {
        "PS": "SLIC3R_MAX_FAN_SPEED",
        "SS": "SLIC3R_MAX_FAN_SPEED",
        value: 0,
        dtype: float
        },
    "slowdown_below_layer_time": {
        "PS": "SLIC3R_SLOWDOWN_BELOW_LAYER_TIME",
        "SS": "SLIC3R_SLOWDOWN_BELOW_LAYER_TIME",
        value: 5,
        dtype: float
        }
    }

fan_max_positive_step = 100

fan_max_negative_step = 100

for variable_name, variable in variables.items():
    if variable[slicer] != "":
        variables[variable_name][value] = os.environ[variable[slicer]]
    if isinstance(variable[value], str) and '%' in variable[value]:
        variables[variable_name][value] = variable[value][:-1:]
    if not isinstance(variable[value], variable[dtype]):
        variables[variable_name][value] = variable[dtype](variable[value])
        
for variable_name, variable in slicer_variables.items():
    if variable[slicer] != "":
        slicer_variables[variable_name][value] = os.environ[variable[slicer]]
    if '%' in variable[value]:
        slicer_variables[variable_name][value] = variable[value][:-1:]
    if not isinstance(variable[value], variable[dtype]):
        slicer_variables[variable_name][value] = variable[dtype](variable[value])

for notes in ["printer_notes", "notes", "filament_notes"]:
    for feature_type, feature in feature_types.items():
        match = re.search(fr"""pps_{feature[slicer].replace(" ", "_").lower()}_cost_multiplier=(\d+\.?\d*|\.\d+)(\s|$)""", slicer_variables[notes][value])
        if match:
            feature_types[feature_type]["Cost_multiplier"] = float(match.group(1))

    for variable_name, variable in variables.items():
        match = re.search(fr"""pps_{variable_name}=(\d+\.?\d*|\.\d+)(\s|$)""", slicer_variables[notes][value])
        if match:
            variables[variable_name][value] = float(match.group(1))
    
    match = re.search(fr"pps_fan_max_positive_step=(\d+\.?\d*|\.\d+)(\s|$)", slicer_variables[notes][value])
    if match:
        fan_max_positive_step = float(match.group(1))
    
    match = re.search(fr"pps_fan_max_negative_step=(\d+\.?\d*|\.\d+)(\s|$)", slicer_variables[notes][value])
    if match:
        fan_max_negative_step = float(match.group(1))

feature_types["Internal infill"]["Cost_multiplier"] = max(feature_types["Internal infill"]["Cost_multiplier"],\
                                                         0.01 * slicer_variables["fill_density"][value] * feature_types["Solid infill"]["Cost_multiplier"])

if variables["default_fan_speed"][value] < 0:
    variables["default_fan_speed"][value] = 0
    if slicer == "PS" and bool(os.environ["SLIC3R_FAN_ALWAYS_ON"]):
        variables["default_fan_speed"][value] = variables["fan_printer_min_speed"][value]

if variables["max_fan_speed"][value] < variables["default_fan_speed"][value]:
    variables["max_fan_speed"][value], variables["default_fan_speed"][value] = variables["default_fan_speed"][value], variables["max_fan_speed"][value]

pps_config = []

for feature_type, feature in feature_types.items():
    pps_config.append(f"""; pps_{feature[slicer].replace(" ", "_").lower()}_cost_multiplier = {feature["Cost_multiplier"]}\n""")

for variable_name, variable in variables.items():
    pps_config.append(f"""; pps_{variable_name} = {variable[value]}\n""")

pps_config.extend([f"; pps_fan_max_positive_step = {fan_max_positive_step}\n", f"; pps_fan_max_negative_step = {fan_max_negative_step}\n"])

pps_config.sort(key=str.lower)

time_50 = 0.5 * (variables["max_fan_speed"][value] + variables["default_fan_speed"][value])

time_amplitude = 0.5 * (variables["max_fan_speed"][value] - variables["default_fan_speed"][value])

a = 2.25 / math.sqrt(14)

def get_key(feature):
    for key, val in feature_types.items():
        if val[slicer] == feature:
            return key
    return "Unknown"

def get_time(speed, x_delta, y_delta, z_delta, e_delta):
    speed = max(1, speed)
    distance = math.sqrt(x_delta * x_delta + y_delta * y_delta + z_delta * z_delta)
    if distance < 0.001:
        return 60 * abs(e_delta) / speed
    return 60 * distance / speed

def delta_fan(layer_time_prev, layer_time_curr, layer_time_next):
    delta = 0
    if layer_time_curr - layer_time_prev < -1 * fan_max_negative_step:
        delta -= layer_time_curr - layer_time_prev + fan_max_negative_step
    elif layer_time_curr - layer_time_prev > fan_max_positive_step:
        delta -= layer_time_curr - layer_time_prev - fan_max_positive_step

    if layer_time_curr - layer_time_next < -1 * fan_max_positive_step:
        delta -= layer_time_curr - layer_time_next + fan_max_positive_step
    elif layer_time_curr - layer_time_next > fan_max_negative_step:
        delta -= layer_time_curr - layer_time_next - fan_max_negative_step

    return delta

class Layer:
    def __init__(self):
        self.layer = []
        self.time = 0
        self.height = 0
        self.features = set([])
        self.fan_speed = 0
        self.delta = 0
        self.delta_coefficient = 0

    def append_line(self, line: str):
        self.layer.append(line)
        
    def extend_lines(self, lines: iter):
        self.layer.extend(lines)

    def add_time(self, time: float):
        self.time += time

    def set_height(self, height: float):
        self.height = max(self.height, height)

    def add_feature(self, feature: str):
        self.features.add(feature)

    def has_not_only_supports(self) -> bool:
        self.features.difference_update(["Support material interface", "Support material"])
        return len(self.features) > 0

    def calculate_delta_coefficient(self):
        t = (self.time - time_50) / time_amplitude
        self.delta_coefficient = max(0.1, a / math.sqrt(25/56 + t ** 2))

    def calculate_fan_speed(self):
        if self.time >= variables["fan_below_layer_time"][value]:
            self.fan_speed = variables["default_fan_speed"][value]
        elif self.time < variables["slowdown_below_layer_time"][value]:
            self.fan_speed = variables["max_fan_speed"][value]
        else:
            self.fan_speed = variables["max_fan_speed"][value] -\
            (self.time - variables["slowdown_below_layer_time"][value]) / (variables["fan_below_layer_time"][value] - variables["slowdown_below_layer_time"][value]) *\
            (variables["max_fan_speed"][value] - variables["default_fan_speed"][value])
        self.calculate_delta_coefficient()

    def set_delta(self, delta: float):
        self.delta = delta

    def update_fan_speed(self):
        self.fan_speed += self.delta * self.delta_coefficient


#END

# Add extruder_partfan speed updates in gcode
#START
layers = []
layer = Layer()

speed = 1

y_prev = 0
z_prev = 0
x_prev = 0
e_prev = 0

x_curr = 0
y_curr = 0
z_curr = 0
e_curr = 0

type_current = "Unknown"
total_time = variables["time_start_gcode"][value]

for line in lines:
    x_prev = x_curr
    y_prev = y_curr
    z_prev = z_curr
    e_prev = e_curr

    match = re.search(r"^;LAYER_CHANGE$", line)
    if match and layer.has_not_only_supports():
        layer.time *= 0.01 * variables["time_estimation_compensation"][value]
        layer.calculate_fan_speed()
        layers.append(layer)
        total_time += layer.time
        layer = Layer()

    match = re.search(r"^;Z(-?(\d+\.?\d*|\.\d+))$", line)
    if match:
        layer.set_height(float(match.group(1)))

    match = re.search(r"^;TYPE:(.+)$", line)
    if match:
        type_current = get_key(match.group(1))
        layer.add_feature(type_current)

    match = re.search(r"^G1.*?F(-?(\d+\.?\d*|\.\d+))", line)
    if match:
        speed = float(match.group(1))

    match = re.search(r"^G1.*?X(-?(\d+\.?\d*|\.\d+))", line)
    if match:
        x_curr = float(match.group(1))

    match = re.search(r"^G1.*?Y(-?(\d+\.?\d*|\.\d+))", line)
    if match:
        y_curr = float(match.group(1))

    match = re.search(r"^G1.*?Z(-?(\d+\.?\d*|\.\d+))", line)
    if match:
        z_curr = float(match.group(1))

    match = re.search(r"^G1.*?E(-?(\d+\.?\d*|\.\d+))", line)
    if match:
        e_curr = float(match.group(1))

    match = re.search(r"^G92 E(-?(\d+\.?\d*|\.\d+))", line)
    if match:
        e_prev = float(match.group(1))
        e_curr = float(match.group(1))

    x_delta = x_curr - x_prev
    y_delta = y_curr - y_prev
    e_delta = e_curr - e_prev
    z_delta = z_curr - z_prev
    feature_types[type_current]["Length"] += e_delta

    if x_delta ** 2 + y_delta ** 2 + z_delta ** 2 + e_delta ** 2 > 0:
        layer.add_time(get_time(speed, x_delta, y_delta, z_delta, e_delta))

    layer.append_line(line)

layer.calculate_fan_speed()
layers.append(layer)

lines = []

while True:
    delta_sum = 0
    for i in range(1, len(layers) - 1):
        layers[i].set_delta(delta_fan(layers[i - 1].fan_speed, layers[i].fan_speed, layers[i + 1].fan_speed))
        delta_sum += abs(layers[i].delta)
    for i in range(1, len(layers) - 1):
        layers[i].update_fan_speed()
    if delta_sum < 0.05 * (1 + len(layers)):
        break

for i in range(min(variables["disable_fan_first_layers"][value] + 1, len(layers))):
    layers[i].fan_speed = 0

while True:
    delta_sum = 0
    for i in range(variables["disable_fan_first_layers"][value] + 1, len(layers) - 1):
        layers[i].set_delta(delta_fan(layers[i - 1].fan_speed, layers[i].fan_speed, layers[i + 1].fan_speed))
        delta_sum += abs(layers[i].delta)
    for i in range(variables["disable_fan_first_layers"][value] + 1, len(layers) - 1):
        layers[i].update_fan_speed()
    if 255 * delta_sum < 0.05  * (1 + len(layers)):
        break
#END

# Cost calculation
#START
variables["time_cost"][value] = total_time * variables["time_cost"][value] / 3600

cost = variables["time_cost"][value]

for feature_type, feature in feature_types.items():
    feature["Cost"] = 0.000_000_25 * math.pi * (slicer_variables["filament_diameter"][value] ** 2) *\
       feature["Length"] * feature["Cost_multiplier"] * slicer_variables["filament_density"][value] * slicer_variables["filament_cost"][value]
    cost += feature["Cost"]

print(f"{cost=:.2f}")
#END

# Add post processing script variables to gcode as a config
layer = []
for line in layers[-1].layer:
    match = re.search(r"^.*_config = begin$", line)
    if match:
        layer.append("; pps_config = begin\n")
        layer.extend(pps_config)
        layer.append("; pps_config = end\n\n")
    layer.append(line)
layers[-1].layer = layer

# Add side fan commands
is_start_gcode_skipped = False

for layer in layers:
    if is_start_gcode_skipped:
        #lines.append(f"SET_FAN_SPEED FAN=extruder_partfan SPEED={layer.fan_speed:.2f}\n")
        fan = max(layer.fan_speed, variables["fan_printer_min_speed"][value]) * 2.55 if layer.fan_speed >= 0.75 * variables["fan_printer_min_speed"][value] else 0
        lines.append(f"M106 P2 S{fan:.2f}\n")
    is_start_gcode_skipped = True
    lines.extend(layer.layer)

print(f"Extruder partfan adjustments: {len(lines)} lines\n")


# Write to file
# Add cost per feature type in the beginning of the gcode
with open(filename, "w") as file:
    for i, line in enumerate(lines):
        if i == 1:
            file.write(f"; Cost calculated by post processing script: {cost:.2f}\n")
            for feature in feature_types.keys():
                if feature_types[feature]["Cost"] > 0:
                    file.write(f"; {feature_types[feature]['Cost']:.2f} - {feature_types[feature][slicer]}\n")
            file.write(f"; {variables['time_cost'][value]:.2f} - Time\n")
        file.write(line)

input("Press enter to exit: ")