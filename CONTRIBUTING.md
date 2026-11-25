# Contributing

The spec belongs to everyone who builds on it. Anyone may propose a change.

## Proposing a change

1. **Open an issue first.** Say what you want to change and why, and which
   implementation needs it. Small fixes (typos, broken links, wording that
   doesn't change meaning) can skip this and go straight to a pull request.
2. **Send a pull request** that changes the spec pages. Keep it to one
   change. Add a line to [CHANGELOG.md](CHANGELOG.md).
3. **Wire changes need two implementations.** A change to anything on the
   wire or in an API (a message, a field, a capability, a format) lands once
   two implementations agree on it, and at least one of them has built it.
   Until then it can sit in the spec marked "proposal".

## The rules every change follows

- **Additive only.** New messages, fields and capabilities are added beside
  the old ones and gated by a capability bit or a version. A machine that
  doesn't know them keeps working.
- **Old versions are never dropped.** A newer client keeps playing with an
  older host, and a newer host keeps serving older clients. A security fix
  may refuse one vulnerable message, never a whole version, and says so.
- **The legacy game protocol stays untouched.** Delta never changes what a
  machine without Delta sees.
- **Numbers come from the registry.** Platform keys, capability bits,
  message types and ports are assigned in [registry.md](registry.md) and
  [registry.json](registry.json), by pull request. Never pick a number in
  your own build and send it: ask first, and send 0 (unknown) until it's
  assigned. Numbers are never reused.

## Numbers

The registry ([registry.md](registry.md), [registry.json](registry.json))
belongs to this repository.

- **Ask by pull request.** A new platform number, capability bit, message
  type or any other number is a pull request that adds it to both
  registry.md and registry.json, with what it's for and who uses it. An
  issue first is fine if you'd rather ask.
- **The spec's maintainers approve it** ([MAINTAINERS.md](MAINTAINERS.md)).
  The number is assigned once the pull request is merged, not before.
- **Never reused.** A number stays with what it was given to, even if that
  platform's port stops or the feature is retired.
- **Wire constants never change.** A label, magic or byte layout that is
  already on the wire stays as it is, even where it names a project
  (registry.md, "Labels").
- **`chupa-*` wire IDs are Chupathingy's.** They name revisions of
  Chupathingy's own code and are listed for reference only. Another
  implementation's host leaves the tag out, or writes a layout 2 tag with
  its own project number (registry.md, "Projects";
  [ports.md](ports.md#if-you-host-games-from-your-port)).

## Implementation notes

The spec pages describe the formats and behavior every implementation
shares. How one implementation does it (its files, settings, menus, tests)
belongs in that implementation's own documentation, which these pages may
link to. Chupathingy's is
[delta-implementation.md](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/delta-implementation.md).

## License

By contributing, you agree that your contribution is licensed under
[CC BY 4.0](LICENSE), and that code samples, hex examples and
`registry.json` changes are also offered under the MIT License. Changes to
the reference client in `reference/` are MIT.
