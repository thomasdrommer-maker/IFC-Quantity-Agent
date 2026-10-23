#!/usr/bin/env python3
from pathlib import Path
import os
import sys

PACKAGE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE_ROOT / "src"))

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "ifc_quantity_agent_mvp1.api:app",
        host=os.getenv("IQA_API_HOST", "127.0.0.1"),
        port=int(os.getenv("IQA_API_PORT", "8000")),
        reload=False,
        app_dir=str(PACKAGE_ROOT / "src"),
    )

