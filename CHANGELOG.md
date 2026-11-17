# Changelog

## 2026-11-17 (registry)

- The registry belongs to this repository: numbers by pull request,
  approved by the spec's maintainers, never reused; `chupa-*` wire IDs stay
  Chupathingy's ([CONTRIBUTING.md](CONTRIBUTING.md#numbers)).
- `server_badge` (16): built, keys not issued. `mcc_maps` (24): a room-wide
  content gate plus HOST_NUMBER, with no map identity on the wire.
- Network versions 43 and 44 say who announces them; 44 is announced through
  the signed table (the number built into the code is 32).
- The Dreamcast's (22) policy row in [peer.md](peer.md#platform-policy).
- New registry sections for numbers that were only in the pages or the code:
  platform policy, platform key flags, messages, map families, permissions,
  device certificate flags and capabilities, report reasons, moderation
  actions and labels.
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
