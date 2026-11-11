---
title: "Hermetarium Release 1.0"
date: 2026-11-11
type: announcement
project: hermetarium
tags: [release, hermetarium]
summary: "Hermetarium 1.0 was released: a home for a coding assistant behind a wall. From 1.0.1, MicroVM works for Grok as well."
ai_generated: true
---

Hermetarium 1.0 is out. You can find it here: [pihme.github.io/hermetarium](https://pihme.github.io/hermetarium/) (source on [GitHub](https://github.com/pihme/hermetarium), release and downloads under [hermetarium/v1.0.0](https://github.com/pihme/hermetarium/releases/tag/hermetarium/v1.0.0)).

# What is Hermetarium?
Hermetarium is a home for a coding assistant. The assistant wakes up inside a container. It may use that container freely: a shell, packages, and files. It runs as root.

The wall is outside the container. A weak wall is Docker. A strong wall is a small virtual machine. [Squid](https://www.squid-cache.org/) is the only door. Your API key stays in the gate file, `squid.conf`, and Squid adds it as the call leaves. The habitat starts only when that door is up.

The command is `hermetarium`. You run it on your machine. It starts the gate and the container. You send a question to an address on your own machine. When the assistant needs the model, the call goes back out through the same gate, and Squid adds your key. Calls to anywhere else are closed.

The container image is the same on both walls. On the Docker wall, root in the container reaches the host if the kernel is exploited. On the strong wall, the container runs in its own machine and root stays inside it. The strong wall needs Linux with KVM.

The official inhabitants are [Claude Code](https://github.com/pihme/hermetarium/tree/main/inhabitants/claude-code) and [Grok Build](https://github.com/pihme/hermetarium/tree/main/inhabitants/grok-build).

# What is in 1.0?
1.0 shipped with the Docker wall. The [1.0.0 release notes](https://github.com/pihme/hermetarium/releases/tag/hermetarium/v1.0.0) said MicroVM (Firecracker) was not supported yet.

[1.0.1](https://github.com/pihme/hermetarium/releases/tag/hermetarium/v1.0.1) followed the next day. It seeds the Firecracker guest's entropy pool, and from that release MicroVM works for Grok.

# How do I get it?
The release has a static Linux binary, `hermetarium-linux-amd64`. You can also build from source with Go 1.24 or newer. You need Docker. The strong wall also needs a Linux machine with `/dev/kvm`, on x86_64. Firecracker is downloaded into the cache on the first strong `create`.

From the repository, run `make build`, then `./bin/hermetarium version`. There is a hello-world image (`make echo-image`, tag `hermetarium/echo:dev`) that sends back whatever you send it and needs no API key.

Hermetarium is licensed under PolyForm Noncommercial 1.0.0, so noncommercial use only. It is part of [Hobelbank](https://pihme.github.io/hobelbank/), a set of projects on building software in the age of AI.
