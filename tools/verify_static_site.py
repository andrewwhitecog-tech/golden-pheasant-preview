#!/usr/bin/env python3
"""Dependency-free integrity and local HTTP smoke checks for the static preview."""

from __future__ import annotations

import argparse
from functools import partial
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import unquote, urlsplit
from urllib.request import urlopen
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "https://andrewwhitecog-tech.github.io/golden-pheasant-preview/"
REQUIRED_FILES = (
    "index.html",
    "logo.png",
    "robots.txt",
    "sitemap.xml",
    "site.webmanifest",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[tuple[str, str, str]] = []
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {name: value or "" for name, value in attrs}
        if data.get("id"):
            self.ids.add(data["id"])
        if tag == "meta":
            key = data.get("name") or data.get("property")
            if key:
                self.meta[key] = data.get("content", "")
        if tag == "link":
            self.links.append(data)
        if tag == "title":
            self.in_title = True
        for attribute in ("href", "src", "action"):
            if data.get(attribute):
                self.references.append((tag, attribute, data[attribute]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def verify_static() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        require((ROOT / relative).is_file(), f"missing required file: {relative}", errors)
    if errors:
        return errors

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(html)

    require(bool("".join(parser.title_parts).strip()), "document title is empty", errors)
    require(parser.meta.get("description", "").strip() != "", "meta description is missing", errors)
    require("licensed" not in parser.meta.get("description", "").lower(),
            "meta description must not claim a verified license while CCB is pending", errors)
    for key in ("og:title", "og:description", "og:url", "og:image", "twitter:card"):
        require(bool(parser.meta.get(key)), f"missing social metadata: {key}", errors)

    canonical_links = [link for link in parser.links if "canonical" in link.get("rel", "").split()]
    require(len(canonical_links) == 1, "expected exactly one canonical link", errors)
    if canonical_links:
        require(canonical_links[0].get("href") == CANONICAL, "canonical URL is incorrect", errors)

    for tag, attribute, reference in parser.references:
        parsed = urlsplit(reference)
        if parsed.scheme in {"http", "https", "mailto", "tel", "data"}:
            continue
        if reference.startswith("#"):
            require(unquote(reference[1:]) in parser.ids,
                    f"broken in-page link: {tag}[{attribute}]={reference}", errors)
            continue
        relative_path = unquote(parsed.path)
        if not relative_path:
            continue
        target = (ROOT / relative_path).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"local reference escapes site root: {reference}")
            continue
        require(target.exists(), f"missing local link target: {reference}", errors)

    json_ld_matches = re.findall(
        r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    require(len(json_ld_matches) == 1, "expected exactly one JSON-LD block", errors)
    if json_ld_matches:
        try:
            schema = json.loads(json_ld_matches[0])
            require(schema.get("@type") == "HousePainter", "JSON-LD @type must be HousePainter", errors)
            def nested_keys(value: object) -> set[str]:
                if isinstance(value, dict):
                    return {str(key).lower() for key in value} | {
                        nested for child in value.values() for nested in nested_keys(child)
                    }
                if isinstance(value, list):
                    return {nested for child in value for nested in nested_keys(child)}
                return set()

            schema_keys = nested_keys(schema)
            for unsupported in ("review", "rating", "openinghours", "license", "streetaddress"):
                require(unsupported not in schema_keys,
                        f"JSON-LD contains unsupported claim field: {unsupported}", errors)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON-LD: {exc}")

    try:
        manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
        require(manifest.get("start_url") == "./", "manifest start_url must stay preview-portable", errors)
        for icon in manifest.get("icons", []):
            require((ROOT / icon.get("src", "")).is_file(),
                    f"manifest icon is missing: {icon.get('src', '')}", errors)
    except json.JSONDecodeError as exc:
        errors.append(f"invalid web manifest JSON: {exc}")

    try:
        sitemap = ET.parse(ROOT / "sitemap.xml")
        locations = [node.text for node in sitemap.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        require(locations == [CANONICAL], "sitemap canonical URL is incorrect", errors)
    except ET.ParseError as exc:
        errors.append(f"invalid sitemap XML: {exc}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    require(f"Sitemap: {CANONICAL}sitemap.xml" in robots, "robots.txt sitemap URL is incorrect", errors)
    for safety_copy in ("PREVIEW DRAFT", "CCB # pending", "uses placeholders", "Nothing is sent or stored"):
        require(safety_copy in html, f"required preview disclosure is missing: {safety_copy}", errors)
    require('href="tel:+15035839175"' in html, "accessible telephone link is missing", errors)
    require('href="mailto:andrew@goldenpheasantpc.com"' in html, "accessible email link is missing", errors)
    return errors


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def verify_http() -> list[str]:
    errors: list[str] = []
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_port}/"
        for relative in REQUIRED_FILES:
            path = "" if relative == "index.html" else relative
            try:
                with urlopen(base + path, timeout=5) as response:
                    body = response.read()
                    require(response.status == 200, f"HTTP {response.status}: /{path}", errors)
                    require(bool(body), f"empty HTTP response: /{path}", errors)
            except Exception as exc:  # pragma: no cover - error path is the report itself
                errors.append(f"HTTP smoke failed for /{path}: {exc}")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--http-smoke", action="store_true", help="also serve the site on an ephemeral local port and fetch every public root asset")
    args = parser.parse_args()
    errors = verify_static()
    if args.http_smoke and not errors:
        errors.extend(verify_http())
    if errors:
        print("FAIL: Golden Pheasant static preview")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: Golden Pheasant static preview")
    print(f"  canonical: {CANONICAL}")
    print(f"  local references: verified")
    print(f"  JSON-LD, manifest, sitemap, and disclosures: verified")
    if args.http_smoke:
        print(f"  local HTTP endpoints: {len(REQUIRED_FILES)}/5 returned 200 with content")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
