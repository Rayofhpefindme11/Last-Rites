# Book of Draw Motion

This book documents Draw Motion for Infinite Inner World.

Draw Motion has two layers:

```text
D2-D5 inside-current-draw motion
Date-to-date incoming/outgoing motion by draw lane
```

## Purpose

Draw Motion answers these questions:

```text
How does the current draw move inside D1-D5?
How did each draw lane move from the previous draw into the current draw?
How will each draw lane move from the current draw into the next draw?
```

## D2-D5 Motion

D2-D5 Motion reads movement inside the current draw face.

It starts at D2 because D1 has no previous lane inside the same draw.

Steps:

```text
D1->D2 starter_to_hold
D2->D3 hold_to_stability
D3->D4 stability_to_control
D4->D5 control_to_ender
```

Fields:

```text
lane
role
from_lane
from_role
from_number
to_number
distance
```

Formula:

```text
distance = to_number - from_number
```

Latest draw:

```text
D1->D2 49->53  +4
D2->D3 53->3   -50
D3->D4 3->26   +23
D4->D5 26->61  +35
```

## Date-To-Date Motion

Date-to-date motion tracks each draw lane across previous, current, and next draw.

Each lane gets:

```text
incoming_motion
outgoing_motion
```

Incoming motion:

```text
incoming_motion = current_draw_lane_number - previous_draw_lane_number
```

Outgoing motion:

```text
outgoing_motion = next_draw_lane_number - current_draw_lane_number
```

If previous draw does not exist:

```text
incoming_motion = None
```

If next draw does not exist:

```text
outgoing_motion = None
```

## Draw Motion Fields

Each lane motion contains:

```text
lane
role
incoming_motion
incoming_motion_class
incoming_motion_gauge
incoming_motion_gauge_range
outgoing_motion
outgoing_motion_class
outgoing_motion_gauge
outgoing_motion_gauge_range
```

## Incoming And Outgoing Meaning

Incoming:

```text
previous draw -> current draw
```

Outgoing:

```text
current draw -> next draw
```

These are lane-specific. D1 compares to previous D1, D2 compares to previous D2, and so on.

## Motion Gauge

Motion gauge uses the absolute value of the motion while preserving the signed motion separately.

```text
0     still
1-2   grunt
3-4   peasant
5-6   medic
7-8   noble
9-10  noble medic
11-12 Herald
13-14 fighter
15-16 Herald fighter
17-18 brawler
19-20 Scrappy Brawler
21-22 grand brawler
23-24 healer
25-26 sacred healer
27-28 true healer
29-30 queen
31-32 False queen
33-34 lost queen
35-36 King
37-38 true king
39-40 High king
41-42 Monarch
43-44 Dark king
45-46 dark queen
47-48 dark prince
49-50 dark monarch
51-52 dark princess
53-54 dark emperor
55-56 dark priest
57-58 dark priestess
59-60 Light queen
61-62 light king
63-64 light hero
65-66 dark hero
67-68 light monarch
69-70 light empresses
```

## Broad Motion Class

Broad motion class uses magnitude:

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

## Latest Draw Example

Latest trusted draw:

```text
Date: 2026-06-17
Draw order: 49-53-3-26-61
Previous draw: 2026-06-15
Next draw: None
```

Incoming lane motion:

```text
D1 starter   incoming -13 Calm Motion / fighter [13-14]
D2 hold      incoming -2  Light Motion / grunt [1-2]
D3 stability incoming -57 Fatigued Motion / dark priestess [57-58]
D4 control   incoming -31 Transitional Motion / False queen [31-32]
D5 ender     incoming +36 Transitional Motion / King [35-36]
```

Outgoing lane motion:

```text
D1 starter   outgoing None
D2 hold      outgoing None
D3 stability outgoing None
D4 control   outgoing None
D5 ender     outgoing None
```

Outgoing is `None` because this is currently the latest draw in the CSV.

## Motion Into Energy

Draw Pressure aggregates date-to-date motion into energy:

```text
incoming_energy = sum(abs(incoming_motion) for D1-D5)
outgoing_energy = sum(abs(outgoing_motion) for D1-D5)
```

Latest draw:

```text
incoming_energy = abs(-13) + abs(-2) + abs(-57) + abs(-31) + abs(+36)
incoming_energy = 139
```

Incoming average:

```text
incoming_energy_average = 139 / 5 = 27.8
```

This becomes:

```text
incoming_energy_class = Directed Motion
```

## What This Book Does Not Cover

This book does not cover:

```text
Draw Style route code
Draw Pressure shape
Set Arc
Pressure Fusion
Set Health
Set Anatomy
```

Those are separate books.
