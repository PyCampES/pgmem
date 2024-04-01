import os
import tarfile
import zipfile
from enum import StrEnum

import httpx


class AcceptedArchs(StrEnum):
    amd64 = "amd64"
    arm64v8 = "arm64v8"
    arm32v6 = "arm32v6"
    arm32v7 = "arm32v7"
    i386 = "i386"
    ppc64le = "ppc64le"


class AcceptedPlatforms(StrEnum):
    DARWIN = "darwin"
    LINUX = "linux"
    WINDOWS = "windows"


def map_architecture(arch: str) -> AcceptedArchs:
    if arch == "arm":
        return AcceptedArchs.arm32v7
    elif arch == "arm64":
        return AcceptedArchs.arm64v8
    elif arch == "x64":
        return AcceptedArchs.amd64
    elif arch == "ppc64":
        return AcceptedArchs.ppc64le
    elif arch == "ia32":
        return AcceptedArchs.i386
    else:
        raise ValueError("Unsupported architecture: " + arch)


def download_file(url: str, filename: str):
    """Downloads a file from the specified URL and saves it with the given filename.

    Args:
        url: The URL of the file to download.
        filename: The name of the file to save the downloaded content to.
    """
    try:
        response = httpx.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful downloads

        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"File downloaded successfully: {filename}")
    except httpx.HTTPError as err:
        # We just skip the ones that fail
        print(f"[Skipping] Download failed: {err}")


def download_binaries() -> None:
    for platform in AcceptedPlatforms:
        for arch in AcceptedArchs:
            platform_value = platform.value
            arch_raw = arch.value
            version = "16.2.0"
            filename = f"data/{version}/embedded-postgres-binaries-{platform_value}-{arch_raw}-{version}.jar"
            os.makedirs(f"data/{version}", exist_ok=True)
            # if os.path.exists(filename):
            #     print(f"File already exists: {filename}")
            #     continue
            url = f"https://repo1.maven.org/maven2/io/zonky/test/postgres/embedded-postgres-binaries-{platform_value}-{arch_raw}/{version}/embedded-postgres-binaries-{platform_value}-{arch_raw}-{version}.jar"
            print(url)
            if not os.path.exists(filename):
                download_file(url, filename)
            if os.path.exists(filename):
                unzip_file(filename, f"data/{version}")


def unzip_file(zip_filename, extract_dir=None):
    """Unzips a file to a specified directory.

    Args:
        zip_filename: The path to the zip file.
        extract_dir: The directory to extract the contents to (optional).
            If not specified, extracts to the current working directory.
    """
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(extract_dir)  # Extract all files to the specified dir


def extract_txz(txz_filename, extract_dir=None):
    """Extracts a txz file to a specified directory.

    Args:
        txz_filename: The path to the .txz file.
        extract_dir: The directory to extract the contents to (optional).
            If not specified, extracts to the current working directory.
    """
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir, exist_ok=True)  # Create dir if it doesn't exist

    with tarfile.open(txz_filename, "r:xz") as tar_ref:
        tar_ref.extractall(extract_dir)


def list_txz_files(folder_path):
  """Lists all files with the .txz extension in a given folder.

  Args:
      folder_path: The path to the folder to search.

  Returns:
      A list of filenames (strings) with the .txz extension, or an empty list if no .txz files are found.
  """
  txz_files = []
  for filename in os.listdir(folder_path):
    if filename.endswith('.txz'):
      txz_files.append(filename)
  return txz_files

