# Delta

Delta is an open network layer for Halo: the part of Halo online that the
original game never had. These pages are its specification. They are given
to the wider community, and anyone may build a client, server, port or tool
that speaks it.

This repository holds the spec only. It is separate from any
implementation.

## Two wires

Every Halo port already shares one thing: the game's own protocol (the
"legacy" protocol, versioned by a network number). Delta never replaces it.
It runs beside it:

1. **The game protocol**, unchanged. Every machine in a game speaks it, with
   or without Delta.
2. **Delta**, beside it: its own messages between the machines of a game
   (Delta Peer), and optional services for lists, stats, profiles and
   server control.

A game, port or server without Delta still plays with everyone: it just
doesn't get the extras.

## Who it's for

Any port, fork or community that wants its players in one player base:
desktop builds, console and handheld ports, dedicated servers, game lists,
stats sites and tools. Nothing in the spec depends on being any one
project, and nothing is secret but signing keys.

## Implementations

| Implementation | What it is | Status |
| --- | --- | --- |
| [Chupathingy](https://github.com/ChupathingyCE/chupathingyce) | the game (PC, Mac, Linux, Android, consoles) and its dedicated server | implements Peer, List, Stats, Control and Link |
| delta-server | a reference network: site, list, stats and accounts anyone can run | planned |
| yours | any port, fork or tool | welcome: see [ports.md](ports.md) and [CONTRIBUTING.md](CONTRIBUTING.md) |

Chupathingy's game repository checks itself against this spec: a test
there fails when [registry.json](registry.json) and the game's code
disagree, and the reference client's golden packets are checked against
the hex examples in [peer.md](peer.md). How Chupathingy implements the spec
(settings, menus, files) is on its own side:
[delta-implementation.md](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/delta-implementation.md).
Paragraphs marked **Chupathingy notes** in these pages describe that
implementation and are not part of the spec.

## Status

| Part | Status |
| --- | --- |
| Delta Peer | in use |
| Delta List | in use |
| Delta Stats | in use |
| Delta Control | in use |
| Delta Link | in use |
| Registry | in use; new numbers by pull request |
| Federation | proposal |
| Delta Social | draft; most of it in use, some parts proposed |

## For developers

Delta has one rule above all: **the player base stays whole.** The legacy
game protocol is the common ground. Delta starts beside it, and when a
capability changes the game itself, every part of Delta still falls back,
per machine, to the plain game protocol for a machine that doesn't share
it. A room-wide capability (one every machine must have) is on only while
every machine in the game has it.

Changes are additive. An old version is never dropped.

### The parts

Delta is one name for parts that cross different trust boundaries:

| Part | Between | What it is | Page |
| --- | --- | --- | --- |
| **Delta Peer** | machines in one game | Delta's own messages beside the game protocol: the handshake, capabilities, and the extras | [peer.md](peer.md) |
| **Delta List** | a host, and the site | announcing and listing games | [list.md](list.md) |
| **Delta Stats** | a host or player, and the site | end-of-game reports and the event stream | [stats.md](stats.md) |
| **Delta Control** | an admin or moderator, and a server | roles, commands, the control API, in-game moderation | [control.md](control.md) |
| **Delta Link** | a player or server, and the site | profiles, devices, linking with a code, clans | [link.md](link.md) |
| **Delta Social** | players, through the site and in one game | friends, presence, invites, parties, chat, voice, clans, moderation | [social/](social/README.md) |

"The site" in these pages is a network's web service: the other end of
Delta List, Stats and Link. Chupathingy's network runs one at
`stats.chupathingy.org`; [federation.md](federation.md) proposes how other
networks run their own.

The legacy number (the game protocol's network version) is not part of
Delta. Delta works around it: [versioning.md](versioning.md).

```
                   the legacy game protocol
  client  <====================================================>  host
     \\    Delta Peer (UDP 5160, inside the same tunnel)           //
      \\  <==================================================>    //
       \\                                                       //
        \\  Delta List / Stats / Link (HTTPS)       Delta List / Stats / Link
         `------------------->     the site     <--------------------'
                                      ^
                                      | Delta Link (server dials out)
                                      |
                              admin's browser  --- Delta Control --->  server
```

The game itself stays peer to peer: one machine hosts, the others join it,
over LAN or the internet tunnel. The site is optional for play: invites,
public listings and LAN work without it, and the site is never in the path
of a game.

### The pages

| Page | What it covers |
| --- | --- |
| [peer.md](peer.md) | Delta Peer, byte by byte: transport, handshake, capability registry, platform keys and policy, the wire format with real examples, the advertisement, the join mark, and every feature's messages |
| [versioning.md](versioning.md) | the legacy number, wire IDs and their ranges, the signed table, legacy compatibility, join reasons |
| [registry.md](registry.md) | every assigned number in one place: platforms, capability bits, wire IDs, network versions, ports (and [registry.json](registry.json)) |
| [list.md](list.md) | the game list: a host's fields, pings before joining |
| [stats.md](stats.md) | reports, the event batch, medals, map facts |
| [control.md](control.md) | server roles, accounts, the link to the site, shared ban lists |
| [link.md](link.md) | profiles, device identity, devices, the doorbell, clans |
| [clients.md](clients.md) | registering an app that signs players in on the site |
| [security.md](security.md) | how Delta treats hostile input, and where each part's checks are |
| [ports.md](ports.md) | a port's path to playing with everyone, with the reference client and its tools |
| [federation.md](federation.md) | proposal: other networks running their own accounts and servers, with names checked across all of them |
| [social/](social/README.md) | Delta Social (draft): friends, presence, invites and joins, parties, party chat, chat, voice, clans, platforms, moderation |
| [MOVING.md](MOVING.md) | what lives in this repository, and what stays with the game |

### How it meets everything else

- **Machines without Delta** see only the legacy protocol and number.
  Nothing changes for them.
- **The internet tunnel** carries Delta Peer's socket like the game's own,
  inside the same encryption.
- **A dedicated server** is a host that speaks Delta Peer, announces through
  Delta List, reports through Delta Stats, and is run through Delta Control
  and Delta Link.
- **Consoles** join as Delta Peer clients with their platform key, so hosts
  keep games to their limits unless their player opts in.
- **Halo Custom Edition 1.0.10** players are outside Delta. Nothing of them
  reaches Delta Peer or the legacy number.
- **The site** is the other end of Delta List, Stats and Link.

## Links

| Where | What |
| --- | --- |
| [CONTRIBUTING.md](CONTRIBUTING.md) | how to propose a change or ask for a number |
| [MAINTAINERS.md](MAINTAINERS.md) | who keeps the spec |
| [CHANGELOG.md](CHANGELOG.md) | what changed, by date |
| [Chupathingy](https://github.com/ChupathingyCE/chupathingyce) | the game, the first implementation |
| [Reference client](reference/) | a small C client with golden packets and a conformance script (MIT) |
| [Playing online](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/online.md) | for players: how to get online with Chupathingy |

## License

The spec text is licensed under
[Creative Commons Attribution 4.0 International](LICENSE) (CC BY 4.0).
Code samples, hex examples and [registry.json](registry.json) written for
this spec are also offered under the MIT License, so an implementation may
copy them into its own code under either license. The reference client in
[reference/](reference/) is MIT ([reference/LICENSE](reference/LICENSE)).
