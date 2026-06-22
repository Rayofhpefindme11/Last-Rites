# Book of Set Pressure Bridge

Infinite Inner World shared metric reference

Folder: the book of complexity

Scope:

```text
Sorted Pressure + Draw Pressure
```

## Purpose

Set Pressure Bridge is the shared pressure container that keeps Sorted Pressure and Draw Pressure together for the same set.

It answers:

```text
What does the set look like after sorting?
What does the same set look like in its natural draw order?
How different are those pressure reads?
```

Sorted Pressure and Draw Pressure are separate reads, but Set Pressure is where they become one shared metric.

## Set Pressure Fields

```text
metric
rule
sorted_pressure
draw_pressure
```

Field meanings:

```text
metric            Set Pressure
rule              explains that pressure is read in sorted and draw form
sorted_pressure   sorted-side pressure object
draw_pressure     draw-side pressure object
```

## Sorted Pressure Side

Sorted Pressure reads the ordered body:

```text
S1 Core -> S2 Entry -> S3 Bridge -> S4 Exit -> S5 Endpoint
```

It carries:

```text
pressure_shape
pressure_type
set_arc
set_arc_35
set_arc_family
set_arc_type
sorted_style
fp
total
edge_pressure
middle_pressure
middle_minus_edge
largest_gap
largest_gap_relation
```

Sorted Pressure is the structural pressure of the set after the numbers are placed into S1-S5.

## Draw Pressure Side

Draw Pressure reads the natural face:

```text
D1 starter -> D2 hold -> D3 stability -> D4 control -> D5 ender
```

It carries:

```text
pressure_shape
pressure_type
set_arc
set_arc_35
set_arc_family
set_arc_type
draw_style
draw_style_family
direction_pattern
transfer_pattern
draw_path_energy
draw_path_energy_average
draw_path_energy_class
draw_path_energy_spectrum
draw_path_energy_spectrum_range
draw_path_energy_gauge
draw_path_energy_gauge_range
sorted_position_energy
incoming_energy
incoming_energy_average
incoming_energy_class
incoming_energy_gauge
incoming_energy_gauge_range
outgoing_energy
outgoing_energy_average
outgoing_energy_class
outgoing_energy_gauge
outgoing_energy_gauge_range
energy_delta
flow_strength
flow_strength_average
flow_strength_class
flow_strength_element
flow_strength_element_range
pressure_flow
pressure_fusion
pressure_fusion_profile
pressure_fusion_constellation
containment_state
```

Draw Pressure is the natural-state pressure of the set in the order it actually appeared.

## Bridge Rule

Set Pressure does not choose one side over the other.

It preserves both:

```text
Sorted Pressure = structural body
Draw Pressure   = natural body
```

The bridge lets later scripts compare:

```text
sorted type vs draw type
sorted arc vs draw arc
sorted structure vs natural route
sorted compression/expansion vs draw motion energy
```

## Latest Draw Example

Latest trusted packet:

```text
date         2026-06-17
draw form    49-53-3-26-61
sorted form  3-26-49-53-61
```

Sorted Pressure:

```text
pressure_type        UPLIFT
pressure_shape       ++++
set_arc_type         SEPARATION
set_arc_family       Burst
set_arc              BBSS
set_arc_35           XII-XII-II-IV
edge_pressure        31
middle_pressure      27
middle_minus_edge    -4
largest_gap          23
largest_gap_relation S1->S2
```

Draw Pressure:

```text
pressure_type              TENSION
pressure_shape             +-++
set_arc_type               RESET
set_arc_family             Volcanic
set_arc                    SEBE
set_arc_35                 II-XXV-XII-XVIII
draw_style                 DRAW_ROUTE_S3_S4_S1_S2_S5
draw_style_family          Crest Valley
draw_path_energy           112
draw_path_energy_average   28.0
draw_path_energy_class     Directed Motion
draw_path_energy_spectrum  Green [27-28]
pressure_flow              UNKNOWN_BOUNDARY
containment_state          BOUNDARY_UNKNOWN
pressure_fusion_profile    UPLIFT_TO_TENSION
pressure_fusion            REDISTRIBUTED_FUSION
pressure_fusion_constellation Draco
```

Plain read:

```text
The sorted body is UPLIFT.
The natural draw body is TENSION.
The shared pressure bridge records the set as UPLIFT_TO_TENSION.
```

## What This Book Does Not Cover

This book does not redefine every sorted or draw pressure field.

Those details live in:

```text
Docs/Sorted form/Book of Sorted Pressure.md
Docs/draw form/Book of Draw Pressure.md
```

This book explains how both pressure sides stay joined as one shared metric.
