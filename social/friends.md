# Friends

Friendship is mutual between two accounts on a network. One player sends
a request by handle; the other accepts or declines. Friends see each
other's presence ([presence.md](presence.md)), can join each other's
games and send invites ([invites.md](invites.md)), and can invite each
other to parties ([parties.md](parties.md)).

**Needs:** an account, and a device token or player key with the `social`
scope ([clients.md](../clients.md)). Only accounts take part: a player
with no account (another port, an older build, a copy never linked) is
never kept, listed or shown.

## Requests

| Request | Body | Answer |
| --- | --- | --- |
| `POST /v1/social/state` | `{"key"}` or a device token (`Authorization: Delta <token>`), `"since"?`, `"limit"?`, `"clan"?` | the state (below), or `{"cursor", "same": true}` |
| `POST /v1/game/friends` | the key or token, `"action"`, `"handle"?` | the state after the action, with `"result"` for a request |

Actions (`"action"`):

| Action | Takes | Does |
| --- | --- | --- |
| `request` | `handle` | sends a request. `"result": "sent"`, or `"friends"` when they had already sent you one (both said yes) |
| `accept`, `decline` | `handle` | answers a request from them |
| `cancel` | `handle` | takes back your own request |
| `remove` | `handle` | ends a friendship (and the invites between you) |
| `block`, `unblock` | `handle` | see Blocks |
| `privacy` | `requests`?, `join`?, `appear_offline`?, `clan_presence`? | see Privacy; a field left out stays as it is |
| `""` or none | | reads the state |

A handle is 3 to 20 characters of `a-z 0-9 _ -`, matched without regard
to case and with a leading `@` ignored. `display` is the same name in the
capitalization the player picked (up to 24 characters); show `display`,
send `handle`.

## The state

```json
{
  "you": {"handle": "milenko", "display": "Milenko", "online": true,
          "appear_offline": false, "show_presence": true,
          "friend_requests": "everyone", "who_can_join": "friends",
          "clan_presence": "friends_and_clan"},
  "friends": [
    {"handle": "sarge", "display": "Sarge", "since": 1762300000,
     "online": true, "playing": true, "joinable": true,
     "game": {"name": "Red Base", "map": "bloodgulch", "engine": 2,
              "mode": "slayer", "players": 6, "maximum_players": 16,
              "teams": true, "platform": "pc_linux", "protocol": 44,
              "version": "0.9.1", "build": "..."}}
  ],
  "more": 0,
  "requests": {"incoming": [{"handle": "grif", "display": "Grif", "time": 1763300000}],
               "outgoing": []},
  "invites": [],
  "blocked": [],
  "recent": [{"handle": "simmons", "display": "Simmons", "time": 1763290000,
              "map": "sidewinder", "friend": false, "requested": false}],
  "counts": {"friends": 1, "online": 1, "requests": 1, "invites": 0, "party_invites": 0},
  "party": null,
  "party_invites": [],
  "doorbell": "0f1e2d3c4b5a69788796a5b4c3d2e1f0",
  "cursor": "9c2f1ab04e7d3355",
  "same": false
}
```

- `friends` are sorted online first, then in a game, then by handle. With
  `"limit": n` (0 means all) the answer has at most n and `"more"` counts
  the rest.
- `game` is null unless the friend is in a game the network lists
  publicly ([presence.md](presence.md)). It never carries the game's
  invite, address or roster.
- `cursor` is a digest of everything else. Asked again with
  `"since": <cursor>`, an unchanged state answers `{"cursor", "same":
  true}` only.
- `party`, `party_invites` ([parties.md](parties.md)) and, with `"clan":
  true`, `clan`, `clan_invites`, `clan_invited` ([clans.md](clans.md))
  ride the same poll, so a client spends no extra requests on them.
- `doorbell` is this device's ring channel ([invites.md](invites.md#the-doorbell)),
  given only to a game client, and also in a `"same"` answer.
- The client marks itself online by asking ([presence.md](presence.md)).

## Recent players

`recent` lists the accounts you shared a game with in your last 20 games,
newest first, at most 24, each once: `time` is the last game shared,
`map` its map, `friend` and `requested` whether you're friends or your
request waits. Only players whose own client proved their account in that
game count, so a name alone never appears. Left out: accounts that hide
their service record, locked accounts, and anyone you block or who blocks
you.

A client may add players verified in its own games this session (Delta
Peer's verified names, [peer.md](../peer.md#verified-names)) before the
network's list, each handle once, never the player's own.

## Blocks

A block is silent:

- It ends any friendship and drops the requests and invites both ways.
- From then on, the blocked player's requests are stored as "silent": the
  sender sees theirs waiting in `outgoing`; the blocker never sees it and
  is never notified. Refusals the blocked player gets are only those
  anyone would get (the privacy rule, a cap).
- Their game and party invites are refused as anyone's who isn't a friend
  would be.
- The blocker shows offline to them and they can't join the blocker's
  game or party, or take a clan invite from them.
- A request to someone you block is refused ("Unblock them first.").
- Unblocking drops the silent requests that waited; it doesn't restore a
  friendship.

## Privacy

| Field | Values | Default | Means |
| --- | --- | --- | --- |
| `requests` (state: `friend_requests`) | `everyone`, `friends_of_friends`, `nobody` | `everyone` | who may send you requests |
| `join` (state: `who_can_join`) | `anyone`, `friends`, `invite` | `friends` | who may join your game through the network; an invite always lets its friend in |
| `appear_offline` | true, false | false | shows you offline to everyone, friends too |
| `clan_presence` | `friends`, `friends_and_clan` | `friends_and_clan` | who besides friends sees whether you're on and what you play |

`show_presence` ("Show when I'm playing") is the account's presence
setting ([presence.md](presence.md)).

## Limits

| Limit | Value | Refusal |
| --- | --- | --- |
| friends | 200 each | 409 "Your friends list is full." / "Their friends list is full." |
| requests waiting from you | 50 | 409 |
| requests waiting for one player | 200 | 409 "They have too many requests waiting." |
| requests sent | 20 an hour | 429 |
| a request's life | 30 days, then it's gone | |
| blocks | 500 | 409 |
| state polls from one device | 6 a minute | 429 `"reason": "busy"` |
| actions from one device (join, invite, party actions) | 20 a minute, counted apart from polls | 429 |

Other refusals: 404 "No profile has that handle.", 400 "That's you.",
409 "You're friends already.", 403 "They aren't taking friend requests.",
404 "That request is gone." (accept, decline), 404 "You're not friends."
(remove), 400 for privacy values the network doesn't take. A copy that
isn't linked to an account gets 404 `{"linked": false}`; a locked account
403.

## Polling

The reference client polls `/v1/social/state` every 20 seconds in the
menus (15 while in a party), every 60 seconds in a game, at once when the
Guide opens or after an action (never sooner than 10 seconds after the
last poll), and at once on a doorbell ring. After 429 it waits 5 minutes;
for an unlinked copy, 10 minutes; with no answer, the wait doubles up to 5
minutes. Polls plus rings stay within the network's 6 a minute, with room
for an action.

## Privacy rules

- No address and no internal player ID in any answer.
- A player's friend list is theirs alone; nothing on these requests
  reveals another player's friends.
- Deleting an account deletes its friendships, requests, blocks and
  privacy rows.

## Without the feature

- A client without friends support never asks; nothing changes in games.
- A network from before a field leaves it out (`recent`, `clan_presence`,
  `party`): the client hides that part.
- Players without an account, and clients without Delta, never appear in
  any friends list and see nothing new.

## With federation

Every `handle` may be qualified:
`{"handle": "goatbutt:example.org", "display": "goatbutt"}`. A request to a
player on another network would go network to network, as the
federation proposal's later step says; blocks and privacy stay with each
player's own network. Not built.
