
# 🎵 Music Searcher & Downloader (MSCDown)

Una herramienta de terminal **minimalista, estética y altamente eficiente** para buscar y descargar música de YouTube directamente a tu biblioteca local.

MSCDown no es solo un descargador; es un asistente de audio diseñado para integrarse perfectamente en tu flujo de trabajo, con soporte para metadatos, miniaturas y sincronización automática con **MPD (Music Player Daemon)**.

---

## ✨ Características Principales

* **Detección Inteligente de Sistema:** El instalador reconoce automáticamente si usas Debian, Arch o Fedora y prepara todo por ti.
* **Modo Dual:** Úsalo de forma interactiva (menú) o mediante línea de comandos para descargas directas.
* **Estética "Aesthetic":** Interfaz cuidada con colores vibrantes, arte ASCII y barras de progreso elegantes.
* **Sincronización Inteligente:** Si usas **MPD**, el programa actualiza tu biblioteca automáticamente al terminar. Si no lo usas, puedes desactivarlo para máxima velocidad.
* **Totalmente Configurable:** Ajusta la calidad (kbps), el formato (mp3, wav, etc.) y la ruta de descarga mediante un archivo de configuración sencillo.

---

## 🚀 Instalación (El corazón de la herramienta)

El script `install.sh` ha sido diseñado para ahorrarte horas de configuración manual. Al ejecutarlo, el script hace lo siguiente:

1. **Detección:** Escanea tu gestor de paquetes (`apt`, `pacman` o `dnf`).
2. **Preparación:** Instala automáticamente `python3`, `pip`, `ffmpeg` (esencial para convertir audio) y `nodejs` (para la extracción rápida de datos).
3. **Alias:** Crea un comando personalizado (ej: `musica`) en tu archivo `.bashrc` o `.zshrc`, permitiéndote ejecutar el programa desde cualquier carpeta de tu terminal.

**Pasos:**

```bash
git clone https://github.com/fc4419039/mscdown.git
cd mscdown
chmod +x install.sh
./install.sh

```

---

## ⚙️ Configuración (`settings.conf`)

Edita el archivo `settings.conf` para adaptar la herramienta a tus necesidades:

```ini
[SETTINGS]
# Ruta donde se guardarán las canciones
output_dir = ~/Music

# Calidad de audio: 320, 192, 128
quality = 320

# Formato: mp3, m4a, ogg, wav
format = mp3

# Sincronización MPD: true o false
auto_update_mpd = true

```

> **Nota sobre MPD:** Si no utilizas MPD, establece `auto_update_mpd = false`. Esto hará que la herramienta sea aún más rápida, ya que el programa omitirá el escaneo de bibliotecas tras cada descarga.

---

## 🛠️ ¿Cómo usarlo?

Tienes dos formas de invocar el programa una vez instalado:

### 1. Modo Interactivo (Menú)

Simplemente escribe el nombre del alias que elegiste en la instalación (por defecto `musica`):

```bash
musica

```

*Se abrirá el buscador interactivo donde podrás seleccionar el resultado que prefieras.*

### 2. Modo Directo (Rápido)

Si ya sabes qué quieres bajar, puedes pasarlo como argumento:

```bash
musica Queen Bohemian Rhapsody

```

*La herramienta buscará y descargará automáticamente la mejor coincidencia.*

---

## 📸 Galería

Aquí puedes ver la herramienta en acción:

**Modo de descarga directa:**
![Descarga directa](assets/direct_down.png)

**Menú interactivo de selección:**
![Menú interactivo](assets/programa.png)


## 💡 ¿Por qué MSCDown?

A diferencia de otras herramientas, MSCDown es **modular**. El entorno virtual (`venv`) se gestiona solo mediante `ejecutar.sh`, manteniendo tu sistema limpio de librerías globales innecesarias. Además, el manejo de errores es silencioso y elegante; si no tienes internet, no verás un "crash" de código, sino una notificación visual clara y limpia.

---

## 🤝 Contribuciones

Este proyecto es de código abierto. Si tienes una mejora, ¡envía un *Pull Request*!


