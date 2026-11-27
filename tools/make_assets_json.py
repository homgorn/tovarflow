"""Prepare a base64 asset bundle for the Cloudflare Workers direct-upload API.

Output: site_assets.json at the repository root:
  { manifest: {path: {hash,size}}, files: {hash: base64}, hashes: {hash: path} }

Hash rule follows Cloudflare's example: sha256(base64(file) + extension), first 32 hex chars.
"""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
OUT = ROOT / "site_assets.json"


def main() -> int:
    manifest, files, hashes = {}, {}, {}
    for path in sorted(SITE.rglob("*")):
        if not path.is_file():
            continue
        content = path.read_bytes()
        ext = path.suffix.lstrip(".")
        encoded = base64.b64encode(content).decode("ascii")
        digest = hashlib.sha256((encoded + ext).encode("ascii")).hexdigest()[:32]
        rel = "/" + path.relative_to(SITE).as_posix()
        manifest[rel] = {"hash": digest, "size": len(content)}
        files[digest] = encoded
        hashes[digest] = rel
    OUT.write_text(json.dumps({"manifest": manifest, "files": files, "hashes": hashes},
                              ensure_ascii=False), encoding="utf-8")
    print(f"{len(manifest)} assets, {OUT.stat().st_size} bytes bundle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
