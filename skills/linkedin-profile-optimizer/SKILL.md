---
name: linkedin-profile-optimizer
description: Rewrite the LinkedIn profile sections (headline, About/Infos, experience bullets, skills order, featured items, open-to-work settings) for a target role, using only facts from the user's master profile and the keywords recruiters search. Use when the user says "optimise mon profil LinkedIn", "améliore mon titre / ma section Infos", "mon profil pour un poste de…", "rewrite my LinkedIn headline / About", "profil LinkedIn recruteurs", or asks why recruiters don't find them.
---

# LinkedIn Profile Optimizer

Recruiter search is keyword search on the headline, About, skills, job titles, plus hard filters on location and open-to-work preferences. **Put the target role's exact search terms in the headline and the first lines of About, backed by true facts, and set the filterable fields. This is the skill.**

Write in the language the user's profile is in (French by default); reply in the user's language.

## Phase 1 — Target and current state

- **Target role**: one title, or two adjacent ones in the headline ("Titre 1 · Titre 2"), never three; more → ask which two; away → the first two from the profile's "Cibles de recherche". Write gendered forms out ("Ingénieure IA Junior", not "Ingénieur(e)").
- **Master profile**: `Read` `~/Documents/candidature/profil-maitre.md`. Hard dependency: without it, ask for a CV; never write from memory.
- **Current LinkedIn text** (optional): ask the user to paste headline + About, or open their profile with Claude in Chrome (`navigate` to `https://www.linkedin.com/in/me/`, click "voir plus / see more" on About, then `get_page_text`) while they are signed in. Neither available → skip the diff and write fresh.

`⚠️ À CONFIRMER` rule: a flag covers the whole block it sits in (an experience's heading and bullets) or the single field it names (a year, a city, availability). Ask once, listing every flagged item you want to use. Unconfirmed or user away → omit flagged experiences entirely; for a flagged field write `[À CONFIRMER : année]` in the deliverable and list it under "⚠️ À confirmer avant de coller".

**Gate:** target title(s) fixed; profile loaded; flagged items resolved as above.

## Phase 2 — Keyword set

List 12–20 terms recruiters type for the target role: the title and its variants (FR + EN), 6–8 hard skills, 2–3 domains, 1–2 contract/location terms ("junior", "Maroc", "France", "télétravail"). Keep only terms the profile supports.

**Gate:** every keyword has evidence in the profile.

## Phase 3 — Rewrite each section

LinkedIn limits: headline 220 characters; About 2,600 characters, of which only the first ~250 show on mobile before "voir plus"; experience title 100 characters, description 2,000; up to 100 skills, with up to 5 "Top skills" shown first.

```md
## Titre (≤ 220 caractères) — <n caractères>
<Titre 1 · Titre 2> | <2–3 compétences clés> | <diplôme : Master SDSI> | <ouvert à : Maroc · France · télétravail>

## Infos (≤ 2 600 caractères ; le titre cible dans les 250 premiers caractères) — <n caractères>
<Ligne 1–3 : qui je suis + rôle cible + 3 mots-clés>

<Paragraphe 2 : 2–3 preuves concrètes (stage, projet, chiffre) avec mots-clés>

<Paragraphe 3 : stack en liste courte : Python · SQL · Scikit-learn · PyTorch · Power BI · …>

<Dernière ligne : ce que je cherche + comment me contacter>

## Expériences
### <Titre tel qu'un recruteur le chercherait, ≤ 100 caractères> — <Entreprise> · <dates ou [À CONFIRMER : année]>
- <3 puces : verbe d'action + mot-clé + résultat ou périmètre, tirées du profil>

## Compétences
- Top skills (5) : <les 5 mots-clés les plus recherchés pour le rôle>
- Ensuite, par pertinence : <…> ; retirer celles hors cible

## À la une (suggestions)
- <repo GitHub du projet le plus pertinent> · <portfolio> · <post ou PDF>

## Paramètres (filtres recruteurs)
- Localisation du profil : <ville, pays confirmés dans le profil, sinon [À CONFIRMER]>
- Open to work : titres <jusqu'à 5> · zones <…> · télétravail / sur site / hybride · type de contrat · disponibilité <du profil ou [À CONFIRMER]>

## ⚠️ À confirmer avant de coller
- <chaque [À CONFIRMER] ci-dessus, ou "aucun">
```

Rules: job titles may be clarified to the market term ("Stagiaire Data Analyst" → "Data Analyst (stage)") but never promoted ("Stagiaire" → "Ingénieure"). Levels stay as in the profile ("LangChain — en approfondissement").

**Do NOT write a buzzword headline.**

```
WRONG: "Passionnée par l'IA | Innovatrice | Future leader de la data 🚀"
RIGHT: "Data Scientist Junior | Python · Scikit-learn · PyTorch · SQL | Master Sciences des Données & Systèmes Intelligents | Maroc · France · télétravail"
```

**Gate:** count each section with `python -c "print(len(open('x.txt',encoding='utf-8').read()))"` (never estimate): within its limit, every claim traceable to the profile, the headline contains the target title and ≥ 3 keywords, the title appears in the first 250 characters of About.

## Phase 4 — Deliver

Return the block above ready to paste, each section with its count, plus a 3-line "avant / après" note if the current text was available. Nothing is published by this skill; the user pastes it. Offer the `/linkedin-post-writer` skill for a first post announcing the new positioning.

**Gate:** every section carries a count ≤ its limit, and every `[À CONFIRMER]` placeholder is listed under "⚠️ À confirmer avant de coller".

## Anti-patterns

- **Headline = current job title.** "Étudiante en Master" hides the candidate; lead with the target role.
- **About written as a cover letter.** Facts and keywords first; no "Bonjour et bienvenue sur mon profil".
- **A long undifferentiated skills list.** Trim to the role; the five Top skills do the filtering work.
- **Inventing a title, a date, or seniority.** Clarify wording, never upgrade it; a flagged year stays a placeholder.
