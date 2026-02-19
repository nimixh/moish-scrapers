from curl_cffi import requests
import json

def search_redbubble():
    url = "https://www.redbubble.com/gql"
    # Example search query for Redbubble
    query = """
    query SearchResults($query: String!, $first: Int) {
      search(query: $query, first: $first) {
        results {
          title
          url
          image {
            url
          }
          artist {
            name
          }
        }
      }
    }
    """
    # This is a guess, I need a real query.
    # Usually you can find it by looking at the network tab in a browser.
    # Since I can't do that easily, I'll try to find an existing open source one.
    pass

# Instead of guessing GraphQL, let's try to fetch the shop page with curl_cffi again 
# but with better impersonation and maybe a different site like TeePublic.

try:
    print("Testing TeePublic with curl_cffi...")
    # TeePublic often has a simpler structure
    r = requests.get("https://www.teepublic.com/t-shirts", impersonate="chrome")
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("Success! Saving teepublic_static.html")
        with open("teepublic_static.html", "w") as f:
            f.write(r.text)
except Exception as e:
    print(f"Error: {e}")

