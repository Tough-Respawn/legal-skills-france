# -*- coding: utf-8 -*-
"""Lint statique du plugin legal-france.

Usage :  python tests/lint.py        (depuis la racine du repo)
Dépendance : PyYAML (pip install pyyaml)

Contrôles :
  1. Frontmatter YAML parsable (commands, SKILL.md, templates)
  2. Descriptions de skills <= 1536 caractères (limite de troncature)
  3. Manifests JSON valides + versions marketplace/plugin identiques
  4. Mots-clés déclencheurs des scénarios tests/triggering.md présents
     dans les descriptions (comparaison insensible à la casse et aux
     espaces/retours à la ligne)
  5. Motifs interdits (citations corrigées le 2026-08-04, commandes fantômes)
  6. Inventaire /rediger (lib/redacteur-engine.md) <-> fichiers templates réels
  7. Contrat de template : clés frontmatter + les 3 sections obligatoires

Complément manuel : `claude plugin validate plugins/legal-france`
(la racine du marketplace échoue sur Claude Code 2.1.104 à cause des clés
"$schema"/"description", acceptées par les versions plus récentes : choix
assumé de les garder).
"""
import glob
import json
import os
import re
import sys

try:
    from yaml import safe_load
except ImportError:
    print("PyYAML manquant : pip install pyyaml")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "plugins", "legal-france")
FAIL = []

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def fm(path):
    m = re.match(r"^---\n(.*?)\n---", read(path), re.S)
    return m.group(1) if m else None

def norm(s):
    return re.sub(r"\s+", " ", s.lower())

def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")

# 1. Frontmatters YAML
fm_files = (
    glob.glob(os.path.join(PLUGIN, "commands", "*.md"))
    + glob.glob(os.path.join(PLUGIN, "skills", "*", "SKILL.md"))
    + glob.glob(os.path.join(PLUGIN, "skills", "*", "templates", "*.md"))
)
for p in sorted(fm_files):
    block = fm(p)
    if block is None:
        FAIL.append("frontmatter absent : %s" % rel(p))
        continue
    try:
        safe_load(block)
    except Exception as e:
        FAIL.append("YAML invalide %s : %s" % (rel(p), e))
print("1. frontmatters YAML : %d fichiers" % len(fm_files))

# 2. Longueur des descriptions
MAX_DESC = 1536
for p in sorted(glob.glob(os.path.join(PLUGIN, "skills", "*", "SKILL.md"))):
    name = os.path.basename(os.path.dirname(p))
    block = fm(p)
    if block is None:
        continue
    desc = (safe_load(block) or {}).get("description", "")
    if len(desc) > MAX_DESC:
        FAIL.append("description > %d : %s (%d)" % (MAX_DESC, name, len(desc)))
print("2. longueurs descriptions : ok (limite %d)" % MAX_DESC)

# 3. Manifests JSON + versions synchronisées
mk_path = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
pl_path = os.path.join(PLUGIN, ".claude-plugin", "plugin.json")
mk = pl = None
for p in (mk_path, pl_path):
    try:
        data = json.loads(read(p))
        if p == mk_path:
            mk = data
        else:
            pl = data
    except Exception as e:
        FAIL.append("JSON invalide %s : %s" % (rel(p), e))
if mk and pl:
    mk_ver = mk["plugins"][0].get("version")
    pl_ver = pl.get("version")
    if mk_ver != pl_ver:
        FAIL.append("versions desynchronisees : marketplace=%s plugin=%s" % (mk_ver, pl_ver))
print("3. manifests JSON + versions : ok")

# 4. Mots-clés déclencheurs (issus de tests/triggering.md)
TRIGGERS = {
    "legal-france": ["prescription", "multi-domaines", "mise en demeure", "attestation"],
    "legal-france-civil": ["proprio", "caution", "divorcer", "vice caché"],
    "legal-france-travail": ["viré", "rupture conventionnelle", "heures sup", "prud'hommes"],
    "legal-france-penal": ["porter plainte", "amende", "garde à vue"],
    "legal-france-affaires": ["sas", "marque", "concurrence", "facture"],
    "legal-france-administratif": ["préfecture", "naturalisation", "caf", "trop-perçu", "recours gracieux"],
    "legal-france-numerique": ["bandeau cookies", "photo", "publication sans accord", "droit à l'oubli", "dpo"],
    "legal-france-europeen": ["cjue", "directive", "citoyen européen"],
}
for skill, kws in TRIGGERS.items():
    p = os.path.join(PLUGIN, "skills", skill, "SKILL.md")
    desc = norm((safe_load(fm(p)) or {}).get("description", ""))
    missing = [kw for kw in kws if kw not in desc]
    if missing:
        FAIL.append("triggers absents de %s : %s" % (skill, missing))
print("4. triggers : %d skills verifies" % len(TRIGGERS))

# 5. Motifs interdits (régressions sur les corrections du 2026-08-04)
BANNED = [
    (r"/analyse-contrat|/consultation\b", os.path.join(PLUGIN, "**", "*.md"),
     "commande fantome"),
    (r"L\. ?131-1.*[Ss]ilence", os.path.join(PLUGIN, "skills", "legal-france", "references", "codes-index.md"),
     "CRPA silence-vaut-acceptation = L.231-1, pas L.131-1"),
    (r"1231-5", os.path.join(PLUGIN, "skills", "legal-france", "templates", "mise-en-demeure-generique.md"),
     "1231-5 (clause penale) hors sujet dans la MED generique"),
    (r"L\. ?1234-1", os.path.join(PLUGIN, "skills", "legal-france-travail", "templates", "lettre-demission.md"),
     "L.1234-1 = preavis de licenciement, pas de demission"),
]
for pattern, scope, why in BANNED:
    for p in glob.glob(scope, recursive=True):
        for i, line in enumerate(read(p).splitlines(), 1):
            if re.search(pattern, line):
                FAIL.append("motif interdit (%s) %s:%d : %s" % (why, rel(p), i, line.strip()[:80]))
print("5. motifs interdits : ok")

# 6. Inventaire /rediger <-> fichiers templates
engine = read(os.path.join(PLUGIN, "lib", "redacteur-engine.md"))
inventory = re.findall(r"^\| `([a-z0-9-]+)` \| \S+ \| `([^`]+)` \|", engine, re.M)
if not inventory:
    FAIL.append("inventaire introuvable dans lib/redacteur-engine.md")
for slug, path in inventory:
    full = os.path.join(PLUGIN, path.replace("/", os.sep))
    if not os.path.isfile(full):
        FAIL.append("inventaire /rediger : fichier manquant pour `%s` : %s" % (slug, path))
listed = {os.path.normpath(os.path.join(PLUGIN, p)) for _, p in inventory}
on_disk = {os.path.normpath(p) for p in glob.glob(os.path.join(PLUGIN, "skills", "*", "templates", "*.md"))}
for orphan in sorted(on_disk - listed):
    FAIL.append("template hors inventaire /rediger : %s" % rel(orphan))
print("6. inventaire /rediger : %d entrees" % len(inventory))

# 7. Contrat de template
REQ_KEYS = ["type", "domain", "short_description", "required_fields", "applicable_law", "disclaimer_level"]
REQ_SECTIONS = ["## Questionnaire", "## Template", "## Vérifications juridiques avant envoi"]
for p in sorted(glob.glob(os.path.join(PLUGIN, "skills", "*", "templates", "*.md"))):
    block = fm(p)
    if block is None:
        continue  # déjà signalé au contrôle 1
    data = safe_load(block) or {}
    for k in REQ_KEYS:
        if k not in data:
            FAIL.append("template %s : cle frontmatter manquante `%s`" % (rel(p), k))
    body = read(p)
    for s in REQ_SECTIONS:
        if s not in body:
            FAIL.append("template %s : section manquante `%s`" % (rel(p), s))
print("7. contrat de template : ok")

print()
if FAIL:
    print("ECHEC : %d probleme(s)" % len(FAIL))
    for f in FAIL:
        print("  - %s" % f)
    sys.exit(1)
print("TOUT PASSE")
