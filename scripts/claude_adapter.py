"""Claude Code distribution and native installation; no legal content here."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess


PLUGIN_ID = "legal-france@legal-france"
MARKETPLACE = "Tough-Respawn/legal-skills-france"
LAYOUT = """## Emplacement des ressources

La racine du plugin est deux dossiers au-dessus de ce SKILL.md.
Les chemins skills/... et lib/... partent de cette racine. Les chemins
references/... et templates/... partent du dossier de ce SKILL.md.
Résoudre les chemins depuis les fichiers chargés, jamais depuis le projet.

"""


def distribution(root, sources, metadata, runtime):
    adapter = root / "adapters/claude-code"
    plugin = root / "plugins/legal-france"
    legacy = json.loads((adapter / "legacy-frontmatter.json").read_text(encoding="utf-8"))
    plan = {}
    for relative, payload in sources.items():
        if relative.endswith("/SKILL.md"):
            name = relative.split("/")[1]
            body = re.sub(r"\A---\n.*?\n---\n", "", payload.decode("utf-8"), count=1, flags=re.S).lstrip()
            text = f"---\n{legacy[name]}\n---\n\n{LAYOUT}{runtime}\n{body}"
            if name == "legal-france":
                text += "\n" + (adapter / "commands-reference.md").read_text(encoding="utf-8")
            payload = (text.rstrip() + "\n").encode("utf-8")
        plan[plugin / relative] = payload
    for command in sorted((adapter / "commands").glob("*.md")):
        plan[plugin / "commands" / command.name] = command.read_bytes()
    manifest = {key: metadata[key] for key in ("name", "version", "description", "author")}
    marketplace = {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": metadata["name"],
        "description": metadata["description"],
        "owner": metadata["owner"],
        "plugins": [{**manifest, "source": "./plugins/legal-france", "category": "knowledge", "homepage": metadata["repository"]}],
    }
    for target, data in ((plugin / ".claude-plugin/plugin.json", manifest), (root / ".claude-plugin/marketplace.json", marketplace)):
        plan[target] = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    plan[plugin / ".env.example"] = (root / ".env.example").read_bytes()
    return plan


def config_root():
    configured = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(configured).expanduser().resolve() if configured else Path.home() / ".claude"


def metadata_file(name):
    path = config_root() / "plugins" / name
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Métadonnées Claude non reconnues : {path}")
    return data


def installed_plugins():
    plugins = metadata_file("installed_plugins.json").get("plugins", {})
    if not isinstance(plugins, dict):
        raise ValueError("Inventaire des plugins Claude non reconnu ; utiliser le gestionnaire natif.")
    return {name: entries for name, entries in plugins.items() if name.split("@")[0] == "legal-france"}


def skill_roots(args):
    project = Path(args.project).resolve() if args.project else Path.cwd()
    return (config_root() / "skills", project / ".claude/skills")


def refuse_duplicate_copy(directory, args, names):
    # Check only Claude destinations; other harnesses share the portable tree.
    if directory.resolve() not in {path.resolve() for path in skill_roots(args)}:
        return
    if installed_plugins():
        raise ValueError(
            "Le plugin legal-france est déjà présent dans Claude. Une copie autonome "
            "créerait des doublons. Utilisez install --agent claude-code pour le gérer "
            "avec son gestionnaire natif ; aucune suppression automatique."
        )


def prepare_install(root, args, names):
    duplicates = [directory / name for directory in skill_roots(args) for name in names if (directory / name / "SKILL.md").is_file()]
    if duplicates:
        raise ValueError(
            "Des skills Claude autonomes sont déjà présents : " + ", ".join(map(str, duplicates))
            + ". Ils sont conservés. Pour passer au plugin natif, sauvegardez puis "
            "retirez ces copies explicitement ; aucune migration destructive automatique."
        )
    executable = shutil.which("claude")
    if not executable and not args.dry_run:
        raise ValueError("Claude Code doit être installé pour utiliser son gestionnaire de plugins. Le ZIP reste disponible pour une copie manuelle.")
    executable = executable or "claude"
    scope = args.scope or ("project" if args.project else "user")
    project = Path(args.project).resolve() if args.project else Path.cwd()
    plugins = installed_plugins()
    if any(name != PLUGIN_ID for name in plugins):
        raise ValueError("legal-france est installé depuis un autre marketplace ; conserver cette installation et utiliser son gestionnaire natif.")
    entries = plugins.get(PLUGIN_ID, [])
    if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
        raise ValueError("Portées du plugin Claude non reconnues ; utiliser le gestionnaire natif.")
    present = any(entry.get("scope") == scope and (scope == "user" or Path(entry.get("projectPath") or "").resolve() == project) for entry in entries)
    markets = metadata_file("known_marketplaces.json")
    market = markets.get("legal-france")
    if market:
        if not isinstance(market, dict):
            raise ValueError("Configuration du marketplace Claude non reconnue.")
        source = market.get("source", {})
        if not isinstance(source, dict):
            raise ValueError("Source du marketplace Claude non reconnue.")
        location = source.get("repo") or source.get("url") or ""
        if not isinstance(location, str):
            raise ValueError("Adresse du marketplace Claude non reconnue.")
        accepted = {
            "Tough-Respawn/legal-skills-france", "Tough-Respawn/claude-legal-skills-france",
            "https://github.com/Tough-Respawn/legal-skills-france", "https://github.com/Tough-Respawn/claude-legal-skills-france",
            "git@github.com:Tough-Respawn/legal-skills-france", "git@github.com:Tough-Respawn/claude-legal-skills-france",
        }
        if location.removesuffix(".git") not in accepted:
            raise ValueError("Le marketplace legal-france utilise une autre source. La configuration existante est conservée ; gérer sa mise à jour dans Claude.")
    commands = [
        [executable, "plugin", "marketplace", "update", "legal-france"] if market
        else [executable, "plugin", "marketplace", "add", MARKETPLACE],
        [executable, "plugin", "update" if present else "install", PLUGIN_ID, "--scope", scope],
    ]
    return commands, project


def run_install(prepared, dry_run):
    commands, directory = prepared
    for command in commands:
        print("Claude Code :", subprocess.list2cmdline(command), flush=True)
        if dry_run:
            continue
        try:
            completed = subprocess.run(command, cwd=directory, check=False, timeout=180)
        except subprocess.TimeoutExpired:
            raise ValueError("Le gestionnaire Claude n'a pas terminé dans le délai prévu. Vérifiez son état avant de relancer.") from None
        if completed.returncode:
            raise ValueError(f"Le gestionnaire Claude a renvoyé le code {completed.returncode}. Les étapes suivantes n'ont pas été lancées.")
