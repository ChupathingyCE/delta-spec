# Platforms

Which platform a player is on: a number on the wire, a key in JSON, and a
logo on screen. The numbers and keys are assigned in the registry
([registry.md](../registry.md#platforms), [registry.json](../registry.json));
never pick one yourself. Until a port has one, it sends 0 (`unknown`).

## Where it travels

| Where | Form | Who says it |
| --- | --- | --- |
| Delta Peer HELLO and WELCOME, the host's roster | byte 0 of the 8-byte platform key ([peer.md](../peer.md#platform-keys)) | each machine, for itself; the host repeats it |
| the game list | `platform` (the host's key), `platform_key` (16 hex), `machines` (counts by key, `legacy` for a machine without Delta) ([list.md](../list.md)) | the host |
| a party member | `platform` (a key) on `/v1/party` | each member's own client |
| a friend's game | `game.platform` (the host's key) | the list |
| a claim or report | `platform` (a key) | the player's own client |

A platform is always the speaker's own word about itself. It decides
logos, sorting and a host's limits for weaker machines, never game state
and never who someone is.

## Showing it

- A client draws a logo for each key it knows, and none for 0 or a key
  it doesn't know.
- The short tags (`WIN`, `MAC`, `LNX`, `XBOX`, `360`...) in the registry
  are for game list rows.
- In the reference client: the scoreboard (logo column), the Guide's
  PLAYERS HERE and PARTY rows, and the game list. The Xbox-styled menus
  show no logos; a player setting turns logos and the verified mark off
  together.
- The verified mark (a small Delta mark for a player whose account is
  proved in this game) shares the logo column
  ([peer.md](../peer.md#verified-names)).

Logo art is each client's own; the spec names platforms, not pictures.

## Privacy rules

A platform says what someone plays on, never where. A host's `machines`
counts are counts only, never per player.

## Without the feature

A machine without Delta has no platform: no logo, counted as `legacy`. A
client that sends no platform is `unknown`. A key a network or client
doesn't know reads as `unknown`; a network refuses a key that isn't in the
registry rather than storing it.

## With federation

Platform numbers stay one registry for every network, so a logo means the
same everywhere. A new platform asks the registry, not a network.
