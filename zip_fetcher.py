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

         # width of terminal - used for determining width of panels
        W = os.get_terminal_size()[0]
        # padding (left and right) defined width of terminal W minus width of logo
        sidepad = int((W-88)/2)

        # header panel 
        self.console.print(Panel(self.logo, box=box.DOUBLE, padding=(2,sidepad), style="#90fc03", width=W, expand=False,subtitle="[#90fc03]by [u link https://talleraas.it/]talleraas.it[/u link https://talleraas.it/][/#90fc03]"))

        # language prompt
        self.message = zf_res.ZFMessage.lang[Prompt.ask("Choose language", choices=["nor","eng"], default="nor")]

        self.console.print(self.message["welcome"], style="green blink")

        # TODO implementer ulike filtyper ordentlig (inkl alternativ meldingsflyt)
        self.filetype = Prompt.ask(self.message["prompt_filetype"], choices=["zip","pdf"], default="zip")

        # regexs
        self.file_pat = r"[A-Za-z0-9%_]+\."+self.filetype # pattern for filename.filetype strings
        self.subfold_pat = r"[A-Za-z_0-9]+" # for name of target (sub)folder
        self.invalid_pat = r'[<>:"|?\*]' # invalid chars for folder names # TODO add support for ':' / absolute paths ?
    

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
        
    
    def _validate_out_dir(self,path:str) -> bool:
        """
        Check if path contains invalid symbols.
        -> True if no invalid symbols
        -> False if any invalid symbol
        """
        if re.search(self.invalid_pat, path) is None:
            return True
        else:
            return False
    

    def _summary_confirm(self, url:str, n_files:int, out_dir:str, cleanup:bool) -> bool:
        # summary and confirmation
        summary = Table(title=self.message["summary"], box=box.DOUBLE)

        summary.add_column("", justify="right", style="cyan")
        summary.add_column("", justify="left", style="magenta")
        summary.show_header = False
        summary.show_lines = True

        summary.add_row(self.message["_from_url"], url)
        summary.add_row(self.message["_n_files"], f"{n_files}")
        summary.add_row(self.message["_out_dir"], out_dir)
        if cleanup is not None:
            summary.add_row(self.message["_cleanup?"], f"{self.message['_no'] if cleanup else self.message['_yes']}")

        self.console.print(summary)

        return True if Prompt.ask(self.message["prompt_start"], choices=["y","n"], default="y") == "y" else False
    

    def _process_downloads(self) -> None:
        # prompt user for source url
        url = Prompt.ask(self.message["prompt_url"].format(ftype=self.filetype), default="https://www.uio.no/studier/emner/matnat/ifi/IN3050/v25/weekly-exercises/") 

        # combined pattern to search for (absolute) urls ending in .filetype
        link_pat = f"{url}{self.file_pat}" if url[-1] == "/" else f"{url}/{self.file_pat}"
        # as a second option if no links are found using absolute path for relative links (e.g. /matnat/ifi/IN3050/v25/weekly-exercises/)
        relative_link_pat = r"\/[0-9A-Za-z\/_-]*\/"

        # gets html for given url
        try:
            with urllib.request.urlopen(url) as page:
                self.html = page.read().decode("utf8")
        except:
            self._error(self.message["err_invalid_url"])
            return

        # search source html for relevant urls
        links = re.findall(link_pat, self.html)
        
        # if no urls are found using absolute link
        if len(links) < 1:
            url_root = re.search(r"http[s]{0,1}:\/\/([a-z0-9]+\.)+[a-z]{2,5}", url).group()
            link_pat = f"{relative_link_pat}{self.file_pat}"

            links = re.findall(link_pat, self.html)

            if len(links) < 1:
                self._error(f"{self.message['err_no_file_found'].format(ftype=self.filetype)} {url}")
                return

            links = [f"{url_root}{link}" for link in links]
            links = set(links)
            
        else:
            links = set(links)

        out_dir = Prompt.ask(self.message["prompt_out_dir"], default=".")

        while not self._validate_out_dir(out_dir):
            self.console.print(f"{self.message['warn_invalid_char']} [#fc0303]{self.invalid_chars}[/#fc0303]")
            out_dir = Prompt.ask(f"{self.message['prompt_out_dir']}", default=".")
        
        # ask to cleanup if zip option is chosen
        if self.filetype=="zip":
            clean = Prompt.ask(self.message["prompt_cleanup"], choices=["y","n"], default="n")

            cleanup = False if clean == "y" else True
            # TODO: (?) prompt for directory to store zips in if cleanup is true (?)
        else:
            cleanup = None

        # number of files found
        n_files = len(links)

        confirm = self._summary_confirm(url, n_files, out_dir, cleanup)

        if confirm == False:
            self.console.print(f"\n[bold green blink]{self.message['user_interrupt']}[/bold green blink]")
            
            self._retry()
            return

        elif self.filetype=="zip":
            for link in track(links,self.message["download_tracker_zip"].format(n_files=n_files,out_dir=out_dir)):
                # isolerer filnavn fra lenke
                name = re.search(self.file_pat, link).group()
                
                # TODO store zip-files in own subdir of out_dir
                # zip_dir = "ZIP"

                # if not os.path.exists(zip_dir):
                #     os.mkdir(zip_dir)

                # laster ned fil med link
                urllib.request.urlretrieve(link, name)

                # pakker ut innhold til folder_out/name
                with zipfile.ZipFile(name, 'r') as zip_ref:
                    subfolder = re.search(self.subfold_pat, name).group()
                    
                    zip_ref.extractall(f"{out_dir}/{subfolder}")

                # hvis valgt: sletter zipfil etter ekstraksjon
                if cleanup and os.path.exists(name):
                    os.remove(name)
        
        elif self.filetype=="pdf":
            for link in track(links,self.message["download_tracker_pdf"].format(n_files=n_files,out_dir=out_dir,ftype=self.filetype)):
                # isolerer filnavn fra lenke
                name = re.search(self.file_pat, link).group()
                
                if not os.path.exists(out_dir):
                    os.mkdir(out_dir)

                # laster ned fil med link
                urllib.request.urlretrieve(link, f"{out_dir}/{name}")


        self.console.print(f"\n[bold green blink]{self.message[f'finished_{self.filetype}']}[/bold green blink]")

    
    def main(self) -> None:

        self._process_downloads()

        self._terminate_program()

ZipFetcher().main()