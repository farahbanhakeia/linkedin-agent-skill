---
name: job-hunt
description: Walk a job application end to end — find offers, tailor the CV, write the recruiter message, send after your go-ahead, track it. Start here for a new application round.
disable-model-invocation: true
---

# Job Hunt

The path from "cherche des offres" to a logged application. Each step is its own skill; this map only says what comes next and when to stop for a decision. **Check for a duplicate before any work, and never send without the user's yes to the final CV and message. This is the skill.**

Shared data lives in `~/Documents/candidature/`: `profil-maitre.md` (source of truth, hard dependency for every step), `offres/`, `cv/`, `suivi-candidatures.csv`.

## Main flow

1. **Profile check** (first for any on-ramp that leads to a CV, a message or a send) — `profil-maitre.md` missing → stop and ask for a CV to build it. `⚠️ À CONFIRMER` lines → list them and ask the user to confirm in chat; unconfirmed or user away → proceed, those facts are off limits for this run.
2. **`/job-offer-finder`** — verified shortlist, tracked offers excluded. Stop and let the user pick which offers to pursue (away → top 3).
3. **`/application-tracker` `check`** — run it before any work on each chosen offer, even one the finder returned. Exit 2 → skip it. Exit 6 (already `préparée`) → go to step 6 with the existing CV and message, or redo 4–5 if the user wants them refreshed.
4. **`/ats-cv-tailor`** — one tailored one-page PDF + gap report per offer. No one-page PDF after its cuts → stop, show the gap report, ask the user before continuing.
5. **`/recruiter-message-writer`** — the message for the offer's channel, with its count. Over the channel limit → have the writer shorten it before step 6; still over → ask the user which lines to cut.
6. **Decision point** — show CV path, gap report, and message; the user validates or asks for edits. No validation, no sending.
7. **`/submit-application`** — sends through the channel after the explicit yes, then logs `envoyée` (`add`, or `update --id` when the entry was `préparée`).

## On-ramps

- The user pastes an offer URL or text → step 1, then fetch it (`WebFetch`, or Claude in Chrome `get_page_text` for LinkedIn), save it to `offres/` with the `/job-offer-finder` offer-file template, then step 3.
- The user already has a CV for the offer → steps 1, 3, then 5.
- CV and message already prepared (a `job-hunt-batch` lot, statut `préparée` in the tracker) → steps 1, 3 (expect exit 6), then 6.
- "Où j'en suis ?", "j'ai relancé", "entretien / refus chez X" → `/application-tracker` `list` to get the id, then `update --id <id> --statut relance|entretien|refus|offre`.

## Standalone

- **`/linkedin-profile-optimizer`** — off the flow; run it once before a search round so recruiters find the profile the CV points to.
- **`/linkedin-post-writer`** — off the flow; use it to publish a project or milestone from the master profile between application rounds.

Unattended batches (find + tailor + message for several offers, stopping before step 6) are the job of the `job-hunt-batch` agent, which walks this same path.
