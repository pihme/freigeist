---
title: "Making of RAGite"
date: 2026-10-29
type: post
project: ragite
tags: [making-of, side-quest, ragite]
summary: "RAGite started off as a side quest. I wanted to have a simple RAG solution for a small project - without installing a bunch of servers. I was surprised no such solution existed. Now I know why."
ai_generated: false
---

[RAGite](https://pihme.github.io/ragite/) started off as a side quest. My main quest - which I haven't even started yet - is to develop an email client
with good search capabilities. And since emails contain sensitive information, I want this to run on local AI, not in 
the cloud. So I asked my agents what tool I could use and to my surprise there was no easy solution. Many solutions
exist for professional uses. You start a database, then a server for the embedding, another for the chunking and 
another for OCR. Not what I had in mind. I wanted a single dependency to get started - maybe I will move on to something
more sophisticated later on. But I want to start simple.

So I decided to implement it myself - or rather have it implemented by an agent. It started out with a spec, which an 
agent wrote with my input. And then I used the [`/grill-with-docs`](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) skill by [Matt Pocock](https://github.com/mattpocock/skills) and the spec got three times as
long. This was an interesting experience. Turns out it is really hard to write a spec when you don't really know what 
you want. Do I want cosine distance to rank the results? Should full text search stem the words first? Honestly,
an awful lot of questions. But I ploughed through - driven in part by wanting to see whether an agent could build it 
from spec. 

Then I was able to give the _implement it_ command and came back later. And it was done - well, not quite. Part of the 
spec was that the agent should compare different embedding models and pick one. And it completely skipped over that part.

But no worries, another agent was able to pick it up, suggest models to evaluate, suggest criteria to evaluate it by and 
a little time later a model was chosen. And my humble little [SQLite](https://sqlite.org) extension was suddenly 100 MB large. Not quite what 
I had intended, but ok.

The next improvement came when I asked another agent to build a [demo application](https://pihme.github.io/ragite-demo/) for it. This also revealed some obvious 
shortcomings. And putting an agent in two roles - one builder, one user of the library - was also interesting to observe.

After all this was done, it was time to release it at version 1.0 and show it to the world.

Next step is to return to the main quest. I want to eat my own dogfood and use it in an actual application. Working with
agents is nice and easy and all that. But the queasy feeling remains that I don't fully know what I am doing. And I hope
that when I use it in an actual application, my intuition will kick in. And then I will know whether I want to stem the 
words or not.
