# Book of Draw Pressure

This book documents Draw Pressure for Infinite Inner World.

Draw Pressure is the set in its natural state. It reads the pressure of the actual D1-D5 draw-order face.

```text
D1 starter -> D2 hold -> D3 stability -> D4 control -> D5 ender
```

## Purpose

Draw Pressure answers these questions:

```text
What pressure shape does the natural draw face form?
How expensive is the draw path?
What Set Arc does the draw face create?
How does natural pressure compare to sorted pressure?
How does incoming energy compare to outgoing energy?
Is the motion contained, strained, or broken?
```

Draw Pressure is the pressure authority used by Set Health.

## Draw Pressure Fields

Draw Pressure contains:

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

## Pressure Shape

Draw pressure shape comes from the four signed draw movements:

```text
D1->D2
D2->D3
D3->D4
D4->D5
```

Each movement becomes:

```text
positive movement -> +
negative movement -> -
zero movement     -> 0
```

Pressure shape class table:

```text
---- RESET
---+ DOWNFALL
--+- YIELD
--++ NEUTRAL
-+-- PRESSED
-+-+ SEPERATION
-++- FLOW
-+++ EXPANSION
+--- CRISIS
+--+ STRETCH
+-+- COMPLUSION
+-++ TENSION
++-+ LINK
++-- STILLNESS
+++- SURGE
++++ UPLIFT
```

Implementation note:

The actual shape always has four signs. Use the exact four-character shape as the key.

## Draw Pressure As Natural State

Sorted Pressure is structural.

Draw Pressure is natural.

That is why Set Health uses Draw Pressure tone:

```text
Set Health = Natural Draw Pressure Tone + sorted body identity
```

## Set Arc

Draw Set Arc uses the four draw gaps and classifies them by size:

```text
S = Small   gap 1-10
M = Medium  gap 11-16
B = Burst   gap 17-24
E = Extreme gap 25+
```

Example:

```text
Draw gaps: 4, 50, 23, 35
Set Arc: S E B E
set_arc = SEBE
```

## Set Arc 35

Set Arc 35 is the Roman 35-class path of the draw gaps.

Example:

```text
Draw gaps: 4, 50, 23, 35
set_arc_35 = II-XXV-XII-XVIII
```

## Set Arc Family And Type

Set Arc Family:

```text
Volcanic  = two or more E, or at least one E and at least one B
Extreme   = exactly one E and no B
Burst     = at least one B and no E
Canonical = no B and no E
```

Set Arc Type:

```text
Volcanic -> RESET
Extreme  -> CRISIS
Burst    -> SEPARATION
Canonical -> COMPRESSION or EXPANSION by S/M balance
```

## Draw Path Energy

Draw Path Energy is the total absolute distance traveled inside D1-D5.

Formula:

```text
draw_path_energy = gap(D1->D2) + gap(D2->D3) + gap(D3->D4) + gap(D4->D5)
```

Average:

```text
draw_path_energy_average = draw_path_energy / 4
```

Latest draw:

```text
gaps = 4, 50, 23, 35
draw_path_energy = 112
draw_path_energy_average = 28.0
```

## Broad Motion Class

Path energy average uses the broad motion scale. It returns `Still Motion` for zero. Values above the lane max are capped into the final broad label, `Chaotic Motion`.

```text
0     Still Motion
1-10  Light Motion
11-20 Calm Motion
21-30 Directed Motion
31-40 Transitional Motion
41-50 Crest Echo Motion
51-60 Fatigued Motion
61-69 Chaotic Motion
```

Latest draw:

```text
draw_path_energy_average = 28.0
draw_path_energy_class = Directed Motion
```

## Path Energy Spectrum

Path energy average also uses the spectrum 35-class scale. It returns `Black` for zero. Values above the lane max are capped into the final spectrum label, `Apex Violet`.

```text
1-2   Infrared
3-4   Deep Red
5-6   Red
7-8   Scarlet
9-10  Vermilion
11-12 Red Orange
13-14 Orange
15-16 Amber
17-18 Gold
19-20 Yellow
21-22 Lemon
23-24 Chartreuse
25-26 Yellow Green
27-28 Green
29-30 Emerald
31-32 Spring Green
33-34 Mint
35-36 Aqua
37-38 Cyan
39-40 Sky Blue
41-42 Azure
43-44 Blue
45-46 Royal Blue
47-48 Indigo
49-50 Deep Indigo
51-52 Violet
53-54 Deep Violet
55-56 Purple
57-58 Lavender
59-60 Magenta
61-62 Rose
63-64 Prism White
65-66 Ultraviolet
67-68 Deep Ultraviolet
69-70 Apex Violet
```

Latest draw:

```text
draw_path_energy_average = 28.0
draw_path_energy_spectrum = Green [27-28]
```

## Energy Gauge

Energy gauge uses the motion gauge names across the total energy value. Unlike a single lane, total energy can exceed 69, so the 35-class gauge cycles forward in two-number spaces.

Latest draw:

```text
draw_path_energy = 112
draw_path_energy_gauge = Monarch [111-112]
```

## Incoming And Outgoing Energy

Incoming energy is the sum of absolute incoming lane motions from previous draw to current draw.

Outgoing energy is the sum of absolute outgoing lane motions from current draw to next draw.

Formulas:

```text
incoming_energy = abs(D1 incoming) + abs(D2 incoming) + abs(D3 incoming) + abs(D4 incoming) + abs(D5 incoming)
outgoing_energy = abs(D1 outgoing) + abs(D2 outgoing) + abs(D3 outgoing) + abs(D4 outgoing) + abs(D5 outgoing)
```

Averages:

```text
incoming_energy_average = incoming_energy / 5
outgoing_energy_average = outgoing_energy / 5
```

If previous or next draw is missing, the corresponding energy is `None`.

## Energy Delta And Flow Strength

Energy delta:

```text
energy_delta = outgoing_energy - incoming_energy
```

Flow strength:

```text
flow_strength = abs(energy_delta)
flow_strength_average = flow_strength / 5
```

## Flow Strength Elements

Flow strength average uses periodic-table labels:

```text
1-2   Hydrogen
3-4   Helium
5-6   Lithium
7-8   Beryllium
9-10  Boron
11-12 Carbon
13-14 Nitrogen
15-16 Oxygen
17-18 Fluorine
19-20 Neon
21-22 Sodium
23-24 Magnesium
25-26 Aluminum
27-28 Silicon
29-30 Phosphorus
31-32 Sulfur
33-34 Chlorine
35-36 Argon
37-38 Potassium
39-40 Calcium
41-42 Scandium
43-44 Titanium
45-46 Vanadium
47-48 Chromium
49-50 Manganese
51-52 Iron
53-54 Cobalt
55-56 Nickel
57-58 Copper
59-60 Zinc
61-62 Gallium
63-64 Germanium
65-66 Arsenic
67-68 Selenium
69-70 Bromine
```

## Pressure Flow

Pressure flow compares incoming and outgoing energy.

```text
outgoing_energy > incoming_energy -> RELEASE
incoming_energy > outgoing_energy -> RETENTION
equal energy                      -> BALANCED_TRANSFER
missing boundary                  -> UNKNOWN_BOUNDARY
```

## Pressure Fusion

Pressure fusion compares sorted pressure against draw pressure.

Fusion classes:

```text
MATCHED_FUSION        Orion
TYPE_FUSION           Lyra
FAMILY_FUSION         Cygnus
REDISTRIBUTED_FUSION  Draco
INVERTED_FUSION       Phoenix
```

Fusion profile:

```text
<sorted_pressure_type>_TO_<draw_pressure_type>
```

Latest draw:

```text
sorted_pressure_type = UPLIFT
draw_pressure_type   = TENSION
pressure_fusion_profile = UPLIFT_TO_TENSION
pressure_fusion = REDISTRIBUTED_FUSION
pressure_fusion_constellation = Draco
```

## Containment State

Containment state uses pressure flow, draw path energy average, and flow strength average.

Current states:

```text
BOUNDARY_UNKNOWN
CONTAINED_MOTION
CONTROLLED_VOLATILE_MOTION
STRAINED_MOTION
BROKEN_MOTION
```

Boundary unknown appears when previous or next draw is missing.

## Latest Draw Example

Latest trusted draw:

```text
Draw order: 49-53-3-26-61
```

Draw Pressure:

```text
pressure_shape                  +-++
pressure_type                   TENSION
set_arc                         SEBE
set_arc_35                      II-XXV-XII-XVIII
set_arc_family                  Volcanic
set_arc_type                    RESET
draw_style                      DRAW_ROUTE_S3_S4_S1_S2_S5
draw_style_family               Crest Valley
direction_pattern               +-++
transfer_pattern                S3-S4-S1-S2-S5
draw_path_energy                112
draw_path_energy_average        28.0
draw_path_energy_class          Directed Motion
draw_path_energy_spectrum       Green [27-28]
draw_path_energy_gauge          Monarch [111-112]
sorted_position_energy          8
incoming_energy                 139
incoming_energy_average         27.8
incoming_energy_class           Directed Motion
outgoing_energy                 None
pressure_flow                   UNKNOWN_BOUNDARY
pressure_fusion_profile         UPLIFT_TO_TENSION
pressure_fusion                 REDISTRIBUTED_FUSION
pressure_fusion_constellation   Draco
containment_state               BOUNDARY_UNKNOWN
```

## What This Book Does Not Cover

This book does not cover individual lane incoming/outgoing motion details. Those are documented in `Book of Draw Motion`.
