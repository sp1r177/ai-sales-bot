from __future__ import annotations

import os
import uuid
from typing import Tuple

from fastapi import UploadFile


MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "media")
MEDIA_ROOT = os.path.abspath(MEDIA_ROOT)


class LocalStorage:
    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or MEDIA_ROOT
        os.makedirs(self.base_dir, exist_ok=True)

    def save_image(self, file: UploadFile) -> Tuple[str, str]:
        ext = os.path.splitext(file.filename or "")[1] or ".bin"
        name = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(self.base_dir, name)
        with open(path, "wb") as f:
            f.write(file.file.read())
        return name, path