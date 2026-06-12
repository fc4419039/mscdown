#!/bin/bash

# --- PALETA DE COLORES AESTHETIC ---
CYAN='\033[38;2;0;255;255m'
MAGENTA='\033[38;2;255;0;255m'
LILA='\033[38;2;180;120;255m'
YELLOW='\033[38;2;255;255;0m'
BOLD='\033[1m'
NC='\033[0m'

# --- 1. DETECCIÓN Y CONFIGURACIÓN DE SHELL ---
CURRENT_SHELL=$(basename "$SHELL")
RC_FILE=$([[ "$CURRENT_SHELL" == *"zsh"* ]] && echo "$HOME/.zshrc" || echo "$HOME/.bashrc")

# --- 2. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA ---
echo -e "${LILA}➜${NC} ${BOLD}Detectando sistema y preparando dependencias...${NC}"

if [ -f /etc/debian_version ]; then
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv ffmpeg nodejs npm
elif [ -f /etc/arch-release ]; then
    sudo pacman -Syu --noconfirm python python-pip ffmpeg nodejs npm
elif [ -f /etc/fedora-release ]; then
    sudo dnf install -y python3 python3-pip ffmpeg nodejs npm
fi

# --- 3. MENSAJES DE IDIOMA ---
if [[ "$LANG" =~ ^es ]]; then
    MSG_TITULO="INSTALADOR DE BUSCADOR MUSICAL"
    MSG_PREGUNTA="¿Qué comando quieres usar? (ej: musica): "
    MSG_CONFIG="Configurando alias"
    MSG_HECHO="¡Instalación completada!"
    MSG_INSTRUCCION="Simplemente escribe"
    MSG_FINAL="en tu terminal."
    MSG_NOTA="Nota: Ejecuta 'source $RC_FILE' para actualizar."
else
    MSG_TITULO="MUSIC SEARCHER INSTALLER"
    MSG_PREGUNTA="What command name do you want? (e.g., musica): "
    MSG_CONFIG="Configuring alias"
    MSG_HECHO="Installation completed!"
    MSG_INSTRUCCION="Simply type"
    MSG_FINAL="in your terminal."
    MSG_NOTA="Note: Run 'source $RC_FILE' to update."
fi

clear
echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${MAGENTA}        ${BOLD}${YELLOW}$MSG_TITULO${NC}${MAGENTA}                  ${CYAN}║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"

# --- 4. CONFIGURACIÓN DEL ALIAS ---
echo -e "\n${LILA}➜${NC} ${BOLD}$MSG_PREGUNTA${NC}"
read -r ALIAS_NAME
[ -z "$ALIAS_NAME" ] && ALIAS_NAME="musica"

ALIAS="alias $ALIAS_NAME='$HOME/mscdown/./ejecutar.sh'"

if ! grep -q "alias $ALIAS_NAME=" "$RC_FILE"; then
    echo "$ALIAS" >> "$RC_FILE"
    echo -e "\n${CYAN}✔${NC} $MSG_CONFIG '${YELLOW}$ALIAS_NAME${NC}' ${CYAN}en${NC} ${LILA}$RC_FILE${NC}"
else
    echo -e "\n${YELLOW}ℹ${NC} El alias '$ALIAS_NAME' ya existe."
fi

# --- 5. CIERRE ELEGANTE ---
echo -e "\n${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}${BOLD}$MSG_HECHO${NC}"
echo -e "${CYAN}$MSG_INSTRUCCION${NC} ${BOLD}${LILA}$ALIAS_NAME${NC} ${CYAN}$MSG_FINAL${NC}"
echo -e "${LILA}$MSG_NOTA${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
