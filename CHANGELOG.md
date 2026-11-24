# Changelog

## Unreleased

- HOST_RULES flag 0x10, `air_turn_aim`: a shot fired while turned around in
  mid-air goes where the player aims (the "180 glitch" fixed), off by
  default ([peer.md](peer.md#host-rules), [registry.md](registry.md#host-rules-flags)).
- The internet listing's flags and 8-byte stamp, shared with OpenCE's
  builds, are in the registry ([registry.md](registry.md#internet-listing),
  registry.json's `internet_listing`), with how to ask for one. Flag 64
  and stamp byte 1 are reserved for Content Evolved, pending its pull
  request.
- [ports.md](ports.md#license) said the reference client was GPL-3.0; it
  is MIT, as reference/LICENSE says.
- [federation.md](federation.md#plain-accounts): a network may run plain
  accounts without certificates. Their names show as plain names;
  certificate-checked names are a level above, with the verified mark.
- [forge.md](forge.md): Forge layout files (`.hmv`, `HFRG`, versions 1 to
  7), byte by byte, with every check a reader makes, so any client can
  read and write them. Network Forge is noted; its wire format comes
  later.

## 2026-11-19

- Platform floors, which landed in Chupathingy after the spec moved here: the
  signed table's `platform_floors` ([versioning.md](versioning.md#platform-floors)),
  and a Platform floors section in [registry.md](registry.md#platform-floors)
  and registry.json (at most 64 rows, none signed yet).
- The game list's `family` values include `pack` (an Xbox map pack's map)
  and `mcc` (an MCC map) ([list.md](list.md)).
- The registry says which copy Chupathingy's `tools/test_delta_registry.py`
  checks: the game's own, kept in step with this one, not this
  repository's yet.

## 2026-11-17

- Delta is the name of the shared spec; Chupathingy is one implementation
  ([README.md](README.md), [federation.md](federation.md)). The name is
  open to change.
- The implementations table lists delta-server (a reference node, draft)
  and Chupathingy's Social.
- The **Chupathingy notes** paragraphs moved to Chupathingy's own
  documentation; notes about one implementation stay out of the spec pages
  ([CONTRIBUTING.md](CONTRIBUTING.md)).
- Removed a stale note in [social/platform.md](social/platform.md): the
  site lists `dreamcast` (22) now.
- The social pages' implementation notes (chat, clans, friends, invites,
  parties, presence, voice) moved out too. The game's went to Chupathingy's
  `docs/delta-implementation.md`; the site's went to the site's own docs.
  Two sentences that are about the spec stay as plain text: the legacy chat
  entries' source ([social/chat.md](social/chat.md)) and what "ranks" means
  ([social/clans.md](social/clans.md)).
- The registry belongs to this repository: numbers by pull request,
  approved by the spec's maintainers, never reused; `chupa-*` wire IDs stay
  Chupathingy's ([CONTRIBUTING.md](CONTRIBUTING.md#numbers)).
- `server_badge` (16): built, keys not issued. `mcc_maps` (24): a room-wide
  content gate plus HOST_NUMBER, with no map identity on the wire.
- Network versions 43 and 44 say who announces them; 44 is announced through
  the signed table (Chupathingy's built-in number is 32).
- The Dreamcast's (22) policy row in [peer.md](peer.md#platform-policy).
- New registry sections for numbers that were only in the pages or the code:
  platform policy, platform key flags, messages, map families, host rules
  flags, game modes, permissions, device certificate flags and
  capabilities, report reasons, moderation actions and labels. Platform
  statuses say "in use" rather than "ours".
- The reference client has `DREF_CAP_LOBBY_READY` (26).

## 2026-11-16

- The spec moved here from the `docs/delta/` folder of
  [ChupathingyCE/chupathingyce](https://github.com/ChupathingyCE/chupathingyce),
  with its history, back to its first page (`docs/network-versioning.md`,
  then `docs/delta.md`, 2026-10-05). It is given to the wider community
  under CC BY 4.0.
- The reference client moved here too, into [reference/](reference/), and
  is now MIT.
- Added the federation proposal ([federation.md](federation.md)).
- The example advertisement in [ports.md](ports.md) is 26 bytes, as
  `conformance.py` expects (it had one byte too many).
- Links into the game's repository are now full URLs, and notes about
  Chupathingy's own implementation are marked **Chupathingy notes**.
- Added [CONTRIBUTING.md](CONTRIBUTING.md) and [MAINTAINERS.md](MAINTAINERS.md).
- Added Delta Social ([social/](social/README.md), draft): friends,
  presence, invites, parties, party chat, chat, voice, clans, platforms and
  moderation.
