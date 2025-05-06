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
      "prompt_filetype":"Angi filtype",
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
      "prompt_start":"Start nedlasting?",
      "prompt_url":"Angi url å hente .{ftype}-filene fra",
      "err_invalid_url":"Ugyldig url.",
      "prompt_out_dir":"Angi mappe for output (enter for å bruke gjeldende mappe)",
      "warn_invalid_char":"Unngå å bruke følgende symboler:",
      "prompt_cleanup":"Beholde .zip-arkiver?",
      "err_no_file_found":"Fant ingen .{ftype}-filer på:",
      "user_interrupt":"Avbrutt av bruker!",
      "download_tracker_zip":"Laster ned {n_files} arkiver og ekstraherer til '{out_dir}'...",
      "download_tracker_pdf":"Laster ned {n_files} dokumenter til '{out_dir}'...",
      "finished_zip":"Nedlasting/ekstraksjon fullført!",
      "finished_pdf":"Nedlasting fullført!"
    },
    "eng":{
      "welcome":"Welcome to ZIP-Fetcher!\n",
      "prompt_filetype":"Select filetype",
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
      "prompt_url":"Provide url to fetch .{ftype}-files from",
      "err_invalid_url":"Invalid url.",
      "prompt_out_dir":"Provide directory for output (press enter to use current dir)",
      "warn_invalid_char":"Avoid the following characters:",
      "prompt_cleanup":"Keep .zip-archives?",
      "err_no_file_found":"No .{ftype}-files found at:",
      "user_interrupt":"Interrupted by user!",
      "download_tracker_zip":"Downloading {n_files} archives and extracting to '{out_dir}'...",
      "download_tracker_pdf":"Downloading {n_files} documents to '{out_dir}'...",
      "finished_zip":"Download/extraction finished!",
      "finished_pdf":"Download finished!"
    }
  }
