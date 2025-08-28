# compress all the files inside a directory, including the ones inside subdirectories. 
# save files creating same exact directory/file tree at the  given address 

import os
from pathlib import Path
#import pandas as pd
from compress_with_keepbits import compress_with_keepbits

# ---- read params from .inf -------------------------------------------
def read_params(inf_path: str | Path) -> dict:
    ''' read params (infput file directory, destination direcstory, and keepbits info) from .inf'''
    params = {}
    with open(inf_path, "r") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if "=" in s:
                k, v = s.split("=", 1)
                params[k.strip()] = v.strip()
    return params

# Load parameters
P = read_params("GiOCEAN.inf") 

SOURCE_DIR  = P["SOURCE_DIR"] # data repo to be compressed
DEST_DIR    = P["DEST_DIR"] # address of compressed data
keepbit_inf = P["KEEPBITS_INF"] # no. of keepbits for each variable

# Make sure destination folder exists
os.makedirs(DEST_DIR, exist_ok=True)

# ---- walk and compress -------------------------------------------------------
#count = 0
#max_count = 5

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
            keepbits_inf=keepbit_inf,
        )

        infile_size  = input_path.stat().st_size / (1024 * 1024)
        outfile_size = out_path.stat().st_size / (1024 * 1024)
        print(f"{infile_size:.2f} MB → {outfile_size:.2f} MB | {infile_size/outfile_size:.2f}x")
        print(f"✔ Wrote compressed file → {out_path}")
        #count += 1
        #if count > max_count:
        #    break
#if __name__ == "__main__":
#    pass  # loop already executed above

