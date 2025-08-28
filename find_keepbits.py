# compute keepbits for each variable and save them in a .inf file

from pathlib import Path
import xarray as xr
import xbitinfo as xb
import time

def compute_and_save_keepbits(
    input_path: str | Path, 
    out_inf: str | Path,
    inflevel: float = 0.99,
) -> Path:
    '''read netcdf file from <input_path>, compute the # of keepbits for each variable
       at <inflevel> information level, and save results in an output config file
       <out_inf>'''

    input_path = Path(input_path)
    out_inf = Path(out_inf) / (input_path.name + ".inf")

    # 1. Load dataset
    ds = xr.open_dataset(input_path, mask_and_scale=False)

    # 2. Select variables to process
    excluded_vars = {"TAITIME", "contacts", "corner_lons", "corner_lats", "anchor"}
    included_vars = [v for v in ds.data_vars if v not in excluded_vars]
    ds_vars = ds[included_vars]

    # 3. Dimensions for xbitinfo
    kb_dims = [d for d, n in ds_vars.sizes.items() if n > 5 and "d" != "nf"] # only "long" enough  dimensions, also exclude "nf" if present
    bitinfo = xb.get_bitinformation(ds_vars, dim=kb_dims) # bitinfo in all dims
    keepbits = xb.get_keepbits(bitinfo, inflevel=inflevel).max(dim="dim") # keep max
    
    with xr.set_options(display_max_rows=100):
        print(keepbits)

    # Save keepbits: first line = source file, then "variable:keepbits"
    out_inf.parent.mkdir(parents=True, exist_ok=True)
    with open(out_inf, "w") as f:
        f.write(f"file={input_path}\n")
        f.write(f"inflevel={inflevel}\n")  
        for v, kb in keepbits.items():
            f.write(f"{v}:{int(kb.item())}\n")

    return out_inf

start = time.time()
if __name__ == "__main__":
    out_put_address = "/home/sadhika8/JupyterLinks/nobackup/gmao-compression/compression.990/"
    data = "/discover/nobackup/projects/gmao/geos-s2s-3/GiOCEAN_e1/sfc_tavg_3hr_glo_L720x361_sfc/GiOCEAN_e1.sfc_tavg_3hr_glo_L720x361_sfc.monthly.199801.nc4"
    compute_and_save_keepbits(input_path=data, out_inf=out_put_address, inflevel=0.99)
end = time.time()
print(f"time: {end-start:.2f} secs")
