# Changelog

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
