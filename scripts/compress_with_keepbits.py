# compress a file with pre-computed keepbits

from pathlib import Path
import shutil
import tempfile
import time
import xarray as xr
#import xbitinfo as xb
import configparser  
import sys

def _read_keepbits(keepbits_ini: str | Path) -> dict[str, int]:
    '''Read pre-computed keepbits from a .ini config file <keepbits_ini>
    and output a {variable: no_of_keepbit} dictionary'''
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.optionxform = str
    cfg.read(keepbits_ini)
    
    return {k: int(v) for k, v in cfg["keepbits"].items()} 


def compress_with_keepbits(
    input_path: str | Path,
    output_path: str | Path,
    keepbits_ini: str | Path,
) -> None:
    '''
    Read precomputed keepbits from a .ini config file <keepbits_ini>, compress 
    the input file <input_path>, then save the compressed file to <output_path>. 
    '''
    input_path = Path(input_path)
    output_path = Path(output_path)

    # 1. Load dataset
    ds = xr.open_dataset(input_path, mask_and_scale=False)

    # 2. Read keepbits from .ini
    kb_map  = _read_keepbits(keepbits_ini)

    # 3. Drop vars with keepbits <= 0 (we won't quantize those)
    kb_selected = {v: kb for v, kb in kb_map.items() if kb > 0}

    # 4. Build per-variable encoding:
    enc = {key: {"compression": "zlib", "shuffle": True}
           for key in ds.data_vars.keys()}

    # 5. Add BitRound only to selected vars
    for key, value in kb_selected.items():
        enc[key] |= {"significant_digits": value, "quantize_mode": "BitRound"}

    # 6. Write to a temporary file, then move atomically into place
    tmp = Path(tempfile.mktemp(suffix=".nc4", dir=str(output_path.parent)))
    ds.to_netcdf(tmp, format="NETCDF4", engine="netcdf4", encoding=enc)
    shutil.move(tmp, output_path)

    ds.close()

    infile_size = input_path.stat().st_size / (1024 * 1024)
    outfile_size = output_path.stat().st_size / (1024 * 1024)
    print(f"input file: {infile_size} MB, compressed file: {outfile_size} MB, compression ratio: {infile_size/outfile_size}")
   # print(f"✔ File written: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(sys.argv[0]).name} <path_to_config_file>")
        sys.exit(1)

    ini_path = Path(sys.argv[1])
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.optionxform = str  # preserve key case
    cfg.read(ini_path)

    # Expecting:
    # [config]
    # INPUT_FILE   = /path/to/file.nc4
    # OUTPUT_FILE  = /path/to/output_file.nc4
    # KEEPBITS_INI = /path/to/keepbits.ini
    input_path   = Path(cfg["config"]["INPUT_FILE"])
    output_path  = Path(cfg["config"]["OUTPUT_FILE"])
    keepbits_ini = Path(cfg["config"]["KEEPBITS_INI"])

    start = time.time()
    compress_with_keepbits(
        input_path=input_path,
        output_path=output_path,
        keepbits_ini=keepbits_ini,
    )
    end = time.time()
    print(f"completed in {end-start:.2f} secs")

