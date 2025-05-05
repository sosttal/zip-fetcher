import urllib.request
import re
import zipfile
import os
from sys import exit
from rich import box
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table

console = Console()

logo = """███████╗██╗██████╗       ███████╗███████╗████████╗ ██████╗██╗  ██╗███████╗██████╗   TM
╚══███╔╝██║██╔══██╗      ██╔════╝██╔════╝╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗
  ███╔╝ ██║██████╔╝█████╗█████╗  █████╗     ██║   ██║     ███████║█████╗  ██████╔╝
 ███╔╝  ██║██╔═══╝ ╚════╝██╔══╝  ██╔══╝     ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗
███████╗██║██║           ██║     ███████╗   ██║   ╚██████╗██║  ██║███████╗██║  ██║
╚══════╝╚═╝╚═╝           ╚═╝     ╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"""


def end():
    input("\nTrykk enter for å avslutte.")
    exit(0)

def error(msg):
    console.print(f"\n[blink #fc0303]FEIL[/blink #fc0303]: {msg}")
    end()

W = os.get_terminal_size()[0]
sidepad = int((W-88)/2)

console.print(Panel(logo, box=box.DOUBLE, padding=(2,sidepad), style="#90fc03", width=W, expand=False,subtitle="[#90fc03]av [u link https://talleraas.it/]talleraas.it[/u link https://talleraas.it/][/#90fc03]"))

# regex mønstre
zip_pat = r"[A-Za-z_0-9]+\.zip" # .zip-fil
subfold_pat = r"[A-Za-z_0-9]+" # for navn på (under)mapper å pakke ut filer til

url = Prompt.ask("Angi url å hente .zip-arkiver fra", default="https://www.uio.no/studier/emner/matnat/ifi/IN3050/v25/weekly-exercises/") # henter url fra bruker

link_pat = f"{url}{zip_pat}" # .zip-fil lenker

# ekstraherer filbaner (for alle lenker til .zip-filer) fra url
try:
    with urllib.request.urlopen(url) as page:
        html = page.read().decode("utf8")
except:
    error("Ugyldig url.")

links = re.findall(link_pat,html)
links = set(links)

folder_out = Prompt.ask("Angi mappe for output (enter for å bruke gjeldende mappe)", default=".")
    
clean = Prompt.ask("Beholde .zip-arkiver?", choices=["y","n"], default="n")

cleanup = False if clean == "y" else True

# antall .zip-lenker funnet
n_files = len(links)

if not n_files > 0:
    error(f"Fant ingen .zip-arkiver på: {url}")

# oppsummering og bekreftelse
summary = Table(title="Oppsummering:", box=box.DOUBLE)

summary.add_column("", justify="right", style="cyan")
summary.add_column("", justify="left", style="magenta")
summary.show_header = False
summary.show_lines = True

summary.add_row("Henter fra:", url)
summary.add_row("Antall arkiver funnet:", f"{n_files}")
summary.add_row("Output-mappe:", folder_out)
summary.add_row("Behold arkiv-filer?", f"{'NEI' if cleanup else 'JA'}")

console.print(summary)

confirm = Prompt.ask("Start nedlasting?", choices=["y","n"], default="y")

if confirm == "n":
    console.print("\n[bold green blink]Avbrutt av bruker![/bold green blink]")
    
    end()

for link in track(links,f"Laster ned {n_files} arkiver og ekstraherer til '{folder_out}'..."):
    # henter filnavn fra lenke
    name = re.search(zip_pat, link).group()

    # laster ned fil med link
    urllib.request.urlretrieve(link, name)

    # pakker ut innhold til folder_out/name
    with zipfile.ZipFile(name, 'r') as zip_ref:
        subfolder = re.search(subfold_pat,name).group()
        
        zip_ref.extractall(f"{folder_out}/{subfolder}")

    # sletter zipfil etter ekstraksjon
    if cleanup:
        os.remove(name)

console.print("\n[bold green blink]Nedlasting/ekstraksjon fullført![/bold green blink]")

end()