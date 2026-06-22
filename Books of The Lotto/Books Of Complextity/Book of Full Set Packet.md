# Book of Full Set Packet

Infinite Inner World shared metric reference

Folder: the book of complexity

Scope:

```text
Complete IIW packet assembly
```

## Purpose

The Full Set Packet is the complete IIW body for one draw.

It answers:

```text
What draw is being read?
What came before it?
What comes after it?
What is the trusted draw-order status?
What are the shared metrics?
What are the Sorted form metrics?
What are the Draw form metrics?
```

This is the packet foundation scripts, predictive scripts, and RD findings should reference when they need the complete IIW read.

## Packet Schema

Current schema:

```text
iiw.draw_and_sorted_set_form.v1
```

## Packet Sections

```text
draw
continuity
draw_order_authority
apex_point
set_pressure
set_health
set_anatomy
sorted_form
draw_form
sorted_style
draw_style
sorted_gaps
draw_gaps
sorted_relations
draw_relations
draw_motion
draw_step_motion
```

## Build Order

The packet is built in this order:

```text
1. draw
2. previous_draw and next_draw
3. sorted_form
4. draw_form
5. apex_point
6. sorted_style
7. draw_style
8. sorted_gaps
9. draw_gaps
10. draw_motion
11. set_pressure
12. sorted_relations
13. draw_relations
14. set_health
15. set_anatomy
16. draw_order_authority
17. final DrawSetPacket
```

The order matters because later metrics depend on earlier ones.

Examples:

```text
set_pressure needs apex_point, sorted_style, draw_style, sorted_gaps, draw_gaps, and draw_motion.
set_health needs set_pressure, sorted_form, and sorted_relations.
set_anatomy needs set_pressure, sorted_form, and sorted_relations.
```

## Draw Section

The draw section carries the raw draw:

```text
draw_date
draw_index
jackpot_usd
white_balls
sorted_white_balls
powerball
powerplay
```

Latest example:

```text
date          2026-06-17
index         1960
white_balls   [49, 53, 3, 26, 61]
sorted_white  [3, 26, 49, 53, 61]
powerball     12
powerplay     2
```

## Continuity Section

Continuity links the packet to its date neighbors:

```text
previous_draw
current_draw
next_draw
```

Latest example:

```text
previous  2026-06-15
current   2026-06-17
next      NONE
```

If next draw is missing, outgoing motion and outgoing energy are `None`.

## Draw Order Authority

Draw order is trusted from:

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

Status values:

```text
TRUSTED_DRAW_ORDER
SORTED_RECORD_ONLY
```

Latest example:

```text
authority_status       TRUSTED_DRAW_ORDER
authority_start_date   2015-10-07
is_trusted_draw_order  true
```

## Shared Metrics In The Packet

Shared metrics:

```text
apex_point
set_pressure
set_health
set_anatomy
```

Set Pressure includes Pressure Fusion inside its draw-pressure side.

## Sorted Form Metrics In The Packet

Sorted-side sections:

```text
sorted_form
sorted_style
sorted_gaps
sorted_relations
sorted_pressure inside set_pressure
```

Sorted form is the structural S1-S5 body.

## Draw Form Metrics In The Packet

Draw-side sections:

```text
draw_form
draw_style
draw_gaps
draw_relations
draw_motion
draw_step_motion
draw_pressure inside set_pressure
```

Draw form is the natural D1-D5 body.

## Latest Full Packet Summary

Latest trusted packet:

```text
date         2026-06-17
draw form    49-53-3-26-61
sorted form  3-26-49-53-61
```

Shared read:

```text
Apex Point
  total 192 Dionysus [191-192]
  fp 58 Athena [57-58]

Set Health
  Tensioned Sky Fighter High Kid High King

Set Anatomy
  S1_CORE_SKY | ENTRY_FIGHTER_HIGH_EXIT_GRUNT | S2_S4_FIGHTER_HIGH_THEN_KID | MIDDLE_STABLE_PRESSURE | ENTRY_EXIT_TILTED_AROUND_MIDDLE | S5_ENDPOINT_HIGH_KING

Set Pressure Bridge
  sorted UPLIFT ++++
  draw   TENSION +-++
  fusion UPLIFT_TO_TENSION
  class  REDISTRIBUTED_FUSION Draco
```

Sorted read:

```text
S1 Core      3 sky
S2 Entry     26 yang
S3 Bridge    49 jester
S4 Exit      53 knight
S5 Endpoint  61 high king
style        Trio
signature    SORTED_STYLE_TRIO_PATTERN_XXCC_GROUPS_LONE_LONE_TRIO
```

Draw read:

```text
D1 starter    49 jester
D2 hold       53 knight
D3 stability  3 sky
D4 control    26 yang
D5 ender      61 high king
style         DRAW_ROUTE_S3_S4_S1_S2_S5
family        Crest Valley
direction     +-++
path_energy   112
```

## Use Rule

Use the Full Set Packet when a script needs all IIW context.

Use individual books when a script only needs one layer:

```text
Sorted form books          sorted-only logic
draw form books            draw-only logic
the book of complexity     shared/full-set logic
```

