# SPDX-License-Identifier: MPL-2.0
# GPL-3.0-or-later combination: see LICENSING.md.
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    def __init__(self):
        with (BASE_DIR / "config.yaml").open(encoding="utf-8") as f:
            config = yaml.safe_load(f)
        for i in config:
            setattr(self, i, config[i])


config = Config()
