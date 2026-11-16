# Moderation

How players and moderators keep chat and games civil: a player's own
mutes and blocks, a host's and a server's moderators, reports, bans and
shared ban lists, and which of these belong to a server and which to a
network. The wire is in Delta Peer ([peer.md](../peer.md#moderation),
[Reports](../peer.md#reports)) and Delta Control
([control.md](../control.md)); this page puts the behavior together.

## Who decides what

| Tool | Belongs to | Reaches |
| --- | --- | --- |
| a player's own mute | the player's client | this game, this client |
| a block | the player's account, on their network | friends, invites, parties, clans, presence on that network |
| the host's mute, kick, ban | the game's host | that game, that host |
| a server's moderators and roles | the dedicated server (its file, its panel accounts, and, if linked, its network's role list) | that server |
| reports | the server that took them; forwarded to its network if linked | that server's moderators |
| bans | the server (by key, account, device or the game's own ban) | that server |
| shared ban lists | servers that choose to share and to take them, through a network | the servers that subscribe |
| name rules (blocked names, look-alikes) | the network | its lists, pages and verified names |

Nothing here reaches across networks. A network can't ban a player
everywhere; each server decides who plays on it
([federation.md](../federation.md)).

## A player's own tools

- **Mute (local):** a player mutes anyone in their game from the chat log
  or the Guide's player list. Their client stops showing that player's
  lines and playing their voice. Nothing is sent; nobody else knows. In
  the reference client mutes last for the current game: a new game starts
  with none.
- **Block (account):** silent and lasting, on the player's network
  ([friends.md](friends.md#blocks)). It covers the social features, not
  what's said in a game: a blocked player in the same game is still heard
  unless muted.
- **Chat filter:** the player's own choice of starring blocked words or
  hiding the line ([chat.md](chat.md)).
- **Report:** see Reports.

## A host's tools (a game a player hosts)

A player's host offers no moderation over the wire. Its player moderates
on their own machine:

- the Moderation screen for its own game: kick and ban, no sign-in, done
  with the game's own kick and ban, so they work on every player, with or
  without Delta;
- `/mute <player> [minutes]` and `/unmute <player>` typed as a chat line:
  the host stops relaying that player's lines and voice and tells their
  client (a legacy client gets the host's notice). Typed in someone else's
  game, these commands are never sent.

## A dedicated server's moderators

A dedicated server offers the `moderation` capability. The same Moderation
screen then signs in to the server instead of acting locally: what a
player does as a host on their own machine becomes a signed action the
server checks.

- **Sign in.** The player opens the Moderation screen and signs in. Their
  client proves its moderator key (or, for a verified player, its account
  through a device certificate that allows moderating) by signing the
  server's challenge, bound to the invite it joined so a signature can't
  be replayed on another server. Nothing is revealed until the player
  signs in.
- **Role.** The server answers with the key's role (none, moderator,
  admin, owner), its permissions and its longest timed ban. The role is the
  highest of: the server's moderators file, a control panel account bound
  to that player's client, and, when linked, the network's role list for
  that server (capped by the operator).
- **Actions:** warn, kick, ban (minutes, 0 forever), end the game, next
  map, mute chat and voice (minutes, 0 until they leave), unmute, lock and
  unlock joins. Each is signed with a rising sequence; the server checks
  the role again for every action, audits it, and answers with the result.
  Only actions the role allows are shown.
- **Notices.** A warning shows as a banner on the player's client and in
  its chat log.
- **Legacy players** can be warned (audit only), muted (through the
  bridge), kicked and banned like anyone, through the game's own
  protocol. They can't be in-game moderators: they can't prove a key.

### Remote moderator accounts

A server's operator gives moderators accounts on its control panel
(a name, a password, a role, an optional second factor; invitations are
single use). A moderator can then:

- moderate from a browser, against the server's panel, wherever they are;
- **log in to the server from the game:** in the panel, "Ask my game"
  sends the player's client a bind request naming the account and the
  server; the player confirms in the game, and their client proves its
  key. From then on, that client signs in with the account's role on that
  server. A bind not answered in 2 minutes is a decline.

A server linked to a network also takes the network's role list: an
account given a role on that server on the network's site has it in the
game, by its linked clients' keys or its verified account. The network's
roles are capped by the operator and expire if the network stops
answering.

## Reports

- A player reports another in their game (the Guide's player list, or the
  scoreboard): a reason from a short list (cheating, abuse in chat or
  voice, griefing or betraying, an offensive name, something else), no
  free text, optionally a clip.
- Only a server that takes reports offers `reports`; a player's host
  doesn't.
- The server limits them: one report of a player a game from one reporter;
  3 a minute and 10 a game from one reporter; 5 a game about one player
  from everyone. It counts by verified account where proved, else by the
  player in this game, never by machine slot.
- A report goes to the server's moderators with what the server knows:
  both names, verified handles, map, game type and the server's own
  refusal counts for the reported machine. Never an address.
- A linked server forwards reports about Delta players to its network,
  where the server's owner and role holders see them; a clip, if any,
  goes only to the network, for that server's moderators and the
  network's admins, and is deleted after 14 days. Reports about legacy
  players stay on the server.
- A report never acts by itself: a moderator decides.

## Bans

- A server bans by moderator key, Delta account or device, or through the
  game's own ban; a moderator can ban an account that already left
  (`sv_ban_account`), for example after a report.
- A player who joined by address alone proves only a name, which never
  gets a role or an account ban.

## Shared ban lists

Both directions are off until a linked server's owner turns them on, and
both go only by Delta account and device, never by address or hardware
ID ([control.md](../control.md#shared-ban-lists)).

- **Sharing:** a server's bans that name an account or device go to its
  owner's list on the network; the owner names who may take it, or the
  network marks it trusted for anyone.
- **Taking:** an owner picks the lists each server takes; the server keeps
  them, checks proven accounts and devices against them, and kicks a match
  with "Banned on <list>".
- **The server decides:** it can unban a shared entry on itself alone; the
  list keeps it.

## The network's name rules

- **Blocked names:** a network may keep a list of names nobody may use or
  be shown under (slurs and hate). Where it shows a player's or a game's
  name, a blocked one shows as removed, and a game with one isn't listed.
  The reference dedicated server ships the same list for its own name
  filter.
- **Look-alikes:** an unverified player whose game name looks like a
  verified player's handle in the same game shows as "Player N"
  ([peer.md](../peer.md#verified-names)).

## Privacy rules

- No address in any report, notice, audit line or answer.
- A player's local mutes and their filter are never sent.
- Nothing said in chat or voice is kept; a report carries no chat log.
- A moderator key is revealed to a server only when its player signs in.

## Without the feature

- A host or server without moderation offers nothing; legacy kick and ban
  still work everywhere.
- A client without moderation can't sign in, but is still subject to the
  server's kicks, bans and mutes (a mute through the host's relay).
- A client without reports can't report; nothing else changes.

## Proposals

- **Report thresholds that hide chat from non-friends:** a network or
  server could hide a player's lines from everyone but their friends once
  they have been muted or reported more than some number of times. Open
  questions: who counts (a server, or a network across servers), over how
  long, how a player learns of it and gets out of it, and how it avoids
  being used by a group against one player. Today's reference
  implementation never acts on report counts alone.
- **Persistent personal mutes** (kept across games, tied to an account):
  today's local mutes last one game; blocks are account-wide but don't
  silence a player in a game.
