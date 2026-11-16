# Parties

A party is a few players (8 at most) who play together: when the leader
joins or hosts a game, the others follow. The network keeps parties in
memory only. Inside a game, the host may keep a party on one team (Delta
Peer's `party_teams`).

**Needs:** a network. An account is needed to invite and be invited; a
linked copy without an account can start a party and join one by its
code, and shows by its game name, marked unverified.

## The request

```
POST /v1/party   {"key" or a device token, "action"?, "name"?, "platform"?, ...}
```

`name` (the game name, for a member without an account; printable, cut
at 24 characters, a leading `@` removed) and `platform` (a registry key,
[platform.md](platform.md); anything else is taken as unknown) come with
every request. Every answer is `{"party", "party_invites"}` after the
action; a refusal is `{"error", "reason"}`. A request with no action
reads the party and counts as the member still being there. For an
account, the friends state carries `party` and `party_invites` too, so a
member polls nothing extra.

| Action | Takes | Who |
| --- | --- | --- |
| `create` | | anyone not in a party |
| `invite` | `handle` | a member with an account, to a friend |
| `accept`, `decline` | `party` (16 hex) | the player invited |
| `join` | `code` (6 characters, or a `halo://party/` link) | as the party's "who can join" allows |
| `leave` | | a member |
| `kick` | `member` (8 hex) | the leader |
| `lead` | `member` | the leader passes the lead; in a party with no leader, any member's vote |
| `rule` | `join`: `anyone`, `friends`, `invite` | the leader |
| `code` | | the leader: a new code and tag |
| `go` | `invite` (`halo://join/...` or the bare invite) | the leader: where the party goes |

## The party

```json
"party": {
  "id": "5e1f0c2a9b7d4e63",
  "code": "K7QHMZ",
  "link": "halo://party/K7QHMZ",
  "leader": true,
  "has_leader": true,
  "who_can_join": "friends",
  "largest": 8,
  "members": [
    {"id": "a1b2c3d4", "name": "Sarge", "handle": "sarge", "verified": true,
     "platform": "pc_linux", "leader": true, "you": true},
    {"id": "e5f60718", "name": "Donut", "handle": null, "verified": false,
     "platform": "android", "leader": false, "you": false}
  ],
  "tag": "8c1d77e0a45b39f2",
  "go": null
},
"party_invites": [
  {"party": "0d9e8f7a6b5c4d3e", "from": "grif", "display": "Grif", "size": 3,
   "time": 1763300000, "expires": 1763300300}
]
```

For a member, `go` is the leader's game:

```json
"go": {"serial": 3, "time": 1763300100,
       "game": {"name": "Red Base", "map": "bloodgulch", "players": 6, "maximum_players": 16},
       "join": "halo://join/3f9a01c2..."}
```

or, when they can't follow, `"reason"` (`locked`, `full`, `closed`, or
`invited`: a member who came in by the code alone and isn't the leader's
friend) and `"error"` in place of `"join"`. A game that isn't listed is
the leader's to share, so it is followed.

## Rules

- **Size:** 8, the leader included. A party of one is the leader waiting.
- **Who can join by code** (`who_can_join`): `anyone`, `friends` (signed
  in and a friend of the leader's; the default) or `invite` (nobody: invites
  only). A player the leader kicked comes back only by invite for 10
  minutes.
- **Blocks:** a player who blocks, or is blocked by, any member can't join
  by code or invite. It shows as any other refusal.
- **One party at a time** per account (or per copy without one).
- **The leader** kicks, passes the lead, sets who can join, makes a new
  code and says where the party goes. A kick makes a new code and tag.
- **Succession:** a leader who leaves, or whose client goes quiet, passes
  the lead to the member who came in first by an invite (or who started
  the party). When every other member came in by the code, nobody leads
  until the leader comes back (by the code, whatever its rule) or the
  members choose: `lead` is then a vote, and the member every member votes
  for leads.
- **Going quiet:** a member whose client asks for nothing for 300 seconds
  is dropped. A party is gone when its last member leaves or goes quiet.
- **Following:** only members who came in by an invite (or started the
  party) and the leader's friends are given `go`'s link. A stranger who
  joined an `anyone` party by its code is told they can't follow.

## Following the leader

The leader's client sends `go` when it joins or hosts a game (the
reference client does while its BRING PARTY TO MY GAME setting,
`delta.bring_party`, is on). `go` lives 120 seconds. Each member's client, on seeing a
new `go.serial`:

| Setting (`delta.follow_leader` in the reference client) | Behavior |
| --- | --- |
| `ask` (default) | shows "Following Sarge to Blood Gulch" for about 5 seconds, A to go now, B to stay; then follows. In a game, it stays unless the player presses join |
| `always` | follows when the seconds run out, in a game too |
| `never` | doesn't offer it |

Or one line saying why it can't follow.

## Keeping the party on one team

The party's `tag` (8 random bytes, 16 hex digits) is the members' to send
their game's host in Delta Peer's PARTY_TAG ([peer.md](../peer.md#party-teams)).
The host learns only which of its machines share a party, and may put
them on one team where the teams stay within one player of each other. It
names no one, and a new party, a kick or a new code makes a new one. The
same tag picks the party voice channel ([voice.md](voice.md)), so it must
be at least 64 bits from a secure random source and never echoed to other
machines.

## Limits

| Limit | Value |
| --- | --- |
| members | 8 |
| an invite's life | 300 s |
| `go`'s life | 120 s |
| a quiet member dropped after | 300 s |
| a kicked player kept out (but by invite) | 600 s |
| invites from one member | 10 a minute |
| wrong codes | 20 an hour a member; 60 an hour an address (counted by a hash, never kept) |
| new parties | 20 an hour a member; 100 an hour an address |
| new codes | 10 an hour |
| parties on the network | the network's own cap (503 `busy`) |

Reasons: `no_party`, `no_leader`, `not_leader`, `no_member`, `in_party`,
`signed_out` (inviting without an account), `you`, `friends_only`,
`member` (already in it), `full`, `gone` (an invite run out), `unknown` (no
party has that code), `invite_only`, `kicked`, `busy`, `bad`.

## Polling

A member polls every 15 seconds in the menus, every 60 in a game, and at
once on a doorbell ring of kind 3: an invite rings the friend invited;
someone joining, leaving or kicked out, a new leader, rule or code, and
`go` ring the other members (and the one kicked). A decline and a quiet
member dropping out ring nobody.

## Privacy rules

- Members are named by handle and display name, or, without an account,
  by the game name they send, marked `verified: false`. Never an address,
  never an internal ID.
- The party page shows only the code, never who is in the party.
- The tag goes only to members and only to their own game's host.

## Without the feature

- A host without `party_teams` places players as it always has; a member
  whose client doesn't speak it sends nothing.
- A client without parties never asks; it can still be in the same games
  by join links.
- A network from before parties answers 404 or leaves `party` out: hide
  the party.

## With federation

Members from other networks would show as `handle:domain`; invites and
codes across networks are a later step. The tag stays network-free: a
host never needs to know which network a party belongs to.

> **Implementation note (Chupathingy's network):** the share link is
> `https://stats.chupathingy.org/party/CODE`. Another network uses its own
> site; the `halo://party/CODE` link is the same everywhere, but a code is
> only meaningful on the network that issued it (see Proposals).

## Proposals

- A network in party links (`halo://party/CODE@domain`), so a code can be
  opened by a client signed in elsewhere.
