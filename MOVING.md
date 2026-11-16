# What lives where

The spec moved here on 2026-11-16 from
[ChupathingyCE/chupathingyce](https://github.com/ChupathingyCE/chupathingyce),
with its history: `docs/network-versioning.md` and `docs/delta.md` (the
single page the spec started as, now `README.md`'s history), the
`docs/delta/` folder, and the reference client from `tools/delta-ref/`.

## This repository

| Files | What they are |
| --- | --- |
| `README.md`, `peer.md`, `versioning.md`, `list.md`, `stats.md`, `control.md`, `link.md`, `clients.md`, `security.md`, `ports.md`, `federation.md` | the spec (CC BY 4.0) |
| `registry.md`, `registry.json` | every assigned number |
| `reference/` | the reference client, its golden packets (`golden.h`), `conformance.py` and `loopback_host.sh` (MIT) |
| `social/` | Delta Social (draft) |
| `CONTRIBUTING.md`, `MAINTAINERS.md`, `CHANGELOG.md`, `LICENSE` | how the spec is kept |

## Chupathingy's repository

These belong to Chupathingy's implementation and stay in its repository:

| File | What it is |
| --- | --- |
| [`docs/delta-implementation.md`](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/delta-implementation.md) | how Chupathingy's own game and server implement the spec |
| [`docs/online.md`](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/online.md) | the players' page on playing online |
| `tools/delta_ref_capture/` | makes `golden.h` from the game's own code and checks `peer.md`'s hex examples against it |
| `tools/test_delta_ref.py`, `tools/test_delta_registry.py`, `tools/test_delta_docs.py` | the game's checks of the kit, of `registry.json` against its code, and of the pages' links |

The game's repository still has its own copies of `docs/delta/` and
`tools/delta-ref/` for now. Later they should point at this repository's
copies, with the game's checks run against them, so a change to the game's
wire shows up as a change to the spec.
