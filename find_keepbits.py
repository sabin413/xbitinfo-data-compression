# compute keepbits for each variable and save them in a .ini file

from pathlib import Path
import configparser
import sys
import xarray as xr
import xbitinfo as xb
import time

def compute_and_save_keepbits(
    input_path: str | Path,
    output_dir: str | Path,
    inflevel: float = 0.99,
) -> None:
    '''Read netcdf file from <input_path>, compute the # of keepbits for each variable
       at <inflevel> information level, and save results in a .ini config file saved inside
       <output_dir>. The config file name will be derived from the input file name to avoid
       potential mismatch.'''

    input_path = Path(input_path)

    # path to the output .ini file
    out_path = Path(output_dir) / (input_path.name + ".ini")

    # 1. Load dataset
    ds = xr.open_dataset(input_path, mask_and_scale=False)

    # 2. Select variables to process
    excluded_vars = {"TAITIME", "contacts", "corner_lons", "corner_lats", "anchor"}
    included_vars = [v for v in ds.data_vars if v not in excluded_vars]
    ds_vars = ds[included_vars]

    # 3. Dimensions for xbitinfo
    kb_dims = [d for d, n in ds_vars.sizes.items() if n > 5 and d != "nf"] # only "long" enough  dimensions, also exclude "nf" if present
    bitinfo = xb.get_bitinformation(ds_vars, dim=kb_dims) # bitinfo in all dims
    keepbits = xb.get_keepbits(bitinfo, inflevel=inflevel).max(dim="dim") # keep max

    with xr.set_options(display_max_rows=100):
        print(keepbits)

    # Save keepbits as an INI:
    # [meta]
    # file = ...
    # inflevel = ...
    #
    # [keepbits]
    # VAR = INT
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        f.write("[meta]\n")
        f.write(f"file = {input_path}\n")
        f.write(f"inflevel = {inflevel}\n\n")
        f.write("[keepbits]\n")
        for v, kb in keepbits.items():
            f.write(f"{v} = {int(kb.item())}\n")

    print (f"wrote bitinformation to {out_path}")

#start = time.time()
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
    # INPUT_FILE = /path/to/file.nc4
    # OUTPUT_DIR  = /path/to/output_dir/
    # INFLEVEL    = 0.99
    input_path = Path(cfg["config"]["INPUT_FILE"])
    output_dir = Path(cfg["config"]["OUTPUT_DIR"])
    inflevel   = float(cfg["config"]["INFLEVEL"])

    start = time.time()
    compute_and_save_keepbits(input_path=input_path, output_dir=output_dir, inflevel=inflevel)
    end = time.time()
    print(f"completed in time: {end-start:.2f} secs")

