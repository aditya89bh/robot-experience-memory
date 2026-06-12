# Industrial validation datasets

Small deterministic JSONL fixtures for examples, benchmarks, and evaluation tests.
They are intentionally dependency-free and synthetic, but model realistic robot-cell
failure/recovery patterns.

## `cnc_tending.jsonl`

A CNC tending sequence with raw-stock loading, chuck confirmation, a coolant-induced
unload slip, a wipe recovery action, and successful unload retry.


## `pick_and_place.jsonl`

A pick-and-place sequence with vision localization, pose-uncertainty failure,
relocalization recovery, successful pick retry, and final placement.
