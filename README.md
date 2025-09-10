# xbitinfo-data-compression

This repository provides Python scripts for compressing a single file, or recursively all files in a directory, using a precomputed bitinformation .ini config file. Once per-variable keepbits (number of fraction bits to retain to meet a target preserved-information level; trailing bits are rounded to zero before lossless compression) are computed and stored in the config, they can be used by xarray’s netCDF4 compression to compress any file in the same collection.
The script used to precompute the bitinformation is also included.
## **Scripts**

- **`find_keepbits.py`**  
  Computes bitinformation **keepbits** for each variable of a NetCDF data file and saves them into a `.ini` config file.

- **`compress_with_keepbits.py`**  
  Compresses a single file using precomputed keepbits from the config file.

- **`compress_with_keepbits_many_files.py`**  
  Compresses multiple files using the precomputed keepbits from the config file.

## **Example Config Files**
Each script has a matching ".ini" config file with the same name for convenience, for example:

find_keepbits.py → find_keepbits.ini

compress_with_keepbits.py → compress_with_keepbits.ini

compress_with_keepbits_many_files.py → compress_with_keepbits_many_files.ini

The user assigned parameters are stored inside these config files. The name of these config files can be changed by the users as long as the structure is matched.

## Usage

Run each script with its corresponding config file.

```bash
python compress_with_keepbits.py compress_with_keepbits.ini 
python compress_with_keepbits_many_files.py compress_with_keepbits_many_files.ini 
pixi run python find_keepbits.py find_keepbits.ini 
```

## Dependencies

- Python **3.9+**
- The scripts for **compression** (`compress_with_keepbits.py` and `compress_with_keepbits_many_files.py`) only need **xarray** in addition to the standard Python libraries.
- The script for **calculating bit information** (`find_keepbits.py`) requires **xbitinfo**.
- For xbitinfo installation: Clone the repo (or "pixi.lock" and "pyproject.toml" files), and run "pixi shell" to download the dependencies. Then run "exit". Then you can run your python scripts on the compute nodes:  "pixi run python find_keepbits.py find_keepbits.ini". For more information see: [xbitinfo GitHub](https://github.com/ashiklom/gmao-compression/blob/main/README.md)
