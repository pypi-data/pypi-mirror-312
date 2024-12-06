import os
import subprocess
import sys
import requests

try:
    import requests
except ImportError:
    print("Requests module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

file_db = {
    2: "https://drive.google.com/uc?export=download&id=1u5joEb01_yXiwfXh6oL-Gip7irRepshh",
    3: "https://drive.google.com/uc?export=download&id=1zBGX5zzu3x3bwyUzQPp6LnTfVWgoXNXZ",
    7: "https://drive.google.com/uc?export=download&id=1PHy8x5PHiaO1K_IpN19apOoHAYUdWgCf",
    5: "https://drive.google.com/uc?export=download&id=1mVCdpwQRGBYL_7eyEpobsSLugY5LACGu",
    8: "https://shorturl.at/5hsGp",  # For file 8, we print the URL
    6: "https://drive.google.com/uc?export=download&id=1KgRx4hCCS1Za9-wIcNZKmTjVc-b6QlRu",
}

def get_file_name(file_number):
    if file_number == 8:
        return "file-8.zip"
    else:
        return f"file-{file_number}.txt"

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def download_file(url, file_path):
    session = requests.Session()

    response = session.get(url, stream=True)

    if 'confirm' in response.url:
        confirm_url = response.url
        confirm_token = confirm_url.split('=')[-1]
        confirm_url = f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={url.split('=')[-1]}"
        response = session.get(confirm_url, stream=True)

    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def main():
    print("Welcome!")
    print("Enter the file number you want to download:")

    try:
        file_number = int(input("File Number: "))

        if file_number in file_db:
            if file_number == 8:
                # For file number 8, just print the URL
                print("file 8 :")
                print("https://shorturl.at/5hsGp")
            else:
                file_url = file_db[file_number]
                file_name = get_file_name(file_number)

                desktop_path = get_desktop_path()
                file_path = os.path.join(desktop_path, file_name)

                print(f"Downloading {file_name} to Desktop...")

                download_file(file_url, file_path)

                print(f"{file_name} has been downloaded to {desktop_path}")
        else:
            print("Invalid file number. Please try again.")
    except ValueError:
        print("Invalid input! Please enter a valid number.")
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")
    except OSError as e:
        print(f"Error saving the file: {e}")

if __name__ == "__main__":
    main()
