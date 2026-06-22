# Book of Set Anatomy

This book documents Set Anatomy for Infinite Inner World.

Set Anatomy is the full sorted technical body. It preserves the useful old technical-body depth while staying in the rebuilt Draw/Sorted system.

## Purpose

Set Anatomy answers this question:

```text
What are all the major structural parts of the sorted set?
```

It expands Set Health without cluttering the readable Set Health title.

Set Health is the compact identity.

Set Anatomy is the full structural body.

## Anatomy Formula

Set Anatomy formula:

```text
Set Anatomy = S1 Starter Slot + Entry Edge + S2-S4 Middle Body + Middle Pressure + Full Set Relation + S5 Endpoint Slot
```

The anatomy order is:

```text
S1_STARTER_SLOT
S1_S2_ENTRY_EDGE
S2_S4_MIDDLE_BODY
S4_S5_EXIT_EDGE
S5_ENDPOINT_SLOT
```

## Set Anatomy Fields

Set Anatomy contains:

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

## Starter Slot

Starter slot reads S1.

Formula:

```text
starter_slot = S1_CORE_<S1 number band>
```

Example:

```text
S1 = 3 sky
starter_slot = S1_CORE_SKY
starter_number = 3
starter_band = Sky
```

## Endpoint Slot

Endpoint slot reads S5.

Formula:

```text
endpoint_slot = S5_ENDPOINT_<S5 number band>
```

Example:

```text
S5 = 61 high king
endpoint_slot = S5_ENDPOINT_HIGH_KING
endpoint_number = 61
endpoint_band = High King
```

## Entry Edge

Entry edge reads the S1->S2 relation.

Fields:

```text
entry_relation
entry_gap
entry_gap_class
```

Example:

```text
S1->S2 Core_to_Entry
3->26
gap 23
entry_gap_class FIGHTER_HIGH
```

## Exit Edge

Exit edge reads the S4->S5 relation.

Fields:

```text
exit_relation
exit_gap
exit_gap_class
```

Example:

```text
S4->S5 Exit_to_Endpoint
53->61
gap 8
exit_gap_class GRUNT
```

## Middle Body

Middle body reads S2-S4 using S2->S3 and S3->S4.

If the two middle relation classes match:

```text
middle_body = S2_S4_DUAL_<relation_class>
```

If they differ:

```text
middle_body = S2_S4_<S2->S3 relation_class>_THEN_<S3->S4 relation_class>
```

Example:

```text
S2->S3 = FIGHTER_HIGH
S3->S4 = KID

middle_body = S2_S4_FIGHTER_HIGH_THEN_KID
```

Middle gap signature:

```text
middle_gap_signature = FIGHTER_HIGH_THEN_KID
```

## Middle Span

Middle span measures S2 to S4.

Formula:

```text
middle_span = S4 number - S2 number
```

Example:

```text
S2 = 26
S4 = 53
middle_span = 53 - 26 = 27
```

## Middle Zone

Middle zone reads S2, S3, and S4 as LOW/MID/HIGH.

Zone rules:

```text
1-23  LOW
24-46 MID
47-69 HIGH
```

Formula:

```text
middle_zone = zone(S2)_zone(S3)_zone(S4)
```

Example:

```text
S2 = 26 MID
S3 = 49 HIGH
S4 = 53 HIGH

middle_zone = MID_HIGH_HIGH
```

## Middle Slot Signature

Middle slot signature names S2, S3, and S4 by lane, role, and number band.

Formula:

```text
S2_<role>_<number band> | S3_<role>_<number band> | S4_<role>_<number band>
```

Example:

```text
S2_ENTRY_YANG | S3_BRIDGE_JESTER | S4_EXIT_KNIGHT
```

## Middle Pressure

Middle pressure uses `middle_minus_edge` from Sorted Pressure plus the two middle relation gaps.

Rules:

```text
middle_minus_edge >= 16
-> MIDDLE_EXPANSION_PRESSURE

middle_minus_edge <= -12
-> MIDDLE_COMPRESSION_PRESSURE

S2->S3 gap > 24 and S3->S4 gap <= 10
-> S3_S4_RECOVERY_AFTER_S2_STRETCH

S2->S3 gap <= 10 and S3->S4 gap > 24
-> S2_S3_LOCK_BEFORE_S4_STRETCH

otherwise
-> MIDDLE_STABLE_PRESSURE
```

## Edge Form

Edge form combines entry and exit relation classes.

Formula:

```text
edge_form = ENTRY_<S1->S2 relation_class>_EXIT_<S4->S5 relation_class>
```

Example:

```text
ENTRY_FIGHTER_HIGH_EXIT_GRUNT
```

## Edge Balance

Edge balance compares entry gap against exit gap.

Formula:

```text
edge_delta = entry_gap - exit_gap
```

Rules:

```text
entry class equals exit class -> EDGE_BALANCED
abs(edge_delta) <= 3          -> EDGE_NEAR_BALANCED
edge_delta > 0                -> ENTRY_HEAVIER
otherwise                     -> EXIT_HEAVIER
```

Example:

```text
entry_gap = 23
exit_gap = 8
edge_delta = 15

edge_balance = ENTRY_HEAVIER
```

## Edge Pressure

Edge pressure classifies entry and exit openness.

Gap openness:

```text
gap <= 10  CONTAINED
gap <= 24  BALANCED
gap >= 25  OPEN
```

If entry and exit openness match:

```text
edge_pressure = EDGE_<OPENNESS>
```

If they differ:

```text
edge_pressure = ENTRY_<ENTRY_OPENNESS>_EXIT_<EXIT_OPENNESS>
```

Example:

```text
entry_gap = 23 -> BALANCED
exit_gap = 8   -> CONTAINED

edge_pressure = ENTRY_BALANCED_EXIT_CONTAINED
```

## Full Set Relation

Full set relation compares the middle against the outer edges.

Rules:

```text
middle_minus_edge >= 16
-> MIDDLE_WIDER_THAN_OUTER_EDGES

middle_minus_edge <= -12
-> OUTER_EDGES_WIDER_THAN_MIDDLE

edge_balance is EDGE_BALANCED or EDGE_NEAR_BALANCED
-> ENTRY_EXIT_BALANCED_AROUND_MIDDLE

otherwise
-> ENTRY_EXIT_TILTED_AROUND_MIDDLE
```

## Technical Signature

Technical signature combines the anatomy parts in a compact scan line.

Formula:

```text
starter_slot |
edge_form |
middle_body |
middle_pressure |
full_set_relation |
endpoint_slot
```

Example:

```text
S1_CORE_SKY | ENTRY_FIGHTER_HIGH_EXIT_GRUNT | S2_S4_FIGHTER_HIGH_THEN_KID | MIDDLE_STABLE_PRESSURE | ENTRY_EXIT_TILTED_AROUND_MIDDLE | S5_ENDPOINT_HIGH_KING
```

## Set Anatomy String

The `set_anatomy` field uses the same parts as the technical signature, separated with `::`.

Example:

```text
S1_CORE_SKY :: ENTRY_FIGHTER_HIGH_EXIT_GRUNT :: S2_S4_FIGHTER_HIGH_THEN_KID :: MIDDLE_STABLE_PRESSURE :: ENTRY_EXIT_TILTED_AROUND_MIDDLE :: S5_ENDPOINT_HIGH_KING
```

## Latest Draw Example

Latest trusted draw:

```text
Draw order:   49-53-3-26-61
Sorted White: 3-26-49-53-61
```

Sorted body:

```text
S1 Core     3 sky
S2 Entry    26 yang
S3 Bridge   49 jester
S4 Exit     53 knight
S5 Endpoint 61 high king
```

Sorted relations:

```text
S1->S2 FIGHTER_HIGH gap 23
S2->S3 FIGHTER_HIGH gap 23
S3->S4 KID gap 4
S4->S5 GRUNT gap 8
```

Sorted Pressure support:

```text
edge_pressure     31
middle_pressure   27
middle_minus_edge -4
```

Set Anatomy:

```text
starter_slot          S1_CORE_SKY
entry_relation        Core_to_Entry
entry_gap             23
entry_gap_class       FIGHTER_HIGH
middle_body           S2_S4_FIGHTER_HIGH_THEN_KID
middle_span           27
middle_zone           MID_HIGH_HIGH
middle_gap_signature  FIGHTER_HIGH_THEN_KID
middle_slot_signature S2_ENTRY_YANG | S3_BRIDGE_JESTER | S4_EXIT_KNIGHT
middle_pressure       MIDDLE_STABLE_PRESSURE
exit_relation         Exit_to_Endpoint
exit_gap              8
exit_gap_class        GRUNT
edge_form             ENTRY_FIGHTER_HIGH_EXIT_GRUNT
edge_balance          ENTRY_HEAVIER
edge_pressure         ENTRY_BALANCED_EXIT_CONTAINED
full_set_relation     ENTRY_EXIT_TILTED_AROUND_MIDDLE
endpoint_slot         S5_ENDPOINT_HIGH_KING
endpoint_number       61
endpoint_band         High King
```

Technical signature:

```text
S1_CORE_SKY | ENTRY_FIGHTER_HIGH_EXIT_GRUNT | S2_S4_FIGHTER_HIGH_THEN_KID | MIDDLE_STABLE_PRESSURE | ENTRY_EXIT_TILTED_AROUND_MIDDLE | S5_ENDPOINT_HIGH_KING
```

## Relationship To Set Health

Set Health:

```text
Tensioned Sky Fighter High Kid High King
```

Set Anatomy explains the hidden body behind that compact read:

```text
S1 Core identity
entry edge
middle body
middle span
middle zone
exit edge
edge pressure
full relation
endpoint identity
```

## What This Book Does Not Cover

This book does not cover:

```text
Draw Style route logic
Date motion
Path Energy
Apex Point
Powerball classification
```

Those are separate books.
