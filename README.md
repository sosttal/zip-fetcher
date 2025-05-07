# ZIP-FETCHER

## Use instructions

**Two options**:

1. Download and run `zip_fetcher.py` (may need to install dependencies):
```bash
python zip_fetcher.py
```

2. [Download](https://github.com/sosttal/zip-fetcher/raw/refs/heads/main/dist/ZIP-FETCHER.exe) and run `ZIP-FETCHER.exe` (Windows only).

- Output-directory is same as location of `zip_fetcher.py`/`ZIP-FETCHER.exe` (i.e. '.') by default.


## Run example

GIF of sample-run:

![](example/animated.gif)

Rich-powered TUI:

![](example/mappe_tui.jpg)

Resulting (sub)folders stored in specified directory (only supporting relative paths currently):

![](example/mappe_explorer.jpg)


## TODO(?)

- Implement support for config-file generation/reading
- More robust input-handeling

<!--
## Explained by Copilot

This file, `zip_fetcher.py`, defines a Python program named `ZIP-FETCHER`. It is a tool designed to download and extract multiple `.zip` archives from a given website. Here's an overview of its functionality:

### Key Features:
1. **Interactive User Interface:**
   - Prompts the user to input a URL containing `.zip` files.
   - Asks for an output directory to save the extracted files.
   - Provides options to keep or delete the `.zip` files after extraction.

2. **Regex-based Validation:**
   - Uses regular expressions to identify `.zip` files and validate folder names.

3. **File Download and Extraction:**
   - Downloads `.zip` files from the provided URL.
   - Extracts their contents into subdirectories based on the `.zip` file names.
   - Optionally deletes the `.zip` files after extraction.

4. **Rich Library for UI Enhancements:**
   - Uses the `rich` Python library to display progress, prompts, tables, and styled messages.
   - Includes a visually appealing ASCII art logo.

5. **Error Handling and Retry Logic:**
   - Handles invalid URLs gracefully by showing error messages and allowing the user to retry.
   - Ensures user inputs are validated before proceeding.

6. **Summary and Confirmation:**
   - Displays a summary table of the operation (e.g., URL, number of `.zip` files found, output directory, etc.) before starting the download.

7. **Core Functionality:**
   - Reads the provided URL's HTML content and finds `.zip` file links.
   - Tracks progress while downloading and extracting files.

### Structure:
- **`LOGO`:** ASCII art displayed at the start of the program.
- **`ZipFetcher` Class:**
  - Contains methods for functionality (`_core`, `_error`, `_retry`, `_validate_input`, etc.).
  - `main()` method serves as the entry point.

### How It Works:
1. **Startup:**
   - Displays a logo and initializes the program.
2. **Input Collection:**
   - Prompts the user for a URL and output directory.
3. **Validation:**
   - Checks if the URL and directory inputs are valid.
4. **Operation Execution:**
   - Downloads and extracts `.zip` files from the provided URL.
   - Deletes `.zip` files if the user opts for cleanup.
5. **Completion:**
   - Displays a success message upon completion.
-->
