from flask import Flask, make_response, request
import re
import secrets
import time

app = Flask(__name__)

"""
Store the data in two dictionaries for fast and easy access.
"""
url_key_dict = {} # { "url": "key" }
key_url_dict = {} # { "key": { "url": "url", "created_at": "created_at" } }
prefix = "http://localhost/"


@app.route("/shortened/")
def get_shortened_url():
  """
  Endpoint /shortened/?url=<url>
  Returns 404 if parameter url is invalid.
  Returns 200 in every other case.

  If the parameter url is not already stored, a new shortened url is created
  and returned for that url.

  If the parameter url is already stored, the expiration time of that shortened url is
  checked. If expired, the url gets stored with a new shortened url and expiration time.
  If not expired, returns the shortened url with the same expiration time.

  """
  url = request.args.get("url")
  if not is_valid_url(url):
    return make_response("The url was not valid! Make sure to start the url with http:// or https://", 404)
  key = url_key_dict.get(url)
  if key:
    if not expired(key):
      return make_response(prefix + key, 200)
    key_url_dict.pop(key, None)
    url_key_dict.pop(url, None)
    key = create_new_key_url_pair(url)
    return make_response(prefix + key, 200)
  key = create_new_key_url_pair(url)
  return make_response(prefix + key, 200)

@app.route("/original/")
def get_original_url():
  """
  Endpoint /original/?url=<url>

  Returns 404 if parameter url did not match "http://localhost/<key_of_16_characters>".
  Returns 404 if there was no shortened url for the parameter url.
  Returns 404 if the shortened url has expired (7 days).
  Returns 200 and the original url only if there was a shortened url
  and it has not expired.
  """
  url = request.args.get("url")
  if not is_valid_shortened_url(url):
    return make_response("The url was not valid! Make sure to start the url with {}".format(prefix), 404)
  key = get_key_from_url(url)
  original_url_object = key_url_dict.get(key)
  if original_url_object:
    if not expired(key):
      return make_response(original_url_object["url"], 200)
    return make_response("The key for {} has expired!".format(original_url_object["url"]), 404)
  return make_response("No url for key {} was found!".format(key), 404)
  


def create_new_key_url_pair(url):
  """
  Returns a new unique key for the given url.
  Adds the key and url to the corresponding dictionaries.

  This function makes sure, that the keys created are unique.
  """
  key = create_new_key()
  while key_url_dict.get(key):
    key = create_new_key()
  url_key_dict[url] = key
  key_url_dict[key] = create_new_url_object(url)
  return key

def get_key_from_url(url):
  return url.replace(prefix, "")

def create_new_url_object(url):
  return { "url": url, "created_at": get_current_time() }

def create_new_key():
  return secrets.token_hex(8)

def is_valid_url(url):
  regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
  return re.match(regex, url)

def is_valid_shortened_url(url):
  regex = r"http:\/\/localhost\/[a-z0-9]{16}$" # Somehow put the prefix variable in the regex!
  return re.match(regex, url)

def expired(key):
  # 7 days is equal to 604800 seconds
  return get_current_time() - key_url_dict[key]["created_at"] > 604800

def get_current_time():
  return int(time.time())

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5003, debug=True)