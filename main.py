import os, sys, locale, re, configparser, contextlib, warnings, questionary, time, shutil, subprocess
from yt_dlp import YoutubeDL
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn
from art import text2art
from questionary import Style

warnings.filterwarnings("ignore", category=DeprecationWarning)
os.environ["YTDLP_JS_RUNTIME"] = "node" # Restaurado
console = Console()

# --- DETECCIÓN DE IDIOMA ORIGINAL ---
def get_text():
    try: lang_code = locale.getlocale()[0]
    except: lang_code = None
    is_es = bool(lang_code and lang_code.startswith('es'))
    return {
        'buscar': "Búsqueda: ", 'buscando': "Buscando...",
        'seleccionar': "Selecciona un resultado:", 'descargando': "Descargando...",
        'finalizado': "✔ Finalizado:", 'error_no_res': "No se encontraron resultados.",
        'error_desc': "Error en descarga:", 'salir': "Saliendo...",
        'error_con': "⚠ Error de conexión: Revisa tu internet." # Nuevo mensaje
    } if is_es else {
        'buscar': "Search: ", 'buscando': "Searching...",
        'seleccionar': "Select a result:", 'descargando': "Downloading...",
        'finalizado': "✔ Done:", 'error_no_res': "No results found.",
        'error_desc': "Download error:", 'salir': "Exiting...",
        'error_con': "⚠ Connection error: Check your internet." # Nuevo mensaje
    }

T = get_text()

# --- CONFIGURACIÓN ORIGINAL ---
def cargar_configuracion():
    config = configparser.ConfigParser()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'settings.conf')
    if os.path.exists(config_path):
        config.read(config_path)
        if 'SETTINGS' in config:
            return {k: os.path.expanduser(config['SETTINGS'][k]) if k == 'output_dir' else config['SETTINGS'][k] for k in config['SETTINGS']}
    return {'output_dir': os.path.expanduser('~/Music'), 'quality': '320', 'format': 'mp3', 'auto_update_mpd': 'true'}

CONFIG = cargar_configuracion()

# --- FUNCIÓN MPD ORIGINAL ---
def actualizar_mpd(file_path):
    if shutil.which("mpc") and CONFIG.get('auto_update_mpd', 'true') == 'true':
        try:
            music_dir = CONFIG['output_dir']
            rel_path = os.path.relpath(file_path, music_dir)
            subprocess.run(["mpc", "rescan"], stdout=subprocess.DEVNULL)
            time.sleep(1)
            subprocess.run(["mpc", "add", rel_path], stdout=subprocess.DEVNULL)
            subprocess.run(["mpc", "update"], stdout=subprocess.DEVNULL)
        except: pass

# --- FUNCIÓN DESCARGA ORIGINAL (CON BARRA BONITA) ---
def descargar_cancion(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(CONFIG["output_dir"], "%(title)s.%(ext)s"),
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": CONFIG['format'], "preferredquality": CONFIG['quality']},
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata", "add_chapters": True}
        ],
        "writethumbnail": True, "quiet": True, "noprogress": True,
    }
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), "[progress.percentage]{task.percentage:>3.0f}%", DownloadColumn(), TransferSpeedColumn(), console=console) as progress:
        task = progress.add_task(f"[cyan]{T['descargando']}", total=100)
        with contextlib.redirect_stderr(open(os.devnull, 'w')):
            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        clean_percent = re.sub(r'\x1b\[[0-9;]*m', '', d.get('_percent_str', '0')).replace('%', '').strip()
                        progress.update(task, completed=float(clean_percent))
                    except: pass
            with YoutubeDL({**ydl_opts, 'progress_hooks': [progress_hook]}) as ydl:
                try:
                    info = ydl.extract_info(url, download=True)
                    file_path = os.path.splitext(ydl.prepare_filename(info))[0] + "." + CONFIG['format']
                    console.print(f"[bold cyan]{T['finalizado']} {info['title']}[/bold cyan]")
                    actualizar_mpd(file_path)
                except Exception as e:
                    console.print(f"[bold red]{T['error_desc']} {e}[/bold red]")

# --- ESTILO QUESTIONARY ORIGINAL ---
custom_style = Style([
    ('pointer', 'fg:cyan bold'),
    ('selected', 'fg:yellow bold'),
    ('highlighted', 'fg:yellow'),
    ('answer', 'fg:cyan bold'),
])

def main():
    # --- LÓGICA DE ARGUMENTOS (NUEVA FUNCIÓN) ---
    is_direct = len(sys.argv) > 1
    if is_direct:
        termino = " ".join(sys.argv[1:])
    else:
        # --- ENTRADA INTERACTIVA ORIGINAL (CON BANNERS) ---
        console.print("[bold cyan]╔══════════════════════════════════════════╗[/bold cyan]")
        console.print("[bold cyan]║[/bold cyan]   [bold yellow]FC4419039 MUSIC Download[/bold yellow]               [bold cyan]║[/bold cyan]")
        console.print("[bold cyan]╚══════════════════════════════════════════╝[/bold cyan]")
        # (He quitado el panel de configuración para no saturar al entrar)
        console.print(f"[bold white]  Introduce el término de búsqueda[/bold white]")
        console.print(f"[bold cyan]  (Ej: [yellow]Bohemian Rhapsody - Queen[/yellow])[/bold cyan]")
        termino = console.input(f"[bold cyan] ➜ [white]{T['buscar']}[/white][/bold cyan]").strip()

    if not termino: return

    # --- BÚSQUEDA CON CONTROL DE ERRORES (NUEVA FUNCIÓN) ---
    try:
        with console.status(f"[bold green]{T['buscando']}"):
            with YoutubeDL({'extract_flat': True, 'quiet': True}) as ydl:
                res = ydl.extract_info(f"ytsearch5:{termino}", download=False)
                entries = res.get('entries', [])
    except:
        console.print(f"[bold red]{T['error_con']}[/bold red]") # Mensaje bonito
        return

    if not entries:
        console.print(f"[bold red]{T['error_no_res']}[/bold red]")
        return

    # --- LÓGICA DE DESCARGA (DIRECTA O INTERACTIVA ORIGINAL) ---
    if is_direct:
        video = entries[0]
        # Mostramos la cabecera original antes de descargar
        print("\n" + text2art("DESCARGANDO", font="small"))
        console.print(f"[bold cyan]➜ Descarga directa:[/bold cyan] {video['title']}")
        descargar_cancion(f"https://www.youtube.com/watch?v={video['id']}")
    else:
        eleccion = questionary.select(
            T['seleccionar'],
            choices=[f"{r['title']} - {r['uploader']}" for r in entries],
            style=custom_style, pointer="➜"
        ).ask()
        
        if eleccion:
            print("\n" + text2art("DESCARGANDO", font="small"))
            video = next(e for e in entries if f"{e['title']} - {e['uploader']}" == eleccion)
            descargar_cancion(f"https://www.youtube.com/watch?v={video['id']}")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: console.print(f"\n[bold yellow]{T['salir']}[/bold yellow]")
