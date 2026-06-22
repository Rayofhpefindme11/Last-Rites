# Book of Sorted Pressure

This book documents the Sorted Pressure side of Set Pressure for Infinite Inner World.

Sorted Pressure reads pressure from the sorted structure:

```text
S1 Core -> S2 Entry -> S3 Bridge -> S4 Exit -> S5 Endpoint
```

Sorted Pressure is structural. It describes how the sorted set is spaced, where its pressure sits, and how its gaps divide between the outer edges and the middle body.

## Purpose

Sorted Pressure answers these questions:

```text
What is the sorted gap structure?
What is the sorted Set Arc?
Where is the largest sorted gap?
Are the outer edges heavier than the middle?
Is the middle heavier than the outer edges?
```

Sorted Pressure is not the natural draw-order pressure tone. Natural pressure comes from Draw Pressure. Set Health uses Draw Pressure for its tone.

## Sorted Pressure Fields

Sorted Pressure contains:

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

Field meanings:

```text
pressure_shape       four-sign shape from sorted gap direction
pressure_type        pressure class from pressure_shape
set_arc              S/M/B/E arc from sorted gap sizes
set_arc_35           Roman 35-class gap path
set_arc_family       family of the S/M/B/E arc
set_arc_type         type produced by the S/M/B/E arc
sorted_style         whole-set Sorted Style name
fp                   finality point, largest number minus smallest number
total                sum of all five white balls
edge_pressure        S1->S2 gap plus S4->S5 gap
middle_pressure      S2->S3 gap plus S3->S4 gap
middle_minus_edge    middle_pressure minus edge_pressure
largest_gap          biggest sorted gap
largest_gap_relation sorted lane pair holding the biggest gap
```

## Important Sorted Pressure Note

Sorted form always ascends:

```text
S1 < S2 < S3 < S4 < S5
```

Therefore the sorted pressure shape is normally:

```text
++++
```

And the sorted pressure type is normally:

```text
UPLIFT
```

That is why Set Health does not use Sorted Pressure as its tone. Set Health uses Draw Pressure because draw order is the set in its natural state.

Sorted Pressure remains useful because its Set Arc, edge pressure, middle pressure, middle-minus-edge, and largest-gap fields still carry real structural information.

## Pressure Shape

Pressure shape is created from the sign of each adjacent lane movement.

For Sorted Pressure:

```text
S1->S2
S2->S3
S3->S4
S4->S5
```

Each step becomes:

```text
+ positive climb
- negative drop
0 zero
```

Since sorted lanes climb, Sorted Pressure usually produces:

```text
++++ UPLIFT
```

Full pressure-shape class table:

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

## Set Arc

Set Arc classifies each sorted gap by size using S/M/B/E.

```text
S = Small   gap 1-10
M = Medium  gap 11-16
B = Burst   gap 17-24
E = Extreme gap 25+
```

Formula:

```text
set_arc = pressure_symbol(gap1) + pressure_symbol(gap2) + pressure_symbol(gap3) + pressure_symbol(gap4)
```

Example:

```text
sorted gaps: 23, 23, 4, 8
set_arc: B B S S
set_arc = BBSS
```

## Set Arc 35

Set Arc 35 is the Roman-numeral version of the same four sorted gaps.

Example:

```text
sorted gaps: 23, 23, 4, 8
set_arc_35: XII-XII-II-IV
```

The Roman range table is documented in `Book of Basics`.

## Set Arc Family

Set Arc Family is derived from the S/M/B/E arc.

Rules:

```text
Volcanic  = two or more E, or at least one E and at least one B
Extreme   = exactly one E and no B
Burst     = at least one B and no E
Canonical = no B and no E
```

## Set Arc Type

Set Arc Type comes from Set Arc Family and the S/M balance.

Rules:

```text
Volcanic -> RESET
Extreme  -> CRISIS
Burst    -> SEPARATION
```

If the family is Canonical:

```text
more S than M -> COMPRESSION
more M than S -> EXPANSION
SMSM or MSMS  -> EXPANSION
otherwise     -> COMPRESSION
```

## Edge And Middle Pressure

Sorted Pressure splits the set into outer edges and middle body.

Outer edge gaps:

```text
S1->S2
S4->S5
```

Middle gaps:

```text
S2->S3
S3->S4
```

Formulas:

```text
edge_pressure = gap(S1->S2) + gap(S4->S5)
middle_pressure = gap(S2->S3) + gap(S3->S4)
middle_minus_edge = middle_pressure - edge_pressure
```

Interpretation:

```text
positive middle_minus_edge = middle wider/heavier than edges
negative middle_minus_edge = outer edges wider/heavier than middle
near zero                  = middle and edges closer to balanced
```

## Largest Gap

Largest gap fields:

```text
largest_gap
largest_gap_relation
```

The largest gap relation is one of:

```text
S1->S2
S2->S3
S3->S4
S4->S5
```

## Latest Draw Example

Latest trusted draw:

```text
Sorted White: 3-26-49-53-61
```

Sorted gaps:

```text
S1->S2 23
S2->S3 23
S3->S4 4
S4->S5 8
```

Sorted Pressure:

```text
pressure_shape       ++++
pressure_type        UPLIFT
set_arc              BBSS
set_arc_35           XII-XII-II-IV
set_arc_family       Burst
set_arc_type         SEPARATION
sorted_style         Trio
fp                   58
total                192
edge_pressure        31
middle_pressure      27
middle_minus_edge    -4
largest_gap          23
largest_gap_relation S1->S2
```

Calculations:

```text
edge_pressure = 23 + 8 = 31
middle_pressure = 23 + 4 = 27
middle_minus_edge = 27 - 31 = -4
```

## How Sorted Pressure Feeds Set Anatomy

Set Anatomy uses:

```text
middle_minus_edge
```

to classify:

```text
middle_pressure
full_set_relation
```

Set Anatomy also uses sorted relation gaps to identify special middle-pressure cases.

## What This Book Does Not Cover

This book does not cover:

```text
Draw Pressure
Path Energy
Incoming Motion
Outgoing Motion
Set Health tone
Set Anatomy body fields
```

Those belong to Draw-side or Shared Metric books.
