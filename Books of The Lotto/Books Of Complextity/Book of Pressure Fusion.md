# Book of Pressure Fusion

Infinite Inner World shared metric reference

Folder: the book of complexity

Scope:

```text
Sorted Pressure type + Draw Pressure type
Sorted Set Arc family + Draw Set Arc family
```

## Purpose

Pressure Fusion classifies how the sorted pressure and draw pressure redistribute inside the same set.

It answers:

```text
Does the set keep the same pressure after draw order is restored?
Does the pressure type match?
Does the pressure family match?
Is the pressure inverted?
Or is the pressure redistributed into a different shape?
```

Pressure Fusion is shared because it needs both Sorted form and Draw form.

## Fields

Pressure Fusion lives inside Draw Pressure, but it is a shared metric because it compares both sides.

Fields:

```text
pressure_fusion
pressure_fusion_profile
pressure_fusion_constellation
```

Field meanings:

```text
pressure_fusion                classification of sorted-vs-draw pressure relationship
pressure_fusion_profile        exact SORTED_TYPE_TO_DRAW_TYPE profile
pressure_fusion_constellation  constellation label attached to the fusion class
```

## Fusion Profile

The profile uses this exact format:

```text
SORTEDPRESSURE_TO_DRAWPRESSURE
```

Examples:

```text
UPLIFT_TO_TENSION
UPLIFT_TO_SEPERATION
UPLIFT_TO_UPLIFT
RESET_TO_CRISIS
```

This profile is the sharpest readable statement of how pressure changed when the same set moved from sorted body to draw body.

## Fusion Classes

```text
MATCHED_FUSION
TYPE_FUSION
FAMILY_FUSION
INVERTED_FUSION
REDISTRIBUTED_FUSION
```

Class meanings:

```text
MATCHED_FUSION
  Sorted pressure type and draw pressure type match.
  Sorted arc family and draw arc family also match.

TYPE_FUSION
  Sorted pressure type and draw pressure type match.
  Arc family does not fully match.

FAMILY_FUSION
  Sorted arc family and draw arc family match.
  Pressure type does not match.

INVERTED_FUSION
  Sorted pressure and draw pressure are known opposite pairs.

REDISTRIBUTED_FUSION
  Pressure does not match by type, family, or inversion.
  The same set redistributed pressure into a different natural shape.
```

## Inverted Pressure Pairs

The known inverted pairs are:

```text
RESET <-> UPLIFT
DOWNFALL <-> SURGE
NEUTRAL <-> STILLNESS
EXPANSION <-> CRISIS
```

If the sorted pressure and draw pressure form one of those pairs, the set receives `INVERTED_FUSION`.

## Constellation Labels

Each fusion class receives a constellation label:

```text
MATCHED_FUSION         Orion
TYPE_FUSION            Lyra
FAMILY_FUSION          Cygnus
REDISTRIBUTED_FUSION   Draco
INVERTED_FUSION        Phoenix
```

Constellations are labels only. They do not change the pressure math.

## Latest Draw Example

Latest trusted packet:

```text
date         2026-06-17
draw form    49-53-3-26-61
sorted form  3-26-49-53-61
```

Pressure sides:

```text
sorted_pressure_type  UPLIFT
sorted_arc_family     Burst

draw_pressure_type    TENSION
draw_arc_family       Volcanic
```

Fusion:

```text
pressure_fusion_profile        UPLIFT_TO_TENSION
pressure_fusion                REDISTRIBUTED_FUSION
pressure_fusion_constellation  Draco
```

Plain read:

```text
The sorted body rises as UPLIFT, but the natural draw body redistributes into TENSION.
```

## What Pressure Fusion Does Not Do

Pressure Fusion does not replace Set Health or Set Anatomy.

It only classifies the pressure relationship between:

```text
sorted pressure
draw pressure
```

Set Health compresses the readable identity.
Set Anatomy expands the technical body.

