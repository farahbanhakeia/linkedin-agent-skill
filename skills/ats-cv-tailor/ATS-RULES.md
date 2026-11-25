# ATS rules the renderer and the spec must respect

Applicant Tracking Systems (Workday, Taleo, SmartRecruiters, Greenhouse, Lever, Welcome Kit…) parse the PDF text into fields, then match strings against the offer. Everything below exists to keep that parse clean and the match high.

## Layout (single column, headings, one-page check and the 0.9 scale floor are enforced by `assets/render_cv.py`; content rules are yours)

- A4, single column, real text (no outlines, no images of text), standard fonts (Helvetica).
- Standard section headings, one language, uppercase: PROFIL / COMPÉTENCES / EXPÉRIENCE PROFESSIONNELLE / PROJETS / FORMATION / CERTIFICATIONS / LANGUES (or their English equivalents).
- No tables, text boxes, columns, icons, photos, progress bars, or skill ratings as graphics.
- Contact line as plain text: city, phone, e-mail, LinkedIn URL, GitHub URL. No headers/footers.
- One page. Margins 13–16 mm; body 9–10 pt.

## Content (your responsibility when writing the spec)

- **Title line = the offer's job title.** Parsers weight it heavily; "Analyste Business Development" on a Data Scientist application costs the match.
- **Use the offer's exact strings** for matched skills: "Scikit-learn" not "sklearn", "Power BI" not "PowerBI", "Machine Learning" not "ML" (write both when the offer uses both).
- **Spell out acronyms once**: "programmation par contraintes (CSP)".
- **Dates as `YYYY – YYYY` or `MM/YYYY – MM/YYYY`**; "6 mois" is fine alongside, never instead of, a year when the profile has one.
- **Bullets start with an action verb**, contain one skill keyword each, and end with a result or a scope when the profile provides one. No pronouns ("je"), no full sentences longer than two lines.
- **Keep every level honest**: "notions", "en approfondissement", "pratiqué en projet" are allowed phrases; "expert", "maîtrise avancée" are allowed only when the profile says "maîtrisé".
- **Omit** hobbies, photo, age, marital status, "références sur demande".

## Fit-to-one-page order of cuts (rerun after each step; stop at the first exit 0)

1. Drop the least relevant project.
2. Rerun with `--scale 0.95` (10 pt → 9.5 pt costs nothing for ATS; a bullet of keyword context does).
3. Trim the experience least relevant to the offer to two bullets, then the next one.
4. Shorten `resume` to three lines.
5. `--scale 0.9`, the script's floor (it refuses anything smaller).
