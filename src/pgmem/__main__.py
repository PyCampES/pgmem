import os
from pathlib import Path
from pgmem.downloader import download_binaries, extract_txz, list_txz_files


download_binaries()
txz_files = list_txz_files("data/16.2.0")

print("---------")
for txz_file in txz_files:
    f = Path(f"data/16.2.0/{txz_file}")
    print(f.stem)
    os.makedirs(f"data/16.2.0/{f.stem}", exist_ok=True)
    file_path = f"data/16.2.0/{txz_file}"
    print(file_path)
    extract_txz(file_path, f"data/16.2.0/{f.stem}")
