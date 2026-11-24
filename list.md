# Delta List

Delta List is the game list: a host (a player's, or a server) announces its
game to the site and withdraws it, and clients read the list. It is
optional for play: system link and invites work without it. Delta's
additions to a plain listing:

- the host's Delta flag and capability summary in the announcement, so the
  list can show "ChupathingyCE" games, Halo PC maps, co-op and so on;
- the legacy number as announced, and the range a client accepts, so the
  list only offers games a client can join;
- the plain-text console list keeps its format; new fields go only at the
  end of a line, never changing existing ones.

## Where public games are

A host of a public game (a player's or a dedicated server) does two things
at once:

- it publishes a signed listing of its game on internet play's brokers
  (the flags and stamp are in [registry.md](registry.md#internet-listing));
- it announces the game to the site (`POST /v1/announce`, below), when the
  game has no password and its host hasn't turned listing off.

So a client that reads only the brokers already sees every public game a
host lists there, password games included. The site's list
(`/v1/games.txt`) adds the extras: Delta's fields, and games announced to
the site alone. OpenCE's brokers are public MQTT brokers. The site also
reads them, and OpenCE's public master list: a game found there and not
announced shows on the site's list as OpenCE's protocol. Chupathingy's
client reads both the brokers and the site's list, and either one alone
still shows the games it carries.

## The announcement

`POST /v1/announce`, form encoded (`application/x-www-form-urlencoded`,
UTF-8). The fields, in the order Chupathingy's builds send them; the site
reads each by name, and a field it doesn't know is ignored:

| Field | What it is |
| --- | --- |
| `invite` | the game's internet play invite, 64 characters, as in its invite link |
| `name` | the game's name, UTF-8. Send at most 16 characters: Chupathingy's clients show no more. The site takes up to 32 |
| `map` | the map's name as the game loads it (`bloodgulch`; `<file>@ce` and the other forms in `family` below) |
| `map_title`, `map_pack`, `map_tag` | optional: an Xbox map pack's map's own name, its pack and the pack's tag; or an MCC map's own name with `map_tag` `MCC` |
| `workshop_id`, `workshop_title` | optional: an MCC map's Steam Workshop item |
| `engine` | the game type's engine: 1 CTF, 2 Slayer, 3 Oddball, 4 King of the Hill, 5 Race, 6 Bomb ([peer.md](peer.md)) |
| `gametype` | optional: the game type's name |
| `players`, `maximum_players` | the players in the game, and its limit |
| `open` | `1` when the game takes joins now, else `0` |
| `score_limit` | the game type's score limit |
| `teams` | `1` for a team game, else `0` |
| `version` | the network version the host announces |
| Delta's fields | below ([The host's fields](#the-hosts-fields)) |
| `locked` | optional: `1` while the host takes no new machines |
| `playlist` | optional, a dedicated server's: its playlist's id on the site, `a-z 0-9 _`, at most 32 characters |
| `badge_cert`, `badge_time`, `badge_signature` | optional, a dedicated server's: its server badge (dormant: no badge key is issued yet) |
| `roster` | last: the players, `team:name` joined by `\|` (`0:Alice\|1:Bob`; team -1 in a game without teams), a name holding no `\|` |

The roster goes last so that a cut-short form loses only players.

The site answers 200 and `ok <seconds>` when the game is listed: it stays
listed that long (75 seconds today) unless announced again. Any other
answer is a refusal, with its reason as text, for example:

| Answer | What it means |
| --- | --- |
| `listed from another address` | the invite is already listed by another address |
| `too many games from this address` | this address lists as many games as it may |
| `taken off the list` | the game was taken off the list, and isn't listed again now |
| `the list is full` | the list takes no new games now |

A host that is refused waits before it tries again (Chupathingy's wait 15
seconds) and never retries at once.

`POST /v1/withdraw` with the one field `invite` takes the game off the
list. Only the address that announced the game can withdraw it. A host
withdraws when it stops hosting, when its game turns private
or gets a password, and before it lists a new invite. A game whose host
stops announcing drops off the list by itself after a while, so a host
that quits without withdrawing is no harm.

## The host's fields

A host's announcement (`POST /v1/announce`, form encoded; `browser.c`'s
`host_fields`) adds, after `version` and before the roster (which stays
last):

| Field | What it is |
| --- | --- |
| `delta` | the Delta major the game is hosted with, or `0` for the legacy protocol alone (`network.protocol = "opence"`, or the Delta port taken); left out until Delta Peer has run a frame |
| `platform_key` | the host machine's platform key (see "Platform keys"), 16 hexadecimal digits |
| `arch` | `x64`, `x86`, `arm64` or `arm` |
| `build` | the build's version (`0.7.1b`) |
| `capabilities` | the capabilities it offers, 8 hexadecimal digits; two bits are set here alone: 12 (`ping`), by a host that answers pings before joining, and 18 (`host_cheats`), by a host with `network.host_cheats` on |
| `machines` | while hosting with Delta: the game's machines by platform, `pc_linux:2,xbox:1,legacy:1` (`legacy`: a machine without Delta; `unknown`: a Delta machine that does not share its platform; a dedicated server leaves itself out). Counts only, never a player |

Compatibility both ways: a site from before these fields ignores them (it
reads the fields it knows), and the site reads each on its own, leaving out
one it can't read rather than refusing the announcement, so older builds
(which send none) and newer ones (a longer platform key, a platform it
doesn't know) are listed as ever.

## The game list's lines

`GET /v1/games.txt` is plain text, one game a line, fields separated by a
tab. A line's first fields:

| Field | What it is |
| --- | --- |
| 1 | `invite` |
| 2 | `name` |
| 3 | `map` |
| 4 | `engine` |
| 5 | `players` |
| 6 | `maximum_players` |
| 7 | `open` |
| 8 | `version` |
| 9 | the listing's age (Chupathingy's client doesn't read it) |
| 10 | `score_limit` |
| 11 | `teams` |
| 12 | `roster`, as announced |

`?fields=N` asks for the fields up to N; the ones after 12 are below. A
client reads the fields it gets and ignores any past the ones it knows; a
line with fewer than 8 fields, or an invite that isn't 64 characters, is
skipped. Some games are listed only to a client that asks for them: a game
on engine 6 (Bomb) only with `fields` of 19 or more, and a co-op game only
with `coop=1`.

From them the site lists each game's `platform`, `hosting` (`official`:
Chupathingy's `[C]` servers, by their hosts; `dedicated`; `player`),
`protocol` (`delta`, `opence`), `family` (by the map's name: `xbox` an Xbox
map; `ce` Custom Edition, `<file>@ce`; `pc` Halo PC retail, `<file>@pc`;
`md` HaloMD, `<file>@md`; `pack` an Xbox map pack's map, `<file>@<pack>`;
`mcc` an MCC map, `mcc_maps\<package>\<level>`) and `machines`; OpenCE's
public games (the brokers) are `opence` and nothing more. The game's
browser reads them from `/v1/games.txt?fields=28&coop=1` (field 13 the
region; 14 to 17: platform, hosting, protocol, machines; 18 an
OpenCE game's gametype; 19 the announced capabilities; 20 to 22 an Xbox map
pack's map name, pack and tag; 23 the playlist; 24 `opence_server` for an
OpenCE dedicated server's game; 25 `1` when the host's joins are locked; 26
and 27 a server badge and its label; 28 the server key its certificate
names; `coop=1` asks for co-op games too, which the
list leaves out unless asked). A list from before a field sends fewer, and
the browser reads what it gets. It shows them: the Online
Games screen's rows (a platform tag before the name, `SRV` for a server), its details (a Host line; the machines beside IN GAME;
"Host cheats on" beside the status for a host with bit 18) and the PC menus'
Server Browser's Rules line. The console list adds platform, hosting and
protocol after its tenth field, which Warthog's reader passes over.

A player's own copy also says its platform (`"platform"`) when it confirms
its line (`/v1/claim`) or reports a game it joined (`/v1/client_report`),
for the site's "Played on" profile badges.

## Announcing from another client

`POST /v1/announce` is open to any client, not only Chupathingy's. A port,
fork or tool that hosts a game anyone can join from its invite may
announce it:

- **Say who you are.** Put your own build name and version in `build`
  (`myport 0.3`, never a Chupathingy version) and your platform key in
  `platform_key`, with your platform's number from the registry
  ([registry.md](registry.md#platforms)). Send `delta` `0` unless your
  host answers HELLO.
- **Announce on change, plus a keep-alive.** Chupathingy's hosts announce
  when the game changes (players join or leave, the map or the game type
  changes), at most once every 3 seconds, and otherwise every 20 seconds
  to keep the game listed. After a failed announcement they wait 15
  seconds. Never announce every frame.
- **Withdraw when you stop** (`POST /v1/withdraw`).
- **Read the list the same way** ([The game list's lines](#the-game-lists-lines)).
  A game you announce shows with the platform your key names.

Announcing is optional: every browser that reads the brokers already sees
a game listed there ([Where public games are](#where-public-games-are)).

## Pings before joining

Online Games shows each listed game's ping before joining: a measured one
where the host answers, `~NN` (an estimate) where it can't, nothing where
nothing is known; sorting by Ping puts measured first, then estimated, then
none. The numbers fill in as they arrive.

There was nothing to reuse: Halo PC servers answer GameSpy queries on
their game port, but nothing of that is in the decomp, OpenCE or our
builds, and no client knows a host's address before signalling (the list
never gives one). Player hosts and dedicated servers are reached the same
way, so one mechanism serves both: a probe through signalling, then a
small ping on the host's tunnel socket bound to the probe.

Signalling (sealed with the invite token's key and published on the
host's topic, like JOIN; OpenCE and older builds act only on `J` there):

| | Layout |
| --- | --- |
| PROBE (`P`), prober to host | `'P'`, version 1, probe id (16, random), reply id (16, random a run; the answer goes to `hceu/3/<its hex>`), address count (1, at most 4), addresses (6 each) |
| PROBE_ANSWER (`Q`), host to prober | `'Q'`, version 1, probe id (16), the host's Ed25519 key (32), address count (1, at most 4), addresses (6 each), Ed25519 signature (64) of `"chupathingy probe"` and everything before it |

A prober takes an answer only when the key's X25519 form hashes to the
invite's host hash and the signature checks, so no one watching the brokers
can point it at another machine.

The tunnel socket (magic `0x6A`; the tunnel's is `0x69`; older builds drop
it unread): every datagram 24 bytes: magic (1), type (1: PING, 2: PONG, 3:
PUNCH), sequence (2), probe id (16), the prober's clock (4, echoed).

A probe is never a peer: no session, no X25519 work, no virtual address,
no stand-in, no broadcast, no slot, no player count; the game never hears
of it. The host keeps its id in a 16-entry table for 10 seconds, and
answers a PING only with a live id, with a PONG of the same 24 bytes, to
the PING's source.

| Limit | |
| --- | --- |
| new probes a host takes | 8 at once, then one each 250 ms |
| a probe's answer said again (the prober's resend) | at most once a second, at no new cost |
| PONGs a probe | 8 |
| the host's PUNCH (for a host behind NAT) | 2 rounds to at most 4 addresses, stopped by the first PING |
| a prober's probes at once | 4 |
| PROBE resent | every 1.5 s, 3 times; given up after 5 s |
| PINGs | every 200 ms to each address, until 3 PONGs or 5 s; the lowest round trip is shown |
| a host measured again | after 60 s (a failed one too) |

Amplification and spoofing: a PONG is never larger than its PING, and a
PING without a live id gets nothing. Probe ids can be read by anyone with a
listed game's token watching the brokers, so a spoofer can at most have 8
PONGs of 24 bytes sent to a victim per id, after paying for a sealed MQTT
publish (larger than that) within the brokers' own limits and the host's 4
new probes a second. The PUNCH goes to addresses the prober names, as
JOIN's punch does today, within the same budget. A forged PONG can only
make one row's number wrong; the number is never used for anything else.

Privacy: no address is shown or logged (the log says "answering pings",
"pinging the listed games", counts only). The prober learns a host's
addresses only through its signed answer, as joining does, and keeps them
in memory. A host sees a prober's public address, as it sees anyone's who
joins; `network.ping_games = false` turns probing off (estimates only).

Estimates: `GET /v1/anchors.txt` lists `anchor<TAB>host<TAB>port<TAB>
regions` lines (regions: continents `EU` or countries `EU-DE`, as a game's
region). The client times a TCP connection to each (twice, the lower kept;
nothing is sent), once a run, the first time Online Games opens with online
play on, and estimates a game from its region: the lowest anchor naming its
country, else its continent. The site's defaults are our own hosts for
North America and a cloud provider's regional endpoints elsewhere
(`--anchors` replaces them).

Compatibility: only hosts that announce bit 12 are probed; older hosts show
an estimate or nothing. A site from before field 19 gives no capabilities:
no probes, estimates only if it has anchors. Nothing else changes meaning,
and the legacy table's per-capability kill switch turns `ping` off (no
answering, no probing). No pings at all with online play off.
