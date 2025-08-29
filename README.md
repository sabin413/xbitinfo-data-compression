# xbitinfo-data-compression

This repository provides Python scripts for compressing a single file, and compressing all files inside a directory and its subdirectories at any depth using a precomputed bitinformation `.ini` config file. It also includes the script used to precompute the bitinformation config file.

## **Scripts**

- **`find_keepbits.py`**  
  Computes **keepbits** for NetCDF data and saves them into a `.ini` config file.

- **`compress_with_keepbits.py`**  
  Compresses a single file using precomputed keepbits.

- **`compress_with_keepbits_many_files.py`**  
  Compresses multiple files in a batch, following the keepbits rules defined in the config.

## **Config Files**
Each script has a **matching `.ini` file** with the same name for convenience, for example:

find_keepbits.py → find_keepbits.ini

compress_with_keepbits.py → compress_with_keepbits.ini

compress_with_keepbits_many_files.py → compress_with_keepbits_many_files.ini

The user assigned parameters are stored inside these config files. The name of these config files can be anything as long as the structure is matched.

## Usage

Run each script with its corresponding config file.

```bash
python find_keepbits.py find_keepbits.ini
python compress_with_keepbits.py compress_with_keepbits.ini
python compress_with_keepbits_many_files.py compress_with_keepbits_many_files.ini
```

## Dependencies

- Python **3.9+**
- The scripts for **compression** (`compress_with_keepbits.py` and `compress_with_keepbits_many_files.py`) only need **xarray** in addition to the standard Python libraries.
- The script for **calculating bit information** (`find_keepbits.py`) requires **xbitinfo**, which can be found here: [xbitinfo GitHub](https://github.com/ashiklom/gmao-compression/blob/main/README.md)
