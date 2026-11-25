# Changelog

## Unreleased

- Account marks: the device certificate's capabilities field keeps bits 0
  to 23 for capabilities, and its top byte holds marks the issuing network
  vouches for about the account. Mark 0x01000000 is `developer`. A mark
  grants nothing, counts only from a certificate that passed the verified
  names checks and chains to the root keys of a network the client knows,
  and a certificate that carries one lasts 2 days. Unknown marks are
  ignored, so format 1 stays ([link.md](link.md#device-identity),
  [registry.md](registry.md#device-certificates), registry.json's
  `device_account_marks`, peer.md's "What shows").
- Project 3 is GulchCE (chester), for its hosts' layout 2 tags
  ([registry.md](registry.md#projects), registry.json's `projects`,
  `DREF_PROJECT_GULCHCE` in the reference code).
- Layout facts by network version: one section with everything a client
  handles differently for a host of each version from 11 to 45 (the game
  settings record's fixed fields, its size, options, local data and
  trailing bytes by version, the further options' bytes, the join request,
  the distributed header, unit state parts, messages added and dropped,
  and Content Evolved's row at 44), the same facts as data in
  `layouts.json`, and "Playing a range": how a client of another project
  uses them, the signed table and Delta's HELLO to join every host from 11
  to 45 ([versioning.md](versioning.md#layout-facts-by-network-version)).
  The signed table's 16 KB cap and its compact encoding are written down
  ([versioning.md](versioning.md#size-and-encoding)). The reference code
  gains `delta_layout.h` and `delta_layout.c` (MIT): the facts, a signed
  table's facts within the limits, and the record converted between any
  two layouts; `conformance.py` gains `layout`, `record` and `convert`.
- Hosts of other projects' code can host with Delta. The tag's layout 2
  names the host's project (a new registry table, Projects: 1 Chupathingy,
  which writes layout 1 alone; 2 Content Evolved) and that project's own
  version, in place of a wire. A client says HELLO to such a host and joins
  it by its network version alone, never by a wire; a reader of layout 1
  alone sees no tag and joins it by its number, as before. ports.md's
  missing "If you host games from your port" says what a port host writes,
  what it answers (WELCOME, ROSTER, LEGACY, BYE), the join mark it clears
  and waits on, the record it sends for each number, and what it never
  claims ([peer.md](peer.md#the-tag),
  [ports.md](ports.md#if-you-host-games-from-your-port),
  [registry.md](registry.md#projects), registry.json's `projects`).
  The reference client writes and reads it (`dref_advert_write_project`,
  `dref_advert_read`'s `project`), writes ROSTER (`dref_roster_write`) and
  reads nothing from a Content Evolved modded game's bytes (`modded`);
  `dref_join_mark_read` reads and clears the join mark on a host's side.
  `conformance.py advert` passes a valid layout 2 tag (and fails one
  beside the old layout's flag, major and wire ID), `check --host`
  checks what a port's host sends, and `listen --project` stands in for a
  port host.
- Listing stamp byte 2, `map_source`, is Content Evolved's: its map source
  ([registry.md](registry.md#listing-stamp)).

- Content Evolved's numbers, at Watanoge's request: a version word of
  0xFF00 to 0xFFFF in the advertisement is a Content Evolved modded game,
  whose 26 reserved bytes are all Content Evolved's; listing flag 64
  (`modded`) and stamp byte 1 (`mod_version`) are in use by it. The
  advertisement's stock layout is in the registry too, with the MCC
  network protocol's flag 0x08 and byte 4, which were missing
  ([peer.md](peer.md#the-advertisement), [registry.md](registry.md#lan-advertisement),
  registry.json's `advertisement`).
- `reference/loopback_host.sh --announce N` works with released servers:
  their local legacy table now has a row for the server's wire that
  announces N (joins 11 to 45), where an empty one left a 0.9.1a server at
  its built-in 41. `--wire` names the wire if the script can't read it
  from the server program ([ports.md](ports.md#testing-your-port)).
- Federation, proposal: a certificate's network is the one whose root key
  signed its issuer certificate, so no certificate changes and today's read
  as `chupathingy.org`; roots.json, the signed list of networks, local
  additions and removals, the offline check and what shows
  ([link.md](link.md#networks), [federation.md](federation.md)), with test
  vectors in [reference/federation_vectors.json](reference/federation_vectors.json).
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
- [ports.md](ports.md#version-rules-for-a-port) says louder that a Delta
  host sends the settings record of the older of its own number and the
  HELLO's, so HELLO can't raise it. In place of 0.9.1's example, how our
  hosts pick the number they announce: an MCC map's game, a pinned
  number, the signed table's row, or the built-in 41 (`chupa-41a`'s
  announce; 32 on a console) for a wire with no row. The built-in 41 is
  `chupa-41a`'s number, not the last release's row
  ([versioning.md](versioning.md#legacy-versions)).
- [list.md](list.md): hosts publish to the brokers and announce to the
  site, so the brokers alone show every public game and the site's list
  adds the extras. The whole announcement form, the withdrawal, the game
  list's first twelve fields, and how another client announces: its own
  `build` and `platform_key`, on change plus a 20-second keep-alive.
  The site's answers too: `ok <seconds>` and its refusals, withdrawal only
  from the announcing address, Bomb and co-op games only to clients that
  ask, and the name's limit.
- Platform numbers are per platform, not per project. Windows is Windows
  and Linux is Linux; a platform has its own number only where it has its
  own build (SteamOS, Legacy PC). A fork or
  another project uses its platform's number and tells itself apart by
  its build name and wire. The registry's For column is now First port. A web build gets a number like any other platform
  ([registry.md](registry.md#platforms), [ports.md](ports.md#the-short-version)).

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
