import requests
import sys

def fetch_shortened_url(url):
  r = requests.get(url = "http://0.0.0.0:5003/shortened/?url={}".format(url.strip()))
  print("Status: {}, message: {}".format(r.status_code, r.content.decode("utf-8")))

def fetch_original_url(url):
  r = requests.get(url = "http://0.0.0.0:5003/original/?url={}".format(url.strip()))
  print("Status: {}, message: {}".format(r.status_code, r.content.decode("utf-8")))
def main():
  if len(sys.argv) != 3:
    print("2 arguments allowed! 1. argument: <method (original/shortened)>, 2. argument: <url>")
  elif sys.argv[1] == "original":
    fetch_original_url(sys.argv[2])
  elif sys.argv[1] == "shortened":
    fetch_shortened_url(sys.argv[2])
  else:
    print("First argument must be (shortened) or (original) that specifies which kind of url you want to fetch. The second argument is the url.")


if __name__ == "__main__":
  main()