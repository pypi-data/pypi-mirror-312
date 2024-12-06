import requests
import os
from pathlib import Path
import json
from tqdm import tqdm


def get_dataset_directory():
    """Get the directory where datasets are stored in the package."""
    package_dir = Path(__file__).resolve().parent
    dataset_dir = package_dir / "datasets"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    return dataset_dir


def get_dataset_repository():
    base_url = "https://raw.githubusercontent.com/"
    gh_repo = "Xpertians/ossbomer-dataset"
    gh_branch = "/main"
    return base_url + gh_repo + gh_branch


def fetch_remote_file(url, local_path):
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed fetch {url}. status: {response.status_code}")

    total_size = int(response.headers.get('content-length', 0))
    if total_size == 0:
        raise Exception(f"The file at {url} is empty or unavailable.")

    with open(local_path, "wb") as file, tqdm(
        desc=f"Downloading {local_path.name}",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))


def is_update_needed(local_path, remote_url):
    """Check if the local dataset needs to be updated by comparing versions."""
    if not local_path.exists():
        return True

    # Fetch the remote dataset
    response = requests.get(remote_url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch dataset from {remote_url}. "
            f"HTTP status: {response.status_code}"
        )

    remote_data = response.json()
    remote_version = remote_data.get("version")
    if not remote_version:
        raise ValueError("Remote dataset does not contain a 'version' field.")

    # Load the local dataset
    with open(local_path, "r") as file:
        local_data = json.load(file)
        local_version = local_data.get("version", "0.0.0")

    return remote_version > local_version


def update_datasets():
    dataset_dir = get_dataset_directory()
    dataset_repo = get_dataset_repository()

    datasets = {
        "license_rules.json": {
            "file_url": dataset_repo + "/license_rules.json"
        }
    }

    for file_name, urls in datasets.items():
        local_path = dataset_dir / file_name
        file_url = urls["file_url"]

        try:
            if is_update_needed(local_path, file_url):
                print(f"Updating {file_name}...")
                fetch_remote_file(file_url, local_path)
                print(f"{file_name} updated successfully!")
            else:
                print(f"{file_name} is already up-to-date.")
        except Exception as e:
            print(f"Error updating {file_name}: {e}")


def update_package_signatures():
    dataset_dir = get_dataset_directory() / "package_signatures"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    dataset_repo = get_dataset_repository()
    remote_base_url = dataset_repo + "/package_signatures/"
    index_url = f"{remote_base_url}index.json"
    response = requests.get(index_url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch package signature index. "
            f"HTTP Status: {response.status_code}"
        )

    package_files = response.json().get("packages", [])
    updated_files = []

    for package_file in package_files:
        file_url = f"{remote_base_url}{package_file}"
        local_path = dataset_dir / package_file

        try:
            if is_update_needed(local_path, file_url):
                print(f"Updating {package_file}...")
                fetch_remote_file(file_url, local_path)
                updated_files.append(package_file)
                print(f"{package_file} updated successfully!")
            else:
                print(f"{package_file} is already up-to-date.")
        except Exception as e:
            print(f"Error updating {package_file}: {e}")

    # Regenerate the local index.json
    regenerate_local_index(dataset_dir)
    print("Local index.json regenerated successfully!")


def regenerate_local_index(dataset_dir):
    package_files = [f.name for f in dataset_dir.glob("*.json")]
    index_data = {"packages": package_files}

    index_path = dataset_dir / "index.json"
    with open(index_path, "w") as file:
        json.dump(index_data, file, indent=4)


def get_inventory():
    """Display an inventory of dataset files and their versions."""
    dataset_dir = get_dataset_directory()
    inventory = []
    dataset_repo = get_dataset_repository()

    # Add license rules to the inventory
    license_file = dataset_dir / "license_rules.json"
    license_remote_url = dataset_repo + "/license_rules.json"
    inventory.append(get_file_info(license_file, license_remote_url))

    # Add package signatures to the inventory
    package_dir = dataset_dir / "package_signatures"
    if package_dir.exists():
        for package_file in package_dir.glob("*.json"):
            if package_file.name == "index.json":
                continue  # Skip index.json
            remote_url = (
                f"{dataset_repo}/package_signatures/{package_file.name}"
            )
            inventory.append(get_file_info(package_file, remote_url))

    # Display the inventory
    print(
        f"{'File':<30} {'Local Version':<15} "
        f"{'Remote Version':<15} {'Status'}"
    )
    print("-" * 75)
    for item in inventory:
        print(
            f"{item['file']:<30} {item['local_version']:<15} "
            f"{item['remote_version']:<15} {item['status']}"
        )


def get_file_info(local_path, remote_url):
    """Retrieve information about a dataset file, including versions."""
    local_version = "N/A"
    remote_version = "N/A"
    status = "Not Downloaded"

    # Check local version
    if local_path.exists():
        try:
            with open(local_path, "r") as file:
                local_data = json.load(file)
                local_version = local_data.get("version", "Unknown")
        except Exception:
            local_version = "Error Reading"

    # Check remote version
    try:
        response = requests.get(remote_url)
        if response.status_code == 200:
            remote_data = response.json()
            remote_version = remote_data.get("version", "Unknown")
    except Exception:
        remote_version = "Error Fetching"

    # Determine status
    if local_version == "N/A":
        status = "Not Downloaded"
    elif local_version == remote_version:
        status = "Up-to-Date"
    elif remote_version != "Unknown" and local_version != remote_version:
        status = "Update Available"

    return {
        "file": local_path.name,
        "local_version": local_version,
        "remote_version": remote_version,
        "status": status,
    }
