#!/usr/bin/env python
"""Render an ATS-safe one-page CV PDF from a JSON spec (reportlab, single column, real text).

Usage:  python -I render_cv.py spec.json out.pdf [--scale 0.95]   (--scale may go anywhere)
Exit 0 if the PDF has exactly 1 page; exit 5 if it overflowed (then shrink the spec and rerun,
or pass --scale 0.95). --scale is clamped to [0.9, 1.0] (exit 2 outside). Requires: reportlab, pypdf.

Spec (all strings UTF-8; omit a section to skip it):
{
 "nom": "Farah BANHAKEIA", "titre": "Data Scientist Junior",
 "contact": ["<ville confirmée, pays> — mobile FR/remote", "<téléphone>", "<email>", "linkedin.com/in/…", "github.com/…"],
 "resume": "3–4 lignes.",
 "competences": [["Machine Learning", "Scikit-learn, …"], ["Data Engineering", "…"]],
 "experiences": [{"titre": "…", "org": "…", "lieu": "…", "dates": "2023 — 6 mois", "points": ["…"]}],
 "projets": [{"titre": "…", "stack": "Python, PyTorch", "points": ["…"]}],
 "formation": [{"titre": "…", "org": "…", "dates": "2024 – 2026"}],
 "certifications": ["…"], "langues": ["Français — C2", "…"],
 "lang": "fr"   // section headings in fr or en
}
"""
import json, sys
from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, KeepTogether

HEAD = {
    "fr": {"resume": "PROFIL", "competences": "COMPÉTENCES", "experiences": "EXPÉRIENCE PROFESSIONNELLE",
           "projets": "PROJETS", "formation": "FORMATION", "certifications": "CERTIFICATIONS", "langues": "LANGUES"},
    "en": {"resume": "SUMMARY", "competences": "SKILLS", "experiences": "PROFESSIONAL EXPERIENCE",
           "projets": "PROJECTS", "formation": "EDUCATION", "certifications": "CERTIFICATIONS", "langues": "LANGUAGES"},
}


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(spec, out, scale):
    f = 10 * scale
    st = {
        "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=18 * scale, leading=21 * scale, spaceAfter=1),
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=11.5 * scale, leading=14 * scale, textColor="#1f3a5f"),
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8.8 * scale, leading=11 * scale, textColor="#333333"),
        "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5 * scale, leading=13 * scale, textColor="#1f3a5f",
                            spaceBefore=6 * scale, spaceAfter=1),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=f, leading=f * 1.25, alignment=TA_JUSTIFY),
        "line": ParagraphStyle("line", fontName="Helvetica", fontSize=f, leading=f * 1.25),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=f, leading=f * 1.25, leftIndent=10, bulletIndent=1),
        "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=f, leading=f * 1.3, spaceBefore=3 * scale),
    }
    L = HEAD.get(spec.get("lang", "fr"), HEAD["fr"])
    el = []

    def section(key):
        el.append(Paragraph(L[key], st["h"]))
        el.append(HRFlowable(width="100%", thickness=0.7, color="#1f3a5f", spaceAfter=3))

    el.append(Paragraph(esc(spec["nom"]), st["name"]))
    el.append(Paragraph(esc(spec["titre"]), st["title"]))
    el.append(Paragraph(esc("  |  ".join(spec.get("contact", []))), st["contact"]))

    if spec.get("resume"):
        section("resume"); el.append(Paragraph(esc(spec["resume"]), st["body"]))
    if spec.get("competences"):
        section("competences")
        for cat, items in spec["competences"]:
            el.append(Paragraph(f"<b>{esc(cat)} :</b> {esc(items)}", st["line"]))
    if spec.get("experiences"):
        section("experiences")
        for x in spec["experiences"]:
            block = [Paragraph(f"{esc(x['titre'])} — {esc(x['org'])}" + (f", {esc(x['lieu'])}" if x.get("lieu") else "")
                               + f"<font color='#555555'>  ·  {esc(x.get('dates',''))}</font>", st["role"])]
            block += [Paragraph(esc(p), st["bullet"], bulletText="•") for p in x.get("points", [])]
            el.append(KeepTogether(block))
    if spec.get("projets"):
        section("projets")
        for x in spec["projets"]:
            block = [Paragraph(f"{esc(x['titre'])}" + (f"<font color='#555555'>  ·  {esc(x['stack'])}</font>" if x.get("stack") else ""), st["role"])]
            block += [Paragraph(esc(p), st["bullet"], bulletText="•") for p in x.get("points", [])]
            el.append(KeepTogether(block))
    if spec.get("formation"):
        section("formation")
        for x in spec["formation"]:
            el.append(Paragraph(f"<b>{esc(x['titre'])}</b> — {esc(x['org'])}<font color='#555555'>  ·  {esc(x.get('dates',''))}</font>", st["line"]))
    if spec.get("certifications"):
        section("certifications")
        el.append(Paragraph(esc("  ·  ".join(spec["certifications"])), st["line"]))
    if spec.get("langues"):
        section("langues")
        el.append(Paragraph(esc("  ·  ".join(spec["langues"])), st["line"]))

    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
                            topMargin=13 * mm, bottomMargin=13 * mm,
                            title=f"CV {spec['nom']} — {spec['titre']}", author=spec["nom"], subject=spec["titre"])
    doc.build(el)


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Render an ATS-safe one-page CV PDF from a JSON spec.")
    ap.add_argument("spec", help="JSON spec file")
    ap.add_argument("out", help="output PDF path")
    ap.add_argument("--scale", type=float, default=1.0, help="font scale, 0.9 to 1.0 (default 1.0)")
    try:
        a = ap.parse_args()
    except SystemExit:
        raise
    if not 0.9 <= a.scale <= 1.0:
        print(f"--scale {a.scale} refused: ATS floor is 0.9 (9 pt body), max 1.0")
        sys.exit(2)
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    build(spec, out, a.scale)
    from pypdf import PdfReader
    n = len(PdfReader(str(out)).pages)
    txt = PdfReader(str(out)).pages[0].extract_text() or ""
    print(f"{out} | pages={n} | chars_extractable={len(txt)}")
    sys.exit(0 if n == 1 else 5)


if __name__ == "__main__":
    main()
