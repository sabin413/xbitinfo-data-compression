# compress with pre-computed keepbits

from pathlib import Path
import shutil
import tempfile
import time
import xarray as xr
#import xbitinfo as xb

def _read_keepbits_inf(path: str | Path) -> tuple[dict[str, int], float]:
    '''read pre-computed keepbits from a file''' 
    kb = {}
    inflevel = None
    with open(path, "r") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("file="):
                continue
            if s.startswith("inflevel="):
                inflevel = float(s.split("=", 1)[1])
            if ":" in s:
                v, k = s.split(":", 1)
                kb[v.strip()] = int(k.strip())
    if inflevel is None:
        raise ValueError("inflevel missing in .inf")
    return kb, inflevel


def compress_with_keepbits(
    input_path: str | Path,
    output_path: str | Path,
    keepbits_inf: str | Path,
) -> None:
    """
    Read precomputed keepbits and then zlib-compress the file using xbitinfo rounding. 
    Save the file at output_path.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    # 1. Load dataset
    ds = xr.open_dataset(input_path, mask_and_scale=False)

    # 2. Read keepbits from .inf 
    kb_map, inflevel = _read_keepbits_inf(keepbits_inf)

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
    
    infile_size = input_path.stat().st_size / (1024 * 1024)
    outfile_size = output_path.stat().st_size / (1024 * 1024)
   # print(infile_size, outfile_size, infile_size/outfile_size)
   # print(f"✔ File written: {output_path}")


if __name__ == "__main__":

    start = time.time()
    data =  "/discover/nobackup/projects/gmao/geos-s2s-3/GiOCEAN_e1/sfc_tavg_3hr_glo_L720x361_sfc/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.monthly.199801.nc4"
    # Directory where Part 1 saved the .inf files; filename derived from input_path
    keepbits_dir = "/home/sadhika8/JupyterLinks/nobackup/gmao-compression/compression.990"
    keepbits_inf = Path(keepbits_dir) / (Path(data).name + ".inf")

    compress_with_keepbits(
        input_path=data,
        output_path="sample.nc4",
        keepbits_inf=keepbits_inf,
    )
    end = time.time()

    print(f"time: {end-start:.2f} secs")
