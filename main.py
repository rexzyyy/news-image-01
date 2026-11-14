#!/usr/bin/env python3
"""Write the bundled make.fun entry image to the requested output directory."""

import base64
import os
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"
MAX_PNG_BYTES = 1_048_576


def main():
    source = Path(__file__).resolve().with_name("entry.png.b64")
    # The bundled source is one base64 line; strip its trailing newline.
    encoded = source.read_text(encoding="ascii").strip()
    try:
        image = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise SystemExit(f"Invalid base64 image in {source.name}: {exc}") from exc

    if not image.startswith(PNG_SIGNATURE):
        raise SystemExit("Decoded image does not have a PNG signature")
    if len(image) > MAX_PNG_BYTES:
        raise SystemExit(f"Decoded PNG is larger than {MAX_PNG_BYTES} bytes")
    if not image.endswith(PNG_IEND):
        raise SystemExit("Decoded PNG is missing its required IEND trailer")

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.png").write_bytes(image)


if __name__ == "__main__":
    main()
