# compress all the files inside a directory, including the ones inside subdirectories at all depth.
# save files creating same exact directory/file tree at the given address

import os
import sys
from pathlib import Path
import configparser
from compress_with_keepbits import compress_with_keepbits

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(sys.argv[0]).name} <path_to_config_file>")
        sys.exit(1)

    ini_path = Path(sys.argv[1])

    cfg = configparser.ConfigParser(interpolation=None)
    cfg.optionxform = str  # preserve case for keys
    cfg.read(ini_path)

    # Expecting:
    # [config]
    # SOURCE_DIR   = /path/to/input
    # DEST_DIR     = /path/to/output
    # KEEPBITS_INI = /path/to/keepbits.ini
    SOURCE_DIR  = cfg["config"]["SOURCE_DIR"]
    DEST_DIR    = cfg["config"]["DEST_DIR"]
    keepbits_ini = cfg["config"]["KEEPBITS_INI"]

    # Make sure destination folder exists
    os.makedirs(DEST_DIR, exist_ok=True)

    # ---- walk and compress -------------------------------------------------------
    for root, _, files in os.walk(SOURCE_DIR):
        for filename in sorted(files):
            if not filename.endswith(".nc4"):
                continue

            input_path    = Path(root) / filename
            relative_path = Path(root).relative_to(SOURCE_DIR)
            out_dir       = Path(DEST_DIR) / relative_path
            out_dir.mkdir(parents=True, exist_ok=True)

            out_path = out_dir / filename

            compress_with_keepbits(
                input_path=input_path,
                output_path=out_path,
                keepbits_ini=keepbits_ini,
            )

            infile_size  = input_path.stat().st_size / (1024 * 1024)
            outfile_size = out_path.stat().st_size / (1024 * 1024)
            print(f"{infile_size:.2f} MB → {outfile_size:.2f} MB | {infile_size/outfile_size:.2f}x")
            print(f"✔ Wrote compressed file → {out_path}")

