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
import zf_res

class ZipFetcher:
    
    def __init__(self):

        self.console = Console()

        self.logo = zf_res.LOGO

        self.invalid_chars = "<, >, :, \", |, ?, *"

         # for å definere bredde på panel
        W = os.get_terminal_size()[0]
        # padding (venstre og høyre) defineres av bredde på terminal W - bredde på logo / 2
        sidepad = int((W-88)/2)

        # header panel 
        self.console.print(Panel(self.logo, box=box.DOUBLE, padding=(2,sidepad), style="#90fc03", width=W, expand=False,subtitle="[#90fc03]by [u link https://talleraas.it/]talleraas.it[/u link https://talleraas.it/][/#90fc03]"))

        # language prompt
        self.message = zf_res.ZFMessage.lang[Prompt.ask("Choose language", choices=["nor","eng"], default="nor")]

        self.console.print(self.message["welcome"], style="green blink")

        # regex mønstre
        self.zip_pat = r"[A-Za-z_0-9]+\.zip" # .zip-fil
        self.subfold_pat = r"[A-Za-z_0-9]+" # for navn på (under)mapper å pakke ut filer til
        self.invalid_pat = r'[<>:"|?\*]' # ugyldige tegn for mappenavn ## TODO endre regler for ':' ?
    

    def _terminate_program(self) -> None:
        input(f"\n{self.message['terminate']}")
        exit(0)


    def _error(self,msg) -> None:
        self.console.print(f"\n[blink #fc0303]{self.message['err']}[/blink #fc0303]: {msg}")

        self._retry()


    def _retry(self) -> None:
        q = Prompt.ask(self.message["restart"], choices=["y","n"], default="n")

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
        summary = Table(title=self.message["summary"], box=box.DOUBLE)

        summary.add_column("", justify="right", style="cyan")
        summary.add_column("", justify="left", style="magenta")
        summary.show_header = False
        summary.show_lines = True

        summary.add_row(self.message["_from_url"], url)
        summary.add_row(self.message["_n_files"], f"{n_files}")
        summary.add_row(self.message["_out_dir"], out_dir)
        summary.add_row(self.message["_cleanup?"], f"{self.message['_no'] if cleanup else self.message['_yes']}")

        self.console.print(summary)

        return True if Prompt.ask(self.message["prompt_start"], choices=["y","n"], default="y") == "y" else False
    

    def _process_downloads(self) -> None:
        url = Prompt.ask(self.message["prompt_url"], default="https://www.uio.no/studier/emner/matnat/ifi/IN3050/v25/weekly-exercises/") # henter url fra bruker

        link_pat = f"{url}{self.zip_pat}" if url[-1] == "/" else f"{url}/{self.zip_pat}" # .zip-fil lenker

        # leser inn kildekode til angitt nettside/url
        try:
            with urllib.request.urlopen(url) as page:
                self.html = page.read().decode("utf8")
        except:
            self._error(self.message["err_invalid_url"])
            return

        # finner alle relevante lenker og fjerner duplikater
        links = re.findall(link_pat, self.html)
        links = set(links)

        out_dir = Prompt.ask(self.message["prompt_out_dir"], default=".")

        while not self._validate_input(out_dir, self.invalid_pat):
            self.console.print(f"{self.message['warn_invalid_char']} [#fc0303]{self.invalid_chars}[/#fc0303]")
            out_dir = Prompt.ask(f"{self.message['prompt_out_dir']}", default=".")
        
        clean = Prompt.ask(self.message["prompt_cleanup"], choices=["y","n"], default="n")

        cleanup = False if clean == "y" else True

        # antall .zip-lenker funnet
        n_files = len(links)

        # verifiserer at det er minst et arkiv på angitt url
        if not n_files > 0:
            self._error(f"{self.message['err_no_zip_found']} {url}")
            return

        confirm = self._summary_confirm(url, n_files, out_dir, cleanup)

        if confirm == False:
            self.console.print(f"\n[bold green blink]{self.message['user_interrupt']}[/bold green blink]")
            
            self._retry()

        else:
            for link in track(links,self.message["download_tracker"].format(n_files=n_files,out_dir=out_dir)):
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

            self.console.print(f"\n[bold green blink]{self.message['finished']}[/bold green blink]")

    
    def main(self) -> None:

        self._process_downloads()

        self._terminate_program()


ZipFetcher().main()
