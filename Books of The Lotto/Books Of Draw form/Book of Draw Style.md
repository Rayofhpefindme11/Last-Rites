# Book of Draw Style

This book documents Draw Style for Infinite Inner World.

Draw Style reads how the natural draw order transfers through the sorted lanes.

```text
D1-D5 draw order -> S1-S5 sorted positions
```

## Purpose

Draw Style answers this question:

```text
What route does the natural draw face take through the sorted body?
```

Sorted Style reads closeness groups.

Draw Style reads route behavior.

## Draw Style Fields

Draw Style contains:

```text
section
draw_style
draw_style_family
rule
direction_pattern
transfer_pattern
sorted_position_path
sorted_position_deltas
sorted_position_energy
turn_count
turn_lanes
steps
```

Field meanings:

```text
section                draw
draw_style             exact route code
draw_style_family      readable route family
rule                   route construction rule
direction_pattern      signed D1-D5 number movement pattern
transfer_pattern       sorted-lane route made by draw order
sorted_position_path   transfer pattern as sorted positions
sorted_position_deltas movement across sorted positions
sorted_position_energy sum of absolute sorted-position deltas
turn_count             number of sign turns in direction pattern
turn_lanes             draw lanes where direction changes
steps                  D lane to S lane mapping
```

## Transfer Steps

Each Draw Style step maps one draw lane back into its sorted lane.

Step fields:

```text
draw_lane
draw_role
draw_number
sorted_lane
sorted_role
sorted_position
```

Example:

```text
D1 starter 49 -> S3 Bridge position 3
```

## Transfer Pattern

Transfer pattern is the sorted-lane route made by D1-D5.

Example:

```text
Draw order:   49-53-3-26-61
Sorted White: 3-26-49-53-61
```

Mappings:

```text
49 -> S3
53 -> S4
3  -> S1
26 -> S2
61 -> S5
```

Transfer pattern:

```text
S3-S4-S1-S2-S5
```

## Draw Style Code

Draw Style code is the transfer pattern with a `DRAW_ROUTE_` prefix.

Formula:

```text
draw_style = DRAW_ROUTE_<transfer_pattern with dashes changed to underscores>
```

Example:

```text
transfer_pattern = S3-S4-S1-S2-S5
draw_style = DRAW_ROUTE_S3_S4_S1_S2_S5
```

## Direction Pattern

Direction pattern reads signed movement across the actual draw numbers.

Rules:

```text
positive movement -> +
negative movement -> -
zero movement     -> 0
```

Example:

```text
49->53 positive -> +
53->3  negative -> -
3->26  positive -> +
26->61 positive -> +

direction_pattern = +-++
```

## Sorted Position Path

Sorted position path turns the transfer pattern into numeric sorted positions.

```text
S1 = 1
S2 = 2
S3 = 3
S4 = 4
S5 = 5
```

Example:

```text
transfer_pattern = S3-S4-S1-S2-S5
sorted_position_path = 3-4-1-2-5
```

## Sorted Position Deltas

Sorted position deltas measure route movement through sorted positions.

Formula:

```text
delta = next sorted position - current sorted position
```

Example:

```text
3->4 = +1
4->1 = -3
1->2 = +1
2->5 = +3

sorted_position_deltas = +1,-3,+1,+3
```

## Sorted Position Energy

Sorted position energy is the sum of absolute sorted-position deltas.

Example:

```text
abs(+1) + abs(-3) + abs(+1) + abs(+3) = 8
```

So:

```text
sorted_position_energy = 8
```

## Turn Count And Turn Lanes

A turn happens when the direction pattern changes sign from one step to the next.

Example:

```text
direction_pattern = +-++
```

Compare adjacent signs:

```text
+ to -  turn
- to +  turn
+ to +  no turn
```

The turn lanes are the draw lanes after the changed step.

Latest draw:

```text
turn_count = 2
turn_lanes = D2,D3
```

## Draw Style Families

Draw Style family summarizes route behavior from the direction pattern.

Rules:

```text
No signs              -> Still
No turns and starts + -> Clean Climb
No turns and starts - -> Clean Drop
3 turns               -> Full Pendulum
2 turns and starts +  -> Crest Valley
2 turns and starts -  -> Valley Crest
1 turn                -> Early/Middle/Late Crest or Valley
```

One-turn naming:

```text
turn after first move  -> Early Crest or Early Valley
turn after second move -> Middle Crest or Middle Valley
turn after third move  -> Late Crest or Late Valley
```

The route is called a Crest when it starts positive.

The route is called a Valley when it starts negative.

## Latest Draw Example

Latest trusted draw:

```text
Draw order:   49-53-3-26-61
Sorted White: 3-26-49-53-61
```

Draw Style:

```text
draw_style             DRAW_ROUTE_S3_S4_S1_S2_S5
draw_style_family      Crest Valley
direction_pattern      +-++
transfer_pattern       S3-S4-S1-S2-S5
sorted_position_path   3-4-1-2-5
sorted_position_deltas +1,-3,+1,+3
sorted_position_energy 8
turn_count             2
turn_lanes             D2,D3
```

Steps:

```text
D1 starter   49 -> S3 Bridge
D2 hold      53 -> S4 Exit
D3 stability 3  -> S1 Core
D4 control   26 -> S2 Entry
D5 ender     61 -> S5 Endpoint
```

## What This Book Does Not Cover

This book does not cover:

```text
Draw Pressure
Path Energy
Date Motion
Incoming and outgoing motion
Set Health
Set Anatomy
```

Those systems use Draw Style, but are documented separately.
