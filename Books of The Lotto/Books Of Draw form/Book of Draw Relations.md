# Book of Draw Relations

This book documents Draw Relations for Infinite Inner World.

Draw Relations classify adjacent lane pairs inside the natural draw-order face.

```text
D1 starter -> D2 hold -> D3 stability -> D4 control -> D5 ender
```

## Purpose

Draw Relations answer this question:

```text
How does each natural draw lane transfer into the next lane?
```

Sorted Relations describe the organized body.

Draw Relations describe the natural face.

## Relation Order

There are exactly four Draw Relations:

```text
D1->D2 starter_to_hold
D2->D3 hold_to_stability
D3->D4 stability_to_control
D4->D5 control_to_ender
```

They read left to right in draw order.

## Relation Fields

Each Draw Relation contains:

```text
section
relation
from_lane
to_lane
from_role
to_role
from_number
to_number
distance
gap
gap_letter
gap_range
relation_class
relation_class_range
```

Field meanings:

```text
section              draw
relation             role-to-role name
from_lane            left draw lane
to_lane              right draw lane
from_role            left draw role
to_role              right draw role
from_number          left draw number
to_number            right draw number
distance             right number minus left number
gap                  absolute distance
gap_letter           Gap Alphabet class
gap_range            Gap Alphabet range
relation_class       35-class relation name
relation_class_range 35-class relation range
```

## Signed Distance

Draw Relations preserve signed distance.

Formula:

```text
distance = to_number - from_number
gap = abs(distance)
```

Examples:

```text
49->53 distance +4
53->3  distance -50
```

This signed movement is important because draw order can climb or drop.

The relation class itself uses the absolute gap.

## Relation Class Scale

Draw Relations use the same 35-class relation scale as Sorted Relations.

```text
1-2   BABE
3-4   KID
5-6   TEEN
7-8   GRUNT
9-10  MENOUS
11-12 GRANDE
13-14 GALLEON
15-16 FIGHTER
17-18 ARCHER
19-20 HARBINGER
21-22 WRESTLER
23-24 FIGHTER_HIGH
25-26 HOLLOW
27-28 BRAGA
29-30 KILLER
31-32 ARRANCAR
33-34 CERO
35-36 EXT_LOW_ENDPOINT_GRUNT
37-38 EXT_LOW_ENDPOINT_HEALER
39-40 EXT_LOW_ENDPOINT_HELPER
41-42 EXT_LOW_ENDPOINT_CREATOR
43-44 EXT_LOW_ENDPOINT_DAECON
45-46 EXT_LOW_ENDPOINT_WRAITH
47-48 LOW_ENDPOINT_GRUNT
49-50 LOW_ENDPOINT_SOLDIER
51-52 LOW_ENDPOINT_LEADER
53-54 LOW_ENDPOINT_CHIEF
55-56 LOW_ENDPOINT_GOD
57-58 MID_ENDPOINT_WAR_CHIEF
59-60 MID_ENDPOINT_NOBLE
61-62 MID_ENDPOINT_GREAT_NOBLE
63-64 HIGH_ENDPOINT_EMPEROR
65-66 HIGH_ENDPOINT_KING
67-68 HIGH_ENDPOINT_HIGH_KING
69-70 HIGH_ENDPOINT_MONARCH
```

## Latest Draw Example

Latest trusted draw:

```text
Draw order: 49-53-3-26-61
```

Relations:

```text
D1->D2 starter_to_hold
49->53
distance +4
gap 4
gap_letter B [3-4]
relation_class KID [3-4]
```

```text
D2->D3 hold_to_stability
53->3
distance -50
gap 50
gap_letter Y [49-50]
relation_class LOW_ENDPOINT_SOLDIER [49-50]
```

```text
D3->D4 stability_to_control
3->26
distance +23
gap 23
gap_letter L [23-24]
relation_class FIGHTER_HIGH [23-24]
```

```text
D4->D5 control_to_ender
26->61
distance +35
gap 35
gap_letter R [35-36]
relation_class EXT_LOW_ENDPOINT_GRUNT [35-36]
```

## How Draw Relations Feed Draw Pressure

Draw Pressure uses the four draw gaps to compute:

```text
pressure_shape
pressure_type
set_arc
set_arc_35
draw_path_energy
draw_path_energy_average
```

The signs of the four relation distances create the pressure shape.

Example:

```text
49->53  positive
53->3   negative
3->26   positive
26->61  positive

pressure_shape = +-++
pressure_type = TENSION
```

The absolute gaps create path energy:

```text
4 + 50 + 23 + 35 = 112
```

## What This Book Does Not Cover

This book does not cover:

```text
Draw Style route through sorted lanes
Draw Pressure formulas beyond relation inputs
Date-to-date Draw Motion
Path Energy gauges
```

Those are covered in their own Draw form books.
