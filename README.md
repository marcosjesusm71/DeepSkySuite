# DeepSkySuite

Descargas de **DeepSkyForce** (apilado y procesado de astrofotografía) y
**DeepSkyCopilot** (copiloto de captura, alineación polar y control de telescopios Alpaca).
Web: https://deepsky.macas.es

> **Beta abierta.** Cualquiera puede descargarla y usarla gratis. Lo que más ayuda es que la
> pruebes en tus noches reales y nos cuentes qué falla y qué echas en falta.

## Cómo opinar

- **Botón «Mensajes»** en la cabecera de las dos apps: cuenta el error o la idea, añade
  capturas si quieres y la app adjunta el registro del día. Cuando se resuelve, la app te
  avisa con la respuesta.
- **Telegram:** https://t.me/deepskysuite
- **Correo:** deepskysuite@gmail.com

## Requisitos

- macOS 13 o posterior en un Mac con Apple Silicon (M1 a M5). No hay versión para Mac Intel.
- Windows 10 u 11 de 64 bits.
- ASTAP (para resolver las fotos) se instala desde la propia app.

## Hardware probado

- **DeepSkyCopilot:** probado con Seestar S30 y S50. S30 Pro, S50 Pro y otros telescopios
  Alpaca deberían funcionar, pero aún no se han probado: cuéntanos qué tal.
- **DeepSkyForce:** probado con imágenes de Seestar y DWARF. Con cámaras mono apila un solo
  filtro (luminancia, Hα…).

Cada versión beta caduca a los 90 días: la app avisa unos días antes y se actualiza con un clic.

## Descarga

Entra en [la última versión](../../releases/latest) y descarga el zip de tu sistema:

- `DeepSkySuite-MacOS-AAAA-MM-DD.zip`
- `DeepSkySuite-Windows-AAAA-MM-DD.zip`

Cada zip contiene las dos aplicaciones. Descomprímelo y sustituye las versiones
anteriores por las nuevas. A partir de ahí, las aplicaciones avisan solas cuando hay
una nueva, muestran sus novedades y se actualizan.

## Primera apertura

Las apps no están firmadas por Apple ni Microsoft, así que el sistema avisa la primera vez.

- **macOS 15 (Sequoia) o posterior:** si aparece un aviso de que la app no se
  puede verificar, ciérralo, abre **Ajustes del Sistema → Privacidad y seguridad**,
  baja hasta el mensaje sobre la app y pulsa **Abrir igualmente** (te pedirá la
  contraseña). Hay que hacerlo **una vez con cada app**: primero con una y luego con la otra.
- **macOS 14 o anterior:** haz clic derecho sobre la app → **Abrir** → **Abrir** (también
  con cada app).
- **Windows:** si aparece SmartScreen, pulsa **Más información → Ejecutar de todas formas**.
- **Si Windows Defender o el antivirus la bloquea:** es un falso positivo habitual en apps
  sin firmar. Si el aviso lo ofrece, pulsa **Más información → Ejecutar de todas formas**; si
  ha puesto el `.exe` en cuarentena, restáuralo desde **Seguridad de Windows → Protección
  antivirus y contra amenazas → Historial de protección → Restaurar**.

## Privacidad

Las apps envían estadísticas anónimas de uso (se desactivan en Ajustes). Todos los detalles en
https://deepsky.macas.es/privacidad

## Novedades

- [DeepSkyForce](releases/DeepSkyForce.txt)
- [DeepSkyCopilot](releases/DeepSkyCopilot.txt)

---

Versión beta gratuita: puede contener errores y se ofrece sin garantías. Contacto: deepskysuite@gmail.com
