# Delta Social

Delta Social is the social part of the spec: friends, presence, invites, parties, chat,
voice, clans, platform icons and moderation. It describes formats and
behavior, not any one program. Chupathingy's game and site are the
reference implementation and the source of every number here. What is
specific to one network (its site's address, its brokers) is in that
implementation's own documentation, not in these pages.

**Status: draft.** These pages describe what Chupathingy's network does
today; anything marked proposed is not built yet.

Text on these pages is licensed CC BY 4.0.

## How it fits with the other parts

| Part | What Delta Social uses from it |
| --- | --- |
| Delta Link ([link.md](../link.md)) | accounts, handles, device identity, device tokens, the `social` scope, the doorbell |
| Delta Peer ([peer.md](../peer.md)) | chat, voice, party teams, moderation, reports and verified names between machines in one game |
| Delta List ([list.md](../list.md)) | the listed game a friend is in (its name, map, counts) |
| Delta Control ([control.md](../control.md)) | a dedicated server's roles, mutes, bans and shared ban lists |
| Federation ([federation.md](../federation.md), proposal) | names as `handle:domain` across networks |

## The pages

| Page | What it covers | Needs an account and a network? |
| --- | --- | --- |
| [friends.md](friends.md) | requests, accept and decline, remove, blocks, social privacy, recent players, limits | yes |
| [presence.md](presence.md) | what a friend sees: online, in a game, which game, platform | yes |
| [invites.md](invites.md) | join links, joining a friend, game invites, the doorbell, codes and links | links: no. Friend join, invites, doorbell: yes |
| [parties.md](parties.md) | making a party, codes, links and QR codes, the leader's go, team keeping | the party itself: a network (no account needed to join by code). Team keeping: peer to peer |
| [party-chat.md](party-chat.md) | what a party can say to each other, today and proposed | peer to peer (in one game) |
| [chat.md](chat.md) | text chat in a game, the host's rules, filters, the bridge to legacy chat | no: peer to peer |
| [voice.md](voice.md) | voice channels, opt-in, the host's rules | no: peer to peer |
| [clans.md](clans.md) | membership, ranks, tags, invites, emblems | yes |
| [platform.md](platform.md) | platform keys, where they show, icons | no |
| [moderation.md](moderation.md) | mutes, blocks, reports, host and server moderators, ban lists | per server: no. Accounts, report forwarding, shared lists: yes |
| [comparison.md](comparison.md) | each feature in Chupathingy, in another project's description, and what isn't in the spec yet | |

## What an implementation needs

Nothing here is required to play. A client that speaks none of it still
plays with everyone over the legacy game protocol.

| Level | What it means |
| --- | --- |
| **Required for any social feature** | ignore fields it doesn't know in every JSON answer; never show or log another player's address; treat every name and text from the network or another machine as hostile (length, UTF-8, control characters) |
| **Peer to peer (no account)** | chat (Delta Peer `chat`, `server_messages`), voice (`voice`), party teams (`party_teams`), local mutes, the platform key. These work on a LAN or the internet tunnel with no site at all |
| **With an account on a network** | friends, presence, invites, parties, clans, recent players, the doorbell. A client needs a device token (or a legacy player key) with the `social` scope ([clients.md](../clients.md)) |
| **Optional extras** | the doorbell (polling alone works), the follow offer, toasts, QR codes, clan emblems drawn in game |

A client may implement any subset. For each feature a page says what it
needs and how it behaves against a peer or a site that lacks it.

## Rules every page follows

- **No addresses.** No answer, message, log line or screen carries an IP
  address or a port of another player. Games are named by their invite,
  and only a join answer hands the invite out.
- **Players are named by handle.** Answers never carry internal player
  IDs. A player without an account (another port, an older build) is never
  kept, listed or shown by the network's social features.
- **Blocks never show.** A blocked player is refused in the same words
  anyone else would be, and sees the blocker offline.
- **Additive changes only.** A newer site adds fields; an older client
  ignores them. A newer client reads a missing field as "not supported"
  and falls back. Old requests keep working. Nothing changes what a client
  without Delta sees.
- **Rate limits answer 429** with `{"error", "reason": "busy"}`; the
  client waits and never retries in a loop.

## Errors

Refusals are JSON: `{"error": "<words for the player>", "reason":
"<code>"}`. The words are for showing; the code is for deciding. Some of
the reference site's older answers (friends' actions) carry only
`"error"`: a client must handle a refusal with no `"reason"` by showing
the words. New endpoints always carry both.

## Names across networks

Within one network, handles are unqualified (`milenko`). With federation
([federation.md](../federation.md)), every `handle` field may carry a
qualified name, `handle:domain` (`milenko:chupathingy.org`). A network
answers its own players unqualified or qualified, and other networks'
players always qualified. Each page shows how its fields look then.
Social features between networks are a later step of the federation
proposal; nothing on these pages works across networks today.
