#!/usr/bin/env python3
"""Install or package legal-france skills. Python 3.10+, standard library only."""

import argparse
import io
import json
from pathlib import Path
import re
import stat
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/legal-france"
SOURCE = ROOT / "src/legal-france"
META = "legal-france"
DOMAINS = ("civil", "penal", "travail", "affaires", "administratif", "numerique", "europeen")
NAMES = (META, *(f"{META}-{domain}" for domain in DOMAINS))
# Prefer the shared location when the client's documentation supports it.
# Sources and caveats, including remote environments, are in COMPATIBILITY.md.
AGENTS = {
    "claude-code": (".claude/skills", ".claude/skills"),
    "codex": (".agents/skills", ".agents/skills"),
    "cursor": (".agents/skills", ".agents/skills"),
    "github-copilot": (".agents/skills", ".agents/skills"),
    "gemini-cli": (".agents/skills", ".agents/skills"),
    "opencode": (".agents/skills", ".agents/skills"),
    "windsurf": (".codeium/windsurf/skills", ".windsurf/skills"),
    "cline": (".cline/skills", ".cline/skills"),
    "roo-code": (".agents/skills", ".agents/skills"),
    "amp": (".agents/skills", ".agents/skills"),
}
PORTABLE_CONTEXT = """## Environnement et ressources

Le dossier contenant ce SKILL.md est la racine du skill. Tous les chemins
`resources/...` et `scripts/...` des instructions et documents inclus partent
de cette racine, même depuis un document imbriqué. Résoudre les fichiers depuis
l'emplacement réellement chargé, jamais depuis le dossier courant du projet.
Les protocoles placés dans resources sont des documents, pas d'autres skills
à installer. Ne charger que les références utiles à la question.

"""


def is_link(path):
    """Account for Windows junctions as well as symbolic links."""
    try:
        info = path.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return False
    return stat.S_ISLNK(info.st_mode) or getattr(info, "st_reparse_tag", None) in {
        getattr(stat, "IO_REPARSE_TAG_SYMLINK", -1),
        getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", -2),
    }


def check_windows_path_length(path, *, directory=False):
    """Keep destinations readable by clients that do not support long paths."""
    if sys.platform != "win32":
        return
    # MAX_PATH includes the terminating NUL. Directory creation also needs
    # room for an 8.3 filename. Keep one unit of margin at both boundaries.
    # https://learn.microsoft.com/windows/win32/fileio/maximum-file-path-limitation
    limit = 248 if directory else 260
    units = len(str(path).encode("utf-16-le", errors="surrogatepass")) // 2
    if units >= limit:
        kind = "dossier" if directory else "fichier"
        raise ValueError(
            f"Chemin de {kind} trop long sous Windows : {units} unités UTF-16 "
            f"(maximum accepté : {limit - 1}) : {path}. "
            "Choisissez une destination plus courte, par exemple une installation "
            "personnelle ou un projet proche de la racine du disque. "
            "Aucun fichier écrit par cette opération."
        )


def checked_path(path):
    path = Path(path).expanduser().absolute()
    check_windows_path_length(path)
    for part in (path, *path.parents):
        if is_link(part):
            raise ValueError(f"Lien symbolique ou jonction dans la destination : {part}")
    resolved = path.resolve()
    check_windows_path_length(resolved)
    return resolved


def split_skill(text):
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("Frontmatter SKILL.md absent ou non reconnu")
    return match.group(1), text[match.end():].lstrip()


def source_files():
    """Explicit allowlist: never collect .env, caches, evaluations or settings."""
    files = {}
    for name in NAMES:
        directory = SOURCE / "skills" / name
        if not (directory / "SKILL.md").is_file():
            raise ValueError(f"Skill source absent : {directory}")
        for path in sorted(directory.rglob("*")):
            if is_link(path):
                raise ValueError(f"Lien dans les sources : {path}")
            if path.is_file() and path.suffix == ".md":
                files[path.relative_to(SOURCE).as_posix()] = path.read_bytes()
    for name in ("redacteur-engine.md", "legifrance-client.md", "judilibre-client.md"):
        path = SOURCE / "lib" / name
        files[f"lib/{name}"] = path.read_bytes()
    script = "skills/legal-france/scripts/legal_api.py"
    files[script] = (SOURCE / script).read_bytes()
    return files


def resource_path(source):
    if source == "skills/legal-france/scripts/legal_api.py":
        return "scripts/legal_api.py"
    path = source.removeprefix("skills/")
    if path.endswith("/SKILL.md"):
        path = path[:-len("SKILL.md")] + "protocol.md"
    return f"resources/{path}"


def portable_text(text, origin, sources):
    """Rebase known references once; leave URLs and legal citations intact."""
    context = origin.split("/")[1] if origin.startswith("skills/") else META
    mapping = {}
    for source in sources:
        target = resource_path(source)
        mapping[source] = target
        if source.startswith("skills/"):
            relative = "/".join(source.split("/")[2:])
            if relative != "SKILL.md":
                mapping[relative] = target
    mapping["SKILL.md"] = resource_path(f"skills/{context}/SKILL.md")
    mapping["templates/"] = f"resources/{context}/templates/"
    pattern = r"(?<![\w./-])(?:" + "|".join(re.escape(key) for key in sorted(mapping, key=len, reverse=True)) + r")(?![\w.-])"
    text = re.sub(pattern, lambda match: mapping[match.group()], text)
    text = text.replace("la racine du module chargé", "la racine du skill installé")
    text = text.replace("depuis le module réellement chargé", "depuis le skill réellement chargé")
    text = text.replace("l'emplacement réellement chargé du module", "l'emplacement réellement chargé du skill")
    text = text.replace("adjacent au skill méta", "inclus dans chaque skill installé")
    text = re.sub(r"beside this resources/[^\s]+\.md", "at the installed skill root", text)
    return text


def portable_files():
    sources = source_files()
    version = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))["version"]
    license_bytes = (ROOT / "LICENSE").read_bytes()
    example_bytes = (ROOT / ".env.example").read_bytes()
    runtime = portable_text((SOURCE / "runtime.md").read_text(encoding="utf-8"), "runtime.md", sources)
    common = {}
    bodies = {}
    descriptions = {}
    for source, content in sources.items():
        if source.endswith(".py"):
            common[resource_path(source)] = content
            continue
        text = content.decode("utf-8").replace("\r\n", "\n")
        if source.endswith("/SKILL.md"):
            frontmatter, text = split_skill(text)
            name = source.split("/")[1]
            # Canonical descriptions use JSON strings, a YAML-compatible subset.
            descriptions[name] = json.loads(re.search(r"^description: (.+)$", frontmatter, re.M).group(1))
            bodies[name] = portable_text(text, source, sources)
        common[resource_path(source)] = portable_text(text, source, sources).encode("utf-8")
    files = {}
    for name in NAMES:
        description = descriptions[name]
        if not 1 <= len(description) <= 1024:
            raise ValueError(f"Description portable hors limite : {name}")
        header = (
            f"---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n"
            f"license: MIT\nmetadata:\n  version: {json.dumps(version)}\n  distribution: portable\n---\n\n"
        )
        files[f"{name}/SKILL.md"] = (header + PORTABLE_CONTEXT + runtime + "\n" + bodies[name]).encode("utf-8")
        files[f"{name}/LICENSE"] = license_bytes
        files[f"{name}/.env.example"] = example_bytes
        for relative, content in common.items():
            files[f"{name}/{relative}"] = content
    return files


def write_files(plan, force=False, dry_run=False, generated=False):
    """Preflight every destination before writing; never remove extra files."""
    pending = []
    for target, content in plan.items():
        target = checked_path(target)
        if (target.is_relative_to(SOURCE) or target.is_relative_to(ROOT / "adapters")
                or target.is_relative_to(ROOT / "scripts")
                or target in {ROOT / "LICENSE", ROOT / ".env.example", ROOT / "project.json"}
                or (target.is_relative_to(PLUGIN) and not generated)):
            raise ValueError(f"Refus de modifier les sources : {target}")
        for parent in target.parents:
            check_windows_path_length(parent, directory=True)
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Le parent n'est pas un dossier : {parent}")
        if target.exists():
            if not target.is_file():
                raise ValueError(f"La destination n'est pas un fichier : {target}")
            if target.read_bytes() == content:
                continue
            if not force:
                raise ValueError(f"Fichier différent existant : {target}. Utilisez --force pour le remplacer.")
        pending.append((target, content))
    if not dry_run:
        for target, content in pending:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    print(f"{'À écrire' if dry_run else 'Écrits'} : {len(pending)} fichiers ; identiques : {len(plan) - len(pending)}.")


def choose_agents():
    if not sys.stdin.isatty():
        raise ValueError("Précisez --agent suivi d'un ou plusieurs noms, ou --skills-dir. Voir la commande list.")
    print("Choisissez une ou plusieurs applications :")
    choices = list(AGENTS)
    for index, name in enumerate(choices, 1):
        print(f"  {index}. {name}")
    selected = input("Applications (noms ou numéros séparés par des espaces) : ").split()
    agents = []
    for item in selected:
        if item.isdigit() and 1 <= int(item) <= len(choices):
            item = choices[int(item) - 1]
        if item not in AGENTS:
            raise ValueError(f"Application inconnue : {item}")
        agents.append(item)
    if not agents:
        raise ValueError("Aucune application sélectionnée ; aucune installation effectuée.")
    return agents


def installation_roots(args):
    if args.skills_dir is not None:
        if args.project is not None or args.scope is not None:
            raise ValueError("--skills-dir s'utilise sans --scope ni --project.")
        return [checked_path(args.skills_dir)]
    scope = args.scope or ("project" if args.project is not None else "user")
    if scope == "user" and args.project is not None:
        raise ValueError("--project ne s'utilise pas avec --scope user.")
    if scope == "project" and args.project is None:
        raise ValueError("Précisez le dossier existant avec --project pour une installation de projet.")
    base = checked_path(args.project if scope == "project" else Path.home())
    if not base.is_dir():
        raise ValueError(f"Dossier de projet ou personnel absent : {base}")
    agents = args.agent or []
    print(f"Portée : {'tous vos projets (compte utilisateur)' if scope == 'user' else 'projet sélectionné'}")
    return list(dict.fromkeys(checked_path(base / AGENTS[agent][scope == "project"]) for agent in agents if agent != "claude-code"))


def install(args):
    if args.skills_dir is None and not args.agent:
        args.agent = choose_agents()
    roots = installation_roots(args)
    from claude_adapter import prepare_install, run_install, refuse_duplicate_copy
    native = None
    if "claude-code" in (args.agent or []):
        native = prepare_install(ROOT, args, NAMES)
    for directory in roots:
        refuse_duplicate_copy(directory, args, NAMES)
    files = portable_files()
    plan = {}
    for directory in roots:
        for name in NAMES:
            destination = directory / name
            if any(destination.is_relative_to(path) or path.is_relative_to(destination) for path in (PLUGIN, SOURCE)):
                raise ValueError(f"La destination recouvre les sources : {destination}")
        print(f"Destination des huit skills : {directory}")
        plan.update((directory / relative, content) for relative, content in files.items())
    # Validate every copy before asking the native manager to change anything.
    if native:
        write_files(plan, args.force, dry_run=True)
        run_install(native, args.dry_run)
    write_files(plan, args.force, args.dry_run)
    if not args.dry_run:
        print("Rechargez les skills ou ouvrez une nouvelle session dans l'application choisie.")
        print("Le plugin natif Claude conserve ses commandes ; les autres harnais utilisent les skills.")
        print("Évitez une seconde copie du même skill dans un autre dossier découvert par l'application.")


def package(args):
    files = portable_files()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, content in sorted(files.items()):
            info = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    target = checked_path(args.output)
    write_files({target: buffer.getvalue()}, args.force, args.dry_run)
    print(f"Archive : {target} ({len(buffer.getvalue())} octets, huit dossiers autonomes)")


def build(args):
    from claude_adapter import distribution
    metadata = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    plan = distribution(ROOT, source_files(), metadata, (SOURCE / "runtime.md").read_text(encoding="utf-8"))
    write_files(plan, args.force, args.dry_run, generated=True)


def export(args):
    domains = set(DOMAINS if "all" in args.domain else args.domain)
    files = portable_files()
    prefix = f"{META}/"
    selected = ["SKILL.md", f"resources/{META}/protocol.md", f"resources/{META}/methodology.md"]
    selected.extend(f"resources/{META}/references/{name}.md" for name in ("qualification", "procedure", "codes-index", "sources"))
    selected.extend(relative.removeprefix(prefix) for relative in files if relative.startswith(f"{prefix}resources/lib/"))
    for domain in DOMAINS:
        if domain in domains:
            selected.extend(relative.removeprefix(prefix) for relative in files if relative.startswith(f"{prefix}resources/{META}-{domain}/"))
    selected.extend(relative.removeprefix(prefix) for relative in files if relative.startswith(f"{prefix}resources/{META}/templates/"))
    selected = list(dict.fromkeys(selected))
    sections = [
        "# legal-france : contexte documentaire\n\n"
        "Les chemins des instructions désignent les sections RESOURCE de ce document. "
        "Seules les ressources listées sont incluses ; demander les extraits manquants "
        "si un autre domaine, le glossaire ou le recueil de décisions est nécessaire. "
        "Cet export ne fournit ni accès web, ni accès aux fichiers, ni scripts exécutables. "
        "Signaler les sources non vérifiées ; ne pas prétendre appeler les API. "
        "Respecter le format demandé et les capacités réelles de l'application.\n\n"
        "Ressources incluses :\n" + "".join(f"- {relative}\n" for relative in selected)
    ]
    for relative in selected:
        sections.append(f"\n---\n\n# RESOURCE: {relative}\n\n" + files[prefix + relative].decode("utf-8").rstrip() + "\n")
    sections.append("\n---\n\n# Licence\n\n" + (ROOT / "LICENSE").read_text(encoding="utf-8"))
    payload = "".join(sections).encode("utf-8")
    target = checked_path(args.output)
    write_files({target: payload}, args.force, args.dry_run)
    print(f"Export : {target} ({len(payload)} octets UTF-8, pas des tokens). Vérifiez la limite de contexte.")


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="Afficher les applications et les destinations")
    builder = commands.add_parser("build", help="Générer le plugin Claude depuis la source commune")
    installer = commands.add_parser("install", help="Installer pour tous vos projets par défaut")
    targets = installer.add_mutually_exclusive_group()
    targets.add_argument("--agent", nargs="+", choices=AGENTS)
    targets.add_argument("--skills-dir", type=Path, help="Dossier parent des skills, emplacement personnalisé")
    installer.add_argument("--scope", choices=("user", "project"), help="user par défaut ; project avec --project")
    installer.add_argument("--project", type=Path, help="Dossier existant ; sélectionne la portée projet")
    packager = commands.add_parser("package", help="Créer un ZIP pour une installation sans Python")
    packager.add_argument("--output", type=Path, required=True)
    exporter = commands.add_parser("export", help="Créer un contexte Markdown pour les interfaces sans skills")
    exporter.add_argument("--domain", nargs="+", choices=(*DOMAINS, "all"), required=True)
    exporter.add_argument("--output", type=Path, required=True)
    for command in (installer, packager, exporter, builder):
        command.add_argument("--dry-run", action="store_true", help="Afficher les écritures prévues sans écrire")
        command.add_argument("--force", action="store_true", help="Remplacer les fichiers distribués différents, conserver les fichiers supplémentaires")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "list":
            for name, (personal, project) in AGENTS.items():
                if name == "claude-code":
                    print(f"{name:16} gestionnaire natif de plugins ; portée user ou project")
                else:
                    print(f"{name:16} personnel : ~/{personal:30} projet : {project}")
            print("Les applications utilisant .agents/skills partagent une seule copie.")
        elif args.command == "install":
            install(args)
        elif args.command == "package":
            package(args)
        elif args.command == "build":
            build(args)
        else:
            export(args)
    except (OSError, ValueError, EOFError) as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Installation interrompue.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
