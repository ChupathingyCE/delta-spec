# Party chat

What a party can say to each other. Today that is voice, inside one game.
Text for parties, and talking outside a game, are proposals.

## Today: the party voice channel

Party members in the same game talk on the PARTY voice channel (channel
4, [voice.md](voice.md)). The host relays a party frame to the machines
whose VOICE_UP said the same party tag ([parties.md](parties.md)),
wherever their players are on the map and whatever their team.

- It needs the host's `voice` capability with the party channel allowed
  (the host's own rule), and each member's voice turned on.
- Only members in the **same game** hear each other: the host relays, and
  members in other games, in the menus or in no game at all aren't on that
  host.
- Without a party there is no tag, and the channel can't be picked.
- A player muted by the host or a moderator is muted here too; a
  player's own mutes are their own.
- Anyone who knows a party's tag hears that party in a game where they
  are, so the tag is secret: at least 64 random bits, given only to
  members, never echoed by a host.

## Today: text

There is no party text channel. Members in one game use the game's chat
([chat.md](chat.md)): everyone, or their team when the party shares one.

## Without the feature

A member whose client has no voice is never sent frames, and a host
without `voice` relays none. Nothing changes for the game.

## Proposals

Open questions, for discussion:

- **Party text chat in a game:** a scope beside everyone and team in
  CHAT_SAY, routed by the host to machines that said the same party tag,
  as voice is. Additive: a host without it refuses the scope (CHAT_REFUSED),
  and the client hides it.
- **Party chat outside a game** (the menus, members in different games):
  needs a relay that isn't a game host: the network, or one member's
  machine. Either way it would see the party's lines, which a game host
  never keeps; a design must say who relays, what is kept (nothing,
  preferably), and how mutes and blocks apply.
- **Whether party chat should exist only in games**, which keeps every
  line peer to peer and off the network.
