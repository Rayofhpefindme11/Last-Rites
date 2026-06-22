# Book of Sorted Relations

This book documents the Sorted Relations system for Infinite Inner World.

Sorted Relations classify the four adjacent lane relationships inside Sorted form:

```text
S1 Core -> S2 Entry -> S3 Bridge -> S4 Exit -> S5 Endpoint
```

Sorted Relations are one of the main foundation layers. Set Health and Set Anatomy both depend on them.

## Purpose

Sorted Relations answer this question:

```text
How far apart are the neighboring sorted lanes, and what class does that relationship belong to?
```

They do not classify whole-set grouping. That belongs to Set Style.

They do not classify pressure. That belongs to Sorted Pressure and Set Pressure.

They do not classify the full body. That belongs to Set Anatomy.

## Relation Order

There are exactly four Sorted Relations:

```text
S1->S2 Core_to_Entry
S2->S3 Entry_to_Bridge
S3->S4 Bridge_to_Exit
S4->S5 Exit_to_Endpoint
```

Each relation reads from left to right in sorted order.

## Relation Fields

Each relation contains:

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
section              sorted
relation             role-to-role name
from_lane            left sorted lane
to_lane              right sorted lane
from_role            left lane role
to_role              right lane role
from_number          left sorted number
to_number            right sorted number
distance             right number minus left number
gap                  absolute distance
gap_letter           Gap Alphabet class
gap_range            Gap Alphabet range
relation_class       35-class relation name
relation_class_range 35-class relation range
```

Because Sorted form is ascending, sorted relation distance is normally positive. The system still stores it as signed distance for consistency with Draw relations.

## Gap Alphabet Dependency

Every relation also receives a Gap Alphabet label.

Example:

```text
S1->S2: 3->26
distance +23
gap 23
gap_letter L
gap_range 23-24
```

The Gap Alphabet itself is documented in `Book of Basics`.

## Relation Class Scale

Sorted Relations use the 35-class relation scale.

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

## Relation Formula

For each adjacent pair:

```text
distance = to_number - from_number
gap = abs(distance)
gap_letter = Gap Alphabet class for gap
relation_class = 35-class relation class for gap
```

Example:

```text
S2->S3 Entry_to_Bridge: 26->49
distance = 49 - 26 = +23
gap = 23
gap_letter = L [23-24]
relation_class = FIGHTER_HIGH [23-24]
```

## Latest Draw Example

Latest trusted draw in the current records:

```text
Sorted White: 3-26-49-53-61
```

Relations:

```text
S1->S2 Core_to_Entry
3->26
distance +23
gap 23
gap_letter L [23-24]
relation_class FIGHTER_HIGH [23-24]
```

```text
S2->S3 Entry_to_Bridge
26->49
distance +23
gap 23
gap_letter L [23-24]
relation_class FIGHTER_HIGH [23-24]
```

```text
S3->S4 Bridge_to_Exit
49->53
distance +4
gap 4
gap_letter B [3-4]
relation_class KID [3-4]
```

```text
S4->S5 Exit_to_Endpoint
53->61
distance +8
gap 8
gap_letter D [7-8]
relation_class GRUNT [7-8]
```

## How Relations Feed Set Health

Set Health uses two middle relations:

```text
S2->S3 Entry_to_Bridge
S3->S4 Bridge_to_Exit
```

Formula piece:

```text
Set Health = Natural Draw Pressure Tone + S1 Core Band + S2->S3 Relation + S3->S4 Relation + S5 Endpoint Band
```

Example from latest draw:

```text
S2->S3 relation = FIGHTER_HIGH -> Fighter High
S3->S4 relation = KID -> Kid
```

So the middle of Set Health becomes:

```text
Fighter High Kid
```

## How Relations Feed Set Anatomy

Set Anatomy uses all four relations:

```text
S1->S2 creates entry edge
S2->S3 creates first middle body part
S3->S4 creates second middle body part
S4->S5 creates exit edge
```

Latest draw:

```text
entry edge:  ENTRY_FIGHTER_HIGH
middle body: S2_S4_FIGHTER_HIGH_THEN_KID
exit edge:   EXIT_GRUNT
edge form:   ENTRY_FIGHTER_HIGH_EXIT_GRUNT
```

## Boundary Notes

Sorted Relations require distinct adjacent numbers.

Powerball white balls do not duplicate inside one draw, so sorted relation gaps should never be zero.

If a zero gap ever appears, the draw data is invalid before relation classification.

## Current Scope

This book covers:

```text
Sorted relation order
relation fields
distance and gap formulas
Gap Alphabet dependency
35-class relation classes
Set Health dependency
Set Anatomy dependency
```

This book does not cover:

```text
Set Style grouping
Set Pressure formulas
Draw relations
Motion
Path Energy
```
