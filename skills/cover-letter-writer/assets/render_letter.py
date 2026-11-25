#!/usr/bin/env python
"""Render a one-page cover letter PDF (lettre de motivation) from a JSON spec. Real text, A4, ATS-safe.

Usage:  python -I render_letter.py spec.json out.pdf [--scale 0.95]
Exit 0 = one page · 5 = overflow (shorten the body, or --scale down to 0.9) · 2 = bad --scale.
Requires: reportlab, pypdf.

Spec:
{
 "expediteur": ["Prénom NOM", "Ville, Pays", "+XXX …", "email", "linkedin.com/in/…"],
 "destinataire": ["Entreprise", "Service recrutement / Nom du recruteur", "Ville"],
 "lieu_date": "Casablanca, le 25 novembre 2026",
 "objet": "Candidature au poste de <titre exact> (réf. …)",
 "salutation": "Madame, Monsieur,",
 "paragraphes": ["…", "…", "…", "…"],
 "formule": "Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.",
 "signature": "Prénom NOM",
 "pj": "CV"
}
"""
import argparse, json, sys
from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(spec, out, k):
    f = 10.5 * k
    st = {
        "sender": ParagraphStyle("sender", fontName="Helvetica", fontSize=9.5 * k, leading=12 * k),
        "sender_name": ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=11 * k, leading=14 * k),
        "to": ParagraphStyle("to", fontName="Helvetica", fontSize=f, leading=f * 1.3, alignment=TA_RIGHT),
        "date": ParagraphStyle("date", fontName="Helvetica", fontSize=f, leading=f * 1.3, alignment=TA_RIGHT),
        "objet": ParagraphStyle("objet", fontName="Helvetica-Bold", fontSize=f, leading=f * 1.3),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=f, leading=f * 1.42, alignment=TA_JUSTIFY, spaceAfter=f * 0.9),
        "line": ParagraphStyle("line", fontName="Helvetica", fontSize=f, leading=f * 1.3),
    }
    el = []
    snd = spec.get("expediteur", [])
    if snd:
        el.append(Paragraph(esc(snd[0]), st["sender_name"]))
        for l in snd[1:]:
            el.append(Paragraph(esc(l), st["sender"]))
    el.append(Spacer(1, 6 * mm))
    for l in spec.get("destinataire", []):
        el.append(Paragraph(esc(l), st["to"]))
    el.append(Spacer(1, 4 * mm))
    if spec.get("lieu_date"):
        el.append(Paragraph(esc(spec["lieu_date"]), st["date"]))
    el.append(Spacer(1, 6 * mm))
    if spec.get("objet"):
        el.append(Paragraph("Objet : " + esc(spec["objet"]), st["objet"]))
        el.append(Spacer(1, 4 * mm))
    el.append(Paragraph(esc(spec.get("salutation", "Madame, Monsieur,")), st["line"]))
    el.append(Spacer(1, 3 * mm))
    for p in spec.get("paragraphes", []):
        el.append(Paragraph(esc(p), st["body"]))
    if spec.get("formule"):
        el.append(Paragraph(esc(spec["formule"]), st["body"]))
    el.append(Spacer(1, 6 * mm))
    el.append(Paragraph(esc(spec.get("signature", "")), st["line"]))
    if spec.get("pj"):
        el.append(Spacer(1, 6 * mm))
        el.append(Paragraph("PJ : " + esc(spec["pj"]), st["sender"]))
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm,
                            title=spec.get("objet", "Lettre de motivation"), author=spec.get("signature", ""))
    doc.build(el)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out")
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    if not 0.9 <= a.scale <= 1.0:
        print(f"--scale {a.scale} refused: allowed 0.9 to 1.0"); sys.exit(2)
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    build(spec, out, a.scale)
    from pypdf import PdfReader
    r = PdfReader(str(out)); n = len(r.pages)
    words = len((r.pages[0].extract_text() or "").split())
    print(f"{out} | pages={n} | words_page1={words}")
    sys.exit(0 if n == 1 else 5)


if __name__ == "__main__":
    main()
