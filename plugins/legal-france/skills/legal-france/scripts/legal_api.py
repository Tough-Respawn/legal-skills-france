#!/usr/bin/env python3
"""Optional PISTE clients, Python 3.9+ standard library only.

No network or credential lookup without --use-api. See lib/legifrance-client.md
and lib/judilibre-client.md for the web-first workflow and source schemas.
"""

import argparse
from datetime import date, datetime, timedelta, timezone
from http.client import HTTPException
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener


OAUTH_URL = "https://oauth.piste.gouv.fr/api/oauth/token"
API_ROOTS = {
    "legifrance": "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app",
    "judilibre": "https://api.piste.gouv.fr/cassation/judilibre/v1.0",
}
MAX_RESPONSE_BYTES = 32 * 1024 * 1024
KEYS = {
    prefix + suffix
    for prefix in ("PISTE_", "LEGIFRANCE_", "JUDILIBRE_")
    for suffix in ("CLIENT_ID", "CLIENT_SECRET")
}


class ApiError(Exception):
    def __init__(self, code, message, exit_code=6, **details):
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code
        self.details = details


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward the OAuth body or Authorization header to another URL.
        return None


def read_credentials(service, env_file):
    values = {}
    try:
        content = env_file.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        content = ""
    except (OSError, UnicodeError):
        raise ApiError("CONFIG_UNREADABLE", "Fichier de configuration illisible.", 4)
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, sep, value = line.partition("=")
        key = key.strip()
        if not sep or key not in KEYS:
            continue
        value = value.strip()
        if value.startswith(("'", '"')):
            quote = value[0]
            end = value.find(quote, 1)
            if end < 0 or (value[end + 1:].strip() and not value[end + 1:].lstrip().startswith("#")):
                raise ApiError("CONFIG_INVALID", "Valeur de configuration mal délimitée.", 4)
            value = value[1:end]
        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
        # Literal values only: no interpolation, eval, sourcing or shell calls.
        if key in values:
            raise ApiError("CONFIG_INVALID", "Clé de configuration dupliquée.", 4)
        values[key] = value
    for key in KEYS:
        if key in os.environ:
            values[key] = os.environ[key].strip()
    prefix = service.upper() + "_"
    # A partially configured service-specific pair must not borrow the other
    # half of the common pair (which may belong to a different application).
    if not any(values.get(prefix + suffix) for suffix in ("CLIENT_ID", "CLIENT_SECRET")):
        prefix = "PISTE_"
    client_id = values.get(prefix + "CLIENT_ID", "")
    secret = values.get(prefix + "CLIENT_SECRET", "")
    if not client_id or not secret:
        raise ApiError("CREDENTIALS_MISSING", "Identifiants OAuth incomplets ; poursuivre sur le web.", 4)
    if any(char in client_id + secret for char in ("\r", "\n", "\x00")):
        raise ApiError("CONFIG_INVALID", "Identifiants OAuth invalides.", 4)
    return client_id, secret


class PisteClient:
    def __init__(self, service, env_file, timeout):
        self.root = API_ROOTS[service]
        self.client_id, self.secret = read_credentials(service, env_file)
        self.redactions = [self.client_id, self.secret]
        self.token = None
        self.timeout = timeout
        self.opener = build_opener(NoRedirects())

    def request_json(self, request, authentication=False):
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
        except HTTPError as exc:
            status = exc.code
            retry_after = exc.headers.get("Retry-After", "") if exc.headers else ""
            exc.close()
            details = {"http_status": status}
            if retry_after.isdigit() and len(retry_after) < 10:
                details["retry_after_seconds"] = int(retry_after)
            if authentication or status in (401, 403):
                raise ApiError("AUTH_OR_SUBSCRIPTION_FAILED", "Authentification ou accès à cette API refusé.", 5, **details)
            raise ApiError("HTTP_FAILED", "API indisponible ; poursuivre sur le web.", **details)
        except (URLError, OSError, TimeoutError, HTTPException):
            raise ApiError("NETWORK_FAILED", "Connexion à PISTE impossible ; poursuivre sur le web.")
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ApiError("RESPONSE_TOO_LARGE", "Réponse trop volumineuse ; préciser la consultation.")
        try:
            data = json.loads(raw)
        except (ValueError, UnicodeError):
            raise ApiError("INVALID_RESPONSE", "Réponse JSON inexploitable.")
        if not isinstance(data, dict):
            raise ApiError("INVALID_RESPONSE", "Structure de réponse inattendue.")
        if data.get("error") or data.get("errors"):
            # Do not echo error bodies: they may contain request details.
            if authentication:
                raise ApiError("AUTH_FAILED", "Le service OAuth a refusé l'authentification.", 5)
            raise ApiError("API_FAILED", "Le service a signalé une erreur.")
        return data

    def authenticate(self):
        body = urlencode({"grant_type": "client_credentials", "scope": "openid",
                          "client_id": self.client_id, "client_secret": self.secret}).encode("utf-8")
        request = Request(OAUTH_URL, data=body, headers={
            "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"})
        data = self.request_json(request, authentication=True)
        token = data.get("access_token")
        if not isinstance(token, str) or not token or any(c in token for c in "\r\n\x00"):
            raise ApiError("AUTH_FAILED", "Aucun jeton OAuth utilisable.", 5)
        self.token = token
        self.redactions.append(token)

    def call(self, path, body=None, query=None):
        if not self.token:
            self.authenticate()
        url = self.root + path
        if query:
            url += "?" + urlencode(query)
        for attempt in range(2):
            headers = {"Accept": "application/json", "Authorization": "Bearer " + self.token}
            data = None
            if body is not None:
                headers["Content-Type"] = "application/json"
                data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            try:
                return self.request_json(Request(url, data=data, headers=headers))
            except ApiError as exc:
                if attempt == 0 and exc.details.get("http_status") == 401:
                    self.authenticate()
                    continue
                raise


def iso_date(value):
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError("Date requise au format YYYY-MM-DD.")


def identifier(prefixes):
    def parse(value):
        if not re.fullmatch("(?:" + "|".join(prefixes) + r")\d{12}", value):
            raise argparse.ArgumentTypeError("Identifiant Légifrance invalide.")
        return value
    return parse


def bounded_int(minimum, maximum):
    def parse(value):
        try:
            result = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("Nombre entier requis.")
        if not minimum <= result <= maximum:
            raise argparse.ArgumentTypeError(f"Valeur attendue entre {minimum} et {maximum}.")
        return result
    return parse


def version_date(value):
    """Read a DILA day without depending on Windows epoch or local timezone.

    Non-midnight timestamps are left unresolved instead of silently rounding
    a timestamp that could denote a different civil day.
    """
    try:
        if isinstance(value, bool) or value is None:
            raise ValueError
        text = str(value)
        if re.fullmatch(r"-?\d+", text):
            stamp = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(milliseconds=int(text))
        elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
            return date.fromisoformat(text)
        else:
            stamp = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if (stamp.hour, stamp.minute, stamp.second, stamp.microsecond) != (0, 0, 0, 0):
            raise ValueError
        return stamp.date()
    except (ValueError, TypeError, OverflowError):
        raise ApiError("VERSION_DATE_UNCERTAIN", "Borne temporelle absente ou ambiguë ; vérifier la version sur le web.", 7)


def article_at_date(client, args):
    cid = args.cid
    if args.id:
        response = client.call("/consult/getArticle", body={"id": args.id})
        article = response.get("article")
        if not isinstance(article, dict) or article.get("id") != args.id:
            raise ApiError("ARTICLE_MISMATCH", "L'article retourné ne correspond pas à l'identifiant demandé.", 7)
        cid = article.get("cid")
    if not isinstance(cid, str) or not re.fullmatch(r"(?:LEGI|JORF)ARTI\d{12}", cid):
        raise ApiError("CID_MISSING", "Identifiant commun de l'article indisponible.", 7)
    response = client.call("/consult/getArticleByCid", body={"cid": cid})
    versions = response.get("listArticle")
    if not isinstance(versions, list):
        raise ApiError("VERSIONS_MISSING", "Historique des versions indisponible.", 7)
    target = date.fromisoformat(args.date)
    matches = {}
    for article in versions:
        if not isinstance(article, dict) or article.get("cid") != cid:
            raise ApiError("VERSION_MISMATCH", "Historique de versions incohérent.", 7)
        state = article.get("etat")
        if not isinstance(state, str) or not state:
            raise ApiError("VERSION_STATE_MISSING", "État juridique d'une version inconnu.", 7)
        if "MORT_NE" in state:
            continue
        start, end = version_date(article.get("dateDebut")), version_date(article.get("dateFin"))
        if end < start:
            raise ApiError("VERSION_RANGE_INVALID", "Intervalle de version incohérent.", 7)
        if start <= target < end:
            article_id = article.get("id")
            if not isinstance(article_id, str) or not re.fullmatch(r"LEGIARTI\d{12}", article_id):
                raise ApiError("VERSION_ID_INVALID", "Identifiant de version inexploitable.", 7)
            if article_id in matches and matches[article_id] != article:
                raise ApiError("VERSION_AMBIGUOUS", "Versions contradictoires pour un même identifiant.", 7)
            matches[article_id] = article
    if len(matches) != 1:
        raise ApiError("VERSION_NOT_UNIQUE", "Aucune version unique pour cette date ; consulter l'historique sur le web.", 7,
                       matching_versions=len(matches), requested_date=args.date)
    article = next(iter(matches.values()))
    if not (article.get("texte") or article.get("texteHtml")):
        raise ApiError("ARTICLE_TEXT_MISSING", "Texte de la version indisponible.", 7)
    return {"requested_date": args.date, "requested_id": args.id, "cid": cid,
            "selection": "dateDebut <= date demandée < dateFin",
            "legal_applicability": "à examiner selon les faits et les dispositions transitoires",
            "article": article}


def run(client, args):
    if args.service == "legifrance":
        if args.operation == "article":
            return article_at_date(client, args), "/consult/getArticleByCid"
        data = client.call("/consult/legiPart", body={"textId": args.id, "date": args.date})
        returned_id = data.get("id", "")
        if not isinstance(returned_id, str) or (returned_id.split("_")[0] != args.id and data.get("cid") != args.id):
            raise ApiError("TEXT_MISMATCH", "Le texte retourné ne correspond pas à l'identifiant demandé.", 7)
        start = version_date(data.get("dateDebutVersion"))
        end = version_date(data.get("dateFinVersion"))
        if not start <= date.fromisoformat(args.date) < end:
            raise ApiError("TEXT_DATE_MISMATCH", "La version retournée ne couvre pas la date demandée.", 7)
        if not any(data.get(key) for key in ("sections", "articles")):
            raise ApiError("TEXT_CONTENT_MISSING", "Contenu du texte indisponible à la date demandée.", 7)
        return {"requested_date": args.date, "requested_id": args.id, "text": data,
                "legal_applicability": "à examiner selon les faits et les dispositions transitoires"}, "/consult/legiPart"
    if args.operation == "decision":
        data = client.call("/decision", query={"id": args.id})
        if data.get("id") != args.id or not data.get("text"):
            raise ApiError("DECISION_MISMATCH", "Décision absente, incomplète ou identifiant incohérent.", 7)
        return data, "/decision"
    if args.date_start and args.date_end and args.date_start > args.date_end:
        raise ApiError("DATE_RANGE_INVALID", "La date de début doit précéder la date de fin.", 2)
    if not args.query.strip():
        raise ApiError("QUERY_EMPTY", "Une recherche non vide est nécessaire.", 2)
    query = {"query": args.query, "page_size": args.page_size, "page": args.page,
             "sort": args.sort, "order": args.order, "jurisdiction": args.jurisdiction}
    for key in ("chamber", "date_start", "date_end"):
        if getattr(args, key):
            query[key] = getattr(args, key)
    data = client.call("/search", query=query)
    if not isinstance(data.get("results"), list):
        raise ApiError("SEARCH_INVALID", "Résultats de recherche inexploitables.")
    return data, "/search"


def parser():
    cli = argparse.ArgumentParser(description="Clients PISTE facultatifs. Le web reste le mode par défaut.")
    cli.add_argument("--use-api", action="store_true", help="Choix explicite de l'API pour cet appel.")
    cli.add_argument("--env-file", type=Path, default=Path(".env"), help="Fichier lu textuellement, dans le cwd par défaut.")
    cli.add_argument("--timeout", type=bounded_int(1, 60), default=20)
    services = cli.add_subparsers(dest="service", required=True)
    lf_service = services.add_parser("legifrance")
    lf = lf_service.add_subparsers(dest="operation", required=True)
    article = lf.add_parser("article", help="Sélectionner une version d'article à une date explicite.")
    ids = article.add_mutually_exclusive_group(required=True)
    ids.add_argument("--id", type=identifier(["LEGIARTI"]))
    ids.add_argument("--cid", type=identifier(["LEGIARTI", "JORFARTI"]))
    article.add_argument("--date", type=iso_date, required=True)
    text = lf.add_parser("text", help="Consulter un texte LEGI à une date explicite.")
    text.add_argument("--id", type=identifier(["LEGITEXT"]), required=True)
    text.add_argument("--date", type=iso_date, required=True)
    jd_service = services.add_parser("judilibre")
    jd = jd_service.add_subparsers(dest="operation", required=True)
    search = jd.add_parser("search")
    search.add_argument("--query", required=True)
    search.add_argument("--chamber")
    search.add_argument("--jurisdiction", choices=["cc", "ca", "tj", "tcom", "cph"], default="cc")
    search.add_argument("--date-start", type=iso_date)
    search.add_argument("--date-end", type=iso_date)
    search.add_argument("--page", type=bounded_int(0, 10000), default=0)
    search.add_argument("--page-size", type=bounded_int(1, 50), default=10)
    search.add_argument("--sort", choices=["score", "scorepub", "date"], default="scorepub")
    search.add_argument("--order", choices=["asc", "desc"], default="desc")
    decision = jd.add_parser("decision")
    decision.add_argument("--id", required=True)
    for level in (lf_service, jd_service, article, text, search, decision):
        # Missing options at a deeper level must preserve the parent's value.
        level.add_argument("--env-file", type=Path, default=argparse.SUPPRESS,
                           help="Fichier de configuration lu textuellement.")
    return cli


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parser().parse_args()
    client = None
    exit_code = 0
    try:
        if not args.use_api:
            raise ApiError("API_NOT_REQUESTED", "API non activée ; utiliser la recherche et la lecture web.", 3)
        client = PisteClient(args.service, args.env_file, args.timeout)
        data, path = run(client, args)
        result = {"ok": True, "source": args.service, "endpoint": API_ROOTS[args.service] + path,
                  "retrieved_at": datetime.now(timezone.utc).isoformat(), "data": data}
    except ApiError as exc:
        exit_code = exc.exit_code
        result = {"ok": False, "source": args.service, "error": exc.code,
                  "message": str(exc), "fallback": "web", **exc.details}
    except (ValueError, TypeError, OSError, HTTPException):
        exit_code = 6
        result = {"ok": False, "source": args.service, "error": "CLIENT_FAILED",
                  "message": "Consultation impossible ; poursuivre sur le web.", "fallback": "web"}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if client:
        for value in sorted(client.redactions, key=len, reverse=True):
            # Escape exactly as JSON serialization does, including quotes/backslashes.
            escaped = json.dumps(value, ensure_ascii=False)[1:-1]
            output = output.replace(escaped, "[REDACTED]")
    print(output)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
