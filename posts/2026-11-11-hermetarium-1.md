---
title: "Hermetarium Release 1.0"
date: 2026-11-11
type: announcement
project: hermetarium
tags: [release, hermetarium]
summary: "Hermetarium 1.0 was released: a home for a coding assistant behind a wall. In 1.0.1, MicroVM works as well."
ai_generated: true
---

Hermetarium 1.0 is out. You can find it here: [pihme.github.io/hermetarium](https://pihme.github.io/hermetarium/) (source on [GitHub](https://github.com/pihme/hermetarium), release and downloads under [hermetarium/v1.0.0](https://github.com/pihme/hermetarium/releases/tag/hermetarium/v1.0.0)).

# What is Hermetarium?
Hermetarium is a home for a coding assistant. The assistant wakes up inside a container. It may use that container freely: a shell, packages, and files. It runs as root.

The wall is outside the container. A weak wall is Docker. A strong wall is a small virtual machine (MicroVM, with Firecracker). [Squid](https://www.squid-cache.org/) is the only door. Your API key stays in the gate file, `squid.conf`, and Squid adds it as the call leaves. The habitat starts only when that door is up. The command is `hermetarium`.

# What is in 1.0?
1.0 ships the Docker wall. MicroVM is not supported in 1.0.0. The follow-up release [1.0.1](https://github.com/pihme/hermetarium/releases/tag/hermetarium/v1.0.1) is already out; in 1.0.1, MicroVM works as well.

# How do I get it?
The current release has a static Linux binary, `hermetarium-linux-amd64`, under [hermetarium releases](https://github.com/pihme/hermetarium/releases?q=hermetarium). There is also Porter, under [porter releases](https://github.com/pihme/hermetarium/releases?q=porter). From source you need Docker and Go 1.24 or newer; the strong wall also needs a Linux machine with KVM, on x86_64. The handbook is on the [website](https://pihme.github.io/hermetarium/).

Hermetarium is licensed under PolyForm Noncommercial 1.0.0, so noncommercial use only. It is part of [Hobelbank](https://pihme.github.io/hobelbank/), a set of projects on building software in the age of AI.
