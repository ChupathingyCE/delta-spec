# Delta Social: comparison

Each social feature in three columns: Chupathingy (the reference
implementation, its status and platforms), Halo Content Evolved as its
author described it publicly on 2026-11-16, and whether the spec covers it.

The Halo Content Evolved column is **from the author's description, not
checked**: nobody read its code for this page. It describes options, not
a judgment of either project's choices.

"Desktop" below means Windows, macOS, Linux and FreeBSD builds; the Delta
Guide (friends, parties, clans) is on desktop and Android, not on consoles
yet.

| Feature | Chupathingy | Halo Content Evolved (from the author's description, not checked) | In the spec |
| --- | --- | --- | --- |
| Accounts and verified names | shipped: accounts, devices, certificates, verified names in games; desktop, Android; consoles link by code | lighter on certificates and names | yes ([link.md](../link.md), [peer.md](../peer.md#verified-names)) |
| Friend list | shipped (0.9.1): Guide and site; desktop, Android | yes | yes ([friends.md](friends.md)) |
| Friend requests | shipped: everyone / friends of friends / nobody, silent blocks | yes | yes ([friends.md](friends.md)) |
| Blocks | shipped, silent | not described | yes ([friends.md](friends.md#blocks)) |
| Presence | shipped: online, in a game, which listed game, appear offline | not described | yes ([presence.md](presence.md)) |
| A friend's own platform | not shown (only the host's platform of their game) | cross-platform sync described | proposal ([presence.md](presence.md#proposals)) |
| Join a friend (insta-join) | shipped: one press, checked by "who can join" | insta-joins | yes ([invites.md](invites.md#joining-a-friend)) |
| Game invites | shipped: friends only, 5 minutes | not described | yes ([invites.md](invites.md#game-invites)) |
| Join links | shipped: `halo://join/`, shared with other builds of the internet tunnel | not described | yes ([invites.md](invites.md#join-links)) |
| Instant notifications | shipped: the doorbell, toasts | not described | yes ([invites.md](invites.md#the-doorbell)) |
| Parties | shipped: 8, codes, links, QR, leader's go, team keeping | not described | yes ([parties.md](parties.md)) |
| Party chat | party voice in a game; no party text | not described | partly; text and outside games are proposals ([party-chat.md](party-chat.md)) |
| Text chat | shipped: Delta chat plus the bridge to legacy chat; desktop, Android, dedicated server; consoles as clients | not described | yes ([chat.md](chat.md)) |
| Voice | shipped, opt-in: team, proximity, everyone, party; Windows, macOS, Linux, Android | not described | yes ([voice.md](voice.md)) |
| Clans | shipped: ranks within a clan, tags, emblems, invites | not described | yes ([clans.md](clans.md)) |
| Player ranks (progression) | none (clan ranks are clan roles, not progression) | yes | not yet: proposal |
| Player emblems | none per player (clan emblems; the player's armor color stands in) | yes | not yet: proposal (clan emblems are in [clans.md](clans.md)) |
| Cross-platform progression sync | stats and service record on the account, from every linked device; no progression to sync | yes | not yet: proposal |
| Platform icons | shipped: registry keys, logos in scoreboard, Guide, list | not described | yes ([platform.md](platform.md)) |
| Moderation | local mutes (one game), account blocks, host mute/kick/ban, server moderators with roles signed in from the game, panel accounts bound to a game, reports to a server's moderators (forwarded when linked), opt-in shared ban lists by account and device; no automatic action on report counts | a mute and report system: a player muted or reported more than 5 times has their messages hidden from anyone who isn't their friend; mutes last a single match | yes ([moderation.md](moderation.md)); report thresholds hiding chat from non-friends: proposal |
| Federation | proposal (`handle:domain`, each network its own keys) | not described | proposal ([federation.md](../federation.md)) |

## Not in the spec yet: to discuss

Each of these needs a short proposal before anyone builds it, so two
implementations make the same thing:

- **Player ranks:** what earns a rank, where it's computed (a network from
  its stats, or a client), whether ranks from different networks compare,
  and how a rank shows next to a name without crowding the scoreboard.
- **Player emblems:** a format (the clan emblem's pieces and colors are a
  ready start), where it's stored (the account), and how other players'
  clients fetch it (the public card).
- **Cross-platform progression sync:** what is synced (settings, unlocks,
  stats), which side wins a conflict, and how it works for a player with
  devices on two networks.
- **Report thresholds that hide chat from non-friends:** the count, the
  window, who counts, how a player sees and leaves the state, and abuse by
  groups ([moderation.md](moderation.md#proposals)).
- **A friend's platform** in presence, and **party text chat**.
