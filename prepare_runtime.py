"""Short, versioned Python environment for Windows. v0.3.7 / 2026-11-03 / OpenAI Codex."""
from hashlib import sha256
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def environment_path(base: Path, requirements: bytes) -> Path:
    key = sha256(requirements + f'|{sys.version_info[:2]}|{sys.platform}'.encode()).hexdigest()[:12]
    return base / ('p314-' + key)


def prepare(base: Path, requirements: Path, runner=subprocess.run) -> Path:
    env = environment_path(base, requirements.read_bytes())
    python = env / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    # Native Windows modules may still hit legacy loader limits.
    if os.name == 'nt' and len(str(env.resolve())) > 130:
        raise RuntimeError('Umgebungspfad zu lang. IQA_ENV_ROOT auf einen kurzen beschreibbaren Ordner setzen.')
    env.parent.mkdir(parents=True, exist_ok=True)
    if not python.exists():
        print('[1/3] Kurze Python-Umgebung wird erstellt: ' + str(env), flush=True)
        runner([sys.executable, '-m', 'venv', str(env)], check=True)
    marker = env / '.ready'
    if not marker.exists():
        print('[2/3] Abhaengigkeiten werden installiert ...', flush=True)
        runner([str(python), '-m', 'pip', 'install', '-r', str(requirements)], check=True)
    try:
        runner([str(python), '-c', 'import ifcopenshell, fastapi, uvicorn'], check=True)
    except subprocess.CalledProcessError:
        marker.unlink(missing_ok=True)
        raise
    marker.write_text('imports checked\n', encoding='utf-8')
    return python


def main():
    if sys.version_info[:2] != (3, 14):
        raise RuntimeError('Der Windows-Starter benoetigt Python 3.14.')
    default = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'IQA'
    base = Path(os.environ.get('IQA_ENV_ROOT', str(default)))
    python = prepare(base, ROOT / 'requirements.txt')
    print('[3/3] Anwendung wird gestartet. Dieses Fenster geoeffnet lassen.', flush=True)
    return subprocess.run([str(python), str(ROOT / 'run_api.py')], cwd=ROOT).returncode


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print('Start fehlgeschlagen: ' + str(exc), flush=True)
        sys.exit(1)
