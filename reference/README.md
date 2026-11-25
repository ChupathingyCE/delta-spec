<!--
SPDX-FileCopyrightText: 2026 Milenko x Horrible Dev
SPDX-License-Identifier: MIT
-->

# Delta reference client

A small C99 client for Delta Peer, for other people's ports of Halo: the
handshake, the capability bits and the game's advertisement. The guide is
[ports.md](../ports.md).

```sh
make            # builds delta_ref.o and runs the tests (BUILD=dir for elsewhere)
python3 conformance.py --help
./loopback_host.sh --help
```

| File | What it is |
| --- | --- |
| `delta_ref.h`, `delta_ref.c` | the client: no allocation, no threads, no OS calls but your send function |
| `delta_ref_test.c`, `golden.h` | its tests, against packets our own code wrote |
| `conformance.py` | checks a port's packets (and a port host's, with `check --host`) and its advertisement, or stands in for a host on 127.0.0.1 (for a port host, with `listen --project`) |
| `conformance_test.py` | conformance.py's own checks (`python3 conformance_test.py`) |
| `federation_vectors.json` | test vectors for federation ([link.md](../link.md#networks)): two networks' roots.json, certificates and a signed list of networks, TEST keys only. delta-server's `node/federation.py` (MIT) reads and checks them |
| `loopback_host.sh` | our dedicated server on 127.0.0.1 alone, to join from your port |
| (game side) | `tools/delta_ref_capture/` in the game's repository makes `golden.h` from the game's own code and tests this client against its real host |

## On bare metal

The client calls nothing, but a compiler may still emit calls to `memset`
and `memcpy` for struct copies and clears, so a port without a C library
must supply those two. It may also add a stack protector that wants
`__stack_chk_guard` and `__stack_chk_fail`; build with
`-fno-stack-protector` to leave it out.

MIT ([LICENSE](LICENSE)). The spec around it is CC BY 4.0.
