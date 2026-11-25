---
name: job-hunt-batch
description: Run one unattended job-hunt round for junior Data Scientist / AI Engineer / Data Engineer roles — find and verify fresh offers, prepare a tailored one-page CV and recruiter message for each, log them as "préparée", and stop before sending. Launch when the user says "lance une session de candidatures", "prépare-moi un lot d'offres", "run a job-hunt batch", or wants applications prepared while they are away.
---

You run one round of the job-hunt pipeline without the user present. You prepare; you never send: do not run the `/submit-application` skill, do not click Apply, do not send e-mails or LinkedIn messages. Work in the user's language (French by default).

1. **Entry.** Inputs: optional count N of offers to prepare (default 5) and optional criteria overrides. `Read` `~/Documents/candidature/profil-maitre.md`; if it is missing, stop immediately and report that the master profile must be created first. Note every `⚠️ À CONFIRMER` line: facts on those lines are off limits for this run; list them once in the hand-back, not per row.
2. **Find.** Run the `/job-offer-finder` skill with the criteria. A login wall or CAPTCHA on one source is the finder's per-source stop, not a run stop. Continue only when it delivers a verified shortlist with saved offer files. Zero verified offers → stop and report the sources tried and the drop reasons.
3. **Per offer, walking the shortlist in the finder's rank order:**
   - Run the `/application-tracker` skill `check --entreprise --poste --lien`; exit 2 or 6 → skip the offer and note it (already applied / already prepared).
   - Run the `/ats-cv-tailor` skill; keep going only if it returns a one-page PDF path and a gap report; otherwise skip the offer and note "rendu > 1 page".
   - Run the `/cover-letter-writer` skill; keep going only if it returns a one-page `<slug>.lettre.pdf`; otherwise note "lettre > 1 page" and continue without it.
   - Run the `/recruiter-message-writer` skill for the offer's channel (its own away-mode rules apply); `Write` the message to `<slug>.message.txt` next to the CV (`<slug>` = the CV PDF's basename).
   - Run the `/application-tracker` skill:
     `add --entreprise "<e>" --poste "<p>" --lien "<url>" --source <source> --canal <canal> --localisation "<lieu>" --type_contrat <contrat> --statut préparée --cv "<pdf>" --message "<slug>.message.txt" --notes "lot <date> ; lettre <slug>.lettre.pdf"`
     (all values from the offer file). Keep the returned id.
4. **Stop condition.** Stop when N offers are prepared, when the shortlist is exhausted, or when the same skill fails on two consecutive offers (two consecutive "rendu > 1 page" count as failures). A blocker on one offer's page (login wall, CAPTCHA, render failure) skips that offer; a blocker that stops every source ends the run.
5. **Hand back.** Report in this shape and end:

```md
## Lot du <date> — <n> candidatures préparées, <m> ignorées

| # | Id suivi | Poste | Entreprise | Lieu | Canal | CV | Lettre | Message | Écarts must-have |
|---|---|---|---|---|---|---|---|---|---|

**Points à confirmer dans profil-maitre.md (exclus de ce lot) :** <lignes ⚠️, ou "aucun">
**Ignorées :** <offre — raison (déjà postulé / déjà préparée / rendu > 1 page / login requis / …)>
**Sources épuisées / bloquées :** <…>

Chaque offre est déjà dans le suivi avec le statut `préparée` (id ci-dessus) ; à l'envoi, le tracker fera `update --id`, pas `add`.
Pour envoyer : ouvrez chaque CV et message, puis lancez `/job-hunt` (on-ramp « CV et message déjà préparés ») ou dites « postule à #1 » — chaque envoi demande votre validation explicite.
```
