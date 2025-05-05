import urllib.request
import re
import zipfile
import os
try:
    from rich.progress import track
    from rich.prompt import Prompt
    RICH = True
except:
    RICH = False

# brukerinput
if RICH:
    folder_out = Prompt.ask("Angi mappe for output (enter for å bruke gjeldende mappe)", default=".")
    
    clean = Prompt.ask("Beholde .zip-filer?", choices=["y","n"], default="n")

else:
    folder_out = input("Angi mappe for output (enter for å bruke gjeldende mappe) (.): ")
    folder_out = folder_out if len(folder_out)>0 else "."
    
    clean = input("Beholde .zip-filer? [y/n] (n velges hvis svar ikke i [n/y]): ")
    if clean not in ("y","n"):
        print("Ugyldig valg, sletter filer")

cleanup = False if clean == "y" else True

with open("files.in","r") as links:
    links = links.read().strip().split("\n")

L = track(links,f"Laster ned til '{folder_out}'...") if RICH else links

for link in L:
    # henter filnavn fra lenke
    name = re.search(r"[A-Za-z_0-9]+\.zip", link).group()

    # laster ned fil med link
    urllib.request.urlretrieve(link, name)

    # pakker ut innhold til folder_out/name
    with zipfile.ZipFile(name, 'r') as zip_ref:
        subfolder = re.search(r"[A-Za-z_0-9]+",name).group()
        
        zip_ref.extractall(f"{folder_out}/{subfolder}")

    # sletter zipfil etter ekstraksjon
    if cleanup:
        os.remove(name)
