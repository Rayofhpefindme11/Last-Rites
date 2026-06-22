# Book of Draw Basics

This book documents the baseline Draw form system for Infinite Inner World.

Draw form is the natural order the white balls came in. It is not sorted order.

```text
D1 starter -> D2 hold -> D3 stability -> D4 control -> D5 ender
```

## Purpose

Draw form answers this question:

```text
What does the set look like in its natural drawn face?
```

Sorted form organizes the set.

Draw form preserves the set's natural route, pressure, motion, and behavior.

## Trusted Draw Order

Draw order is trusted only from:

```text
2015-10-07
```

Authority fields:

```text
authority_start_date
is_trusted_draw_order
authority_status
rule
```

Trusted status values:

```text
TRUSTED_DRAW_ORDER
SORTED_RECORD_ONLY
```

Rule:

```text
Draw-order style, draw pressure, and date-to-date draw motion are trusted only on or after 2015-10-07.
```

## Draw Lanes

There are five Draw lanes:

```text
D1 starter
D2 hold
D3 stability
D4 control
D5 ender
```

Every draw lane uses the full white-ball range:

```text
D1 starter   1-69
D2 hold      1-69
D3 stability 1-69
D4 control   1-69
D5 ender     1-69
```

Unlike Sorted lanes, Draw lanes do not have rising lane constraints. Any lane can hold any valid white ball.

## Draw Lane Fields

Each draw lane contains:

```text
lane
role
number
number_band
allowed_start
allowed_end
in_lane_range
```

Field meanings:

```text
lane          D1 through D5
role          starter, hold, stability, control, ender
number        white-ball value in that draw position
number_band   1-2 number-band identity
allowed_start lowest allowed lane value
allowed_end   highest allowed lane value
in_lane_range lane validity status
```

## Number Bands

Draw lanes use the same 1-2 number-band system documented in Sorted `Book of Basics`.

```text
1-2   Air
3-4   sky
5-6   light
7-8   feather
9-10  Life
11-12 Greed
13-14 Gravity
15-16 nova
17-18 Star
19-20 Polar
21-22 Water
23-24 Ying
25-26 yang
27-28 Dark
29-30 Volt
31-32 tree
33-34 leaf
35-36 beach
37-38 stem
39-40 truth
41-42 lie
43-44 red
45-46 blue
47-48 green
49-50 jester
51-52 king
53-54 knight
55-56 pope
57-58 emperor
59-60 prince
61-62 high king
63-64 high queen
65-66 noble Prince
67-68 high priest
69-70 monarch
```

## Draw Gaps

Draw gaps read the natural adjacent draw route:

```text
D1->D2
D2->D3
D3->D4
D4->D5
```

Each draw gap stores:

```text
section
from_lane
to_lane
from_number
to_number
distance
gap
gap_letter
gap_range
```

Important:

```text
distance is signed
gap is absolute
```

Draw gaps can go up or down because draw order is not sorted.

## Draw Relations

Draw Relations use the same 35-class relation scale as Sorted Relations, but they read Draw lane roles:

```text
D1->D2 starter_to_hold
D2->D3 hold_to_stability
D3->D4 stability_to_control
D4->D5 control_to_ender
```

Draw relation fields:

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

## Latest Draw Example

Latest trusted draw:

```text
Draw order: 49-53-3-26-61
```

Draw lanes:

```text
D1 starter   49 jester
D2 hold      53 knight
D3 stability 3 sky
D4 control   26 yang
D5 ender     61 high king
```

Draw gaps:

```text
D1->D2 49->53 distance +4  gap 4  B [3-4]
D2->D3 53->3  distance -50 gap 50 Y [49-50]
D3->D4 3->26  distance +23 gap 23 L [23-24]
D4->D5 26->61 distance +35 gap 35 R [35-36]
```

Draw relations:

```text
D1->D2 starter_to_hold      KID [3-4]
D2->D3 hold_to_stability    LOW_ENDPOINT_SOLDIER [49-50]
D3->D4 stability_to_control FIGHTER_HIGH [23-24]
D4->D5 control_to_ender     EXT_LOW_ENDPOINT_GRUNT [35-36]
```

## Draw Form Scope

Draw form includes:

```text
Draw lanes
Draw number bands
Draw gaps
Draw relations
Draw Style
Draw Pressure
Draw Motion
Path Energy
Flow and containment
```

These are documented across the Draw form books.
