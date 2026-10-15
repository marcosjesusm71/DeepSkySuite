"""Prepara la parte de ESTA plataforma de una versión de DeepSkySuite.

Se ejecuta en cada máquina (macOS y Windows) después de compilar DeepSkyForce y
DeepSkyCopilot con su build.sh / build.bat:

    python tools/prepare_release.py                 # etiqueta = fecha de hoy
    python tools/prepare_release.py --tag 2026-10-20

Hace tres cosas:
  1. Crea dist/DeepSkySuite-<MacOS|Windows>-<etiqueta>.zip con las dos aplicaciones.
  2. Copia el releases.txt de cada aplicación a releases/.
  3. Anota en versions.json, para esa etiqueta y plataforma, el zip y la fecha de
     compilación de CADA aplicación (leída de su build/build_info.json). Las
     aplicaciones comparan esa fecha con la suya para saber si hay versión nueva.

Después: adjuntar el zip a la Release de GitHub con la MISMA etiqueta y, sólo
entonces, commit + push (ver README.md). El zip nunca se sube con git.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS = ("DeepSkyForce", "DeepSkyCopilot")
PLATFORM = {"darwin": "MacOS", "win32": "Windows"}.get(sys.platform)


def build_artifact(project, name):
    """Aplicación compilada: .app en macOS, .exe (un solo fichero) en Windows."""
    dist = project / "dist"
    return dist / (f"{name}.app" if sys.platform == "darwin" else f"{name}.exe")


def read_build_info(project):
    path = project / "build" / "build_info.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    built_at = datetime.fromisoformat(data["built_at"]).astimezone(timezone.utc)
    return built_at, data


def make_zip(artifacts, destination):
    """Zip con una carpeta DeepSkySuite/ que contiene las dos aplicaciones."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    if sys.platform == "darwin":
        # ditto conserva enlaces simbólicos, permisos y firma de los .app;
        # zipfile de Python los rompería y la app no arrancaría.
        with tempfile.TemporaryDirectory(prefix="deepskysuite-") as tmp:
            staging = Path(tmp) / "DeepSkySuite"
            staging.mkdir()
            for artifact in artifacts:
                subprocess.run(["ditto", str(artifact), str(staging / artifact.name)],
                               check=True)
            subprocess.run(["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent",
                            str(staging), str(destination)], check=True)
    else:
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
            for artifact in artifacts:
                archive.write(artifact, f"DeepSkySuite/{artifact.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", default=date.today().isoformat(),
                        help="Etiqueta de la Release (por defecto, la fecha de hoy AAAA-MM-DD)")
    for name in APPS:
        parser.add_argument(f"--{name.lower()}", type=Path, default=ROOT.parent / name,
                            help=f"Proyecto de {name} (por defecto ../{name})")
    args = parser.parse_args()
    if PLATFORM is None:
        raise SystemExit("Sólo se puede preparar una versión en macOS o Windows.")

    artifacts, apps = [], {}
    for name in APPS:
        project = getattr(args, name.lower()).resolve()
        artifact = build_artifact(project, name)
        if not artifact.exists():
            raise SystemExit(f"No encuentro {artifact}: compila {name} antes.")
        built_at, info = read_build_info(project)
        built = datetime.fromtimestamp(artifact.stat().st_mtime, timezone.utc)
        if built < built_at - timedelta(minutes=1):
            raise SystemExit(f"{artifact.name} es anterior a su build_info.json: "
                             "¿falló la última compilación? Vuelve a compilar.")
        artifacts.append(artifact)
        apps[name] = {"built_at": built_at.isoformat(timespec="seconds"),
                      "version": info.get("version", "")}
        notes = project / "releases.txt"
        if notes.exists():
            shutil.copyfile(notes, ROOT / "releases" / f"{name}.txt")
        print(f"  {name}: versión {apps[name]['version']} compilada {apps[name]['built_at']}")

    zip_name = f"DeepSkySuite-{PLATFORM}-{args.tag}.zip"
    zip_path = ROOT / "dist" / zip_name
    print(f"==> Creando {zip_path.relative_to(ROOT)} ...")
    make_zip(artifacts, zip_path)

    versions_path = ROOT / "versions.json"
    data = json.loads(versions_path.read_text(encoding="utf-8"))
    versions = data.setdefault("versions", [])
    entry = next((v for v in versions if v.get("tag") == args.tag), None)
    if entry is None:
        entry = {"tag": args.tag}
        versions.append(entry)
    elif PLATFORM in entry:
        print(f"  Aviso: la etiqueta {args.tag} ya tenía versión de {PLATFORM}; se sustituye.")
    entry[PLATFORM] = {"zip": zip_name, "size": zip_path.stat().st_size, "apps": apps}
    versions.sort(key=lambda v: v.get("tag", ""), reverse=True)
    versions_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")

    size_mb = zip_path.stat().st_size / 1e6
    print(f"""
Listo ({size_mb:.0f} MB). Siguientes pasos, EN ESTE ORDEN:
  1. En https://github.com/marcosjesusm71/DeepSkySuite/releases :
     - si la Release {args.tag} no existe: «Draft a new release», etiqueta {args.tag};
     - si ya existe (la otra plataforma la creó): ábrela y pulsa «Edit».
     Adjunta dist/{zip_name} y publica / actualiza.
  2. git add -A && git commit -m "{PLATFORM} {args.tag}" && git push
Las aplicaciones avisan en cuanto versions.json llega a GitHub (paso 2): por eso
el zip debe estar adjunto antes.""")


if __name__ == "__main__":
    main()
