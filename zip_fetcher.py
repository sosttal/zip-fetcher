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
import zfASCII

class ZipFetcher:
    
    def __init__(self):

        self.console = Console()

        self.logo = zfASCII.LOGO

        # regex mønstre
        self.zip_pat = r"[A-Za-z_0-9]+\.zip" # .zip-fil
        self.subfold_pat = r"[A-Za-z_0-9]+" # for navn på (under)mapper å pakke ut filer til
        self.invalid_chars = r'[<>:"|?\*]' # ugyldige tegn for mappenavn ## TODO endre regler for ':' ?
    

    def _terminate_program(self) -> None:
        input("\nTrykk enter for å avslutte... ")
        exit(0)


    def _error(self,msg) -> None:
        self.console.print(f"\n[blink #fc0303]FEIL[/blink #fc0303]: {msg}")

        self._retry()


    def _retry(self) -> None:
        q = Prompt.ask("Starte på nytt?", choices=["y","n"], default="n")

        if q == "y":
            self.console.print()
            self._process_downloads()
        else:
            self._terminate_program()
        
    
    def _validate_input(self,input:str, regex:str) -> bool:
        # NOTE uklar logikk TODO fikse/endre?
        if re.search(regex, input) is None:
            return True
        else:
            return False
    

    def _summary_confirm(self, url:str, n_files:int, out_dir:str, cleanup:bool) -> bool:
        # oppsummering og bekreftelse
        summary = Table(title="Oppsummering:", box=box.DOUBLE)

        summary.add_column("", justify="right", style="cyan")
        summary.add_column("", justify="left", style="magenta")
        summary.show_header = False
        summary.show_lines = True

        summary.add_row("Henter fra:", url)
        summary.add_row("Antall arkiver funnet:", f"{n_files}")
        summary.add_row("Output-mappe:", out_dir)
        summary.add_row("Behold arkiv-filer?", f"{'NEI' if cleanup else 'JA'}")

        self.console.print(summary)

        return True if Prompt.ask("Start nedlasting?", choices=["y","n"], default="y") == "y" else False
    

    def _process_downloads(self) -> None:
        url = Prompt.ask("Angi url å hente .zip-arkiver fra", default="https://www.uio.no/studier/emner/matnat/ifi/IN3050/v25/weekly-exercises/") # henter url fra bruker

        link_pat = f"{url}{self.zip_pat}" if url[-1] == "/" else f"{url}/{self.zip_pat}" # .zip-fil lenker

        # leser inn kildekode til angitt nettside/url
        try:
            with urllib.request.urlopen(url) as page:
                self.html = page.read().decode("utf8")
        except:
            self._error("Ugyldig url.")
            return

        # finner alle relevante lenker og fjerner duplikater
        links = re.findall(link_pat, self.html)
        links = set(links)

        out_dir = Prompt.ask("Angi mappe for output (enter for å bruke gjeldende mappe)", default=".")

        while not self._validate_input(out_dir, self.invalid_chars):
            out_dir = Prompt.ask(f"Unngå å bruke følgende symboler: [#fc0303]<, >, :, \", |, ?, *[/#fc0303]\nAngi mappe for output (enter for å bruke gjeldende mappe)", default=".")
        
        clean = Prompt.ask("Beholde .zip-arkiver?", choices=["y","n"], default="n")

        cleanup = False if clean == "y" else True

        # antall .zip-lenker funnet
        n_files = len(links)

        # verifiserer at det er minst et arkiv på angitt url
        if not n_files > 0:
            self._error(f"Fant ingen .zip-arkiver på: {url}")
            return

        confirm = self._summary_confirm(url, n_files, out_dir, cleanup)

        if confirm == False:
            self.console.print("\n[bold green blink]Avbrutt av bruker![/bold green blink]")
            
            self._retry()

        else:
            for link in track(links,f"Laster ned {n_files} arkiver og ekstraherer til '{out_dir}'..."):
                # isolerer filnavn fra lenke
                name = re.search(self.zip_pat, link).group()

                # laster ned fil med link
                urllib.request.urlretrieve(link, name)

                # pakker ut innhold til folder_out/name
                with zipfile.ZipFile(name, 'r') as zip_ref:
                    subfolder = re.search(self.subfold_pat, name).group()
                    
                    zip_ref.extractall(f"{out_dir}/{subfolder}")

                # hvis valgt: sletter zipfil etter ekstraksjon
                if cleanup and os.path.exists(name):
                    os.remove(name)

            self.console.print("\n[bold green blink]Nedlasting/ekstraksjon fullført![/bold green blink]")

    
    def main(self) -> None:
        # for å definere bredde på panel
        W = os.get_terminal_size()[0]
        # padding (venstre og høyre) defineres av bredde på terminal W - bredde på logo / 2
        sidepad = int((W-88)/2)

        self.console.print(Panel(self.logo, box=box.DOUBLE, padding=(2,sidepad), style="#90fc03", width=W, expand=False,subtitle="[#90fc03]av [u link https://talleraas.it/]talleraas.it[/u link https://talleraas.it/][/#90fc03]"))

        self._process_downloads()

        self._terminate_program()


ZipFetcher().main()
