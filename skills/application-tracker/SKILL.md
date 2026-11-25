---
name: application-tracker
description: Add, update, duplicate-check, or list job applications in the tracking sheet suivi-candidatures.csv (entreprise, poste, lieu, date, lien, CV envoyé, statut, contact recruteur). Use when the user says "ajoute au suivi", "est-ce que j'ai déjà postulé", "marque en entretien / refus / relance", "montre mes candidatures", "où j'en suis dans mes candidatures", "tableau de suivi des candidatures", "application tracker", "did I already apply", or when another skill must check or log an application.
---

# Application Tracker

One ledger, one script. Every read or write goes through `assets/tracker.py` so the CSV never gets hand-edited into an inconsistent state. **Check for a duplicate before anything is added or sent. This is the skill.**

Reply in the user's language. Ledger: `~/Documents/candidature/suivi-candidatures.csv` (override with env `CANDIDATURE_DIR`); the script creates it lazily.

## Phase 1 — Identify the operation

Map the request to one of four operations:

| User says | Operation |
| --- | --- |
| "j'ai déjà postulé ?", "doublon ?", before any add or send | `check` |
| "ajoute", "enregistre la candidature", after a submission | `add` |
| "marque en entretien", "refus", "relance", "ajoute une note" | `update` |
| "montre / liste mes candidatures", "où j'en suis" | `list` |

Required inputs: `check` needs entreprise + poste, or lien (give all three when you have them). `add` needs entreprise, poste, lien; localisation, type_contrat, source, canal, cv, message, contact are soft fields. `update` needs the `id`: get it from `list` when the user gives only a company name; two matching rows → ask which.

**Gate:** operation chosen and its required fields known. A required field missing → ask once; if the user is away, stop (an `add` without entreprise/poste/lien is refused by the script). Only soft fields missing and user away → run `add` and list the gaps in `--notes`.

## Phase 2 — Run the script

Use `Bash` with Python 3 (hard dependency, stdlib only; the script switches its own output to UTF-8):

```
python -I "<skill dir>/assets/tracker.py" check  --entreprise "ACME" --poste "Data Scientist Junior" --lien "URL"
python -I "<skill dir>/assets/tracker.py" add    --entreprise "ACME" --poste "Data Scientist Junior" --localisation "Paris" --type_contrat CDI --lien "URL" --source linkedin --cv "cv/CV_x.pdf" --message "cv/CV_x.message.txt" --canal easy_apply --statut envoyée --contact "Nom – rôle – email"
python -I "<skill dir>/assets/tracker.py" update --id 20261125-acme-data-scientist --statut entretien --notes "entretien le 02/12"
python -I "<skill dir>/assets/tracker.py" list   [--statut envoyée] [--json]
```

Statuts: `préparée` · `envoyée` · `relance` · `entretien` · `offre` · `refus` · `retirée` · `doublon`. Source: `linkedin|indeed|wttj|rekrute|site|autre`. Canal: `easy_apply|email|formulaire|autre`.

Exit codes: `0` ok · `2` duplicate (same URL, or same entreprise + poste after normalisation; `add` always refuses a duplicate, `check` returns 2 only when the match is not `préparée`) · `6` on `check`: the only match is `préparée`, so the offer is in the pipeline and the next step is `update --id`, not `add` · `3` unknown id · `4` invalid statut · `1` missing required argument.

**Gate:** the script exited 0, or exited 2 / 6 on `check` and you are branching on it as above. Any other non-zero exit → show the script's message, fix the arguments, rerun once.

## Phase 3 — Report

One line, in the user's language, quoting the script's output: the id, the statut, and for a duplicate the date of the earlier application. For `list`, paste the table as is.

**Do NOT reinterpret a duplicate as a new application.**

```
WRONG: "Candidature ajoutée pour ACME." (script exited 2)
RIGHT: "Déjà postulé chez ACME pour ce poste le 2026-11-25 (id 20261125-acme-data-scientist, statut envoyée). Rien ajouté."
```

**Gate:** the user has the id (or the duplicate's id) in the reply.

## Anti-patterns

- **Editing the CSV directly.** Breaks ids and the BOM; always go through the script.
- **Skipping `check` because the user is sure.** Run it anyway: it catches reposted offers under new URLs.
- **Inventing a contact.** `--contact` only from the offer page or the user; otherwise leave it empty.
