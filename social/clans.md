# Clans

Groups of accounts on a network, with a name, a tag, a motto, an emblem
and ranked members. A clan's tag can show before a verified player's name
in games.

**Needs:** an account. Making a clan, ranks, renaming and the emblem may
be on the network's site alone; inviting, kicking, answering invites and
leaving can be done from a client.

## A clan

| Field | Rule |
| --- | --- |
| `name` | 2 to 32 characters: letters, digits, spaces and `' . & _ -`, starting with a letter or digit; unique |
| `tag` | 2 to 8 letters and digits; unique in any case |
| `motto` | up to 64 characters |
| `emblem` | `{"fg", "bg", "c1", "c2", "c3"}`: a foreground shape in two colors on a background shape in one, colors from Halo's 18 armor colors |
| members | 50 at most; one clan per account |

Names, tags and mottos pass the network's name filter.

### Ranks

| Rank | May |
| --- | --- |
| `leader` (one) | everything: name, tag, motto, emblem, invites, ranks, kick anyone, hand the clan to another member |
| `officer` | motto, emblem, invites, kick members |
| `member` | leave |

A leader leaves only once another member leads, or when alone (the clan
goes with them).

## Requests from a client

```
POST /v1/game/clan   {"key" or a device token, "action": ...}
```

| Action | Takes |
| --- | --- |
| `accept`, `decline` | `clan` (its ID, from an invite) |
| `leave` | |
| `invite`, `kick` | `handle` (a leader's or officer's) |
| `roster` | nothing changed: read |

Answer:

```json
{
  "clan": {"id": "...", "name": "Blood Gulch Blues", "tag": "BGB",
           "motto": "Red team sucks", "emblem": {"fg": 4, "bg": 0, "c1": 3, "c2": 0, "c3": 1},
           "created": 1762000000, "rank": "officer", "count": 12, "hidden": 1, "more": 0,
           "members": [{"handle": "church", "display": "Church", "rank": "leader",
                        "online": true, "playing": false, "game": null},
                       {"handle": "tucker", "display": "Tucker", "rank": "member", "you": true}]},
  "clan_invites": [],
  "clan_invited": [{"handle": "caboose", "time": 1763200000}]
}
```

- `members` carry presence as a friend's would ([presence.md](presence.md)):
  hidden while a member appears offline or hides their game, and offline
  to a clanmate who isn't a friend when the member's `clan_presence` is
  `friends`. A client's own line has `you` and no presence.
- At most 24 members in a client's answer; `more` counts the rest.
  Members who hide their service record are left out and counted in
  `hidden`.
- `clan_invited`: the invites the clan has out, for a leader or officer
  only.
- With no clan: `clan` is null and `clan_invites` lists `{"id", "name",
  "tag", "count"}` for each clan that invited the player.
- The friends poll with `"clan": true` carries the same three fields, so a
  client polls nothing extra ([friends.md](friends.md)).
- The profile request (`/v1/game/profile`) carries `clan` and
  `clan_invites` too (members by display name and rank, without presence)
  and the privacy setting `show_clan_tag`.

Refusals are `{"error"}`: 404 "You're not in a clan." / "That invite is
gone." / "They're not in your clan." / no such handle, 403 "Your rank
can't do that.", 409 "They're in a clan already." / "The clan is full." /
"They have too many invites waiting." / "Make another member leader
first." / "Leave your clan first.", 400 "That's you.".

## Invites

- By handle, from a leader or officer; kept 30 days; dropped when the
  player joins any clan.
- A clan may have 50 invites out; a player may have 20 waiting.
- An invite from someone the player blocks is silent: the inviter sees it
  waiting, the player never sees it and can't take it.
- An invite rings the player's doorbell, kind 5 ([invites.md](invites.md#the-doorbell)).
- Membership is always the player's own choice: nobody is added without
  accepting.

## Tags in games

A verified player ([peer.md](../peer.md#verified-names)) who shows their
tag appears as `[TAG] Name` on the scoreboard, the postgame report and the
lobby, the name cut to fit with "...". The public card other players'
clients fetch (`POST /v1/game/players`) carries `"clan": {"tag", "name"}`
only while its owner shows it. `show_clan_tag` is the player's own
setting.

## The emblem

The pieces (shapes on a 100 by 100 field, filled even-odd, and the 18
colors) are published by the network (`GET /v1/clans/emblem`), so a
client can draw the same emblem the site does. Public lookups: `GET
/v1/clans?q=TEXT` (by name or tag), `GET /v1/clans/<TAG>` (a clan's page).

## Privacy rules

- No address and no internal ID in any answer but the clan's own ID.
- Members hiding their service record are counted, not listed.
- A locked account shows in no list.

## Without the feature

- A client without clans shows no tags and no CLAN section; nothing
  changes in games.
- Players without Delta, and clients that don't fetch cards, see game
  names without tags.
- A network from before clans leaves the fields out; from before the
  roster in the friends poll, it leaves them out of that poll and the
  client uses the profile request.

## With federation

A clan belongs to the network where it was made. Its tag is unique only
there, so across networks a client should show a clan from another
network qualified where it must tell two apart (`[BGB] church:example.org`).
Members from other networks would need cross-network invites (a later
step).

> **Implementation note (Chupathingy's network):** making and editing a
> clan, ranks and the emblem are on the site's own pages
> (`/v1/session/clan/*`), which are the site's, not the spec's. "Ranks"
> here are clan roles, not player progression ranks (see
> [comparison.md](comparison.md)).
