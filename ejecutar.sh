#!/bin/bash
BASE_DIR="$HOME/mscdown"
VENV_DIR="$BASE_DIR/venv"
REQUIREMENTS="$BASE_DIR/requirements.txt"

# CORRECCIÓN AQUÍ:
# 1. Obtenemos la ruta limpia
RAW_DIR=$(grep 'output_dir' "$BASE_DIR/settings.conf" | cut -d'=' -f2 | xargs)
# 2. Expandimos el ~ manualmente usando ${VAR/#\~/$HOME}
MUSIC_DIR="${RAW_DIR/#\~/$HOME}"

# Si por alguna razón sigue vacío, usamos el predeterminado
[ -z "$MUSIC_DIR" ] && MUSIC_DIR="$HOME/Music"

# 1. Crear directorios necesarios (ahora ya usa la ruta expandida correctamente)
mkdir -p "$MUSIC_DIR"

[ ! -d "$VENV_DIR" ] && python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# 2. Actualización silenciosa
python3 -m pip install -r "$REQUIREMENTS" --quiet --timeout 5 2>/dev/null

# 3. Ejecución
cd "$BASE_DIR" || exit 1
python3 main.py "$@"
