# DeepSkySuite

Descargas de **DeepSkyForce** (apilado y procesado de astrofotografía) y
**DeepSkyCopilot** (copiloto de captura, alineación polar y control de telescopios Alpaca).

## Descarga

Entra en [Releases](../../releases) y descarga el zip de tu sistema:

- `DeepSkySuite-MacOS-AAAA-MM-DD.zip`
- `DeepSkySuite-Windows-AAAA-MM-DD.zip`

Cada zip contiene las dos aplicaciones. Las aplicaciones avisan automáticamente
cuando hay una versión nueva, muestran sus novedades y ofrecen descargarla.

## Primera apertura

- **macOS:** si aparece "no se puede abrir porque es de un desarrollador no
  identificado", haz clic derecho sobre la app → Abrir → Abrir.
- **Windows:** si aparece SmartScreen, pulsa "Más información" → "Ejecutar de todas formas".

## Novedades

- [DeepSkyForce](releases/DeepSkyForce.txt)
- [DeepSkyCopilot](releases/DeepSkyCopilot.txt)

---

## Publicar una versión (sólo para el mantenedor)

En cada máquina (macOS y Windows), con este repositorio junto a los proyectos
`DeepSkyForce` y `DeepSkyCopilot`:

1. `git pull` en este repositorio.
2. Compilar las dos aplicaciones (`build.sh` / `build.bat` de cada proyecto).
3. `python tools/prepare_release.py --tag AAAA-MM-DD` (por defecto, la fecha de hoy).
   Genera `dist/DeepSkySuite-<plataforma>-<etiqueta>.zip`, copia los `releases.txt`
   a `releases/` y anota la versión de cada aplicación en `versions.json`.
4. En GitHub → Releases: crear la Release con esa etiqueta (o editarla si la otra
   plataforma ya la creó) y adjuntar el zip de `dist/`.
5. Sólo después: `git add -A && git commit && git push`.

Las aplicaciones leen `versions.json` y `releases/` de la rama `main`, y descargan
el zip desde la Release. Los zips nunca se suben con git (GitHub rechaza ficheros
de más de 100 MB en un push).
