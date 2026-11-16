# Voice

Voice chat between players in one game, relayed by the game's host over
Delta Peer's `voice` (bit 22). Peer to peer: no account, no network, and
nothing is recorded anywhere. The bytes are in
[peer.md](../peer.md#voice); this page is the behavior.

## Opt-in

- Voice is **off** on each player's client until they turn it on (retail
  had none). Once on, push to talk is the default; open mic is a choice.
- The microphone opens only when the player first talks.
- A host with voice off doesn't offer the capability. A dedicated server's
  voice is off unless its operator turns it on, since relaying costs its
  upload. A player's host has it on by default (the channels below).

## Channels

A player talks on one channel at a time and switches with a button:

| Channel | Number | Who hears |
| --- | --- | --- |
| TEAM | 1 | their team; everyone in co-op; nobody in a game without teams |
| PROXIMITY | 2 | anyone alive within the host's range, played from where the speaker stands through the game's 3D sound |
| EVERYONE | 3 | everyone in the game, only where the host allows it (off unless set) |
| PARTY | 4 | their party in this game ([party-chat.md](party-chat.md)) |

Outside play (the pregame lobby, the postgame), everyone hears everyone
on any channel but party, if the host's lobby voice is on.

## The host's rules

The host decides who hears whom; a client never does. It sends each client
VOICE_CONFIG with the channels it relays, lobby voice, quality and range,
and the client shows a channel it can't use dimmed with one plain reason.

| Rule | A player's host default | A dedicated server default |
| --- | --- | --- |
| voice relayed | on | off |
| team, proximity, party | on | as set |
| everyone | off | off |
| lobby voice | on | as set |
| range | 15 world units | as set |
| quality | 24 kbps | as set |
| talkers at once | 4 | 8 |

## Listening and relaying

- A client says the channels it plays and its party tag every 2 seconds;
  the host sends it frames only on those channels, and nothing once it
  has been silent for 6 seconds. A channel at volume 0 is off: it costs the
  host nothing.
- The host checks each frame (session, budget, size, channel, mute,
  talkers), names the speaker itself, never decodes a frame and never
  sends one back to its speaker.

## Mutes

- **A host's or moderator's mute** ([moderation.md](moderation.md)) mutes
  voice too: the host relays none of the player's frames and tells their
  client, which stops sending.
- **A player's own mutes** are their client's alone, never sent.

## The codec

Opus, 48 kHz mono, 20 ms frames, one a datagram, VOIP mode, variable
bitrate at the host's quality, in-band FEC for 10% loss, complexity 5; a
60 ms jitter buffer per speaker. At 24 kbps a frame is about 60 bytes,
about 5 KB a second per talker per listener with headers.

## Privacy rules

Nothing is recorded or kept, by the host or anyone. Nothing of voice goes
to the network. The party tag is never echoed.

## Without the feature

A build without voice never agrees to `voice` and is sent no frames; a
host without it relays nothing. Players without Delta have no Delta voice.

> **Implementation note (Chupathingy):** voice is on Windows, macOS, Linux
> and Android; consoles are never sent voice for now. A bridge to another
> project's voice is planned as a clean-room spec, not built.
