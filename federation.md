# Federation (proposal)

**Status: proposal.** Nothing on this page is built yet. It describes how
any project can run its own network on the open network spec (the formats
on these pages), with its own accounts and servers, and still play and
verify names with every other network. Delta is the name of the shared
spec. Chupathingy is one implementation of it, and the network its site
runs is one network among others. Comments are welcome on the issue
tracker.

## The idea

Today there is one network, Chupathingy's: its site issues the
certificates that prove a player's name ([link.md](link.md#device-identity)). That works, but
it means every port, fork or community that wants verified names, friends or
profiles has to rely on one project's servers.

Federation removes that. Like email or Matrix, each community can run its own
network, and the networks work together:

- **Your network, your accounts.** A project runs its own site, its own
  sign-in and its own moderation. Nobody else gets access to its servers,
  its database or its players' data.
- **One player base.** A player from any network can join any game, and the
  game can check that player's name, whichever network issued it.
- **No live calls between networks.** Checking a name never contacts the
  other network. If a network goes down, its players keep playing; they
  only stop getting new certificates until it's back.
- **Optional for everyone.** A game, a port or a server that doesn't take
  part loses nothing. The legacy game protocol stays the common ground, as
  everywhere in the spec.

## Names

A name is a handle plus the network that issued it:

```
handle:domain
milenko:chupathingy.org
someone:example.org
```

- The handle follows today's rules (lowercase `a-z 0-9 _ -`, 3 to 20
  characters, [link.md](link.md)).
- The domain is the network's own: the one whose root keys signed the
  player's issuer certificate ([link.md](link.md#networks) has the rules
  for a domain).
- Two networks can each have a `milenko`. They're different players, and
  the domain keeps them apart. A player's account is the pair of the
  domain and the account ID, never the account ID alone.
- Typed in (to find or add a player), a name is read in any capitals, and
  a handle alone means the reader's own network.
- **What shows.** A game shows its own network's players as today, by
  name alone, and every other network's verified players as `Name:domain`
  (the handle in its owner's capitals, the domain in lowercase), so a
  familiar name never hides where it came from. A game's own network is
  the one its copy signs in to.
- Certificates issued before federation read as `chupathingy.org`, the
  network whose root keys signed them. No certificate changes.

## How a name is checked

Each network uses the same chain the spec already defines
([link.md](link.md#device-identity)), with its own keys:

1. **Root keys** (a primary and a recovery key), kept offline by the network.
   They sign the network's **issuer certificate** (CISS).
2. **The issuer** signs short-lived **device certificates** (CDEV, 7 days on
   desktops) that say "this device's key holds handle X on this network".
3. **A game or server** checks a certificate offline: the issuer certificate
   must be signed by a root key it trusts, and the device certificate by
   that issuer, inside its dates. At join, the device proves it holds its
   key by signing a challenge.

Federation adds one thing: **which networks' root keys to trust**, and so
which network a certificate belongs to. The formats are in
[link.md](link.md#networks):

- **Each network publishes its root keys** at
  `https://<domain>/.well-known/open-network/roots.json`, each key with a
  signature that proves the publisher holds it, for that domain.
- **Every game has a list of networks**: each one's domain and root keys.
  The list is a signed document, like the signed table of network versions
  ([versioning.md](versioning.md)), so it can be updated without a new
  release. It has its own signing keys (a primary and a recovery key),
  never the table's. A game gets it from its own network's site and ships with the
  copy it had at release.
- A network asks to be listed by publishing its roots.json and asking the
  list's publisher. Listing means "this network's names are checked",
  nothing more; it gives nobody any access to anyone's servers.
- A game, server or player may also add or remove networks locally (a
  setting), for private or test networks. The game's own network is never
  changed by a list or a setting.
- A game finds a certificate's network by the root key that signed its
  issuer certificate. No root key may belong to two networks.
- Short-lived certificates mean no network has to run an always-on check
  for others: a removed device simply can't renew. Each network publishes
  its own revocation list (CREV) for the rest of a certificate's life.
  Other networks' lists aren't checked in this version: the 7-day device
  certificate is the limit, so a revoked device of another network shows
  as verified until its certificate expires. Checking them is later.

## What each network runs

| Piece | What it does | Required? |
| --- | --- | --- |
| Root keys | sign the issuer certificate; kept offline | yes |
| roots.json | the root keys, published on the network's domain | yes |
| Issuer | signs device certificates and the revocation list | yes |
| Sign-in and profiles | accounts, linking a game copy, handles | yes |
| Game list | its games, in the Delta List format ([list.md](list.md)) | optional |
| List of networks | serves the signed list its games read | optional |
| Stats | reports and service records ([stats.md](stats.md)) | optional |
| Moderation | bans and reports for its own players and servers | its own choice |

A network can be as small as one site and one signer process.
[delta-server](https://github.com/ChupathingyCE/delta-server) (MIT) runs one
from a settings file: its own domain, roots.json, issuer and signer, with
a tool that makes root keys, issuer certificates and signed lists.

## Plain accounts

A network may also run accounts without certificates: IDs alone, with no
root keys and no issuer. Its players sign in, keep a profile and play as
usual. No game can check such a name, so it shows as a plain name, the
same as a player's game name ([Verified names](peer.md#verified-names)).
A name checked against a certificate is a level above it: the game shows
the verified mark beside it. A plain name never shows the mark, and one
that looks like a verified player's handle is masked as for anyone else.

A network can start with plain accounts and add certificates later. Its
players' names gain the mark once it does.

## Between networks

What works across networks from the start:

- Joining any game, with names checked as above.
- Seeing which network a player belongs to.
- Game lists: a game may read several networks' lists and show them together.

What would come later, network to network, only where both sides agree:

- Friends, invites and parties across networks.
- Shared ban lists: each network decides whose lists it reads, as servers
  already can with shared ban lists ([control.md](control.md)).

Bans, reports and moderation always stay with each network. One network
can't ban another network's player everywhere; a server owner decides who
plays on their server.

## For a port or fork

A port that only wants to play with everyone needs nothing here: the legacy
protocol and Delta Peer already work ([ports.md](ports.md)).

A port or fork that wants its own accounts and verified names:

1. Run an issuer and sign-in (the formats are in [link.md](link.md)).
2. Make root keys, publish them at your domain, and ask to be listed.
3. Your players' names then show and verify in every game that speaks the
   spec, as `handle:yourdomain`.

Today, before federation exists, a port can register an app and sign its
players in with Chupathingy's network ([clients.md](clients.md)).

## Order of work

1. Client IDs and scopes for apps, so apps don't share one identity (done).
2. Qualified names (`handle:domain`) in the game and the site, with today's
   names read as `:chupathingy.org`. The network comes from the root key
   that signed a certificate, so no certificate format changes
   ([link.md](link.md#networks), proposal).
3. The signed list of networks, roots.json, and a local setting to add or
   remove a network ([link.md](link.md#networks), proposal).
4. A reference issuer that any network can run: delta-server, published
   for review; nobody should run it on the internet before its security
   review.
5. Later: other networks' revocation lists, roles and bans by domain, then
   friends, invites and parties between networks.
