# linkedin-agent-skill

Un ensemble de skills Claude Code pour une recherche d'emploi junior en Data / IA (Data Scientist, Ingénieur·e IA, Data Engineer) et pour la présence LinkedIn qui va avec. Chaque skill fait un seul travail ; un routeur `/job-hunt` les enchaîne ; un agent `job-hunt-batch` prépare des lots de candidatures sans jamais envoyer.

Tout ce que les skills écrivent (CV, messages, profil) vient d'un seul fichier que vous tenez à jour : `profil-maitre.md`. Si un fait n'y est pas, il n'existe pas. Aucun diplôme, aucune expérience, aucun niveau n'est inventé.

## Les skills

| Skill | Ce qu'il fait | Exemples de déclencheurs |
| --- | --- | --- |
| `job-offer-finder` | Trouve des offres récentes et ouvertes (0–3 ans, CDI/CDD/stage pré-embauche, Maroc/France/télétravail), ouvre et vérifie chacune, exclut celles déjà dans le suivi, enregistre le texte dans `offres/` | « cherche des offres », « find junior data jobs » |
| `ats-cv-tailor` | Génère un CV PDF d'une page, compatible ATS, adapté à une offre, avec un rapport des compétences manquantes | « adapte mon CV à cette offre » |
| `cover-letter-writer` | Lettre de motivation d'une page en PDF : chaque paragraphe répond à une exigence de l'offre avec une preuve du profil | « lettre de motivation pour cette offre » |
| `recruiter-message-writer` | Note d'invitation, message LinkedIn, e-mail de candidature ou relance, deux preuves concrètes puis la demande d'entretien | « écris un message au recruteur » |
| `submit-application` | Envoie (Easy Apply, e-mail, formulaire) uniquement après un « oui » explicite pour cette offre, puis enregistre dans le suivi | « postule », « envoie la candidature » |
| `application-tracker` | Ajoute, met à jour, vérifie les doublons et liste le tableau de suivi (`suivi-candidatures.csv`) | « est-ce que j'ai déjà postulé chez … ? », « marque en entretien » |
| `linkedin-post-writer` | Un post LinkedIn (accroche ≤ 140 caractères, corps court, question finale, 3–5 hashtags) à partir d'un sujet, d'un lien ou d'un projet | « écris un post LinkedIn sur … » |
| `linkedin-profile-optimizer` | Titre, section Infos, expériences, Top skills, paramètres Open to work, pour un rôle cible | « optimise mon profil LinkedIn » |
| `job-hunt` | Routeur, à taper soi-même : `/job-hunt`. Décrit l'ordre des étapes et les points de validation | — |

Agent `job-hunt-batch` : « prépare-moi un lot d'offres ». Il cherche, vérifie, génère CV et message pour N offres, les enregistre en statut `préparée`, puis s'arrête. L'envoi passe toujours par votre validation, une offre à la fois.

## Installation

Prérequis : Claude Code (CLI ou application de bureau), Python 3.10+ avec `reportlab` et `pypdf` (pour le rendu du CV).

```powershell
pip install reportlab pypdf
```

Puis, depuis le dossier du dépôt :

```powershell
.\install.ps1
```

Le script copie `skills/*` dans `~/.claude/skills/`, `agents/job-hunt-batch.md` dans `~/.claude/agents/`, et crée `~/Documents/candidature/` avec un `profil-maitre.md` à partir du modèle s'il n'existe pas encore. Installation manuelle : copiez les mêmes dossiers aux mêmes endroits. Les skills apparaissent à la prochaine session Claude Code.

## Avant la première utilisation

1. Remplissez `~/Documents/candidature/profil-maitre.md` à partir de votre CV réel. Gardez les niveaux honnêtes (maîtrisé / pratiqué / notions) : les skills ne les relèvent jamais.
2. Laissez les lignes `⚠️ À CONFIRMER` tant qu'un fait n'est pas sûr ; les skills les ignorent et vous les listent.
3. Lancez `/linkedin-profile-optimizer` une fois, puis `/job-hunt` pour un premier tour.

## Données

```
~/Documents/candidature/
├── profil-maitre.md          # source de vérité, éditée par vous seul
├── suivi-candidatures.csv    # tableau de suivi (UTF-8, s'ouvre dans Excel)
├── offres/                   # texte intégral des offres vérifiées
└── cv/                       # CV générés (JSON de spec + PDF) et messages
```

Le suivi n'est jamais modifié à la main : tout passe par `skills/application-tracker/assets/tracker.py` (`check`, `add`, `update`, `list`). Codes de sortie : `0` ok, `2` doublon, `6` déjà préparée (utiliser `update`), `3` id inconnu, `4` statut invalide.

## Connecteurs optionnels

Les skills fonctionnent sans connecteur. Trois en améliorent une étape, à connecter dans Claude si vous le souhaitez :

- **Indeed** : une source d'offres supplémentaire pour `job-offer-finder`.
- **Gmail** : envoi direct des candidatures par e-mail dans `submit-application` (sinon un brouillon est préparé et vous l'envoyez).
- **Google Sheets** : si vous préférez un suivi en ligne plutôt que le CSV local.

Pour LinkedIn (Jobs, Easy Apply, lecture du profil), les skills utilisent Claude in Chrome avec votre session déjà ouverte. Ils ne saisissent jamais de mot de passe et ne résolvent jamais de CAPTCHA.

## Garde-fous

- Aucun envoi sans votre « oui » explicite à un récapitulatif (offre, canal, CV, message), une offre à la fois.
- Aucune candidature en double : le suivi est vérifié avant tout travail et avant tout envoi.
- Aucun fait hors du profil maître sur un CV, un message ou un profil.

## Structure du dépôt

```
skills/<nom-du-skill>/SKILL.md     # un skill = un dossier
skills/application-tracker/assets/tracker.py
skills/ats-cv-tailor/assets/render_cv.py, ATS-RULES.md
skills/cover-letter-writer/assets/render_letter.py
agents/job-hunt-batch.md
templates/profil-maitre.template.md
install.ps1
```
