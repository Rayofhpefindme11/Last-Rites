# Book of Set Style

This book documents the Sorted form Set Style system for Infinite Inner World.

Set Style identifies connected number families inside sorted order. It does not read draw order. It reads only the sorted lanes:

```text
S1 Core -> S2 Entry -> S3 Bridge -> S4 Exit -> S5 Endpoint
```

## Purpose

Set Style answers one question:

```text
How are the sorted numbers grouped by closeness?
```

It does not classify pressure, motion, Set Health, or Set Anatomy. Those systems use their own books.

## Connection Rule

Two adjacent sorted numbers are connected when the gap between them is under `10`.

Under `10` means:

```text
1-9 connected
10+ split
```

The scanner reads left to right through the four sorted gaps:

```text
S1->S2
S2->S3
S3->S4
S4->S5
```

Each adjacent gap becomes one marker:

```text
C = connected
X = split
```

Example:

```text
1-7-27-41-69

S1->S2 gap 6  = C
S2->S3 gap 20 = X
S3->S4 gap 14 = X
S4->S5 gap 28 = X

connected_pattern = CXXX
```

## Group Names

Connected lanes form groups.

```text
1 number  Lone
2 numbers Duo
3 numbers Trio
4 numbers Quad
5 numbers Noble
```

Examples:

```text
Lone:  S1 by itself
Duo:   S1-S2 connected
Trio:  S1-S2-S3 connected
Quad:  S1-S2-S3-S4 connected
Noble: S1-S2-S3-S4-S5 connected
```

## Whole-Set Styles

The whole set style is chosen from the connected group sizes.

```text
Noble          = one connected group of 5
Quad           = one connected group of 4
Blended Family = one Trio and one Duo in the same set
Trio           = one connected group of 3
Third-Wheel    = two Duo groups with a Lone also present
Duo            = one connected group of 2
Altogether     = no connected group
```

Classification priority:

```text
1. Noble
2. Quad
3. Blended Family
4. Trio
5. Third-Wheel
6. Duo
7. Altogether
```

This priority matters when a set contains more than one connected group.

## Set Style Fields

Each Sorted Style record contains:

```text
section
set_style
set_signature
connection_rule
connected_pattern
group_signature
groups
```

Field meanings:

```text
section           sorted
set_style         readable whole-set style name
set_signature     compact uppercase signature for lookup and script use
connection_rule   adjacent gap under 10 spaces; connected gaps are 1-9
connected_pattern four C/X markers across S1->S5
group_signature   group names from left to right
groups            each group with style, lanes, numbers, and size
```

## Set Signature

Set Style signature formula:

```text
SORTED_STYLE_<SET_STYLE>_PATTERN_<CONNECTED_PATTERN>_GROUPS_<GROUP_SIGNATURE>
```

Spaces and hyphens become underscores.

Example:

```text
Set Style:        Trio
connected_pattern XXCC
group_signature   Lone-Lone-Trio

set_signature:
SORTED_STYLE_TRIO_PATTERN_XXCC_GROUPS_LONE_LONE_TRIO
```

## Full Pattern Table

There are four adjacent sorted gaps, so there are 16 possible C/X patterns.

```text
XXXX Altogether  Lone-Lone-Lone-Lone-Lone
CXXX Duo         Duo-Lone-Lone-Lone
XCXX Duo         Lone-Duo-Lone-Lone
XXCX Duo         Lone-Lone-Duo-Lone
XXXC Duo         Lone-Lone-Lone-Duo
CCXX Trio        Trio-Lone-Lone
XCCX Trio        Lone-Trio-Lone
XXCC Trio        Lone-Lone-Trio
CCCX Quad        Quad-Lone
XCCC Quad        Lone-Quad
CCCC Noble       Noble
CXCX Third-Wheel Duo-Duo-Lone
CXXC Third-Wheel Duo-Lone-Duo
XCXC Third-Wheel Lone-Duo-Duo
CCXC Blended Family Trio-Duo
CXCC Blended Family Duo-Trio
```

## User Examples

The original rebuild examples map this way:

```text
1-7-27-41-69
CXXX
Duo
```

```text
1-7-16-27-41
CCXX
Trio
```

```text
1-7-16-21-41
CCCX
Quad
```

```text
1-7-16-21-30
CCCC
Noble
```

```text
1-7-16-30-37
CCXC
Blended Family
```

```text
1-7-20-40-45
CXXC
Third-Wheel
```

## Current Draw Example

Latest trusted draw in the current records:

```text
Sorted White: 3-26-49-53-61
```

Gaps:

```text
3->26  gap 23 = X
26->49 gap 23 = X
49->53 gap 4  = C
53->61 gap 8  = C
```

Style:

```text
connected_pattern XXCC
group_signature   Lone-Lone-Trio
set_style         Trio
set_signature     SORTED_STYLE_TRIO_PATTERN_XXCC_GROUPS_LONE_LONE_TRIO
```

Groups:

```text
Lone(3)
Lone(26)
Trio(49,53,61)
```

## Boundary Notes

`1-9` is connected.

`10` is not connected.

Examples:

```text
1-10 gap 9  = connected
1-11 gap 10 = split
```

Set Style is intentionally sorted-only. Draw order can look like:

```text
65-1-44-12-38
```

That kind of route belongs to Draw Style, not Sorted Style.

## What This Book Does Not Cover

This book does not cover:

```text
Set Health
Set Anatomy
Set Pressure
Set Arc
Draw Style
Motion
Path Energy
```

Those are separate books so the foundation stays clean.
