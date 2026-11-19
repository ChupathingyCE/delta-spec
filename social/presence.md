# Presence

What a friend (and, by choice, a clanmate) sees of a player: whether
they're on, whether they're in a game, which game, and where it runs.

**Needs:** an account. A player who has none has no presence.

## Online

A player is **online** while a client of theirs asked for its friends
state ([friends.md](friends.md)) in the last 150 seconds, or told the
network it is playing (below) in the last 180 seconds. Asking is the
signal: there is no separate "I'm online" request. Coming online (after
more than 150 seconds without asking) rings the friends' doorbells, kind 4
([invites.md](invites.md#the-doorbell)).

## Playing

```
POST /v1/presence   {"key" or a device token, "invite": "<64 or 44 hex digits>"}
```

A client sends it about once a minute while all of these hold:

- the player allows it (the client's own setting, `network.share_presence`
  in the reference client);
- it is in a multiplayer game over the network, hosted by a machine that
  speaks Delta (never for a game on a host without Delta);
- its copy is linked to an account;
- it knows the game's invite (the same token a `halo://join/` link
  carries, [invites.md](invites.md#join-links)).

Answers (plain text):

| Answer | Means | Client waits |
| --- | --- | --- |
| `ok` | noted | a minute, then again |
| `off` | no account, "Show when I'm playing" off, or a hidden service record | 30 minutes, or until the player's own choices change |
| 429 | too many from this address | 10 minutes |

The network keeps presence in memory only, for 180 seconds, with no
address. Nothing is sent from the menus (online covers them), and never
for another player.

`GET /v1/presence` answers `{"online": n}`: how many accounts are playing
now, counting only those that show it.

## What a friend sees

In each friend's line of the state:

| Field | |
| --- | --- |
| `online` | true or false |
| `playing` | in a game the player shares |
| `joinable` | the network would let *you* join now ([invites.md](invites.md#joining-a-friend)) |
| `game` | the game, if the network lists it publicly: `name`, `map`, `engine`, `mode`, `players`, `maximum_players`, `teams`, `platform`, `protocol`, `version`, `build`; else null |

`game` never carries the invite, the address or the roster. A friend in a
game that isn't listed (a private game, a LAN game reached by the tunnel)
shows as playing with `game: null` ("In a game").

The reference client makes one status line from it: the game type, the
map and the count ("Slayer · Blood Gulch · 6/16"), else "In a game",
"Online" or "Offline". `engine` is the game type: 1 CTF, 2 Slayer, 3
Oddball, 4 King, 5 Race, 6 Bomb.

## What hides it

| Setting or state | Effect |
| --- | --- |
| `appear_offline` | offline to everyone, friends too; no ring when it is turned on |
| "Show when I'm playing" off (`show_presence: false`) | online, never playing; presence answers `off` |
| a hidden service record | never playing |
| a block | the blocker is offline to the blocked |
| `clan_presence: "friends"` | a clanmate who isn't a friend sees offline |

## Platform

- **A friend's game:** `game.platform` is the platform of the game's host
  as the list has it (a registry key, [platform.md](platform.md)).
- **A party member:** each member carries the platform its own client
  sends ([parties.md](parties.md)).
- **A player in the same game:** the Delta Peer platform key.
- **A friend's own platform** is not in the friends state today. See
  Proposals.

## Toasts

A client may show a short notice when a friend comes online. The
reference client has it off by default, in the menus only (and in a game
only with a second setting).

## Without the feature

- A client that never sends presence still shows online from its polls;
  friends see "Online", never a game.
- A network from before presence leaves `playing`, `joinable` and `game`
  out: show online and offline only.
- A client in a game on a host without Delta sends nothing; friends see it
  online.

## With federation

Presence would cross networks only for friendships that cross them, by
the federation proposal's later step. Each network decides from its own
player's privacy what goes out; the other network shows what it gets.
Not built.

## Proposals

- `platform` on a friend's line: the platform of the client that last
  asked, a registry key, shown as the friend's logo.
- Presence for games that aren't listed, carrying only "in a game" and a
  game type.
