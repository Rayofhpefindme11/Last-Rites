# Infinite Inner World Clean Slate

This is the rebuild ledger for `Scripts of the lotto/Foundation Scripts/Infinite_Inner_World.py`.

The first reset is complete by intention: the old category system has been removed from the script.
The first rebuilt category is now present: every draw has a clear Sorted section, Draw section,
date continuity, D2-D5 draw-form motion, and date-to-date draw-lane motion.

## Current Foundation

- Script: `Scripts of the lotto/Foundation Scripts/Infinite_Inner_World.py`
- CSV: `Powerball records/PB_All.csv`
- Environment override: `IIW_POWERBALL_CSV`
- Current purpose: draw intake, validation, Sorted section, Draw section, Set Style, Set Pressure, and continuity display
- Trusted draw-order start: `2015-10-07`
- Current output modes:
  - readable draw packets
  - JSON draw packets
  - JSON foundation summary

## Removed From The Script

The clean-slate file no longer contains:

- Pair snapshots
- Memory virtual rooms
- Set-type classification
- FP classification
- style, arc, and pressure classification
- old draw-order category logic
- old motion category logic
- old project lineage names
- live packet construction
- candidate selection
- transition law
- era detection
- BP, CP, or ECABP metrics

## Remaining Contract

The script currently preserves only the minimum historical draw contract:

- draw date
- draw index
- jackpot value when present
- five white balls
- sorted copy of the five white balls for plain inspection
- Powerball
- Power Play when present

## Shared Metric: Apex Point

Purpose: publish the shared numeric weight of the five-number set before either Sorted or Draw interpretation.

Fields:

- `total`: all five white-ball numbers added together
- `total_sum_gauge`: total sum classified on the repeating Olympus gauge
- `fp`: Finality Point, largest white-ball number minus smallest white-ball number
- `fp_gauge`: FP classified on the repeating Olympus gauge
- `smallest_number`: smallest white-ball number in the set
- `largest_number`: largest white-ball number in the set

Example:

- if the set contains `65` and `4`, `fp = 65 - 4 = 61`

Gauge rule:

- Apex gauges no longer borrow motion labels
- both `fp_gauge` and `total_sum_gauge` use the Olympus names as a repeating two-number cycle
- the Olympus cycle is `Zeus`, `Hera`, `Poseidon`, `Demeter`, `Athena`, `Apollo`, `Artemis`, `Ares`, `Aphrodite`, `Hephaestus`, `Hermes`, `Dionysus`

## Shared Metric: Set Pressure

Purpose: identify how much tension the set is carrying and where that tension lives.

Source canon brought over from Serenity draw-order books:

```text
Motion explains behavior.
Structure explains form.
Pressure explains tension inside form.
Energy measures cost.
```

Set Pressure is split into two sections:

- `sorted_pressure`: pressure inside `S1-S5` form
- `draw_pressure`: pressure created by `D1-D5` route, transfer, and date motion

Draw-order authority:

- draw-order style, draw pressure, and date-to-date draw motion are trusted only on or after `2015-10-07`
- rows before `2015-10-07` can still be inspected, but they are marked `SORTED_RECORD_ONLY`
- trusted rows are marked `TRUSTED_DRAW_ORDER`

Set Arc:

- `S`: gap `1-10`
- `M`: gap `11-16`
- `B`: gap `17-24`
- `E`: gap `25+`

Pressure shape and type:

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

Sorted Pressure fields:

- `pressure_shape`: four-sign formation pattern
- `pressure_type`: sign-shape pressure label
- `set_arc`: traditional `S/M/B/E` set arc path
- `set_arc_35`: Roman-numeral 35-class gap path for Set Arc
- `set_arc_family`: Set Arc family reference
- `set_arc_type`: Set Arc type reference
- `edge_pressure`: `S1->S2 + S4->S5`
- `middle_pressure`: `S2->S3 + S3->S4`
- `middle_minus_edge`
- `largest_gap`
- `largest_gap_relation`

Draw Pressure fields:

- `pressure_shape`: four-sign formation pattern
- `pressure_type`: sign-shape pressure label
- `set_arc`: traditional `S/M/B/E` draw set arc path
- `set_arc_35`: Roman-numeral 35-class draw gap path for Set Arc
- `set_arc_family`: Set Arc family reference
- `set_arc_type`: Set Arc type reference
- `draw_style`
- `draw_style_family`
- `direction_pattern`
- `transfer_pattern`
- `draw_path_energy`: total absolute `D1-D5` gap energy
- `draw_path_energy_average`: `draw_path_energy / 4`
- `draw_path_energy_class`: broad motion class from the normalized path average
- `draw_path_energy_spectrum`: 35-class spectrum-color name from the normalized path average
- `sorted_position_energy`: route cost through `S1-S5`
- `incoming_energy`: total absolute incoming date motion
- `incoming_energy_average`: `incoming_energy / 5`
- `incoming_energy_class`: broad motion class from the normalized incoming average
- `outgoing_energy`: total absolute outgoing date motion
- `outgoing_energy_average`: `outgoing_energy / 5`
- `outgoing_energy_class`: broad motion class from the normalized outgoing average
- `energy_delta`: outgoing minus incoming
- `flow_strength`: absolute `energy_delta`
- `flow_strength_average`: `flow_strength / 5`
- `flow_strength_class`: broad motion class from the normalized flow-strength average
- `flow_strength_element`: 35-class periodic-table name from the normalized flow-strength average
- `pressure_flow`: `RELEASE`, `RETENTION`, `BALANCED_TRANSFER`, or `UNKNOWN_BOUNDARY`
- `pressure_fusion`: relation between sorted pressure and draw pressure for the same set
- `pressure_fusion_profile`: exact `SORTED_PRESSURE_TO_DRAW_PRESSURE` profile, for example `UPLIFT_TO_SEPERATION`
- `pressure_fusion_constellation`: constellation name attached to the pressure-fusion class
- `containment_state`: whether the motion is contained, controlled volatile, strained, broken, or boundary unknown

Motion-state authority:

- IIW no longer carries a separate `motion_state` label
- `draw_path_energy_class` is the main current-draw motion-state read
- `pressure_flow` explains release, retention, balanced transfer, or boundary unknown
- `flow_strength_class` explains how strong the redistribution is
- `containment_state` explains whether the motion is contained or strained

Broad motion classes:

```text
0 Still Motion
1-10 Light Motion
11-20 Calm Motion
21-30 Directed Motion
31-40 Transitional Motion
41-50 Crest Echo Motion
51-60 Fatigued Motion
61-69 Chaotic Motion
```

Pressure fusion classes:

```text
MATCHED_FUSION Orion
TYPE_FUSION Lyra
FAMILY_FUSION Cygnus
REDISTRIBUTED_FUSION Draco
INVERTED_FUSION Phoenix
```

## Shared Metric: Set Health

Purpose: give the set a compact readable health title instead of forcing every lower-level label into the main read.

Formula:

```text
Set Health = Natural Draw Pressure Tone + S1 Core Band + S2->S3 Relation + S3->S4 Relation + S5 Endpoint Band
```

Fields:

- `set_health`: full readable title
- `pressure_tone`: natural draw pressure type converted into readable form
- `core_band`: S1 number band
- `middle_entry_bridge`: S2->S3 relation class
- `middle_bridge_exit`: S3->S4 relation class
- `endpoint_band`: S5 number band

Example:

```text
Uplifting Sky Grunt Babe High Priest
```

## Shared Metric: Set Anatomy

Purpose: keep the clean Set Health title, but preserve the old technical-body depth in the rebuilt language.

Formula:

```text
Set Anatomy = S1 Starter Slot + S1->S2 Entry Edge + S2-S4 Middle Body + S4->S5 Exit Edge + S5 Endpoint Slot
```

Fields:

- `starter_slot`: S1 core slot built from the rebuilt S1 number band
- `entry_relation`: S1->S2 relation and gap class
- `middle_body`: S2-S4 body using S2->S3 and S3->S4 relation classes
- `middle_span`: S4 minus S2
- `middle_zone`: LOW/MID/HIGH zone read for S2, S3, and S4
- `middle_slot_signature`: S2/S3/S4 lane role plus number-band signature
- `middle_pressure`: edge-vs-middle pressure read from rebuilt sorted pressure
- `exit_relation`: S4->S5 relation and gap class
- `edge_form`: combined entry/exit relation form
- `edge_balance`: whether entry and exit are balanced, near-balanced, entry-heavy, or exit-heavy
- `edge_pressure`: contained/balanced/open edge read
- `full_set_relation`: final outer-edge versus middle-body relation
- `endpoint_slot`: S5 endpoint slot built from the rebuilt S5 number band
- `technical_signature`: compact scan line combining the anatomy parts

Example shape:

```text
S1_CORE_SKY | ENTRY_GRUNT_EXIT_BABE | S2_S4_GRUNT_THEN_BABE | MIDDLE_COMPRESSION_PRESSURE | OUTER_EDGES_WIDER_THAN_MIDDLE | S5_ENDPOINT_HIGH_PRIEST
```

## Sorted Style

Purpose: identify special connected properties inside a sorted five-number set.

Sorted Style reads `S1-S5`.

Connection rule:

- adjacent numbers connect only when the gap is under `10`
- under `10` means `1-9`
- the scanner reads left to right

Group names:

```text
1 number  Lone
2 numbers Duo
3 numbers Trio
4 numbers Quad
5 numbers Noble
```

Whole-set names:

- `Duo`: one connected group of 2
- `Trio`: one connected group of 3
- `Quad`: one connected group of 4
- `Noble`: one connected group of 5
- `Blended Family`: a Trio and a Duo in the same set
- `Third-Wheel`: two Duo groups with a lone number also present
- `Altogether`: no connected group

Fields:

- `set_style`: readable whole-set style name
- `set_signature`: compact uppercase style signature
- `connected_pattern`: four-character closeness pattern where `C` means connected and `X` means split
- `group_signature`: left-to-right group names
- `groups`: exact group lanes, numbers, and sizes

Signature formula:

```text
SORTED_STYLE_<SET_STYLE>_PATTERN_<CONNECTED_PATTERN>_GROUPS_<GROUP_SIGNATURE>
```

Examples:

```text
1-7-27-41-69  -> Duo
1-7-16-27-41  -> Trio
1-7-16-21-41  -> Quad
1-7-16-21-30  -> Noble
1-7-16-30-37  -> Blended Family
1-7-20-40-45  -> Third-Wheel
```

## Draw Style

Purpose: rebuild draw-order style slowly without forcing the Sorted Style closeness rule onto draw order.

Current rule:

- `Draw Style` reads `D1-D5`
- the exact style identity is the `D1-D5` route through `S1-S5`
- every possible draw order has its own route code
- the route transfers the draw order back into sorted form without guessing
- family labels are secondary and only summarize route behavior

Current fields:

- `draw_style`: exact route code, such as `DRAW_ROUTE_S5_S1_S4_S2_S3`
- `draw_style_family`: readable motion family, such as `Full Pendulum`
- `direction_pattern`: the four signed moves across `D1-D5`, such as `-+-+`
- `transfer_pattern`: the sorted-lane path made by draw order, such as `S5-S1-S4-S2-S3`
- `sorted_position_path`: the same transfer as sorted positions, such as `5-1-4-2-3`
- `sorted_position_deltas`: the movement across sorted positions, such as `-4,+3,-2,+1`
- `sorted_position_energy`: the sum of absolute sorted-position moves
- `turn_count`: count of direction changes
- `turn_lanes`: draw lanes where direction turns, such as `D2,D3,D4`
- `steps`: each `D` lane number mapped to its sorted `S` lane

Family labels:

- `Clean Climb`: all moves rise
- `Clean Drop`: all moves fall
- `Early Crest`, `Middle Crest`, `Late Crest`: rise first, then fall once
- `Early Valley`, `Middle Valley`, `Late Valley`: fall first, then rise once
- `Crest Valley`: two turns, rising first
- `Valley Crest`: two turns, falling first
- `Full Pendulum`: three turns

Example:

```text
65-1-44-12-38
D movement: 65->1->44->12->38
direction_pattern: -+-+
sorted form: 1-12-38-44-65
transfer_pattern: S5-S1-S4-S2-S3
draw_style: DRAW_ROUTE_S5_S1_S4_S2_S3
draw_style_family: Full Pendulum
sorted_position_path: 5-1-4-2-3
sorted_position_deltas: -4,+3,-2,+1
sorted_position_energy: 10
turn_lanes: D2,D3,D4
```

## Shared Gap Alphabet

Purpose: provide one shared gap class language used by both Sorted gaps and Draw gaps.

Rule:

- classify adjacent gaps in `1-2` bands
- cover `1-70` with `35` classes
- use alphabet letters through the 26th class
- after `Z`, continue with `Aa`, then doubled lowercase pairs

Gap classes:

```text
1-2 A
3-4 B
5-6 C
7-8 D
9-10 E
11-12 F
13-14 G
15-16 H
17-18 I
19-20 J
21-22 K
23-24 L
25-26 M
27-28 N
29-30 O
31-32 P
33-34 Q
35-36 R
37-38 S
39-40 T
41-42 U
43-44 V
45-46 W
47-48 X
49-50 Y
51-52 Z
53-54 Aa
55-56 bb
57-58 cc
59-60 dd
61-62 ee
63-64 ff
65-66 gg
67-68 hh
69-70 ii
```

Sorted gaps:

- `S1->S2`
- `S2->S3`
- `S3->S4`
- `S4->S5`

Draw gaps:

- `D1->D2`
- `D2->D3`
- `D3->D4`
- `D4->D5`

Draw gaps keep signed `distance`, but the shared alphabet class uses the absolute gap size.

## Set Relations

Purpose: name each adjacent lane relation using the existing gap alphabet plus a relation class.

Sorted relations:

- `S1->S2`: `Core->Entry`
- `S2->S3`: `Entry->Bridge`
- `S3->S4`: `Bridge->Exit`
- `S4->S5`: `Exit->Endpoint`

Draw relations:

- `D1->D2`: `starter->hold`
- `D2->D3`: `hold->stability`
- `D3->D4`: `stability->control`
- `D4->D5`: `control->ender`

Relation classes:

```text
1-2 BABE
3-4 KID
5-6 TEEN
7-8 GRUNT
9-10 MENOUS
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

Draw relations keep signed `distance`, but relation class uses absolute gap size.

The relation scale has exactly 35 two-number slots. The supplied names `SKY`, `GOD`, and `HIGH_KING` from the first block are not used in this pass because the endpoint block already supplies the final high-end relation names.

## Rebuilt Category 1: Draw And Sorted Sections

Purpose: give every draw two sharp sections before any deeper interpretation is rebuilt.

Sorted section:

- `S1 Core`
- `S2 Entry`
- `S3 Bridge`
- `S4 Exit`
- `S5 Endpoint`

Sorted lane ranges:

- `S1`: starts at `1`, ends at `65`
- `S2`: starts at `2`, ends at `66`
- `S3`: starts at `3`, ends at `67`
- `S4`: starts at `4`, ends at `68`
- `S5`: starts at `5`, ends at `69`

Draw section:

- `D1 starter`
- `D2 hold`
- `D3 stability`
- `D4 control`
- `D5 ender`

Draw lane ranges:

- every D lane can hold `1-69`

Number bands:

- `1-2 Air`
- `3-4 sky`
- `5-6 light`
- `7-8 feather`
- `9-10 Life`
- `11-12 Greed`
- `13-14 Gravity`
- `15-16 nova`
- `17-18 Star`
- `19-20 Polar`
- `21-22 Water`
- `23-24 Ying`
- `25-26 yang`
- `27-28 Dark`
- `29-30 Volt`
- `31-32 tree`
- `33-34 leaf`
- `35-36 beach`
- `37-38 stem`
- `39-40 truth`
- `41-42 lie`
- `43-44 red`
- `45-46 blue`
- `47-48 green`
- `49-50 jester`
- `51-52 king`
- `53-54 knight`
- `55-56 pope`
- `57-58 emperor`
- `59-60 prince`
- `61-62 high king`
- `63-64 high queen`
- `65-66 noble Prince`
- `67-68 high priest`
- `69-70 monarch`

Continuity:

- every selected draw keeps its actual previous and next draw from the full CSV
- example: `2026-06-10 -> 2026-06-13 -> 2026-06-15`

Draw-order motion:

- date-to-date motion is only calculated for D lanes
- `incoming_motion` is current D value minus previous D value
- `outgoing_motion` is next D value minus current D value
- example: if `D1` moves from `3` to `12`, the distance is `+9`

Motion gauge:

- motion gauge uses the absolute size of incoming/outgoing motion
- signed motion is preserved separately
- `0` is `still`
- all other motion gauge classes use the same two-number spacing as the rest of IIW
- each lane also receives the broad class: Light, Calm, Directed, Transitional, Crest Echo, Fatigued, or Chaotic Motion

```text
1-2 grunt
3-4 peasant
5-6 medic
7-8 noble
9-10 noble medic
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

D2-D5 motion:

- `D1` is the starter, so inside-draw motion starts at `D2`
- `D2` distance is `D2 - D1`
- `D3` distance is `D3 - D2`
- `D4` distance is `D4 - D3`
- `D5` distance is `D5 - D4`
- this is separate from date-to-date motion

Validation currently checks:

- CSV file exists
- required numeric fields are present
- five white balls are present
- white balls are in the legal `1-69` range
- white balls are unique within a draw
- Powerball is in the historical CSV `1-39` range
- draw dates ascend
- draw indexes ascend
- draw indexes are not duplicated

## Current Commands

Print the first loaded row:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Infinite_Inner_World.py" --limit 1
```

Print the neutral foundation summary:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Infinite_Inner_World.py" --summary
```

Print a date window:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Infinite_Inner_World.py" --from-date 2026-06-01 --to-date 2026-06-17
```

Print one date as JSON:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Infinite_Inner_World.py" --from-date 2026-06-13 --to-date 2026-06-13 --json
```

## Rebuild Rule

Every new category must be added deliberately with:

- a short purpose
- allowed inputs
- exact output fields
- a leakage rule
- a smoke command
- a note explaining why the category belongs in IIW

No removed category should be reintroduced by name or behavior unless we explicitly define its new purpose from scratch.
