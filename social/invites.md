# Invites and joining

How players get each other into games: join links that work with no
account, joining a friend in one press, invites between friends, party
codes, and the doorbell that makes all of it show up in about a second.

## Join links

A game reachable over the internet tunnel has an **invite**: 64 lowercase
hex digits (44 from older hosts). The first 32 digits name the host (a
hash of its tunnel key); the rest is the token. The internet tunnel
defines it; this spec only carries it.

```
halo://join/3f9a01c27be44d10a8c5e6f7091b2c3d5e6f708192a3b4c5d6e7f8091a2b3c4d
```

- Opening the link joins the game. Any client that speaks the internet
  tunnel can join it; no account is needed.
- A host shows or copies its own link to share.
- A game with a password: the link still needs the password. The network
  never hands such a game's invite to a friend (`locked`).
- The invite is the only way the network names a game. It is never an
  address, and a friend's state never carries it: only a join answer
  hands it out, after the checks below.

## Joining a friend

```
POST /v1/social/join   {"key" or a device token, "friend": "<handle>"}
```

| Status | Answer |
| --- | --- |
| 200 | `{"join": "halo://join/<invite>", "friend": "<handle>", "game": {...} or null}` |
| 404 | `{"error", "reason": "unknown"}`: no such handle |
| 409 | `{"error", "reason"}`, the reasons below |

| Reason | Means |
| --- | --- |
| `offline` | they're offline (or appear so to you) |
| `not_playing` | they're not in a game they share |
| `friends_only` | their "who can join" is friends, and you aren't one |
| `invite_only` | they take only players they invite |
| `unlisted` | their game isn't listed: ask for an invite |
| `locked` | their game has a password: ask for the link |
| `full` | full |
| `closed` | not taking players now |

The client then joins the link as it would any invite. An invite from
that friend to that game skips "who can join" (but not `locked`, `full` or
`closed`). The friends state's `joinable` is this check done ahead, so a
client can show JOIN only where it would work.

The reference client calls this "JOIN" on a friend's row (one press: the
check, then the join), and the same for accepting a game invite.

## Game invites

```
POST /v1/social/invite   {"key" or a device token, "to": "<handle>", "invite"?: "halo://join/..." or the bare invite}
```

Without `invite`, the network uses the game the sender's presence named.

| Status | Answer |
| --- | --- |
| 200 | `{"ok": true, "id": "<16 hex>", "expires": 300}` |
| 403 | `{"error": "You can invite friends only."}` (also for someone who blocks you: it never shows) |
| 409 | `{"error", "reason"}`: `not_playing`, `locked` ("share its invite link instead"), `full`, `closed` |
| 429 | 10 invites a minute |

- Friends only. One invite from you to one friend at a time: a new one
  replaces the old.
- Kept in memory for 300 seconds, never stored.
- It shows in the friend's state:

```json
"invites": [{"id": "a1b2c3d4e5f60718", "from": "sarge", "display": "Sarge",
             "time": 1763300000, "expires": 1763300300,
             "game": {"name": "Red Base", "map": "bloodgulch", "players": 6,
                      "maximum_players": 16}}]
```

- The friend joins it with `/v1/social/join` naming the sender, or
  dismisses it (it simply runs out).
- Removing the friend or a block drops the invites both ways.
- The sender's client may mark the friend INVITED while the invite lives;
  that mark is the sender's own.

Party invites are in [parties.md](parties.md); clan invites in
[clans.md](clans.md).

## Codes and links

| What | Form | Where |
| --- | --- | --- |
| a game | `halo://join/<invite>` | anywhere; no account |
| a party | a code of 6 characters from `ABCDEFGHJKMNPQRSTUVWXYZ23456789` (no 0, O, 1, I or L), shown `ABC-DEF` | typed in the game |
| a party, as a link | `halo://party/ABCDEF` | opens the game's join |
| a party, to share | `https://<network's site>/party/ABCDEF` | a page that shows the code and opens `halo://party/ABCDEF`; the QR code holds this link |

A client takes a code as typed or pasted in any of these forms, with
dashes and spaces left out and letters made capitals.

## The doorbell

Polling alone works, but a friend request or an invite would take up to a
poll interval to show. The doorbell tells a client to poll now.

- **The channel.** The network hands each linked client its doorbell in
  the friends state (`"doorbell"`: 32 hex digits). It is derived by the
  network from a secret only it has, the client's ID and the week, so
  nobody can work out another client's doorbell or whose a doorbell is,
  and a leaked one goes stale within a week. The network rings the one it
  last handed out, so a ring at the turn of the week still arrives; the
  next poll hands over the new one.
- **The ring** is one byte, the kind of change, and nothing else (no
  handle, no name, no game):

| Kind | Change |
| --- | --- |
| 1 | friends (a request, a new friend, a removal) |
| 2 | a game invite |
| 3 | the party |
| 4 | presence (a friend came online or into a game) |
| 5 | clan (an invite) |

  Any other value, or none, is a ring all the same.
- **Who is rung.** A request rings the one it went to (never when they
  block the sender: a block rings only the blocker's own clients);
  becoming friends or a removal rings both; a decline rings only the one
  who declined; an invite rings the friend invited; coming online, into a
  game, or out of "appear offline" rings the friends (never while
  appearing offline or hiding the game). Party changes ring the other
  members (and the one kicked). A clan invite rings the player invited.
  Only clients that polled in the last 3 minutes are rung, at most 12
  times a minute each.
- **On a ring** the client polls at once, at least 2 seconds after its
  last poll, while fewer than 2 polls went out early for rings and fewer
  than 5 went out at all in the last minute. A ring never cuts short a
  wait the network asked for (429, an unlinked copy).
- **Failing** costs only speed: without rings, polling goes on.

The transport in the reference implementation is MQTT: the client
subscribes to `doorbell/<doorbell>` at QoS 0 with the doorbell as its
user name, and the ring is a QoS 0, not-retained message of one byte.
The brokers let a client read only its own topic and only the network
publish ([link.md](../link.md#the-doorbell)). Another network may carry
the same ring another way; the ring's meaning and the client's polling
rules stay the same.

> **Implementation note (Chupathingy's network):** the doorbell rides the
> MQTT connections internet play's signalling already keeps to
> Chupathingy's own brokers; no new connection is opened. The party page
> is on the stats site. Both are the network's own choices.

## Privacy rules

- A friend's game is named by its listing, never by its invite or
  address, until a join answer hands the invite out.
- A ring says only that something changed.
- Invites live in memory and expire; nothing of them is stored.

## Without the feature

- Join links work everywhere the internet tunnel does, account or not.
- A client without friend join just has no JOIN on a friend.
- A client that doesn't listen for rings polls on its schedule.
- A network without `joinable` (older) leaves it out: the client offers
  JOIN on any friend who is playing and shows the refusal.

## With federation

A join answer from another network would still be a `halo://join/` link:
the tunnel is the same everywhere. Invites and joins across networks need
friendships across networks (later step). Doorbells stay with each
player's own network.
