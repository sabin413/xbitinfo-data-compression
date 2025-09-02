# xbitinfo-data-compression

This repository provides Python scripts for compressing a single file (or all files inside a directory and its subdirectories at any depth) using a precomputed bitinformation `.ini` config file. Once the number of keepbits for each variable is precomputed and stored in a config  file, it can be used by netcdf4's standard compression method to compress any file in the same collection.
The script used to precompute the bitinformation is also included.
## **Scripts**

- **`find_keepbits.py`**  
  Computes bitinformation **keepbits** for a NetCDF data file and saves them into a `.ini` config file.

- **`compress_with_keepbits.py`**  
  Compresses a single file using precomputed keepbits from the config file.

- **`compress_with_keepbits_many_files.py`**  
  Compresses multiple files in a batch using the precomputed keepbits from the config file.

## **Example Config Files**
Each script has a **matching `.ini` ** config file with the same name for convenience, for example:

find_keepbits.py → find_keepbits.ini

compress_with_keepbits.py → compress_with_keepbits.ini

compress_with_keepbits_many_files.py → compress_with_keepbits_many_files.ini

The user assigned parameters are stored inside these config files. The name of these config files can be changed by the users as long as the structure is matched.

## Usage

Run each script with its corresponding config file.

```bash
python compress_with_keepbits.py compress_with_keepbits.ini # compress single file with pre-computed keepbits
python compress_with_keepbits_many_files.py compress_with_keepbits_many_files.ini # compress multiple files with pre-computed keepbits
pixi run python find_keepbits.py find_keepbits.ini # if you want to compute keepbits for your file (needs xbitinfo)
```

## Dependencies

- Python **3.9+**
- The scripts for **compression** (`compress_with_keepbits.py` and `compress_with_keepbits_many_files.py`) only need **xarray** in addition to the standard Python libraries.
- The script for **calculating bit information** (`find_keepbits.py`) requires **xbitinfo**.
- For xbitinfo installation: Download the "pixi.lock" and "pyproject.toml" files. Then try "pixi install --locked". For more information see: [xbitinfo GitHub](https://github.com/ashiklom/gmao-compression/blob/main/README.md)
