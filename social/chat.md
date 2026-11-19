# Chat

Text chat between players in one game, the host's own lines, and the
bridge that lets players with Delta chat with players whose clients only
have the legacy chat. Chat is peer to peer: it needs no account and no
network, and the network never sees a line.

The bytes are in Delta Peer ([peer.md](../peer.md#chat)): `chat` (bit 3)
for players' lines, `server_messages` (bit 2) for the host's. This page
describes the behavior.

## Saying a line

- A client sends CHAT_SAY: a scope (everyone or team) and up to 120 bytes
  of UTF-8 (80 characters).
- **The host checks**, in order: the session, a rising sequence, the
  budget (1 a second, 3 at once; the same line again within 10 seconds is
  too fast), the text (valid UTF-8; no control characters, bidirectional
  overrides or isolates, zero-width characters; not blank), the speaker's
  mute, then its own rules: a team line in a game without teams is
  refused (in co-op everyone is one team), an everyone line where the host
  allows team lines only, and, with its filter on, a line with a blocked
  word.
- A refused line is answered with CHAT_REFUSED and its reason and goes
  nowhere else.
- **Relaying:** the host names the speaker from its own player list (a
  client never names itself) and sends CHAT_LINE to every machine that may
  hear it: everyone, or the speaker's team. The host's own player is a
  speaker and a listener like any other.

## The host's lines

A dedicated server's message (`sv_say`, its control panel's Say) is a
CHAT_LINE of kind server, with no speaker, to every machine that agreed to
`server_messages`. Warnings stay moderation notices (a banner), also kept
in the client's chat log.

## Showing a line

- A client takes CHAT_LINE only from its host, of its session, at most 10
  a second, and checks its text and name again.
- It shows the line in the game's font (a character the font lacks as
  `?`).
- The player's own settings decide the rest: chat on or off, shown or
  hidden, the filter (blocked words starred out, or the line hidden), and
  their mutes.

## Mutes

| Mute | Who | How long | Sent? |
| --- | --- | --- | --- |
| a host's or moderator's | the host, a moderator ([moderation.md](moderation.md)) | until the player leaves, or for some minutes | the host stops relaying their lines and their voice, and tells their client (CHAT_CONFIG, and VOICE_CONFIG for voice) |
| a player's own | anyone, on their own client | this game: the reference client clears them when a new game starts | never sent; nobody else knows |

## Nothing is kept

Neither a host nor a dedicated server writes down what is said; the
network never sees it. Only moderators' actions (a server message, a
mute) go in the server's audit file.

## The bridge to legacy chat

Some builds without Delta carry their own text chat in the game's
distributed messages: a client's line up to its host, the host's line
down to each machine that hears it, and the host's chat settings (chat
allowed, links allowed) to each client, sent as they change and every
3 seconds. Their text is printable ASCII without `|`, at most 63
characters. The entries are listed in [peer.md](../peer.md#chat).

A host with Delta chat bridges the two, so everyone in the game talks
together. Each line goes to a machine one way or the other, never both.

**On a host with Delta chat:**

- To each machine with no Delta chat session, it sends its chat settings
  from its own configuration: chat allowed while its chat is on and it
  lets legacy players chat (on by default; a host may turn it off), links
  allowed.
- It takes a legacy line only from that machine's own player and checks it
  as it checks CHAT_SAY: the same budget, repeat check, text check, mute,
  mode and filter. A refusal goes back as the host's notice.
- A line it takes (from either side, or its own player's) goes to each
  Delta machine as CHAT_LINE and to each legacy machine that may hear it
  as a legacy line, its UTF-8 made ASCII (accented Latin letters without
  their accents, typographic quotes and dashes as plain ones, anything
  else `?`) and cut to 63 characters.
- A server line goes to legacy machines as the host's notice.
- A legacy "vehicle" line is a team line (Delta has no narrower scope); a
  team line in a game without teams is everyone's.
- With legacy chat turned off, legacy machines are sent only the setting
  (chat not allowed), and a refusal if they say a line anyway.

**On a client whose host has no Delta chat:** it follows that host's
settings: it says its lines the legacy way once the host allows chat, and
shows the host's legacy lines (notices as system lines; blank ones and
repeats within 15 seconds left out). The player's own settings apply as
for Delta lines. It takes nothing but the host's stream.

**Either way:** a message of the wrong size is dropped and logged once (by
machine index, never address). Nothing about chat ever ends a connection.

### The welcome line

A host may (off unless turned on) send a machine with no Delta session
one line, a few seconds after its player first spawns, once each time it
joins, saying what kind of game this is. It goes as the game's notice
message, so a legacy client shows it in its chat even with chat off:
printable ASCII without `|`, at most 63 characters. A Delta machine never
gets it, nor does anyone while the host has no Delta.

## Without the feature

- Machines without Delta never send or receive Delta chat; with the bridge
  they still chat with everyone through their own chat.
- A Delta client that takes server messages but not chat is sent only
  those.
- A host without chat offers neither capability; a client shows nothing.

## Limits

| | |
| --- | --- |
| a line | 120 bytes of UTF-8, 80 characters; 63 ASCII characters to legacy machines |
| budget | 1 a second, 3 at once; a repeat within 10 s refused |
| lines a client takes | 10 a second |

## The legacy chat entries

The legacy chat entries' format is the one another project published under
CC0 on 2026-10-18; this spec describes it only so clients can interoperate.
