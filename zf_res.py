# constants
LOGO = """███████╗██╗██████╗       ███████╗███████╗████████╗ ██████╗██╗  ██╗███████╗██████╗   TM
╚══███╔╝██║██╔══██╗      ██╔════╝██╔════╝╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗
  ███╔╝ ██║██████╔╝█████╗█████╗  █████╗     ██║   ██║     ███████║█████╗  ██████╔╝
 ███╔╝  ██║██╔═══╝ ╚════╝██╔══╝  ██╔══╝     ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗
███████╗██║██║           ██║     ███████╗   ██║   ╚██████╗██║  ██║███████╗██║  ██║
╚══════╝╚═╝╚═╝           ╚═╝     ╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"""


class ZFMessage:
  """
  Dicts for multilingual functionality.
  """
  lang = {
    "nor":{
      "welcome":"Velkommen til ZIP-Fetcher!\n",
      "terminate":"Trykk enter for å avslutte...",
      "err":"FEIL",
      "restart":"Starte på nytt?",
      "summary":"Oppsummering:",
      # keys with _-prefix used in summary-table
      "_from_url":"Henter fra:",
      "_n_files":"Antall arkiver funnet:",
      "_out_dir":"Output-mappe:",
      "_cleanup?":"Behold arkiv-filer?",
      "_yes":"JA",
      "_no":"NEI",
      ##########################################
      "prompt_start":"Start nedlastning?",
      "prompt_url":"Angi url å hente .zip-arkiver fra",
      "err_invalid_url":"Ugyldig url.",
      "prompt_out_dir":"Angi mappe for output (enter for å bruke gjeldende mappe)",
      "warn_invalid_char":"Unngå å bruke følgende symboler:",
      "prompt_cleanup":"Beholde .zip-arkiver?",
      "err_no_zip_found":"Fant ingen .zip-arkiver på:",
      "user_interrupt":"Avbrutt av bruker!",
      "download_tracker":"Laster ned {n_files} arkiver og ekstraherer til '{out_dir}'...",
      "finished":"Nedlasting/ekstraksjon fullført!"
    },
    "eng":{
      "welcome":"Welcome to ZIP-Fetcher!\n",
      "terminate":"Press enter to terminate program...",
      "err":"ERROR",
      "restart":"Restart?",
      "summary":"Summary:",
      # keys with _-prefix used in summary-table
      "_from_url":"Fetching from:",
      "_n_files":"# archives found:",
      "_out_dir":"Output-directory:",
      "_cleanup?":"Keep archive-files?",
      "_yes":"YES",
      "_no":"NO",
      ##########################################
      "prompt_start":"Start download?",
      "prompt_url":"Provide url to fetch the archives from",
      "err_invalid_url":"Invalid url.",
      "prompt_out_dir":"Provide directory for output (press enter to use current dir)",
      "warn_invalid_char":"Avoid the following characters:",
      "prompt_cleanup":"Keep .zip-archives?",
      "err_no_zip_found":"No .zip-archives found at:",
      "user_interrupt":"Interrupted by user!",
      "download_tracker":"Downloading {n_files} archives and extracting to '{out_dir}'...",
      "finished":"Download/extraction finished!"
    }
  }
