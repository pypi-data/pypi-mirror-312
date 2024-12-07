import requests
def get_google():
    response=requests.get("http://www.google.com")
    return response.text[:100]

if __name__ == "__main__":
    print(get_google())