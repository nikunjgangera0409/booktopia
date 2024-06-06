import requests
import pandas as pd

def fetch_resolved_urls(isbn_list):
    base_url = "https://www.booktopia.com.au/search.ep?keywords={}"
    resolved_urls = []

    for isbn in isbn_list:
        search_url = base_url.format(isbn)
        try:
            response = requests.get(search_url, allow_redirects=True)
            if response.status_code == 200:
                resolved_urls.append(response.url)
                print(f"Resolved URL for ISBN {isbn}: {response.url}")
            else:
                resolved_urls.append(None)
        except requests.RequestException as e:
            print(f"Error fetching {search_url}: {e}")
            resolved_urls.append(None)

    return resolved_urls

if __name__ == "__main__":
    input_file = r"C:\Users\nikun\Downloads\input_list.csv"
    output_file = r"resolved_urls.csv"

    # Read the ISBN list and ensure they are treated as strings
    isbn_13 = pd.read_csv(input_file)['ISBN13'].astype(str).tolist()

    # Fetch resolved URLs
    resolved_urls = fetch_resolved_urls(isbn_13)

    # Save resolved URLs to CSV
    df = pd.DataFrame({"ISBN13": isbn_13, "ResolvedURL": resolved_urls})
    df.to_csv(output_file, index=False)
