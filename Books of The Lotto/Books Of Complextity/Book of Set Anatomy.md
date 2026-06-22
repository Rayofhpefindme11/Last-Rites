# Book of Set Anatomy

Infinite Inner World shared metric reference

Folder: the book of complexity

Scope:

```text
Expanded full-set body
Sorted structure + pressure bridge support
```

## Purpose

Set Anatomy expands Set Health into a technical body.

It answers:

```text
What is the starter slot?
What are the entry and exit edges?
What is the middle body?
Is the middle wider than the edges?
Is the entry heavier or exit heavier?
What is the endpoint slot?
```

Set Health is the readable phrase.
Set Anatomy is the detailed body map.

## Fields

```text
set_anatomy
starter_slot
starter_number
starter_band
entry_relation
entry_gap
entry_gap_class
middle_body
middle_span
middle_zone
middle_gap_signature
middle_slot_signature
middle_pressure
exit_relation
exit_gap
exit_gap_class
edge_form
edge_balance
edge_pressure
full_set_relation
endpoint_slot
endpoint_number
endpoint_band
technical_signature
anatomy_order
rule
```

## Anatomy Order

Anatomy is read in this order:

```text
S1_STARTER_SLOT
S1_S2_ENTRY_EDGE
S2_S4_MIDDLE_BODY
S4_S5_EXIT_EDGE
S5_ENDPOINT_SLOT
```

This keeps the full body readable from start to end.

## Starter Slot

Starter slot uses S1 Core:

```text
starter_slot = S1_CORE_<S1 number band>
```

Example:

```text
S1 = 3 sky
starter_slot = S1_CORE_SKY
```

## Endpoint Slot

Endpoint slot uses S5 Endpoint:

```text
endpoint_slot = S5_ENDPOINT_<S5 number band>
```

Example:

```text
S5 = 61 high king
endpoint_slot = S5_ENDPOINT_HIGH_KING
```

## Entry And Exit Edges

Entry edge is:

```text
S1->S2
Core_to_Entry
```

Exit edge is:

```text
S4->S5
Exit_to_Endpoint
```

Each edge stores:

```text
relation name
gap
relation class
```

## Middle Body

Middle body uses:

```text
S2->S3
S3->S4
```

If both middle relation classes match:

```text
S2_S4_DUAL_<relation class>
```

If they differ:

```text
S2_S4_<S2->S3 class>_THEN_<S3->S4 class>
```

Latest example:

```text
S2->S3 = FIGHTER_HIGH
S3->S4 = KID

middle_body = S2_S4_FIGHTER_HIGH_THEN_KID
```

## Middle Span

Middle span is the numeric distance from S2 to S4:

```text
middle_span = S4 number - S2 number
```

Latest example:

```text
S2 = 26
S4 = 53

middle_span = 27
```

## Middle Zone

Each middle lane is grouped into a broad numeric zone:

```text
1-23   LOW
24-46  MID
47-69  HIGH
```

Middle zone joins S2, S3, and S4:

```text
S2 zone + S3 zone + S4 zone
```

Latest example:

```text
S2 = 26 MID
S3 = 49 HIGH
S4 = 53 HIGH

middle_zone = MID_HIGH_HIGH
```

## Middle Pressure

Middle pressure compares sorted middle pressure against sorted edge pressure.

Inputs:

```text
middle_minus_edge
S2->S3 gap
S3->S4 gap
```

Classes:

```text
MIDDLE_EXPANSION_PRESSURE
MIDDLE_COMPRESSION_PRESSURE
S3_S4_RECOVERY_AFTER_S2_STRETCH
S2_S3_LOCK_BEFORE_S4_STRETCH
MIDDLE_STABLE_PRESSURE
```

Rules:

```text
middle_minus_edge >= 16          MIDDLE_EXPANSION_PRESSURE
middle_minus_edge <= -12         MIDDLE_COMPRESSION_PRESSURE
S2->S3 gap > 24 and S3->S4 <= 10 S3_S4_RECOVERY_AFTER_S2_STRETCH
S2->S3 gap <= 10 and S3->S4 > 24 S2_S3_LOCK_BEFORE_S4_STRETCH
otherwise                        MIDDLE_STABLE_PRESSURE
```

## Edge Balance

Edge balance compares entry gap against exit gap.

Classes:

```text
EDGE_BALANCED
EDGE_NEAR_BALANCED
ENTRY_HEAVIER
EXIT_HEAVIER
```

Rules:

```text
same entry/exit relation class EDGE_BALANCED
absolute gap delta <= 3        EDGE_NEAR_BALANCED
entry gap > exit gap           ENTRY_HEAVIER
exit gap > entry gap           EXIT_HEAVIER
```

## Edge Pressure

Each edge gap receives an openness read:

```text
0-10   CONTAINED
11-24  BALANCED
25+    OPEN
```

Combined edge pressure:

```text
EDGE_<same openness>
ENTRY_<entry openness>_EXIT_<exit openness>
```

## Full Set Relation

Full set relation reads edge pressure against middle pressure.

Classes:

```text
MIDDLE_WIDER_THAN_OUTER_EDGES
OUTER_EDGES_WIDER_THAN_MIDDLE
ENTRY_EXIT_BALANCED_AROUND_MIDDLE
ENTRY_EXIT_TILTED_AROUND_MIDDLE
```

Rules:

```text
middle_minus_edge >= 16   MIDDLE_WIDER_THAN_OUTER_EDGES
middle_minus_edge <= -12  OUTER_EDGES_WIDER_THAN_MIDDLE
edge balanced/near        ENTRY_EXIT_BALANCED_AROUND_MIDDLE
otherwise                 ENTRY_EXIT_TILTED_AROUND_MIDDLE
```

## Technical Signature

Technical signature joins the main anatomy parts:

```text
starter_slot
edge_form
middle_body
middle_pressure
full_set_relation
endpoint_slot
```

The `set_anatomy` field uses the same parts separated with `::`.

## Latest Draw Example

Latest trusted packet:

```text
date         2026-06-17
draw form    49-53-3-26-61
sorted form  3-26-49-53-61
```

Anatomy:

```text
starter_slot       S1_CORE_SKY
starter_number     3
starter_band       Sky

entry_relation     Core_to_Entry
entry_gap          23
entry_gap_class    FIGHTER_HIGH

middle_body        S2_S4_FIGHTER_HIGH_THEN_KID
middle_span        27
middle_zone        MID_HIGH_HIGH
middle_pressure    MIDDLE_STABLE_PRESSURE
middle_slots       S2_ENTRY_YANG | S3_BRIDGE_JESTER | S4_EXIT_KNIGHT

exit_relation      Exit_to_Endpoint
exit_gap           8
exit_gap_class     GRUNT

edge_form          ENTRY_FIGHTER_HIGH_EXIT_GRUNT
edge_balance       ENTRY_HEAVIER
edge_pressure      ENTRY_BALANCED_EXIT_CONTAINED

endpoint_slot      S5_ENDPOINT_HIGH_KING
endpoint_number    61
endpoint_band      High King

full_set_relation  ENTRY_EXIT_TILTED_AROUND_MIDDLE
```

Technical signature:

```text
S1_CORE_SKY | ENTRY_FIGHTER_HIGH_EXIT_GRUNT | S2_S4_FIGHTER_HIGH_THEN_KID | MIDDLE_STABLE_PRESSURE | ENTRY_EXIT_TILTED_AROUND_MIDDLE | S5_ENDPOINT_HIGH_KING
```

## What Set Anatomy Does Not Do

Set Anatomy does not replace Set Health.

Use:

```text
Set Health   for compact readable full-set identity
Set Anatomy  for technical body structure
```

