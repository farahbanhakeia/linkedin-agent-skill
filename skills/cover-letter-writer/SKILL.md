---
name: cover-letter-writer
description: Write a one-page lettre de motivation / cover letter as a PDF for one specific job offer, from the user's master profile, with the offer's requirements answered by real proofs. Use when the user says "lettre de motivation", "cover letter", "lettre pour cette offre", "rédige ma lettre", "LM en PDF", or asks for a letter to attach to an application. Not for a short recruiter message or e-mail (that is the recruiter message writer).
---

# Cover Letter Writer

A recruiter skims the letter for one thing: does this person answer *our* requirements with evidence? **Each body paragraph answers one requirement of the offer with one proof from the profile. This is the skill.** No paragraph about passion, no paragraph about the company's greatness.

Write in the offer's language; reply in the user's language. Output: `~/Documents/candidature/cv/<slug>.lettre.pdf` next to the CV, `<slug>` = the CV PDF's basename (or `LM_<Nom>_<Entreprise>_<Poste>` if no CV exists yet).

## Phase 1 — Inputs

- **Offer**: path in `~/Documents/candidature/offres/`, URL (`WebFetch`; LinkedIn via Claude in Chrome `get_page_text`, else ask for a paste), or pasted text. Extract company, exact title, reference if any, the recruiter's name if shown, and the 3 requirements the offer insists on most.
- **Profile**: `Read` `~/Documents/candidature/profil-maitre.md`. Hard dependency: without it, ask for a CV. `⚠️ À CONFIRMER` items: ask once if needed; user away → leave them out (no availability claim beyond "disponible rapidement", flagged).
- If the `/ats-cv-tailor` skill already ran on this offer, reuse its keyword table and gap report instead of re-deriving them.

**Gate:** company, title, three requirements, and for each a proof line from the profile (or an honest gap to acknowledge in one clause).

## Phase 2 — Draft the spec

Body = 4 paragraphs, 220–320 words in total, in this order:

1. **Accroche** (2 sentences): the exact title, where you saw it, and the one element of the offer that matches your trajectory (a mission, a stack, a sector), not a compliment.
2. **Preuve 1** (3–4 sentences): the requirement they rank first → the experience or project that proves it, with the offer's own keywords, dates and tools as in the profile, a result when the profile has one.
3. **Preuve 2 + honnêteté** (3–4 sentences): the second requirement → second proof. If a must-have is Missing or Partial in the gap report, one clause names it truthfully ("notions de Spark, que je compte approfondir") instead of hiding it.
4. **Ce que j'apporte + demande** (2–3 sentences): how you would work in the first months (concrete, tied to the offer), availability, interview request.

```json
{
 "expediteur": ["<Nom>", "<Ville, Pays>", "<Téléphone>", "<E-mail>", "<LinkedIn>"],
 "destinataire": ["<Entreprise>", "<Nom du recruteur ou Service recrutement>", "<Ville>"],
 "lieu_date": "<Ville>, le <jour mois année>",
 "objet": "Candidature au poste de <titre exact>",
 "salutation": "<Madame X, | Monsieur X, | Madame, Monsieur,>",
 "paragraphes": ["<accroche>", "<preuve 1>", "<preuve 2 + honnêteté>", "<apport + demande>"],
 "formule": "Je vous prie d'agréer, <Madame, Monsieur>, l'expression de mes salutations distinguées.",
 "signature": "<Nom>",
 "pj": "CV"
}
```

**Do NOT open with the generic sentence.**

```
WRONG: "Passionnée par la data et l'intelligence artificielle, je souhaite mettre mes compétences au service de votre entreprise innovante."
RIGHT: "Votre offre de Data Engineer Junior met l'accent sur des pipelines Python/SQL fiables : c'est le travail que j'ai fait six mois chez Marsa Maroc sur des données de trafic maritime."
```

**Gate:** save the four paragraphs to a temp file and count with `python -c "print(len(open('lm.txt',encoding='utf-8').read().split()))"`: 220–320 words; every fact traceable to a profile line; each paragraph names one offer requirement; no banned opener ("passionnée", "dynamique et motivée", "votre entreprise innovante").

## Phase 3 — Render

```
python -I "<skill dir>/assets/render_letter.py" "<cv dir>/<slug>.lettre.json" "<cv dir>/<slug>.lettre.pdf"
```

Hard dependency: Python 3 with `reportlab` and `pypdf`. Exit 5 → cut paragraph 4 to two sentences, then paragraph 1 to one, then `--scale 0.95`, then `0.9`. Open the PDF once with `Read`.

**Gate:** exit 0, one page, layout clean.

## Phase 4 — Deliver

```md
**Lettre générée :** `~/Documents/candidature/cv/<slug>.lettre.pdf` (1 page, <n> mots)
**Exigences de l'offre traitées :** 1) … → <preuve> · 2) … → <preuve> · 3) … → <preuve ou écart assumé>
**Points à confirmer :** <⚠️ laissés de côté, ou "aucun">
```

Nothing is sent by this skill; the `/submit-application` skill attaches it with the CV.

## Anti-patterns

- **Letter = CV in prose.** Three requirements, three proofs; the rest is on the CV.
- **Praising the company.** One concrete element of the offer, then your evidence.
- **Hiding a gap the offer calls must-have.** One honest clause beats a recruiter finding it in interview.
