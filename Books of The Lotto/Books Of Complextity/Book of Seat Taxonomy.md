# Book of Seat Taxonomy

Infinite Inner World transition-physics reference

Folder:

```text
Books of The Lotto / Books Of Complextity
```

Active script:

```text
Scripts of the lotto/Foundation Scripts/Seat_Taxonomy.py
```

Schema:

```text
iiw.seat_taxonomy.transition_physics.v1
```

## Doctrine

Seat Taxonomy is the transition-physics layer built on top of Infinite Inner World.

Core law:

```text
Draw order is cause/motion.
Sorted order is result/body.
```

Read order:

```text
previous draw order
-> current draw order
-> outgoing motion contract
-> next draw order
-> sorted body result
```

This means Seat Taxonomy does not read sorted body as a guess for draw order.
It reads draw order as transition physics first, then reads sorted body as the result/body.

## Purpose

Seat Taxonomy answers:

```text
What hit the current set?
Where did that force store itself?
Which lane carried the burden?
What condition is the system in?
What event/action is happening?
What outgoing motion contract did the set produce?
What reusable motion room identity does this transition belong to?
```

The chain is:

```text
incoming motion
-> pressure origin
-> lane burden
-> pressure map
-> pressure world
-> pressure authority
-> motion state
-> motion archetype
-> collision point
-> outgoing contract
-> technical draw address
-> origin weight validation
```

## Sections

Seat Taxonomy currently outputs these sections:

```text
doctrine
draw
continuity
draw_order_transition
draw_order_face_identity
draw_order_taxonomy
incoming_motion
current_pressure
pressure_origin
lane_burden
pressure_map
pressure_authority
motion_state
motion_archetype
collision_point
technical_draw_address
origin_weight_validation
incoming_body_effect
outgoing_contract
next_technical_body
motion_law_candidate
sorted_result_body
```

## Draw Order Transition

Draw Order Transition is the main cause/motion section.

It carries:

```text
previous_draw_order
current_draw_order
next_draw_order
incoming_draw_delta
outgoing_draw_delta
incoming_draw_sign
outgoing_draw_sign
incoming_draw_family
outgoing_draw_family
incoming_energy
incoming_energy_class
outgoing_energy
outgoing_energy_class
dominant_incoming_draw_lane
dominant_incoming_draw_motion
dominant_outgoing_draw_lane
dominant_outgoing_draw_motion
```

It answers:

```text
How did draw order move from previous to current?
How did draw order move from current to next?
Which draw lane dominated each side of the transition?
```

## Draw Order Face Identity

Draw Order Face Identity describes the current draw-order face.

It carries:

```text
order_pattern
draw_order_band_pattern
sorted_position_path
transfer_pattern
direction_pattern
turn_count
turn_lanes
max_abs_lane
face_family
draw_style
```

It answers:

```text
What is the natural face of this set?
How does D1-D5 route through S1-S5?
How many turns does the face make?
Where is the largest internal draw-order lane move?
```

## Draw Order Taxonomy

Draw Order Taxonomy reads each D lane as a cause/motion lane.

Each lane carries:

```text
draw_lane
draw_role
number
draw_order_band
mapped_sorted_seat
mapped_sorted_zone
incoming_motion
incoming_sign
incoming_family
incoming_gauge
incoming_gauge_range
outgoing_motion
outgoing_sign
outgoing_family
outgoing_gauge
outgoing_gauge_range
incoming_to_outgoing_transfer
```

It answers:

```text
What did each D lane carry into the set?
Where did each D lane land in sorted body?
Did each lane carry, reverse, hinge, or remain boundary-unknown?
```

## Current Pressure

Current Pressure pulls the current set body condition from IIW.

It carries:

```text
set_health
set_relation
middle_pressure
edge_pressure
technical_signature
sorted_pressure
draw_pressure
pressure_flow
pressure_fusion_profile
pressure_fusion
```

It answers:

```text
What body is receiving the incoming motion?
Is the middle compressed, expanded, stable, or stretched?
How are edge pressure and pressure fusion behaving?
```

## Pressure Origin

Pressure Origin explains why a seat became pressured.

It is the causal layer before Pressure Map and Lane Burden.

Rule:

```text
Pressure Origin
-> Pressure Map
-> Lane Burden
-> Motion State
-> Motion Archetype
-> Outgoing Contract
```

It answers:

```text
Why does this seat have pressure?
Which contributors created the burden score?
Which origin did we underestimate if the wrong lane wins later?
```

Origin categories:

```text
INCOMING_MOTION
GAP_STRUCTURE
MIDDLE_COMPRESSION
EDGE_IMBALANCE
HINGE_TRAP
TRANSFER_REVERSAL
```

Category meanings:

```text
INCOMING_MOTION
  Pressure inherited from previous draw motion mapped into this sorted seat.

GAP_STRUCTURE
  Pressure created by left/right sorted gap geometry.

MIDDLE_COMPRESSION
  Pressure created because S2-S4 are carrying middle compression.

EDGE_IMBALANCE
  Pressure created by edge asymmetry, such as ENTRY_HEAVIER or EXIT_HEAVIER.

HINGE_TRAP
  Pressure created when a middle seat is trapped between tight adjacent gaps.

TRANSFER_REVERSAL
  Pressure created by incoming/outgoing sign inversion.
```

Each pressure-origin seat carries:

```text
seat
role
number
taxonomy
source_draw_lane
incoming_motion
incoming_direction
gap_pressure
left_gap
right_gap
middle_edge_modifier
pressure_origins
burden_score
burden_level
burden_gauge
burden_gauge_range
burden_state
structural_pressure
dynamic_pressure
dominant_pressure_type
pressure_level
pressure_gauge
pressure_gauge_range
pressure_role
```

Example:

```text
S3 Bridge: score=102
INCOMING_MOTION +54
GAP_STRUCTURE +5
MIDDLE_COMPRESSION +20
HINGE_TRAP +10
TRANSFER_REVERSAL +13
```

Now S3 is not only labeled `EXTREME`.
It is explainable.

## Structural And Dynamic Pressure

Pressure Origin separates pressure into two major forms.

Structural Pressure:

```text
pressure created by the body itself
```

Structural sources:

```text
GAP_STRUCTURE
MIDDLE_COMPRESSION
EDGE_IMBALANCE
HINGE_TRAP
```

Dynamic Pressure:

```text
pressure created by movement through time
```

Dynamic sources:

```text
INCOMING_MOTION
TRANSFER_REVERSAL
CARRY_FORWARD
COUNTER_ROTATION
```

Each seat therefore reads as:

```text
S3
structural_pressure = body-created pressure
dynamic_pressure    = motion-created pressure
total_pressure      = structural + dynamic
dominant_type       = STRUCTURAL / DYNAMIC / BALANCED / NONE
```

This matters because two seats can have the same total pressure but mean different things.

Example:

```text
Seat A
structural = 60
dynamic    = 10
total      = 70

Read:
the body itself is unstable.
```

```text
Seat B
structural = 10
dynamic    = 60
total      = 70

Read:
the body is being disturbed by motion.
```

This is the first step toward pressure authority:

```text
Which pressure source releases first?
Which pressure source carries?
Which pressure source wins when origins conflict?
```

## Lane Burden

Burden means stored pressure on a lane before it moves.

Rule:

```text
incoming motion = what hit the set
burden = where that hit got stored
outgoing motion = where the stored pressure escaped
```

Lane Burden reads all five sorted seats:

```text
S1 Core
S2 Entry
S3 Bridge
S4 Exit
S5 Endpoint
```

Each seat carries:

```text
incoming_motion
incoming_direction
adjacent_gap_pressure
gap_pressure
left_gap
right_gap
middle_edge_modifier
burden_score
burden_level
burden_gauge
burden_gauge_range
burden_state
pressure_level
pressure_gauge
pressure_gauge_range
pressure_role
```

Lane Burden also gives:

```text
highest_burden_seat
highest_burden_state
highest_burden_level
highest_burden_score
highest_burden_gauge
highest_burden_gauge_range
smallest_burden_seat
smallest_burden_state
smallest_burden_level
smallest_burden_score
smallest_burden_gauge
smallest_burden_gauge_range
```

It answers:

```text
Which seat is carrying unresolved pressure?
Which seat is least loaded?
Is the seat compressed, stretched, trapped, saturated, dragged, or holding?
```

## Burden Gauge

Burden Gauge is the IIW-level 35-class burden scale.

It uses Norse names in 1-2 spaces.

```text
1-2   Odin
3-4   Frigg
5-6   Thor
7-8   Sif
9-10  Baldr
11-12 Nanna
13-14 Hodr
15-16 Hermod
17-18 Tyr
19-20 Bragi
21-22 Idun
23-24 Heimdall
25-26 Loki
27-28 Sigyn
29-30 Hel
31-32 Fenrir
33-34 Jormungandr
35-36 Freyr
37-38 Freyja
39-40 Njord
41-42 Skadi
43-44 Ullr
45-46 Forseti
47-48 Vidar
49-50 Vali
51-52 Gefjon
53-54 Eir
55-56 Saga
57-58 Fulla
59-60 Gna
61-62 Var
63-64 Vor
65-66 Syn
67-68 Hlin
69-70 Snotra
```

The gauge cycles beyond 70 so high burden scores remain precise.

Example:

```text
burden_score 116 -> Forseti [115-116]
```

## Pressure Map

Pressure Map describes all five seats as one field.

It carries:

```text
dominant_pressure_seat
dominant_pressure_score
dominant_burden_gauge
dominant_burden_gauge_range
smallest_pressure_seat
smallest_pressure_score
smallest_burden_gauge
smallest_burden_gauge_range
pressure_shape
pressure_gauge_shape
burden_gauge_shape
structural_pressure_total
dynamic_pressure_total
map_pressure_type
pressure_center
pressure_balance
pressure_distribution
pressure_world
seats
```

Each pressure-map seat carries:

```text
incoming_motion
gap_pressure
left_gap
right_gap
middle_edge_modifier
structural_pressure
dynamic_pressure
dominant_pressure_type
burden_score
burden_gauge
burden_gauge_range
pressure_level
pressure_gauge
pressure_gauge_range
pressure_role
```

It answers:

```text
Where is the body storing force?
What is the whole pressure shape?
Is pressure left-heavy, right-heavy, center-heavy, or edge-heavy?
Is pressure focused, split, or spread?
What named pressure world does this map belong to?
```

## Pressure Worlds

Pressure Worlds are the readable handles for pressure topology.

The technical world key is built from:

```text
pressure authority
pressure center
pressure balance
pressure distribution
```

Pressure authority:

```text
STRUCTURAL_DOMINANT
DYNAMIC_DOMINANT
STRUCTURAL_DYNAMIC_BALANCED
```

Pressure center:

```text
CORE
MIDDLE
ENDPOINT
```

Pressure balance:

```text
LEFT_HEAVY
CENTER_HEAVY
RIGHT_HEAVY
EDGE_HEAVY
```

Pressure distribution:

```text
FOCUSED
SPLIT
SPREAD
```

There are:

```text
27 named topology worlds
108 exact world slots
```

The name is the readable handle.
The technical key remains underneath it.

Example:

```text
Medusa
= DYNAMIC_DOMINANT::MIDDLE::SPLIT
```

Then the exact world slot adds balance:

```text
WORLD_050
= DYNAMIC_DOMINANT::MIDDLE::LEFT_HEAVY::SPLIT
```

This means the research read can be:

```text
Go to Medusa world.
It is dynamic-dominant middle split pressure.
Then check which balance variant is active.
```

Named topology worlds:

```text
TOPOLOGY_WORLD_01 Altera      STRUCTURAL_DOMINANT::CORE::FOCUSED
TOPOLOGY_WORLD_02 Nova        STRUCTURAL_DOMINANT::CORE::SPLIT
TOPOLOGY_WORLD_03 Nyx         STRUCTURAL_DOMINANT::CORE::SPREAD
TOPOLOGY_WORLD_04 Citrine     STRUCTURAL_DOMINANT::MIDDLE::FOCUSED
TOPOLOGY_WORLD_05 Lumina      STRUCTURAL_DOMINANT::MIDDLE::SPLIT
TOPOLOGY_WORLD_06 Nirvana     STRUCTURAL_DOMINANT::MIDDLE::SPREAD
TOPOLOGY_WORLD_07 Alcides     STRUCTURAL_DOMINANT::ENDPOINT::FOCUSED
TOPOLOGY_WORLD_08 Artoria     STRUCTURAL_DOMINANT::ENDPOINT::SPLIT
TOPOLOGY_WORLD_09 Nero        STRUCTURAL_DOMINANT::ENDPOINT::SPREAD

TOPOLOGY_WORLD_10 Rama        DYNAMIC_DOMINANT::CORE::FOCUSED
TOPOLOGY_WORLD_11 Suzuka      DYNAMIC_DOMINANT::CORE::SPLIT
TOPOLOGY_WORLD_12 Tomoe Gozen DYNAMIC_DOMINANT::CORE::SPREAD
TOPOLOGY_WORLD_13 Karna       DYNAMIC_DOMINANT::MIDDLE::FOCUSED
TOPOLOGY_WORLD_14 Medusa      DYNAMIC_DOMINANT::MIDDLE::SPLIT
TOPOLOGY_WORLD_15 Kurohime    DYNAMIC_DOMINANT::MIDDLE::SPREAD
TOPOLOGY_WORLD_16 Irisviel    DYNAMIC_DOMINANT::ENDPOINT::FOCUSED
TOPOLOGY_WORLD_17 Circe       DYNAMIC_DOMINANT::ENDPOINT::SPLIT
TOPOLOGY_WORLD_18 Scathach    DYNAMIC_DOMINANT::ENDPOINT::SPREAD

TOPOLOGY_WORLD_19 Anastasia   STRUCTURAL_DYNAMIC_BALANCED::CORE::FOCUSED
TOPOLOGY_WORLD_20 Izumo       STRUCTURAL_DYNAMIC_BALANCED::CORE::SPLIT
TOPOLOGY_WORLD_21 Hanasaka    STRUCTURAL_DYNAMIC_BALANCED::CORE::SPREAD
TOPOLOGY_WORLD_22 Stheno      STRUCTURAL_DYNAMIC_BALANCED::MIDDLE::FOCUSED
TOPOLOGY_WORLD_23 Sasaki      STRUCTURAL_DYNAMIC_BALANCED::MIDDLE::SPLIT
TOPOLOGY_WORLD_24 Carmilla    STRUCTURAL_DYNAMIC_BALANCED::MIDDLE::SPREAD
TOPOLOGY_WORLD_25 Semiramis   STRUCTURAL_DYNAMIC_BALANCED::ENDPOINT::FOCUSED
TOPOLOGY_WORLD_26 Consort Yu  STRUCTURAL_DYNAMIC_BALANCED::ENDPOINT::SPLIT
TOPOLOGY_WORLD_27 Kashin      STRUCTURAL_DYNAMIC_BALANCED::ENDPOINT::SPREAD
```

Each topology has four exact balance variants:

```text
LEFT_HEAVY
CENTER_HEAVY
RIGHT_HEAVY
EDGE_HEAVY
```

## Pressure Gauge

Pressure Gauge is the IIW-level 35-class raw pressure scale.

It uses Chinese names in 1-2 spaces.

```text
1-2   Pangu
3-4   Nuwa
5-6   Fuxi
7-8   Shennong
9-10  Huangdi
11-12 Xiwangmu
13-14 Dongwanggong
15-16 Yuhuang
17-18 Guanyin
19-20 Mazu
21-22 Chang'e
23-24 Houyi
25-26 Erlang Shen
27-28 Nezha
29-30 Lei Gong
31-32 Dian Mu
33-34 Feng Bo
35-36 Yu Shi
37-38 Zhurong
39-40 Gonggong
41-42 Houtu
43-44 Wenchang
45-46 Caishen
47-48 Zao Jun
49-50 Tudi Gong
51-52 Chenghuang
53-54 Long Wang
55-56 Yanluo Wang
57-58 Zhong Kui
59-60 Lu Dongbin
61-62 He Xiangu
63-64 Li Tieguai
65-66 Lan Caihe
67-68 Han Xiangzi
69-70 Zhang Guolao
```

The gauge cycles beyond 70 if needed.

Example:

```text
gap_pressure 32 -> Dian Mu [31-32]
```

## Motion State

Motion State describes the condition of the system.

Examples:

```text
COUNTER_ROTATION
RETENTIVE
RELEASING
BALANCED_TRANSFER
BOUNDARY_UNKNOWN
```

Body Motion State describes the body condition:

```text
COMPRESSED
EXPANDING
REBOUNDING
RELEASING
RETENTIVE
STABLE
BOUNDARY_UNKNOWN
```

It answers:

```text
What condition is the transition in right now?
```

## Pressure Authority

Pressure Authority answers:

```text
Which pressure source has the right to control the motion?
```

Raw pressure asks:

```text
Which seat has the biggest total?
```

Authority asks:

```text
Which origin is allowed to speak loudest in this pressure world?
```

Authority reads existing fields only:

```text
pressure_origin
pressure_world
motion_state
motion_archetype
```

It does not create new pressure.
It weights pressure origins that already exist.

Authority origin families:

```text
INCOMING_MOTION
GAP_STRUCTURE
MIDDLE_COMPRESSION
EDGE_IMBALANCE
HINGE_TRAP
TRANSFER_REVERSAL
```

World read:

```text
STRUCTURAL_DOMINANT
  structural origins gain authority.

DYNAMIC_DOMINANT
  motion origins gain authority.

STRUCTURAL_DYNAMIC_BALANCED
  no origin wins automatically; topology and conflict matter more.
```

Pressure Authority outputs:

```text
authority_world
authority_winner_seat
authority_winner_origin
authority_winner_score
authority_winner_draw_lane
raw_pressure_winner_seat
raw_pressure_winner_score
authority_changed_winner
seats
```

Each seat carries:

```text
seat
role
raw_pressure
authority_pressure
winning_origin
winning_origin_pressure
source_draw_lane
origin_breakdown
```

Each origin breakdown carries:

```text
origin
raw_pressure
authority_weight
authority_pressure
meaning
```

It answers:

```text
What had authority?
Did authority agree with raw pressure?
Which origin created the authority?
```

## Motion Archetype

Motion Archetype describes the action/event.

Examples:

```text
MIDDLE_RELEASE
COUNTER_RELEASE
CARRY_LOCK
TAIL_RELEASE
PRESSURE_TRANSFER
COUNTER
RELEASE
CARRY
EXCHANGE
LIFT
COLLAPSE
TRANSFER
BOUNDARY_UNKNOWN
```

It answers:

```text
What kind of motion event is happening?
```

## Resolution Bias

Resolution Bias is the missing layer between Authority and Collision.

It answers:

```text
Which destination family is this room biased toward before final collision?
```

The working chain is now:

```text
Pressure World
-> Authority
-> Conflict Signature
-> Resolution Bias
-> Collision Point
-> Outgoing Lane
```

Seat families:

```text
EDGE_FAMILY
  S1 <-> S5

HINGE_FAMILY
  S2 <-> S4

CENTER_FAMILY
  S3
```

Resolution Bias carries:

```text
bias_status
authority_seat
authority_family
bias_type
primary_bias_seat
primary_bias_family
secondary_bias_seat
secondary_bias_family
tertiary_bias_seat
tertiary_bias_family
bias_reason
candidates
```

Bias types currently include:

```text
DIRECT_BIAS
EDGE_BIAS
HINGE_BIAS
HINGE_EDGE_SPLIT_BIAS
EDGE_RESOLUTION_BIAS
STRUCTURAL_REPAIR_BIAS
CENTER_BIAS
CENTER_TO_EDGE_BIAS
TAIL_BIAS
```

By default, Resolution Bias is diagnostic.
Collision Point still uses the existing collision rule unless the script is run with:

```powershell
--use-resolution-bias
```

This is intentional.
The first operational bias values did not improve the full audit.
So Resolution Bias is now available for inspection and tuning without silently replacing the stronger baseline collision behavior.

Example:

```text
MEDUSA
AUTHSEAT_S2
FULL_REVERSAL

resolution_bias:
  HINGE_EDGE_SPLIT_BIAS
  primary   S4 HINGE_FAMILY
  secondary S5 EDGE_FAMILY
  tertiary  S1 EDGE_FAMILY
```

## Collision Point

Collision Point answers:

```text
Where does the winning authority terminate?
```

Outgoing Contract says what happened.
Collision Point explains why that outgoing lane or sorted seat was chosen.

Read:

```text
pressure creates force
authority chooses the governing force
collision shows where that force lands
```

Collision reads:

```text
pressure_authority
resolution_bias
pressure_map
motion_state
motion_archetype
outgoing_contract
```

It carries:

```text
collision_status
authority_seat
authority_origin
authority_score
collision_seat
collision_zone
collision_type
collision_reason
expected_draw_lane
observed_draw_lane
observed_sorted_seat
collision_seat_validation
collision_lane_validation
validation_result
resolution_bias_type
resolution_primary_family
resolution_secondary_seat
resolution_secondary_family
used_resolution_bias
```

Collision types:

```text
DIRECT_RELEASE
  The authority seat releases through itself.

TRANSFER_RELEASE
  The authority pressure steps into a nearby or dominant pressure seat.

COUNTER_TERMINATION
  The authority pressure reverses across the body.

EDGE_COLLISION
  The authority pressure terminates at S1 or S5.
```

Example:

```text
authority_seat  S2
collision_seat  S4
collision_type  COUNTER_TERMINATION

Read:
S2 had authority, but split reversal pushed the force across the body into S4.
```

Collision validation is split into two checks:

```text
collision_seat_validation
  Did the predicted collision seat match the observed outgoing sorted seat?

collision_lane_validation
  Did the expected draw lane match the observed outgoing draw lane?
```

This distinction matters because the system may know where the force landed but miss which draw lane carried it.

Possible reads:

```text
seat=MATCH lane=MATCH
  The system found the landing seat and carrier lane.

seat=MATCH lane=MISS
  The system found where force landed, but not which draw lane delivered it.

seat=MISS lane=MATCH
  The system found the carrier lane, but not the sorted collision seat.

seat=MISS lane=MISS
  The collision read missed both landing seat and carrier lane.
```

## Collision Law Report

Collision Law Report aggregates historical transitions into reusable law keys.

Command:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --collision-laws --limit 25
```

The report scans the full selected date window.
With `--collision-laws`, `--limit` controls how many law rows are displayed, not how many draws are scanned.

Law key format:

```text
<topology_name>::
<world_key>::
AUTHSEAT_<authority_winner_seat>::
AUTHORITY_<authority_winner_origin>::
STATE_<motion_state>::
TRANSFER_<transfer>::
CTYPE_<collision_type>
```

Example law key:

```text
MEDUSA::
DYNAMIC_DOMINANT::MIDDLE::LEFT_HEAVY::SPLIT::
AUTHSEAT_S2::
AUTHORITY_INCOMING_MOTION::
STATE_COUNTER_ROTATION::
TRANSFER_FULL_REVERSAL::
CTYPE_COUNTER_TERMINATION
```

Each law row carries:

```text
appearances
collision_seat_match_count
collision_seat_match_rate
collision_lane_match_count
collision_lane_match_rate
both_match_count
both_match_rate
most_common_predicted_collision_seat
most_common_observed_collision_seat
most_common_observed_lane
observed_collision_seat_counts
observed_lane_counts
dates
```

This answers:

```text
When this exact world + authority + state + transfer + collision type appears,
where does force usually terminate,
and which draw lane usually carries it?
```

Example report read:

```text
MEDUSA::DYNAMIC_DOMINANT::MIDDLE::LEFT_HEAVY::SPLIT::AUTHSEAT_S2::AUTHORITY_INCOMING_MOTION::STATE_COUNTER_ROTATION::TRANSFER_FULL_REVERSAL::CTYPE_COUNTER_TERMINATION
  appearances 1
  both=1 seat=1 lane=1
  predicted=S4 observed_seat=S4 observed_lane=D3
```

## Collision Law Audit

Collision Law Audit classifies the collision-law report into proof states.

Command:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --collision-law-audit --limit 25
```

Like `--collision-laws`, the audit scans the full selected date window.
With `--collision-law-audit`, `--limit` controls how many audit rows are displayed.

Audit levels:

```text
--collision-law-level 1
  topology + base world + authority seat + authority origin

--collision-law-level 2
  level 1 + motion state + transfer

--collision-law-level 3
  level 2 + collision type

--collision-law-level 4
  level 3 + exact world key, including center/balance/distribution
```

Level 1 is broad.
Level 4 is exact.

The purpose is to see whether a law is stable broadly or only stable inside a precise world/balance room.

Status labels:

```text
PROVEN
  appearances >= 5 and both_match_rate >= 80

PROMISING
  appearances >= 3 and both_match_rate >= 60

UNSTABLE
  appearances < 3 with both_match_rate <= 20,
  or enough appearances to inspect but the law is not clean enough yet

FAILED
  both_match_rate < 50 after it has at least 3 appearances

LOW_SAMPLE
  appearances < 3 unless it is already extremely weak
```

Each audit row adds:

```text
law_status
conflict_signature
dominant_failure_pattern
recommended_action
```

Conflict Signature reads whether a room converges or branches.

It carries:

```text
conflict_type
primary_collision_seat
primary_collision_count
primary_collision_rate
secondary_collision_seat
secondary_collision_count
secondary_collision_rate
tertiary_collision_seat
tertiary_collision_count
tertiary_collision_rate
seat_rank
lane_rank
branch_rank
read
```

Conflict types:

```text
CONVERGENT
  One observed collision destination dominates.

LEANING_CONVERGENT
  One destination leads, but secondary pressure still matters.

DIVERGENT
  Multiple destinations are competing.

SPLIT_FIELD
  The field is spread and needs another discriminator.

LOW_SAMPLE_CONFLICT
  Not enough appearances to read branching yet.
```

This changes the audit question from:

```text
Did the law fail?
```

to:

```text
Is the room convergent or branching?
If it branches, which destination is primary and which is secondary?
```

Recommended actions:

```text
KEEP_AS_LAW_CANDIDATE
KEEP_AND_VALIDATE_MORE_WINDOWS
COLLECT_MORE_APPEARANCES_BEFORE_CHANGING_RULE
REBUILD_COLLISION_RULE_FOR_THIS_WORLD_AUTHORITY_PATTERN
INSPECT_SEAT_LANE_SPLIT_AND_ADD_CONFLICT_RULE
```

Full audit run from `2015-10-07`:

```text
Historical draws  1368
Boundary skipped  1
Law keys          432

FAILED      96
PROMISING   8
UNSTABLE    230
PROVEN      3
LOW_SAMPLE  95
```

Level comparison from `2015-10-07`:

```text
LEVEL 1
law_keys 77
FAILED 43 | UNSTABLE 22 | PROMISING 2 | LOW_SAMPLE 10

LEVEL 2
law_keys 258
FAILED 88 | UNSTABLE 109 | PROMISING 7 | PROVEN 1 | LOW_SAMPLE 53

LEVEL 3
law_keys 295
FAILED 88 | UNSTABLE 131 | PROVEN 1 | PROMISING 6 | LOW_SAMPLE 69

LEVEL 4
law_keys 432
FAILED 96 | PROMISING 8 | UNSTABLE 230 | PROVEN 3 | LOW_SAMPLE 95
```

Level 4 conflict signature counts:

```text
LOW_SAMPLE_CONFLICT 321
DIVERGENT           56
CONVERGENT          38
LEANING_CONVERGENT  13
SPLIT_FIELD         4
```

Failed-room conflict breakdown:

```text
FAILED_DIVERGENT           56
FAILED_CONVERGENT          26
FAILED_LEANING_CONVERGENT  10
FAILED_SPLIT_FIELD         4
```

Read:

```text
The failures are not random.
Many failed rooms are divergent, meaning the current rule is missing the condition that chooses between repeatable branches.
```

Read:

```text
Broad grouping is not automatically better.
Level 1 mixes too many different balance and transfer behaviors.
Level 4 exposes exact world/balance laws, including Medusa, Irisviel, Artoria, and Lumina patterns.
```

Resolution Bias mode comparison:

```text
DEFAULT DIAGNOSTIC MODE
LEVEL 1 law_keys=77  FAILED 43 | UNSTABLE 22  | PROMISING 2 | LOW_SAMPLE 10
LEVEL 2 law_keys=258 FAILED 88 | UNSTABLE 109 | PROMISING 7 | PROVEN 1 | LOW_SAMPLE 53
LEVEL 3 law_keys=295 FAILED 88 | UNSTABLE 131 | PROMISING 6 | PROVEN 1 | LOW_SAMPLE 69
LEVEL 4 law_keys=432 FAILED 96 | UNSTABLE 230 | PROMISING 8 | PROVEN 3 | LOW_SAMPLE 95

--use-resolution-bias MODE
LEVEL 1 law_keys=77  FAILED 44 | UNSTABLE 26  | PROMISING 1 | LOW_SAMPLE 6
LEVEL 2 law_keys=258 FAILED 89 | UNSTABLE 116 | PROMISING 6 | PROVEN 1 | LOW_SAMPLE 46
LEVEL 3 law_keys=290 FAILED 87 | UNSTABLE 144 | PROMISING 5 | PROVEN 1 | LOW_SAMPLE 53
LEVEL 4 law_keys=410 FAILED 91 | UNSTABLE 221 | PROMISING 7 | PROVEN 1 | LOW_SAMPLE 90
```

Read:

```text
The first resolution-bias values are useful diagnostically, but they are not ready to drive collision by default.
Operational bias reduced Level 4 proven rooms from 3 to 1.
So the bias values need tuning before live use.
```

Resolution Bias adjustment target audit:

```text
resolution_bias_adjustment_targets_2015-10-07.json
resolution_bias_branch_findings_2015-10-07.json

Rule:
Level-4 rooms with appearances >= 10 where the current predicted collision seat
does not match the historical primary branch.

Branch findings:
All level-4 rooms with appearances >= 10, including rooms where the old prediction
already matches the primary branch.

Target count:
17

Branch finding count:
30

Grouped by topology:
Medusa   7
Lumina   4
Alcides  1
Altera   1
Artoria  1
Citrine  1
Karna    1
Suzuka   1
```

Top first-pass value targets:

```text
Suzuka | DYNAMIC_DOMINANT::CORE::LEFT_HEAVY::SPLIT | AUTH S1 | HYBRID_COUNTER | EDGE_COLLISION
current S1 -> primary branch S5 at 40.0%

Lumina | STRUCTURAL_DOMINANT::MIDDLE::RIGHT_HEAVY::SPLIT | AUTH S4 | HYBRID_COUNTER | TRANSFER_RELEASE
current S5 -> primary branch S1 at 52.94%

Artoria | STRUCTURAL_DOMINANT::ENDPOINT::RIGHT_HEAVY::SPLIT | AUTH S5 | HYBRID_COUNTER | EDGE_COLLISION
current S5 -> primary branch S1 at 50.0%

Lumina | STRUCTURAL_DOMINANT::MIDDLE::LEFT_HEAVY::SPLIT | AUTH S2 | HYBRID_COUNTER | DIRECT_RELEASE
current S2 -> primary branch S4 at 52.63%

Karna | DYNAMIC_DOMINANT::MIDDLE::LEFT_HEAVY::FOCUSED | AUTH S2 | HYBRID_COUNTER | DIRECT_RELEASE
current S2 -> primary branch S1 at 44.44%
```

Read:

```text
The next work is not adding a new concept.
The next work is calibrating resolution-bias values against the conflict signatures.
The first adjustment pass should target Medusa and Lumina because they hold 11 of the 17 high-sample disagreements.
```

Branch findings mode:

```text
--use-resolution-bias
```

now means:

```text
Use the exact historical branch finding when a level-4 room has enough evidence.
If no finding exists, keep the baseline collision read.
```

This replaced the earlier broad family-driven operational bias.
The generic family bias still prints as context, but it no longer overrides collision by itself.

Calibrated branch-finding audit from `2015-10-07`:

```text
LEVEL 1
law_keys 77
FAILED 42 | UNSTABLE 23 | PROMISING 2 | LOW_SAMPLE 10

LEVEL 2
law_keys 258
FAILED 86 | UNSTABLE 111 | PROMISING 7 | PROVEN 1 | LOW_SAMPLE 53

LEVEL 3
law_keys 295
FAILED 85 | UNSTABLE 134 | PROMISING 6 | PROVEN 1 | LOW_SAMPLE 69

LEVEL 4
law_keys 432
FAILED 88 | PROMISING 11 | UNSTABLE 235 | PROVEN 3 | LOW_SAMPLE 95
```

Read:

```text
The findings layer improved the audit because it uses observed branch destinations.
Level 4 failed rooms dropped from 96 to 88.
Level 4 promising rooms rose from 8 to 11.
Proven rooms stayed at 3.
The remaining failed rooms are mostly split/branch problems, not proof that the family idea is wrong.
```

## Pre-Collision Preference Field

The audit shows that the problem is often upstream of Collision Point.

The revised chain is:

```text
Pressure
-> Authority
-> Pre-Collision Preference Field
-> Branch Selector
-> Resolution Bias
-> Collision
```

Pre-Collision Preference Field answers:

```text
What weighted seat universe exists before the final collision seat is selected?
```

Common universes:

```text
EDGE_BINARY
  S1 <-> S5

HINGE_BINARY
  S2 <-> S4

CENTER_MIXED
  S3 is part of the preference field.

MIXED_FAMILY_FIELD
  Edge, hinge, or center families are competing.
```

Selection reads:

```text
PRIMARY_SELECTED
  Baseline collision already chose the strongest historical branch.

SECONDARY_SELECTED
  Baseline collision chose the second branch.

CORRECT_FAMILY_WRONG_SEAT
  Baseline collision found the right family but picked the wrong member.

SECONDARY_FAMILY_SELECTED
  Baseline collision chose the secondary family.

OUTSIDE_PREFERENCE_FIELD
  Baseline collision landed outside the measured preference field.
```

Cross-level evidence file:

```text
resolution_bias_pre_collision_evidence_2015-10-07.json
```

High-sample universe counts:

```text
LEVEL 1
EDGE_BINARY 19 | MIXED_FAMILY_FIELD 11 | HINGE_BINARY 1
primary family: EDGE_FAMILY 30 | HINGE_FAMILY 1

LEVEL 2
MIXED_FAMILY_FIELD 14 | EDGE_BINARY 13 | CENTER_MIXED 1 | HINGE_BINARY 1
primary family: EDGE_FAMILY 25 | HINGE_FAMILY 4

LEVEL 3
EDGE_BINARY 15 | MIXED_FAMILY_FIELD 10 | HINGE_BINARY 4 | CENTER_MIXED 4
primary family: EDGE_FAMILY 23 | HINGE_FAMILY 10

LEVEL 4
EDGE_BINARY 16 | MIXED_FAMILY_FIELD 7 | HINGE_BINARY 4 | CENTER_MIXED 3
primary family: EDGE_FAMILY 21 | HINGE_FAMILY 9
```

Level 4 selection problem counts:

```text
PRIMARY_SELECTED             13
CORRECT_FAMILY_WRONG_SEAT     9
OUTSIDE_PREFERENCE_FIELD      6
SECONDARY_FAMILY_SELECTED     2
```

Read:

```text
The collision engine is often not operating in a five-seat universe.
It is often operating inside a two-seat preference field, especially S1 <-> S5.
That means many misses are not full law failures.
They are pre-collision selection problems: correct field, wrong branch.
```

## Branch Selector

Branch Selector answers:

```text
Inside the measured preference field, which branch wins?
```

Example:

```text
EDGE_BINARY
S1 <-> S5

Branch Selector decides:
S1 wins
or
S5 wins
```

The branch selector does not call a split a failure.
It classifies the outcome:

```text
PRIMARY_BRANCH_WON
SECONDARY_BRANCH_WON
TERTIARY_BRANCH_WON
FIELD_RIGHT_ALT_BRANCH
OUTSIDE_FIELD
NO_FIELD
```

Audit command:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --branch-selector-audit --branch-selector-level 2 --limit 25
```

Audit statuses:

```text
PROVEN
  sample >= 5 and selected branch rate >= 80

PROMISING
  sample >= 3 and selected branch rate >= 60

SPLIT
  primary and secondary branches are within 10 percentage points

UNSTABLE
  enough to inspect, but no branch is strong yet

LOW_SAMPLE
  sample < 3
```

Branch selector level comparison from `2015-10-07`:

```text
LEVEL 1
selector_keys 27
SPLIT 8 | UNSTABLE 16 | PROMISING 3

LEVEL 2
selector_keys 30
SPLIT 10 | UNSTABLE 15 | PROMISING 5

LEVEL 3
selector_keys 571
LOW_SAMPLE 570 | PROMISING 1

LEVEL 4
selector_keys 577
LOW_SAMPLE 577
```

Read:

```text
Level 2 is the current learning layer.
Level 1 is useful but too broad.
Level 3 and Level 4 are too specific and collapse into low sample.
```

Current promising branch selector laws:

```text
Medusa | EDGE_BINARY | DYNAMIC_DOMINANT::MIDDLE::LEFT_HEAVY::SPLIT | AUTH S2 INCOMING_MOTION
S1 wins 63.89% over S5 27.78% | sample 36

Medusa | EDGE_BINARY | DYNAMIC_DOMINANT::MIDDLE::RIGHT_HEAVY::SPLIT | AUTH S4 INCOMING_MOTION
S5 wins 67.74% over S1 25.81% | sample 31

Irisviel | MIXED_FAMILY_FIELD | DYNAMIC_DOMINANT::ENDPOINT::RIGHT_HEAVY::FOCUSED | AUTH S5 INCOMING_MOTION
S5 wins 60.0% over S2 13.33% | sample 15

Medusa | EDGE_BINARY | DYNAMIC_DOMINANT::MIDDLE::CENTER_HEAVY::SPLIT | AUTH S3 INCOMING_MOTION
S1 wins 72.73% over S5 27.27% | sample 11

Medusa | EDGE_BINARY | DYNAMIC_DOMINANT::MIDDLE::CENTER_HEAVY::SPLIT | AUTH S4 INCOMING_MOTION
S1 wins 60.0% over S5 30.0% | sample 10
```

Read:

```text
This is the beginning of the branch law.
The system is no longer only asking where pressure terminates.
It is learning which side of the preference field wins under a technical condition.
```

Saved audit JSON files:

```text
collision_law_audit_level_1_2015-10-07.json
collision_law_audit_level_2_2015-10-07.json
collision_law_audit_level_3_2015-10-07.json
collision_law_audit_level_4_2015-10-07.json
collision_law_audit_2015-10-07.json
collision_law_audit_level_1_resolution_bias_2015-10-07.json
collision_law_audit_level_2_resolution_bias_2015-10-07.json
collision_law_audit_level_3_resolution_bias_2015-10-07.json
collision_law_audit_level_4_resolution_bias_2015-10-07.json
resolution_bias_adjustment_targets_2015-10-07.json
resolution_bias_branch_findings_2015-10-07.json
collision_law_audit_level_1_branch_findings_2015-10-07.json
collision_law_audit_level_2_branch_findings_2015-10-07.json
collision_law_audit_level_3_branch_findings_2015-10-07.json
collision_law_audit_level_4_branch_findings_2015-10-07.json
resolution_bias_pre_collision_evidence_2015-10-07.json
branch_selector_audit_level_1_2015-10-07.json
branch_selector_audit_level_2_2015-10-07.json
branch_selector_audit_level_3_2015-10-07.json
branch_selector_audit_level_4_2015-10-07.json
```

This is the current truth of the system:

```text
The framework is working.
The first-pass authority/collision rules are not fully proven yet.
Most rooms now move into unstable instead of low-sample, which is useful because the system can start inspecting them instead of ignoring them.
```

Current proven laws:

```text
ALTERA::STRUCTURAL_DOMINANT::CORE::LEFT_HEAVY::FOCUSED::AUTHSEAT_S1::AUTHORITY_INCOMING_MOTION::STATE_COUNTER_ROTATION::TRANSFER_HYBRID_COUNTER::CTYPE_EDGE_COLLISION
  appearances=7 both=85.71%

LUMINA::STRUCTURAL_DOMINANT::MIDDLE::RIGHT_HEAVY::SPLIT::AUTHSEAT_S4::AUTHORITY_GAP_STRUCTURE::STATE_RELEASING::TRANSFER_CARRY_PRESSURE::CTYPE_TRANSFER_RELEASE
  appearances=6 both=83.33%

LUMINA::STRUCTURAL_DOMINANT::MIDDLE::RIGHT_HEAVY::SPLIT::AUTHSEAT_S4::AUTHORITY_MIDDLE_COMPRESSION::STATE_COUNTER_ROTATION::TRANSFER_HYBRID_COUNTER::CTYPE_TRANSFER_RELEASE
  appearances=6 both=83.33%
```

Current promising laws:

```text
MEDUSA::DYNAMIC_DOMINANT::MIDDLE::LEFT_HEAVY::SPLIT::AUTHSEAT_S2::AUTHORITY_INCOMING_MOTION::STATE_COUNTER_ROTATION::TRANSFER_HYBRID_COUNTER::CTYPE_TRANSFER_RELEASE
  appearances=36 both=61.11%

IRISVIEL::DYNAMIC_DOMINANT::ENDPOINT::RIGHT_HEAVY::FOCUSED::AUTHSEAT_S5::AUTHORITY_INCOMING_MOTION::STATE_COUNTER_ROTATION::TRANSFER_HYBRID_COUNTER::CTYPE_EDGE_COLLISION
  appearances=15 both=60.0%

ARTORIA::STRUCTURAL_DOMINANT::ENDPOINT::RIGHT_HEAVY::SPLIT::AUTHSEAT_S5::AUTHORITY_INCOMING_MOTION::STATE_COUNTER_ROTATION::TRANSFER_HYBRID_COUNTER::CTYPE_EDGE_COLLISION
  appearances=5 both=60.0%

CITRINE::STRUCTURAL_DOMINANT::MIDDLE::LEFT_HEAVY::FOCUSED::AUTHSEAT_S2::AUTHORITY_INCOMING_MOTION::STATE_COUNTER_ROTATION::TRANSFER_HYBRID_COUNTER::CTYPE_DIRECT_RELEASE
  appearances=4 both=75.0%

KARNA::DYNAMIC_DOMINANT::MIDDLE::CENTER_HEAVY::FOCUSED::AUTHSEAT_S2::AUTHORITY_INCOMING_MOTION::STATE_COUNTER_ROTATION::TRANSFER_HYBRID_COUNTER::CTYPE_DIRECT_RELEASE
  appearances=3 both=66.67%

LUMINA::STRUCTURAL_DOMINANT::MIDDLE::CENTER_HEAVY::SPLIT::AUTHSEAT_S2::AUTHORITY_GAP_STRUCTURE::STATE_COUNTER_ROTATION::TRANSFER_HYBRID_COUNTER::CTYPE_DIRECT_RELEASE
  appearances=3 both=66.67%

LUMINA::STRUCTURAL_DOMINANT::MIDDLE::RIGHT_HEAVY::SPLIT::AUTHSEAT_S4::AUTHORITY_GAP_STRUCTURE::STATE_RETENTIVE::TRANSFER_CARRY_PRESSURE::CTYPE_TRANSFER_RELEASE
  appearances=3 both=66.67%

LUMINA::STRUCTURAL_DOMINANT::MIDDLE::LEFT_HEAVY::SPLIT::AUTHSEAT_S2::AUTHORITY_MIDDLE_COMPRESSION::STATE_COUNTER_ROTATION::TRANSFER_HYBRID_COUNTER::CTYPE_TRANSFER_RELEASE
  appearances=3 both=100.0%
```

## Technical Draw Address

Technical Draw Address is the compact reusable motion room identity.

Format:

```text
TECH_DRAW::
IN_<incoming_draw_family>::
OUT_<outgoing_draw_family>::
STATE_<motion_state>::
ARCHETYPE_<motion_archetype>::
BURDEN_<seat>_<level>_<state>::
AUTHORITY_<authority_origin>::
AUTHSEAT_<authority_seat>::
DS_<draw_singularity_family>::
DSSUB_<draw_singularity_subfamily>::
DSPROFILE_<draw_singularity_internal_profile>::
COLLISION_<collision_seat>::
CTYPE_<collision_type>::
FLOW_<pressure_flow>::
TRANSFER_<transfer>::
OUTLANE_<dominant_outgoing_lane>::
FACE_<face_family>::
BODY_<set_relation>::
MIDDLE_<middle_pressure>::
CENTER_<pressure_center>::
BALANCE_<pressure_balance>::
DIST_<pressure_distribution>::
PTYPE_<map_pressure_type>::
WSLOT_<world_slot>::
TOPONAME_<topology_name>
```

It answers:

```text
What exact motion room is this?
```

The address keeps both forms:

```text
TOPONAME_MEDUSA
```

is the readable world.

```text
DYNAMIC_DOMINANT::MIDDLE::LEFT_HEAVY::SPLIT
```

is the technical world key.

The authority and collision fields keep the reason and termination point in the room address:

```text
AUTHORITY_INCOMING_MOTION
AUTHSEAT_S2
COLLISION_S4
CTYPE_COUNTER_TERMINATION
```

This means the address identifies:

```text
why the motion happened
where the motion terminated
```

## Origin Weight Validation

Origin Weight Validation tests whether the strongest raw pressure source became the dominant outgoing release.

Collision Point is more refined than Origin Weight Validation.

Origin Weight Validation asks:

```text
Did the highest raw pressure seat release directly?
```

Collision Point asks:

```text
Did the authority terminate at the observed outgoing seat?
```

This is why a draw can have:

```text
origin_weight_validation = MISS
collision_point          = MATCH
```

That means raw pressure did not release directly, but the authority/collision law still explained the observed outgoing lane.

It carries:

```text
dominant_origin_seat
dominant_origin_score
dominant_origin_type
dominant_outgoing_lane
dominant_outgoing_sorted_seat
validation_result
structural_pressure_total
dynamic_pressure_total
pressure_type_total
debug_read
```

It answers:

```text
Did the highest-pressure seat become the dominant outgoing seat?
If not, which pressure source did we underestimate?
```

This is the validation layer that turns observation into motion physics.

Future statistics should group by:

```text
topology_name
map_pressure_type
dominant_origin_type
dominant_origin_seat
dominant_outgoing_sorted_seat
validation_result
```

## Latest Confirmed Example

Example:

```text
date         2026-06-15
current      62-55-60-57-25
next         49-53-3-26-61
```

Draw-order transition:

```text
incoming_delta  +12,+42,+16,+54,-28
outgoing_delta  -13,-2,-57,-31,+36
incoming_sign   ++++-
outgoing_sign   ----+
dominant_in     D4 +54
dominant_out    D3 -57
```

Pressure origin:

```text
dominant S2 score=117
smallest S5 score=39

S1 Core     INCOMING_MOTION +28, GAP_STRUCTURE +40, EDGE_IMBALANCE +20, TRANSFER_REVERSAL +13
S2 Entry    INCOMING_MOTION +42, GAP_STRUCTURE +42, MIDDLE_COMPRESSION +20, TRANSFER_REVERSAL +13
S3 Bridge   INCOMING_MOTION +54, GAP_STRUCTURE +5, MIDDLE_COMPRESSION +20, HINGE_TRAP +10, TRANSFER_REVERSAL +13
S4 Exit     INCOMING_MOTION +16, GAP_STRUCTURE +5, MIDDLE_COMPRESSION +20, HINGE_TRAP +10, TRANSFER_REVERSAL +13
S5 Endpoint INCOMING_MOTION +12, GAP_STRUCTURE +2, EDGE_IMBALANCE +12, TRANSFER_REVERSAL +13
```

Structural/dynamic split:

```text
S1 Core     struct=60 dyn=41 type=STRUCTURAL
S2 Entry    struct=62 dyn=55 type=STRUCTURAL
S3 Bridge   struct=35 dyn=67 type=DYNAMIC
S4 Exit     struct=35 dyn=29 type=STRUCTURAL
S5 Endpoint struct=14 dyn=25 type=DYNAMIC

map totals  structural=206 dynamic=217 DYNAMIC_DOMINANT
```

Pressure map:

```text
pressure_shape    EXTREME-EXTREME-EXTREME-MEDIUM-LOW
burden_gauges     Fenrir-Vidar-Fenrir-Vor-Njord
pressure_gauges   Lei Gong-Dian Mu-Fuxi-Fuxi-Pangu
pressure_center   MIDDLE
pressure_balance  LEFT_HEAVY
distribution      SPLIT
world             WORLD_050 | TOPOLOGY_WORLD_14 Medusa
world_key         DYNAMIC_DOMINANT::MIDDLE::LEFT_HEAVY::SPLIT
```

Lane burden:

```text
highest  S2 EXTREME HINGE_LOAD score=117 Vidar [117-118]
smallest S5 LOW HOLD score=39 Njord [39-40]
```

Motion:

```text
motion_state      COUNTER_ROTATION
body_state        COMPRESSED
motion_archetype  MIDDLE_RELEASE
```

Pressure authority:

```text
winner      S2 INCOMING_MOTION score=184.3
raw winner  S2 score=117 changed=False

S1 Core     raw=101 auth=137.75 win=INCOMING_MOTION draw_lane=D5
S2 Entry    raw=117 auth=184.3  win=INCOMING_MOTION draw_lane=D2
S3 Bridge   raw=102 auth=174.15 win=INCOMING_MOTION draw_lane=D4
S4 Exit     raw=64  auth=103.85 win=INCOMING_MOTION draw_lane=D3
S5 Endpoint raw=39  auth=60.45  win=TRANSFER_REVERSAL draw_lane=D1
```

Collision point:

```text
status       HISTORICAL_VALIDATION
authority    S2 INCOMING_MOTION score=184.3
collision    S4 MIDDLE COUNTER_TERMINATION
expected     D3
observed     D3 S4
validation   MATCH
seat         MATCH
lane         MATCH
reason       split reversal pushed authority across the body
```

Technical draw address:

```text
TECH_DRAW::IN_LIFT_DOMINANT_TRANSITIONAL_MOTION_D4::OUT_DROP_DOMINANT_DIRECTED_MOTION_D3::STATE_COUNTER_ROTATION::ARCHETYPE_MIDDLE_RELEASE::BURDEN_S2_EXTREME_HINGE_LOAD::AUTHORITY_INCOMING_MOTION::AUTHSEAT_S2::COLLISION_S4::CTYPE_COUNTER_TERMINATION::FLOW_RETENTION::TRANSFER_FULL_REVERSAL::OUTLANE_D3::FACE_VALLEY_CREST::BODY_OUTER_EDGES_WIDER_THAN_MIDDLE::MIDDLE_MIDDLE_COMPRESSION_PRESSURE::CENTER_MIDDLE::BALANCE_LEFT_HEAVY::DIST_SPLIT::PTYPE_DYNAMIC_DOMINANT::WSLOT_WORLD_050::TOPONAME_MEDUSA
```

Origin weight validation:

```text
result      MISS
origin->out S2 score=117 -> D3 S4
totals      structural=206 dynamic=217 DYNAMIC_DOMINANT
read        dominant outgoing lane came from a different pressure seat
```

## Boundary Rule

If the current draw has no next draw yet:

```text
outgoing_motion = None
outgoing_contract = OPEN_BOUNDARY_NO_NEXT_DRAW
motion_state = BOUNDARY_UNKNOWN
motion_archetype = BOUNDARY_UNKNOWN
```

This prevents the script from pretending to know an outgoing event before the next draw exists.

## Draw Singularity Lens

The Serenity Draw Singularity books and scripts clarified the missing layer.

The old question was:

```text
pressure authority
-> resolution bias
-> collision point
```

The audit showed that this was not enough.
Many misses were not random failures.
They were branch-selection problems inside a measurable preference field.

The new layer is:

```text
pressure authority
-> Draw Singularity Lens
-> pre-collision preference field
-> branch selector
-> collision point
```

Draw Singularity Lens answers:

```text
What named motion problem is alive before the branch is selected?
```

It is not a number pick.
It is not a memory shortcut.
It is the named motion problem formed from:

```text
previous draw order
current draw order
incoming sorted body
current pressure world
pressure authority
resolution bias
motion state
motion archetype
outgoing contract
branch universe
```

## DS Identity

The IIW-native DS identity has three depths.

Family:

```text
EDGE_BRANCH_SINGULARITY
HINGE_BRANCH_SINGULARITY
CENTER_MIXED_SINGULARITY
MIXED_BRANCH_SINGULARITY
UNMEASURED_BRANCH_SINGULARITY
```

Family names the branch universe.

Subfamily:

```text
topology name
base pressure world
pressure center
pressure balance
pressure distribution
authority seat
authority origin
```

Example:

```text
MEDUSA::DYNAMIC_DOMINANT::MIDDLE::RIGHT_HEAVY::SPLIT::AUTH_S4::INCOMING_MOTION
```

Subfamily names the pressure-world authority room.

Internal profile:

```text
motion state
motion archetype
transfer
incoming draw sign
outgoing draw sign
dominant incoming draw lane
dominant outgoing lane
resolution bias
preference universe
```

Example:

```text
COUNTER_ROTATION::PRESSURE_TRANSFER::HYBRID_COUNTER::IN_MMMMP::OUT_NNNNN::INLANE_D3::OUTLANE_NONE::BIAS_EDGE_BIAS::PREF_UNMEASURED
```

Internal profile is the exact room identity.

For audits, the script also creates a compressed selector profile:

```text
motion state
motion archetype
transfer
resolution bias
preference universe
```

This prevents the branch audit from collapsing into low sample too early.

## DS Caste Patterns

Draw Singularity Lens records lane caste patterns for both draw and sorted motion.

It stores:

```text
incoming_draw_caste_pattern
incoming_draw_caste_side_pattern
outgoing_draw_caste_pattern
outgoing_draw_caste_side_pattern
incoming_sorted_caste_pattern
incoming_sorted_caste_side_pattern
outgoing_sorted_caste_pattern
outgoing_sorted_caste_side_pattern
```

The caste-side pattern keeps the exact signed strength language.

Example:

```text
-FIGHTER:LOW|-GRUNT:HIGH|-DARK_PRIESTESS:LOW|-FALSE_QUEEN:LOW|+KING:HIGH
```

This is the bridge between:

```text
broad motion family
```

and:

```text
strict exact lane behavior
```

## DS Branch Audit

The new audit level is:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --branch-selector-audit --branch-selector-level 5 --limit 20
```

Level 5 uses:

```text
preference universe
DS family
DS subfamily
compressed DS selector profile
authority seat
authority origin
```

It does not use the full internal profile as the audit key.
The full internal profile remains in the packet and technical draw address for exact-room study.

Audit result from `2015-10-07`:

```text
Historical draws       577
Skipped draws          792
Selector keys          57
Selector level         5
Status counts          LOW_SAMPLE 7 | UNSTABLE 16 | SPLIT 8 | PROMISING 21 | PROVEN 5
```

This is a major improvement over the first raw DS attempt:

```text
raw full-profile DS keys: 435
low sample rooms:        412
```

The compressed DS selector profile keeps the rooms learnable.

## Current Meaning

The audit now says:

```text
Level 2 was useful but broad.
Level 3 and Level 4 were too raw and too specific.
Draw Singularity Level 5 compresses the right fields into reusable motion-problem rooms.
```

This is the current clean read:

```text
Pressure World tells where force lives.
Pressure Authority tells which source has control.
Draw Singularity tells what motion problem is alive.
Preference Field tells which branches are legal.
Branch Selector learns which branch wins.
Collision Point records where the motion terminates.
```

Saved audit JSON:

```text
Books of The Lotto\Books Of Complextity\branch_selector_audit_level_5_draw_singularity_2015-10-07.json
```

## World Accuracy Profiles

World Accuracy Profiles answer:

```text
Inside each named topology world, what field actually improves branch selection?
```

This audit exists because different worlds do not fail the same way.

Medusa is not Lumina.
Lumina is not Suzuka.
Suzuka is not Artoria.

The clean read is:

```text
world
-> branch distribution
-> legal preference field
-> best current-draw discriminator
-> world status
-> action
```

Command:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --world-accuracy-audit --limit 15
```

Saved JSON:

```text
Books of The Lotto\Books Of Complextity\world_accuracy_audit_2015-10-07.json
```

Audit result:

```text
Historical draws       577
Skipped draws          792
Worlds                 12
Status counts          TRUE_SPLIT_WORLD 3
                       WORLD_NEEDS_NEW_DISCRIMINATOR 4
                       WORLD_FIXABLE_WITH_DISCRIMINATOR 2
                       WORLD_HAS_WEAK_DISCRIMINATOR 3
```

The audit tests current-draw fields only.
It does not use future numbers as a discriminator.

Tested fields include:

```text
preference_universe
DS family
DS selector profile
authority seat
authority origin
pressure center
pressure balance
pressure distribution
map pressure type
dominant pressure seat
pressure shape
burden gauge shape
motion state
motion archetype
transfer
resolution bias
incoming draw sign
dominant incoming draw lane
incoming draw caste side pattern
draw face family
turn lanes
set relation
middle pressure
edge pressure
pressure fusion
```

## Anti-Cheating Rule

The first version let tiny high-accuracy pockets look like world-level fixes.
That was wrong.

The corrected audit separates:

```text
world-level discriminator
```

from:

```text
narrow micro-pocket
```

A discriminator must have meaningful coverage before it can be treated as a world fix.

This prevents:

```text
3 of 3 hit
```

from pretending to be:

```text
the world is solved
```

Low-coverage perfect fields are kept as micro-pocket evidence, not promoted to world law.

## Current World Cards

Medusa:

```text
appearances 218
status      TRUE_SPLIT_WORLD
branches    S1 57 | S5 53 | S4 51 | S2 32 | S3 25
best field  ds_selector_profile
rate        51.83%
coverage    100%
read        true split world; DS profile helps but does not solve it yet
action      keep DS selector profile, then find a deeper branch-side discriminator
```

Lumina:

```text
appearances 109
status      TRUE_SPLIT_WORLD
branches    S1 38 | S5 31 | S4 15 | S2 13 | S3 12
best field  ds_selector_profile
rate        51.38%
coverage    100%
read        structural gap world still splits between edge repair paths
action      keep DS selector profile, inspect geometry-side discriminator next
```

Suzuka:

```text
appearances 51
status      WORLD_NEEDS_NEW_DISCRIMINATOR
branches    S5 19 | S2 13 | S1 13 | S4 3 | S3 3
best field  motion_archetype
rate        62.75%
coverage    100%
read        core escape world; motion archetype separates some outcomes but not enough
action      add a Suzuka-specific discriminator around core pressure versus edge escape
```

Karna:

```text
appearances 34
status      TRUE_SPLIT_WORLD
branches    S1 12 | S4 9 | S5 9 | S2 3 | S3 1
best field  ds_selector_profile
rate        64.71%
coverage    100%
read        split world with useful DS profile lift, but not solved
action      use DS selector profile and inspect hinge/edge handoff
```

Circe:

```text
appearances 32
status      WORLD_NEEDS_NEW_DISCRIMINATOR
branches    S5 12 | S1 7 | S2 6 | S4 5 | S3 2
best field  ds_selector_profile
rate        59.38%
coverage    100%
read        endpoint world still needs another discriminator
action      inspect endpoint suppression versus tail release
```

Alcides:

```text
appearances 27
status      WORLD_HAS_WEAK_DISCRIMINATOR
branches    S5 10 | S1 9 | S4 4 | S2 3 | S3 1
best field  ds_selector_profile
rate        70.37%
coverage    100%
read        DS profile gives a usable split between S1 and S5
action      promote DS selector profile as a candidate discriminator, then walk-forward validate
```

Artoria:

```text
appearances 24
status      WORLD_FIXABLE_WITH_DISCRIMINATOR
branches    S1 12 | S5 8 | S2 2 | S3 2
best field  ds_selector_profile
rate        83.33%
coverage    100%
read        strongest current world fix; DS profile separates pressure transfer from tail release
action      walk-forward validate DS selector profile immediately
```

Nova:

```text
appearances 23
status      WORLD_HAS_WEAK_DISCRIMINATOR
branches    S1 8 | S5 8 | S3 3 | S4 3 | S2 1
best field  ds_selector_profile
rate        66.67%
coverage    91.3%
read        true edge mirror world; DS profile helps identify which edge wins
action      keep DS profile, inspect release/carry side separately
```

Rama:

```text
appearances 18
status      WORLD_NEEDS_NEW_DISCRIMINATOR
branches    S1 8 | S2 3 | S4 3 | S3 2 | S5 2
best field  ds_selector_profile
rate        61.11%
coverage    100%
read        mixed field still too loose
action      inspect mixed-family branch authority before tuning
```

Irisviel:

```text
appearances 15
status      WORLD_HAS_WEAK_DISCRIMINATOR
branches    S5 9 | S2 2 | S3 2 | S1 1 | S4 1
best field  ds_selector_profile
rate        66.67%
coverage    100%
read        endpoint/right-heavy retention world mostly wants S5
action      validate DS profile and endpoint authority together
```

Citrine:

```text
appearances 14
status      WORLD_NEEDS_NEW_DISCRIMINATOR
branches    S1 5 | S2 3 | S5 2 | S3 2 | S4 2
best field  ds_selector_profile
rate        57.14%
coverage    100%
read        secondary-family world, not enough separation yet
action      add a discriminator for secondary-family selection
```

Altera:

```text
appearances 12
status      WORLD_FIXABLE_WITH_DISCRIMINATOR
branches    S5 6 | S1 3 | S3 2 | S4 1
best field  ds_selector_profile
rate        75.0%
coverage    100%
read        edge world that improves cleanly with DS selector profile
action      walk-forward validate DS selector profile
```

## World Accuracy Doctrine

The worlds are now split into four practical classes.

```text
WORLD_FIXABLE_WITH_DISCRIMINATOR
  The world has a clear current-draw discriminator.
  Next step is walk-forward proof.

WORLD_HAS_WEAK_DISCRIMINATOR
  The world has a useful discriminator, but it is not strong enough for live trust.
  Next step is refine and validate.

TRUE_SPLIT_WORLD
  The world is genuinely branching.
  Next step is find the missing branch-side discriminator.

WORLD_NEEDS_NEW_DISCRIMINATOR
  Existing fields do not explain enough.
  Next step is add a new world-specific field, not force the current rule.
```

Current best field:

```text
DS selector profile is the strongest broad discriminator across most worlds.
```

But the important correction is:

```text
DS selector profile does not solve every world.
It tells us where the next missing field lives.
```

## Walk-Forward Audit

Walk-Forward Audit is the proof layer.

Discovery audits can use historical outcomes to find possible laws.
Walk-forward cannot.

The rule is:

```text
For each draw:
1. Build a live-safe key from previous/current information only.
2. Look backward at prior matching keys only.
3. If enough prior cases exist, choose the prior dominant branch.
4. Then compare against the next draw.
5. Add the current result to memory only after scoring.
```

This means the next draw is used only as the answer key.
It is not allowed into the prediction key.

Command:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --walk-forward-audit --walk-forward-level 2 --walk-forward-min-sample 3 --limit 15
```

Saved JSON:

```text
Books of The Lotto\Books Of Complextity\walk_forward_audit_level_1_live_safe_2015-10-07.json
Books of The Lotto\Books Of Complextity\walk_forward_audit_level_2_live_safe_2015-10-07.json
Books of The Lotto\Books Of Complextity\walk_forward_audit_level_3_live_safe_2015-10-07.json
```

## Live-Safe Key

The live-safe walk-forward key deliberately avoids leak-prone fields.

It does not use:

```text
outgoing transfer
outgoing motion archetype
future branch finding
next draw motion
full DS discovery profile
```

Instead it rebuilds a safe pressure read from:

```text
INCOMING_MOTION
GAP_STRUCTURE
MIDDLE_COMPRESSION
EDGE_IMBALANCE
HINGE_TRAP
```

It excludes:

```text
TRANSFER_REVERSAL
```

because transfer reversal depends on outgoing/current-to-next behavior.

Walk-forward levels:

```text
LEVEL 1
  topology only

LEVEL 2
  live-safe exact world
  live-safe authority seat
  live-safe authority origin

LEVEL 3
  level 2
  incoming draw sign
  dominant incoming draw lane
  draw face family

LEVEL 4
  level 3
  pressure shape
  body relation
  middle pressure
```

## Walk-Forward Result

Run window:

```text
from 2015-10-07 through latest available draw
minimum prior sample: 3
```

Level 1:

```text
total cases      1368
predicted cases  1309
coverage         95.69%
branch hits      383 / 1309 = 29.26%
family hits      725 / 1309 = 55.39%
```

Level 2:

```text
total cases      1368
predicted cases  1076
coverage         78.65%
branch hits      299 / 1076 = 27.79%
family hits      575 / 1076 = 53.44%
```

Level 3:

```text
total cases      1368
predicted cases  1
coverage         0.07%
branch hits      0 / 1 = 0.0%
family hits      1 / 1 = 100.0%
```

## Walk-Forward Meaning

The honest result:

```text
Discovery found real structure.
Walk-forward says the current live-safe branch selector is not accurate enough yet.
```

Level 1 is broad enough to fire but too blunt.
It mostly learns the majority branch of a topology world.

Level 2 is more technical, but the added live-safe world/authority fields do not improve branch accuracy yet.

Level 3 is too specific.
It starves the system of prior samples.

Therefore:

```text
Do not promote DS branch discovery into live trust yet.
```

The current system is better at:

```text
family direction
```

than:

```text
exact branch seat
```

That matters because family hit rates are around the mid-50s while exact branch hit rates are around the high-20s.

## Walk-Forward World Notes

Level 2 world examples:

```text
Artoria
  predicted 67 / 81
  branch hit 37.31%
  family hit 65.67%

Nova
  predicted 93 / 110
  branch hit 30.11%
  family hit 62.37%

Rama
  predicted 10 / 16
  branch hit 60.0%
  family hit 60.0%
  low sample, do not overtrust

Alcides
  predicted 32 / 37
  branch hit 15.62%
  family hit 62.5%

Lumina
  predicted 481 / 535
  branch hit 26.82%
  family hit 53.01%

Medusa
  predicted 173 / 219
  branch hit 27.17%
  family hit 49.71%
```

This changes the priority.

Earlier discovery said:

```text
Artoria and Altera looked fixable.
```

Walk-forward says:

```text
Artoria has useful family direction but not proven exact branch accuracy.
Altera did not hold strongly enough in live-safe branch form.
```

So the next refinement should focus on:

```text
turning family direction into exact branch seat
```

not pretending the exact branch selector is already solved.

## Next Accuracy Work

The next missing layer is probably not another broad world label.

It is a live-safe branch-side discriminator.

The candidates to test next:

```text
edge polarity
hinge polarity
core escape pressure
endpoint suppression
draw face side
incoming caste side reduced to dominant lane only
left/right gap imbalance as a signed field
family-first prediction before seat prediction
```

The audit now proves the work order:

```text
1. Predict branch family first.
2. Only then predict exact seat inside that family.
3. Reject exact-seat calls when the prior room only proves family direction.
```

That is the honest path toward higher accuracy without cheating ourselves.

## Family-First Walk-Forward

Family-First Walk-Forward changes the scoring order.

The old walk-forward tried to call the exact branch seat directly.
That overclaims because the audit already showed the system is stronger at family direction than exact seat selection.

Family-First uses this order:

```text
1. Build the live-safe key from prior/current information only.
2. Look backward at prior matching rooms only.
3. Predict the branch family first.
4. If family strength is not high enough, abstain.
5. If family is strong enough, test exact seat strength inside that family.
6. If exact seat strength is not high enough, keep the family call but mark exact seat unstable.
7. Score against the next draw only after the call is made.
```

This keeps the system honest:

```text
family direction can be useful
exact branch seat must be proven separately
```

Command examples:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --family-first-walk-forward-audit --walk-forward-level 1 --walk-forward-min-sample 3 --family-first-threshold 50 --exact-branch-threshold 65 --limit 15

py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --family-first-walk-forward-audit --walk-forward-level 2 --walk-forward-min-sample 3 --family-first-threshold 50 --exact-branch-threshold 65 --limit 15

py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --family-first-walk-forward-audit --walk-forward-level 2 --walk-forward-min-sample 3 --family-first-threshold 55 --exact-branch-threshold 70 --limit 15
```

Saved JSON:

```text
Books of The Lotto\Books Of Complextity\family_first_walk_forward_level_1_f50_e65_2015-10-07.json
Books of The Lotto\Books Of Complextity\family_first_walk_forward_level_2_f50_e65_2015-10-07.json
Books of The Lotto\Books Of Complextity\family_first_walk_forward_level_2_f55_e70_2015-10-07.json
```

## Family-First Results

Level 1, family threshold 50%, exact threshold 65%:

```text
total cases      1368
family calls     1224 / 1368 = 89.47%
family hits      694 / 1224 = 56.7%
exact calls      112 / 1368 = 8.19%
exact hits       33 / 112 = 29.46%
```

Level 2, family threshold 50%, exact threshold 65%:

```text
total cases      1368
family calls     979 / 1368 = 71.56%
family hits      548 / 979 = 55.98%
exact calls      372 / 1368 = 27.19%
exact hits       106 / 372 = 28.49%
```

Level 2, family threshold 55%, exact threshold 70%:

```text
total cases      1368
family calls     715 / 1368 = 52.27%
family hits      399 / 715 = 55.8%
exact calls      140 / 1368 = 10.23%
exact hits       41 / 140 = 29.29%
```

Status evidence:

```text
Level 1 f50/e65
  FAMILY_PREDICTED_EXACT_UNSTABLE: 1091
  FAMILY_AND_EXACT_PREDICTED: 112

Level 2 f50/e65
  FAMILY_PREDICTED_EXACT_UNSTABLE: 534
  FAMILY_AND_EXACT_PREDICTED: 372

Level 2 f55/e70
  FAMILY_PREDICTED_EXACT_UNSTABLE: 528
  FAMILY_AND_EXACT_PREDICTED: 140
```

The main finding:

```text
Family-first improves honesty, not exact-seat accuracy.
```

It proves the system often has enough prior evidence to say:

```text
this room leans toward this branch family
```

but not enough to safely say:

```text
this exact seat is the live destination
```

That is why `FAMILY_PREDICTED_EXACT_UNSTABLE` is valuable.
It is not a failure label.
It is the system refusing to overstate the exact branch.

## Family-First Meaning

The strongest conclusion is:

```text
branch family is a real intermediate layer
exact branch seat still needs another discriminator
```

The stricter run reduced exact calls from 372 to 140, but exact hit rate only moved from 28.49% to 29.29%.

That means the missing accuracy is not solved by raising thresholds.
The missing accuracy is inside the branch split itself.

The next question is no longer:

```text
which world is strongest?
```

The next question is:

```text
inside a proven family lean, what decides S1 over S5, S2 over S4, or edge over hinge?
```

Until that discriminator is found, the live-safe doctrine is:

```text
Call family when prior evidence is strong enough.
Mark exact seat unstable unless exact-seat evidence is separately proven.
```

## Truth Control

Truth Control prevents Seat Taxonomy from turning explanation into false certainty.

The script now separates every major claim into authority levels:

```text
OBSERVED_FACT
  Directly read from the current or previous/current draw.

LIVE_SAFE_INFERENCE
  Computed from current/prior information only.

HISTORICAL_FACT
  Known only because the next historical draw exists.

HISTORICAL_EXPLANATION
  Explains how the known next draw resolved.

DISCOVERY_ONLY
  Learned from historical fields and not trusted live by itself.

UNPROVEN
  Pattern exists but exact answer authority is not proven.

NO_CALL
  Not enough live-safe evidence to make the claim.
```

The most important rule:

```text
Seat Taxonomy may describe exact branch history.
Seat Taxonomy may not treat exact branch history as a live answer unless prior-only memory proof upgrades it.
```

Live-safe fields:

```text
current draw
sorted body
incoming motion
current pressure
live-safe pressure context
pressure origin from:
  INCOMING_MOTION
  GAP_STRUCTURE
  MIDDLE_COMPRESSION
  EDGE_IMBALANCE
  HINGE_TRAP
```

Blocked from live prediction:

```text
outgoing_contract
outgoing motion state
outgoing motion archetype
branch_selector observed result
collision validation result
transfer reversal built from current-to-next motion
```

So the script can still explain:

```text
why S3 moved
why S1 won historically
why a family split happened
```

but it must label those reads correctly:

```text
historical explanation
not live-safe proof
```

## Conditional Motion Memory

Conditional Motion Memory is the bridge between foundation and prediction.

It is not answer lookup.
It is not brute force.

It asks:

```text
When this kind of live-safe room appeared before,
how did it resolve?
```

The memory condition is built from current/prior-safe fields:

```text
topology world
exact pressure world key
authority seat
authority origin
pressure type
pressure center
pressure balance
pressure distribution
dominant pressure seat
incoming draw sign
dominant incoming draw lane
incoming draw family
incoming energy class
face family
body relation
middle pressure
edge pressure
burden seat/state
dominant origin seat
```

The memory outcome records what happened historically:

```text
actual outgoing branch
actual outgoing family
actual outgoing draw lane
actual outgoing motion
outgoing flow
outgoing transfer
outgoing sign pattern
```

That gives the real motion sentence:

```text
current live-safe room
+ prior matching rooms
+ current pressure/body/motion
= lawful historical tendency
```

## Conditional Memory Result

Conditional Memory now has two exports.

Level 2 export:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --conditional-motion-memory --conditional-memory-level 2 --walk-forward-min-sample 3 --family-first-threshold 50 --exact-branch-threshold 65 --exact-proven-threshold 80 --limit 20
```

Hierarchical Level 2-5 export:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Seat_Taxonomy.py" --from-date 2015-10-07 --hierarchical-conditional-motion-memory --walk-forward-min-sample 3 --family-first-threshold 50 --exact-branch-threshold 65 --exact-proven-threshold 80 --limit 20
```

Saved JSON:

```text
Books of The Lotto\Books Of Complextity\conditional_motion_memory_level_2_2015-10-07.json
Books of The Lotto\Books Of Complextity\hierarchical_conditional_motion_memory_levels_2_5_2015-10-07.json
```

Level 2 result:

```text
total cases       1368
boundary skipped  1
scenario count    130

status counts:
  FAMILY_ONLY_EXACT_UNSTABLE  58
  LOW_SAMPLE                  56
  FAMILY_UNSTABLE             8
  EXACT_PROMISING             8

truth authority:
  HISTORICAL_FAMILY_FIELD   58
  HISTORICAL_EXACT_MOMENT   56
  HISTORICAL_SPLIT_FIELD    8
  HISTORICAL_EXACT_PATTERN  8
```

Hierarchical Level 2-5 result:

```text
total cases       1368
boundary skipped  1
scenario count    4207

status counts:
  FAMILY_ONLY_EXACT_UNSTABLE  60
  LOW_SAMPLE                  4130
  FAMILY_UNSTABLE             8
  EXACT_PROMISING             9

truth authority:
  HISTORICAL_FAMILY_FIELD   60
  HISTORICAL_EXACT_MOMENT   4130
  HISTORICAL_SPLIT_FIELD    8
  HISTORICAL_EXACT_PATTERN  9
```

Level summaries:

```text
Level 2
  scenarios 130
  broad repeated world/authority memory

Level 3
  scenarios 1341
  motion/face memory

Level 4
  scenarios 1368
  body/pressure exact moment memory

Level 5
  scenarios 1368
  fusion/burden/turn exact moment memory
```

The correction:

```text
Level 3/4/5 are not useless.
They are exact historical moment evidence.
```

They do not automatically create a live exact answer by themselves, but they do tell the system:

```text
this exact kind of motion/body moment happened before
and this is how it resolved
```

So the clean doctrine is:

```text
Level 2 = repeated world field
Level 3 = motion/face evidence
Level 4 = body/pressure evidence
Level 5 = exact historical moment evidence
```

## Conditional Memory Meaning

The new memory gives the system natural understanding without cheating.

Example shape:

```text
World: Altera
Authority: S1 / INCOMING_MOTION
Pressure type: DYNAMIC_DOMINANT
Body: compressed or split

Historical outcomes:
  EDGE_FAMILY wins most often
  exact seat is split between S1 and S5

Live use:
  family can be read
  exact branch is unstable
```

This is the exact distinction the system needs.

It can now say:

```text
This room historically wants EDGE.
But it has not proven S1 over S5.
```

instead of pretending:

```text
S1 is the answer.
```

Current foundation result:

```text
Conditional Motion Memory reduces brute force by using history as motion evidence.
Truth Control prevents historical evidence from being mislabeled as guaranteed live certainty.
The next live read should reflect current draw evidence through the Level 2-5 memory chain.
```

## Conditional Memory Resolver

Conditional Memory Resolver is the bridge from memory theory into live reading.

Script:

```text
Scripts of the lotto\Foundation Scripts\Conditional_Memory_Resolver.py
```

Command:

```powershell
py -3 -B "Scripts of the lotto\Foundation Scripts\Conditional_Memory_Resolver.py" --latest
```

Saved latest JSON:

```text
Books of The Lotto\Books Of Complextity\conditional_memory_resolver_latest.json
```

The resolver does this:

```text
1. Build the current Seat Taxonomy packet.
2. Build live-safe memory keys for Level 2, Level 3, Level 4, and Level 5.
3. Search hierarchical conditional memory.
4. Return every matched room.
5. Separate repeated field memory from exact historical moment memory.
6. Produce the outgoing outcome field from the matched rooms.
```

Latest resolver example:

```text
date:
  2026-06-17

live room:
  Suzuka
  DYNAMIC_DOMINANT
  CORE LEFT_HEAVY SPLIT

authority:
  S1 INCOMING_MOTION

incoming:
  DROP_DOMINANT_DIRECTED_MOTION_D3
  sign ----+

memory matches:
  L2 match
    n=39
    HISTORICAL_FAMILY_FIELD
    EDGE_FAMILY 56.41%
    branch S5 41.03%

  L3 match
    n=1
    HISTORICAL_EXACT_MOMENT
    EDGE_FAMILY 100.0%
    branch S1 100.0%

  L4 miss
  L5 miss
```

The read:

```text
History has a repeated Suzuka Level 2 field.
History also has one exact Level 3 moment.
History does not yet have this exact Level 4/5 room.
```

Outcome field:

```text
family:
  EDGE_FAMILY 57.5%
  HINGE_FAMILY 35.0%
  CENTER_FAMILY 7.5%

branch:
  S5 40.0%
  S2 22.5%
  S1 17.5%
  S4 12.5%
  S3 7.5%

flow:
  RETENTION 75.0%
  RELEASE 25.0%

transfer:
  HYBRID_COUNTER 65.0%
  CARRY_PRESSURE 17.5%
```

This is the intended shape.

The resolver does not ask:

```text
what discriminator should we invent?
```

It asks:

```text
what memory room does this current motion belong to?
what did that room do before?
how deep does the match go?
```

## Synthetic Memory Direction

Synthetic memory should not become a handwritten script.

The correct structure is:

```text
generator script
  creates fake IIW draw sequences

Seat Taxonomy
  converts fake sequences into motion/body/world rooms

memory writer
  stores generated rooms as JSONL or JSON shards

Conditional Memory Resolver
  searches official memory first
  searches synthetic memory second
  reports both separately
```

The memory itself should be data, not code.

That prevents ambiguity:

```text
official historical memory = what actually happened
synthetic memory = generated coverage of possible motion rooms
current draw = current truth
```

Synthetic memory is useful because it can fill the missing Level 4/5 address space.
It should expand coverage, not override official history.
