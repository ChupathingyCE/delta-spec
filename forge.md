# Forge layouts

A Forge layout is a map's placed objects, spawn points, teleporters and
game type objects, saved as a file. This page is its format, byte by byte,
so any client or tool can read and write the same files. A layout made in
one client loads in another, on any platform.

## The file

- A layout is a file named `<stem>.hmv`. The stem is 1 to 28 characters of
  `a-z 0-9 _ -`. A client keeps a map's layouts in a folder of that map's
  own; where that folder is, is the client's choice.
- Every number is little-endian, whatever the machine. Floats are IEEE 754
  single precision. Signed numbers are two's complement.
- A file is at least 64 bytes (its header) and at most 65,536 bytes.
- A file is read whole or not at all: a reader checks everything below
  before it uses a byte of it, and refuses the file at the first thing
  wrong.

A file is, in order: the header, the packs, the paths, the records and the
meta. Nothing comes between them or after them.

## The header

64 bytes.

| Offset | Size | Field | What it is |
| --- | --- | --- | --- |
| 0 | 4 | magic | `HFRG` (48 46 52 47) |
| 4 | 2 | version | 1 to 7 ([Versions](#versions)) |
| 6 | 2 | header size | 64 |
| 8 | 4 | flags | bit 0: some record is not a plain object (kind 0). No other bit |
| 12 | 32 | map name | the map's short name (`bloodgulch`): 1 to 31 characters of `a-z 0-9 _`, zeros after it |
| 44 | 4 | map hash | the map's checksum (the one its cache file's header holds) when the layout was saved. A reader doesn't refuse a file for another checksum: it may say so |
| 48 | 2 | pack count | 0 to 8 |
| 50 | 2 | path count | 0 to 256 |
| 52 | 2 | record count | 0 to 256 |
| 54 | 2 | meta size | 4 to 2048 |
| 56 | 4 | payload size | the bytes after the header, exactly: the file's size less 64 |
| 60 | 4 | checksum | CRC-32 of the bytes after the header (the IEEE polynomial, reflected, 0xEDB88320; starting at 0xFFFFFFFF and ended with a NOT, as zlib's `crc32`) |

## The packs

`pack count` entries of 32 bytes. A pack is a set of extra objects the
layout was made with.

| Offset | Size | Field | What it is |
| --- | --- | --- | --- |
| 0 | 8 | recipe | two 32-bit numbers naming how the pack was made |
| 8 | 24 | name | 1 to 24 characters of `a-z 0-9 _ -` and space, zeros after it (24 characters leave no zero) |

A reader checks each name and may ignore the list: a record whose object
the reader doesn't have is skipped when the layout is placed.

## The paths

`path count` entries, each:

| Size | Field | What it is |
| --- | --- | --- |
| 4 | group | the object's tag group, a 32-bit number (below) |
| 1 | length | 1 to 127 |
| length | path | the object's tag path (`vehicles\warthog\mp_warthog`), no zero after it |

A record names its object by an index into this list, so objects travel by
path, never by a tag index. A path is 1 to 127 characters of
`a-z 0-9 _ - .`, space and `\`; it doesn't start or end with `\`, and has
no `..` and no `\\` (no empty part). No group and path come twice.

The groups a layout may name (the number is the group's four letters read
as a big-endian number, then stored little-endian like every number):

| Group | Number | Objects |
| --- | --- | --- |
| `vehi` | 0x76656869 | vehicles |
| `weap` | 0x77656170 | weapons |
| `eqip` | 0x65716970 | equipment |
| `scen` | 0x7363656E | scenery |
| `bipd` | 0x62697064 | bipeds |
| `mach` | 0x6D616368 | machines |
| `ctrl` | 0x6374726C | controls |
| `lifi` | 0x6C696669 | light fixtures |
| `actv` | 0x61637476 | AI characters (actor variants) |

## The records

`record count` entries of 48 bytes.

| Offset | Size | Field | What it is |
| --- | --- | --- | --- |
| 0 | 2 | path index | an index into the paths, or 0xFFFF for none |
| 2 | 1 | kind | what the record is (below) |
| 3 | 1 | team | signed: a team, a channel or an index, by kind |
| 4 | 12 | position | x, y, z: three floats, in world units |
| 16 | 12 | angles | yaw, pitch, roll: three floats, in radians |
| 28 | 2 | respawn | seconds, 0 to 600 |
| 30 | 1 | count | 0 to 16 |
| 31 | 2 | game types | the game types it's in, one bit each (below) |
| 33 | 1 | variant | 0 to 15; a game type object's type |
| 34 | 1 | flags | below |
| 35 | 1 | AI team | an AI character's team (below), from version 2; 0 before |
| 36 | 12 | reserved | zero |

The game types field is not aligned: read it byte by byte.

**Angles.** Yaw turns about the world's up (z), from +x toward +y. Pitch
lifts the front up from the ground. Roll turns about the forward
direction, a positive roll tipping the top to the right. Each is within
plus or minus pi (a reader allows 0.0001 past it).

**Kinds:**

| Kind | What it is | Path | From version |
| --- | --- | --- | --- |
| 0 | an object: a vehicle, weapon, equipment, scenery, machine, control, light fixture, biped or AI character | any group above | 1 |
| 1 | a squad (nothing writes it) | `actv` | 1 |
| 2 | a player spawn point | none | 4 (written); read in any version ([Checking a file](#checking-a-file)) |
| 3 | a weapon spawn (nothing writes it) | `weap` or `eqip` | 1 |
| 4 | a vehicle spawn (nothing writes it) | `vehi` | 1 |
| 5 | a game type object: a CTF flag's spot, a hill point, an oddball spawn, a race checkpoint | none | 6 |
| 6 | (refused) | | |
| 7 | a teleporter sender | none | 5 |
| 8 | a teleporter receiver | none | 5 |
| 9 and up | (refused) | | |

**Flags:**

| Bit | Value | Name | On | From version |
| --- | --- | --- | --- | --- |
| 0 | 0x01 | place at start | placed when the layout starts | 1 |
| 1 | 0x02 | AI off | an AI character's: it stands as placed | 2 |
| 2 | 0x04 | AI respawn | an AI character's: placed again its respawn time after it dies | 3 |
| 3 | 0x08 | initial spawn | a player spawn point's: a round's first spawns; without it, a respawn point | 4 |
| 4 | 0x10 | fixed | an object's: it never moves | 7 |
| 5 | 0x20 | phased | an object's: it has no collision | 7 |

**Game types:** 0x01 CTF, 0x02 Slayer, 0x04 Oddball, 0x08 King of the
Hill, 0x10 Race, and 0x20 Infection (a player spawn point's only).

**AI teams:** 0 the character's own, 1 the player's (it fights for the
player, never against), 2 human, 3 Covenant, 4 Flood, 5 Sentinel.

**Game type objects** (kind 5): the variant is the type and the team is
its index.

| Variant | Type | Indices |
| --- | --- | --- |
| 0 | a CTF flag's spot | 0 to 1 (a team) |
| 2 | an oddball spawn | 0 to 15 |
| 3 | a race checkpoint | 0 to 31 |
| 8 | a hill point | 0 to 15 (a hill) |

## The meta

`meta size` bytes: four texts, each UTF-8 ended by a zero byte, in this
order, filling the meta exactly.

| Text | Bytes before its zero |
| --- | --- |
| title | 1 to 31 |
| author | 0 to 31 |
| description | 0 to 127 |
| date | 0, or 16: `YYYY-MM-DD HH:MM` (digits where the letters are) |

Each text is valid UTF-8: no overlong form, no surrogate, nothing past
U+10FFFF, and no control character (below 0x20, 0x7F, or U+0080 to
U+009F).

## Versions

Each version adds what a record may hold. A writer writes the lowest
version that holds the layout, so a layout without the newer things stays
readable by older readers.

| Version | Adds |
| --- | --- |
| 1 | objects: place, facing, team, respawn time, place at start |
| 2 | an AI character's AI team, and AI off |
| 3 | an AI character's respawn |
| 4 | player spawn points: team (any, red, blue), game types, initial spawn |
| 5 | teleporters: senders and receivers linked by channel |
| 6 | game type objects |
| 7 | an object's physics: fixed or phased |

Later versions add to the format. **A reader refuses a version it doesn't
know**, and says the file was made by a newer client; it never reads part
of one.

## Checking a file

A reader checks, in this order, and refuses the file at the first failure:

1. **Size:** at least 64 bytes, at most 65,536.
2. **Header:** the magic; the version at least 1 and no newer than the
   reader knows; the header size 64; no unknown flag; the map name as
   above, and the map the reader expects, if it expects one.
3. **Counts:** packs at most 8, paths at most 256, records at most 256,
   meta at most 2048 bytes.
4. **Payload:** its size exactly the bytes after the header, and its
   CRC-32.
5. **Packs, paths, records and meta,** each within the file, as above.
   Every record's floats are finite and its reserved bytes zero.
6. **Each record,** for the file's version: a known kind (0 to 5, 7 or
   8); a game type object (5) only from version 6, and a teleporter (7,
   8) only from version 5. Kinds 5, 7 and 8 have their own rules (further
   below) in place of the rest of this list. For kinds 0 to 4:
   - a kind with an object (0, 1, 3, 4): its path index below the path
     count, and the path's group one the kind takes; any other kind: path
     index 0xFFFF;
   - team -1 to 7; respawn at most 600; count at most 16 (a kind 0
     object's 0 or 1); game types within 0x1F; variant at most 15;
   - no flag the file's version doesn't have; the initial spawn flag only
     on a player spawn point;
   - the AI team 0 in version 1; from version 2, 0 to 5, and the AI team
     or AI off only on an AI character's record (path group `actv`);
   - AI respawn only on an AI character's record with a respawn of 1 or
     more;
   - fixed or phased only on a kind 0 record that isn't an AI character,
     and never both;
   - positions strictly between -5000 and 5000; angles within plus or
     minus pi.

   A **player spawn point** (2) in version 4 or later also has team -1
   (any), 0 (red) or 1 (blue); game types within 0x3F (in place of 0x1F);
   no flag but initial spawn; respawn, count, variant and AI team 0. In
   versions 1 to 3, a writer never puts one, but a reader takes it under
   the list above alone: path index 0xFFFF, team -1 to 7, game types
   within 0x1F, only the flags its version has (never initial spawn), and
   no AI team, AI off, AI respawn or physics.

   In place of the list above:
   - a **teleporter** (7, 8): team (its channel) 0 to 15; respawn, count,
     game types, variant, flags and AI team 0; pitch and roll 0;
   - a **game type object** (5): a variant in the table above and a team
     within its indices; respawn, count, game types, flags and AI team 0;
     pitch and roll 0.

   Both have their floats finite, positions strictly between -5000 and
   5000, and angles within plus or minus pi.
7. **The layout:**
   - at most 32 teleporters, and every sender's channel has a receiver;
   - at most 64 game type objects, and at most 12 points in one hill;
   - the header's flag bit 0 set exactly when some record's kind isn't 0;
   - a file of version 3 to 7 holds something that version adds: an AI
     respawn (3), a player spawn point (4), a teleporter (5), a game type
     object (6), or a fixed or phased object (7).
8. **The meta:** four texts as above, the title not empty, nothing after
   the date's zero.

When a layout is placed, a reader still trusts nothing in it: a path the
map doesn't have is skipped, and its own limits (how many objects, the
map's bounds) apply again.

## Network Forge

Players forging one map together over the network exists in
[ChupathingyCE/halo-ce-vita](https://github.com/ChupathingyCE/halo-ce-vita),
not yet in Chupathingy's main game. It is negotiated between machines (no
network version changes), the host is authoritative (every edit is a
request the host checks and applies, then sends to every machine), and a
layout in this format is sent to each machine that joins. Its wire format
comes to this spec in a later pull request.
