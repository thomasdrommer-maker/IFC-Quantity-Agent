#!/usr/bin/env python3
from pathlib import Path
import json
import sys

PACKAGE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE_ROOT / "src"))

from ifc_quantity_agent_mvp1.api import app


target = PACKAGE_ROOT / "openapi" / "ifc_quantity_agent_mvp1_openapi_v1.json"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(app.openapi(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(target)

