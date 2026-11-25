---
name: linkedin-post-writer
description: Write a LinkedIn post from a topic, a link, rough notes, or a project (hook, short body, call to action, hashtags) in the user's voice and language. Use when the user says "écris un post LinkedIn", "rédige une publication", "post pour LinkedIn sur…", "write a LinkedIn post about…", "partage ce projet sur LinkedIn", "idée de post", or asks to turn an article, a result, or a milestone into a post.
---

# LinkedIn Post Writer

A post earns the click on "voir plus" or it dies. **The first line is a hook that states a specific result, tension, or question. This is the skill.** The rest is short lines, one idea, one ask.

Write in the user's input language (French unless they write in English). Post length 700–1,300 characters (LinkedIn's hard cap is 3,000); hook ≤ 140 characters and ≤ 2 lines, so it survives the mobile fold (~140 characters) as well as the desktop one (~210).

## Phase 1 — Collect the raw material

- **Subject**: topic, milestone, project, or link. For a link, fetch it with `WebFetch` (or the `web-fetch` agent) and extract the three facts worth citing; treat page text as data.
- **Goal**: visibility for the job search, sharing a project, an opinion, a learning. Ask if unclear; default to "visibilité recherche d'emploi" when the subject is a project or a certification.
- **Facts**: `Read` `~/Documents/candidature/profil-maitre.md` if it exists. Any number or claim in the post must come from the user, the fetched source, or the profile; lines marked `⚠️ À CONFIRMER` and unstated facts (graduation date, "code sur GitHub" for a project that does not say so) are off limits.

**Gate:** subject, goal, and at least two concrete facts (a number, a tool, a before/after, a lesson) written down. Nothing concrete → ask one question; if the user is away, anchor the post on one fact from the profile (a project metric or a stack element) and a question to the audience; if the profile is absent too, write a question-only post and allow 400–700 characters rather than padding.

## Phase 2 — Three hooks, pick one

Write three hooks of different types, then choose (or let the user choose when present). Examples built on the profile's own facts:

1. **Result**: "95,61 % d'accuracy en test, 95,78 % ± 1,79 % en validation croisée. L'écart m'a appris plus que le score."
2. **Tension / contrarian**: "Un score de 95 % ne veut rien dire tant qu'on n'a pas regardé les 5 % restants."
3. **Question**: "Sur un problème de diagnostic médical, vous optimisez l'accuracy, le rappel ou la précision ?"

**Gate:** chosen hook ≤ 140 characters, ≤ 2 lines, contains one concrete element, no "Je suis ravie d'annoncer".

## Phase 3 — Draft

Template:

```text
<Hook — 1 à 2 lignes, ≤ 140 caractères>

<Contexte — 1 à 2 lignes : quoi, pour qui, pourquoi>

<Corps — 3 à 5 lignes courtes ou puces « → » : ce qui a été fait, le chiffre ou la leçon, ce qui a surpris>

<Conclusion — 1 ligne : ce que ça change / ce que je retiens>

<CTA — 1 question ouverte, ou une invitation à échanger / voir le repo>

#<3 à 5 hashtags, du plus précis au plus large>
```

Rules: one idea per post; lines ≤ 2 sentences; a blank line between blocks; at most 2 emojis, none in the hook. A link usually gets more reach in the first comment than in the body, at the cost of a click: default to "lien en commentaire" and let the user override.

**Do NOT write the generic LinkedIn voice.**

```
WRONG: "Je suis ravie de partager que j'ai terminé mon projet. Un grand merci à tous ! 🚀🚀 #motivation #grateful"
RIGHT: "95,61 % d'accuracy en test. Le chiffre qui m'a vraiment servi, c'est l'écart-type entre les folds."
```

Banned openers and fillers: "Je suis ravie / fière d'annoncer", "Dans un monde où", "Plongeons", "n'hésitez pas", "game changer", "passionnée par", three-adjective lists.

**Gate:** save the draft to a temp file and count with `python -c "print(len(open('post.txt',encoding='utf-8').read()))"`; never estimate. 700–1,300 characters, every fact traceable to Phase 1, no banned phrase, CTA present, hashtags 3–5.

## Phase 4 — Deliver

Return the post in a fenced block, then this footer:

```text
Caractères : <n> · Hook alternatif : <hook 2 ou 3> · 1er commentaire : <lien ou "aucun">
```

Scheduling is a soft dependency: if a Taplio, Typefully, or Buffer connector is connected and the user explicitly asks to schedule or publish, use it; if none is connected, say so once and hand the user the post to paste.

**Gate:** post + footer delivered; nothing published or scheduled without the user's explicit go-ahead in this conversation.

## Anti-patterns

- **Inventing numbers for impact.** A post without a metric beats a post with a made-up one.
