import requests
import os

BASE_URL = "https://ssm.dexhub.ai"
API_TOKEN = os.getenv("DEXHUB_API_TOKEN", None)

def get_dataset_uuids() -> list:
    """
    Fetch the list of dataset UUIDs along with their details.
    
    Returns:
        list: A list of dictionaries containing dataset details (UUID, name, description, download URL).
    """
    url = f"{BASE_URL}/data/datasets"
    headers = {
        "API_TOKEN": API_TOKEN,
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "Success" and "items" in data:
                datasets = []
                for item in data["items"]:
                    dataset = {
                        "uuid": item["uuid"],
                        "name": item.get("name", ""),
                        "description": item.get("description", ""),
                        "download_url": item.get("zipKey", ""),
                    }
                    datasets.append(dataset)
                return datasets
            else:
                print("No datasets found or unexpected response structure.")
                return []
        else:
            print(f"Failed to fetch datasets: {response.status_code}")
            print(response.text)
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

def download_dataset(uuid: str):
    """
    Download a dataset by UUID.
    
    Args:
        uuid (str): The UUID of the dataset to download.
    """
    url = f"{BASE_URL}/data/dataset/download/{uuid}"
    headers = {
        "API_TOKEN": API_TOKEN,
    }

    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            filename = f"dataset_{uuid}.zip"  # Save as a zip file
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Dataset {uuid} downloaded successfully as {filename}.")
        else:
            print(f"Failed to download dataset: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    datasets = get_dataset_uuids()
    if datasets:
        print("Fetched datasets:")
        for dataset in datasets:
            print(f"UUID: {dataset['uuid']}")
            print(f"Name: {dataset['name']}")
            print(f"Description: {dataset['description']}")
            print(f"Download URL: {dataset['download_url']}\n")

        # Download the first dataset
        download_dataset(datasets[0]["uuid"])
    else:
        print("No datasets available.")