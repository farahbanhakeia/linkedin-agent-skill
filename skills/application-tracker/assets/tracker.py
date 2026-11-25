#!/usr/bin/env python
"""Ledger operations for suivi-candidatures.csv (UTF-8 with BOM, Excel-friendly).

Usage:
  python -I tracker.py check  --entreprise "ACME" --poste "Data Scientist Junior" [--lien URL]
  python -I tracker.py add    --entreprise ... --poste ... --localisation ... --type_contrat ... --lien URL
                              [--source linkedin|indeed|wttj|rekrute|site|autre] [--cv PATH] [--message PATH]
                              [--canal easy_apply|email|formulaire|autre] [--statut préparée|envoyée]
                              [--contact "Nom – rôle – email/URL"] [--notes TEXT] [--date YYYY-MM-DD]
  python -I tracker.py update --id ID --statut entretien [--notes TEXT] [--contact ...]
  python -I tracker.py list   [--statut envoyée] [--json]

Exit codes: 0 ok · 2 duplicate (same URL, or same entreprise+poste after normalisation; `add` always
            refuses a duplicate; `check` returns 2 only when a match is not préparée)
            · 6 already prepared (check: the only matches are statut=préparée → use update --id, not add)
            · 3 unknown id (update) · 4 bad statut (add/update) · 1 missing required argument.
Ledger path: $CANDIDATURE_DIR/suivi-candidatures.csv, default ~/Documents/candidature/.
"""
import argparse, csv, json, os, re, sys, unicodedata
from datetime import date
from pathlib import Path

FIELDS = ["id", "date_candidature", "entreprise", "poste", "localisation", "type_contrat",
          "lien_offre", "source", "cv_envoye", "message_envoye", "canal", "statut",
          "contact_recruteur", "notes"]
STATUTS = ["préparée", "envoyée", "relance", "entretien", "offre", "refus", "retirée", "doublon"]
LEDGER = Path(os.environ.get("CANDIDATURE_DIR", Path.home() / "Documents" / "candidature")) / "suivi-candidatures.csv"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"\b(h/f|f/h|m/f|f/m|junior|stage|cdi|cdd|alternance)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def norm_url(u: str) -> str:
    u = (u or "").strip().lower().split("?")[0].split("#")[0].rstrip("/")
    return re.sub(r"^https?://(www\.)?", "", u)


def load():
    if not LEDGER.exists():
        return []
    with LEDGER.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save(rows):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    tmp = LEDGER.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    tmp.replace(LEDGER)


def find_dupes(rows, entreprise, poste, lien):
    e, p, u = norm(entreprise), norm(poste), norm_url(lien)
    out = []
    for r in rows:
        if u and norm_url(r["lien_offre"]) == u:
            out.append((r, "même lien"))
        elif e and e == norm(r["entreprise"]) and p and p == norm(r["poste"]):
            out.append((r, "même entreprise + poste"))
    return out


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", norm(s)).strip("-")[:30] or "x"


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("op", choices=["check", "add", "update", "list"])
    for f in FIELDS:
        ap.add_argument(f"--{f}")
    ap.add_argument("--lien", dest="lien_offre_alias")
    ap.add_argument("--cv", dest="cv_alias")
    ap.add_argument("--message", dest="message_alias")
    ap.add_argument("--contact", dest="contact_alias")
    ap.add_argument("--date", dest="date_alias")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    lien = a.lien_offre or a.lien_offre_alias or ""
    cv = a.cv_envoye or a.cv_alias or ""
    msg = a.message_envoye or a.message_alias or ""
    contact = a.contact_recruteur or a.contact_alias or ""
    day = a.date_candidature or a.date_alias or date.today().isoformat()
    rows = load()

    if a.op == "check":
        if not lien and not (a.entreprise and a.poste):
            sys.exit("check : donner --entreprise et --poste, ou --lien")
        d = find_dupes(rows, a.entreprise or "", a.poste or "", lien)
        if d:
            for r, why in d:
                print(f"DOUBLON ({why}) : {r['id']} · {r['entreprise']} · {r['poste']} · {r['date_candidature']} · statut={r['statut']}")
            if all(r["statut"] == "préparée" for r, _ in d):
                print(f"PRÉPARÉE, pas encore envoyée : utiliser 'update --id {d[0][0]['id']}' pour l'envoi (pas 'add').")
                sys.exit(6)
            sys.exit(2)
        print("OK : aucune candidature existante pour cette offre.")
        return

    if a.op == "add":
        if not (a.entreprise and a.poste and lien):
            sys.exit("--entreprise, --poste et --lien sont obligatoires")
        statut = a.statut or "préparée"
        if statut not in STATUTS:
            print(f"statut invalide : {statut} ; valeurs : {', '.join(STATUTS)}")
            sys.exit(4)
        d = find_dupes(rows, a.entreprise, a.poste, lien)
        if d:
            r, why = d[0]
            print(f"REFUS : doublon ({why}) de {r['id']} — utilise 'update --id {r['id']}' au lieu d'ajouter.")
            sys.exit(2)
        rid = f"{day.replace('-', '')}-{slug(a.entreprise)}-{slug(a.poste)}"
        n = 2
        base = rid
        while any(r["id"] == rid for r in rows):
            rid = f"{base}-{n}"; n += 1
        rows.append({"id": rid, "date_candidature": day, "entreprise": a.entreprise, "poste": a.poste,
                     "localisation": a.localisation or "", "type_contrat": a.type_contrat or "",
                     "lien_offre": lien, "source": a.source or "", "cv_envoye": cv, "message_envoye": msg,
                     "canal": a.canal or "", "statut": statut, "contact_recruteur": contact, "notes": a.notes or ""})
        save(rows)
        print(f"AJOUTÉ : {rid} (statut={statut})")
        return

    if a.op == "update":
        if not a.id:
            sys.exit("--id obligatoire")
        for r in rows:
            if r["id"] == a.id:
                if a.statut:
                    if a.statut not in STATUTS:
                        print(f"statut invalide : {a.statut} ; valeurs : {', '.join(STATUTS)}")
                        sys.exit(4)
                    r["statut"] = a.statut
                for k, v in (("notes", a.notes), ("contact_recruteur", contact), ("cv_envoye", cv),
                             ("message_envoye", msg), ("canal", a.canal), ("date_candidature", a.date_candidature or a.date_alias)):
                    if v:
                        r[k] = (r[k] + " | " + v) if k == "notes" and r[k] else v
                save(rows)
                print(f"MIS À JOUR : {r['id']} · statut={r['statut']}")
                return
        print(f"ID inconnu : {a.id}")
        sys.exit(3)

    if a.op == "list":
        sel = [r for r in rows if not a.statut or r["statut"] == a.statut]
        if a.json:
            print(json.dumps(sel, ensure_ascii=False, indent=1))
            return
        if not sel:
            print("Aucune candidature." if not rows else "Aucune candidature avec ce statut.")
            return
        print("| id | date | entreprise | poste | lieu | statut | lien |")
        print("|---|---|---|---|---|---|---|")
        for r in sel:
            print(f"| {r['id']} | {r['date_candidature']} | {r['entreprise']} | {r['poste']} | {r['localisation']} | {r['statut']} | {r['lien_offre']} |")
        counts = {}
        for r in rows:
            counts[r["statut"]] = counts.get(r["statut"], 0) + 1
        print("\nTotal :", len(rows), "·", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
