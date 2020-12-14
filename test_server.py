import re
from server import app, create_new_key, create_new_key_url_pair, get_current_time, get_key_from_url, is_valid_shortened_url, is_valid_url, key_url_dict, prefix, url_key_dict
import unittest
from unittest.mock import patch

keys = [
  "fbk2fmwkuoeqrmda",
  "fbk2fmwkuoeqjmdb",
  "fbk203wkupeqomdc"
]

class TestFlaskApp(unittest.TestCase):
  def setUp(self):
    self.app = app.test_client()

  @patch("server.create_new_key")
  def test_shortened_returns_correct_url(self, create_new_key):
    create_new_key.return_value = keys[0]
    with patch.dict(url_key_dict, {}, clear=True):
      with patch.dict(key_url_dict, {}, clear=True):
        r = self.app.get("/shortened/?url=https://hiqfinland.fi/avoimet-tyopaikat/")
        expected = "http://localhost/{}".format(keys[0])
        self.assertEqual(r.data, bytes(expected, encoding="utf-8"))
        self.assertEqual(r.status_code, 200)
  
  def test_shortened_returns_error_if_invalid_url(self):
    r = self.app.get("/shortened/?url=invalid")
    expected = "The url was not valid! Make sure to start the url with http:// or https://"
    self.assertEqual(r.data, bytes(expected, encoding="utf-8"))
    self.assertEqual(r.status_code, 404)
  
  def test_original_returns_error_if_invalid_url(self):
    r = self.app.get("/original/?url=invalid")
    expected = "The url was not valid! Make sure to start the url with {}".format(prefix)
    self.assertEqual(r.data, bytes(expected, encoding="utf-8"))
    self.assertEqual(r.status_code, 404)
  
  def test_get_key_from_url_returns_the_key(self):
    url = "http://localhost/whateverkey"
    self.assertEqual(get_key_from_url(url), "whateverkey")
  
  def test_valid_original_urls(self):
    valid_urls = [
      "http://youtube.com",
      "https://youtube.com",
      "http://www.youtube.com",
      "https://www.youtube.com",
      "http://youtube.com/search/?id=search_id&views=599"
    ]
    for u in valid_urls:
      self.assertTrue(is_valid_url(u))
  
  def test_invalid_original_urls(self):
    invalid_urls = [
      "www.youtube.com",
      "youtube.com",
      "youtube",
      "http://localhost:5000",
      "https:///youtube.com",
      "https://youtube"
    ]
    for u in invalid_urls:
      self.assertFalse(is_valid_url(u))
  
  def test_valid_shortened_urls(self):
    valid_urls = [
      "http://localhost/1234567891234567",
      "http://localhost/hdgkhsg73h8phs87"
    ]
    for u in valid_urls:
      self.assertTrue(is_valid_shortened_url(u))

  def test_invalid_shortened_urls(self):
    invalid_urls = [
      "localhost/1234567891234567",
      "https://localhost/hdjkhsg73h8phs87",
      "www.dsd.com/1234567891234567",
      "http://localhost/needstohave16ok",
      "http://localhost/needstohave16okay"
    ]
    for u in invalid_urls:
      self.assertFalse(is_valid_shortened_url(u))
  
  def test_tokens_are_unique(self):
    """
    This test does not assure that the keys are unique.
    It only gives a hint to the programmer, in case this test fails.
    """
    test_dict = {}
    for i in range(100000):
      t = create_new_key()
      self.assertFalse(test_dict.get(t))
      test_dict[t] = True
  
  @patch("server.create_new_key")
  @patch("server.get_current_time")
  def test_create_new_key_url_pair_returns_unique_key_and_updates_dictonaries(self, get_current_time, create_new_key):
    create_new_key.side_effect = [keys[0], keys[0], keys[1]]
    get_current_time.side_effect = [1000, 1001]
    with patch.dict(url_key_dict, {}, clear=True):
      with patch.dict(key_url_dict, {}, clear=True):
        create_new_key_url_pair("https://hiqfinland.fi/avoimet-tyopaikat/")
        create_new_key_url_pair("https://youtube.com")
        self.assertEqual(url_key_dict, {
          "https://hiqfinland.fi/avoimet-tyopaikat/": keys[0],
          "https://youtube.com": keys[1]
        })
        self.assertEqual(key_url_dict, {
          keys[0]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 1000 },
          keys[1]: { "url": "https://youtube.com", "created_at": 1001 }
        })
  
  @patch("server.create_new_key")
  @patch("server.get_current_time")
  def test_shortened_sets_dictionaris_correctly_when_new_urls_requested(self, get_current_time, create_new_key):
    get_current_time.side_effect = [12345, 12350]
    create_new_key.side_effect = [keys[0], keys[1]]
    with patch.dict(url_key_dict, {}, clear=True):
      with patch.dict(key_url_dict, {}, clear=True):
        self.app.get("/shortened/?url=https://hiqfinland.fi/avoimet-tyopaikat/")
        self.assertEqual(url_key_dict, { "https://hiqfinland.fi/avoimet-tyopaikat/": keys[0] })
        self.assertEqual(key_url_dict, { keys[0]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 12345 } })
        
        self.app.get("/shortened/?url=https://www.youtube.com")
        self.assertEqual(url_key_dict, {
          "https://hiqfinland.fi/avoimet-tyopaikat/": keys[0],
          "https://www.youtube.com": keys[1]
        })
        self.assertEqual(key_url_dict, {
          keys[0]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 12345 },
          keys[1]: { "url":  "https://www.youtube.com", "created_at": 12350 }
        })

  @patch("server.create_new_key")
  @patch("server.get_current_time")
  def test_shortened_returns_existing_shortened_url_if_not_expired(self, get_current_time, create_new_key):
    get_current_time.side_effect = [1000, 605800]
    create_new_key.side_effect = [keys[0]]
    with patch.dict(url_key_dict, {}, clear=True):
      with patch.dict(key_url_dict, {}, clear=True):
        self.app.get("/shortened/?url=https://hiqfinland.fi/avoimet-tyopaikat/")
        self.assertEqual(url_key_dict, { "https://hiqfinland.fi/avoimet-tyopaikat/": keys[0] })
        self.assertEqual(key_url_dict, { keys[0]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 1000 } })
        
        r = self.app.get("/shortened/?url=https://hiqfinland.fi/avoimet-tyopaikat/")
        self.assertEqual(url_key_dict, {
          "https://hiqfinland.fi/avoimet-tyopaikat/": keys[0]
        })
        self.assertEqual(key_url_dict, {
          keys[0]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 1000 },
        })

        expected = "http://localhost/{}".format(keys[0])
        self.assertEqual(r.data, bytes(expected, encoding="utf-8"))
        self.assertEqual(r.status_code, 200)

    
  @patch("server.create_new_key")
  @patch("server.get_current_time")
  def test_shortened_returns_existing_shortened_url_if_expired(self, get_current_time, create_new_key):
    get_current_time.side_effect = [1000, 605801, 605802] # 604800 is 7 days
    create_new_key.side_effect = [keys[0], keys[1]]
    with patch.dict(url_key_dict, {}, clear=True):
      with patch.dict(key_url_dict, {}, clear=True):
        self.app.get("/shortened/?url=https://hiqfinland.fi/avoimet-tyopaikat/")
        self.assertEqual(url_key_dict, { "https://hiqfinland.fi/avoimet-tyopaikat/": keys[0] })
        self.assertEqual(key_url_dict, { keys[0]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 1000 } })
        
        # Removes the previous dict keys, and creates new ones
        r = self.app.get("/shortened/?url=https://hiqfinland.fi/avoimet-tyopaikat/")
        self.assertEqual(url_key_dict, {
          "https://hiqfinland.fi/avoimet-tyopaikat/": keys[1]
        })
        self.assertEqual(key_url_dict, {
          keys[1]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 605802 },
        })
        
        expected = "http://localhost/{}".format(keys[1])
        self.assertEqual(r.data, bytes(expected, encoding="utf-8"))
        self.assertEqual(r.status_code, 200) 
  
  @patch("server.create_new_key")
  @patch("server.get_current_time")
  def test_original_returns_error_if_no_matching_shortened_url(self, get_current_time, create_new_key):
    get_current_time.side_effect = [1000]
    create_new_key.side_effect = [keys[0], keys[1]]
    with patch.dict(url_key_dict, {}, clear=True):
      with patch.dict(key_url_dict, {}, clear=True):
        r = self.app.get("/shortened/?url=https://hiqfinland.fi/avoimet-tyopaikat/")

        r = self.app.get("/original/?url={}{}".format(prefix, keys[1]))
        self.assertEqual(url_key_dict, {
          "https://hiqfinland.fi/avoimet-tyopaikat/": keys[0]
        })
        self.assertEqual(key_url_dict, {
          keys[0]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 1000 },
        })

        self.assertEqual(r.data, bytes("No url for key {} was found!".format(keys[1]), encoding="utf-8"))
        self.assertEqual(r.status_code, 404)
  
  @patch("server.create_new_key")
  @patch("server.get_current_time")
  def test_original_returns_error_if_shortened_url_has_expired(self, get_current_time, create_new_key):
    get_current_time.side_effect = [1000, 605801, 605802]
    create_new_key.side_effect = [keys[0], keys[1]]
    with patch.dict(url_key_dict, {}, clear=True):
      with patch.dict(key_url_dict, {}, clear=True):
        r = self.app.get("/shortened/?url=https://hiqfinland.fi/avoimet-tyopaikat/")

        r = self.app.get("/original/?url={}{}".format(prefix, keys[0]))
        self.assertEqual(url_key_dict, {
          "https://hiqfinland.fi/avoimet-tyopaikat/": keys[0]
        })
        self.assertEqual(key_url_dict, {
          keys[0]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 1000 },
        })

        self.assertEqual(r.data, bytes("The key for https://hiqfinland.fi/avoimet-tyopaikat/ has expired!", encoding="utf-8"))
        self.assertEqual(r.status_code, 404)
  
  @patch("server.create_new_key")
  @patch("server.get_current_time")
  def test_original_returns_shortened_url_if_not_expired(self, get_current_time, create_new_key):
    get_current_time.side_effect = [1000, 1001, 1002]
    create_new_key.side_effect = [keys[0], keys[1]]
    with patch.dict(url_key_dict, {}, clear=True):
      with patch.dict(key_url_dict, {}, clear=True):
        r = self.app.get("/shortened/?url=https://hiqfinland.fi/avoimet-tyopaikat/")

        r = self.app.get("/original/?url={}{}".format(prefix, keys[0]))
        self.assertEqual(url_key_dict, {
          "https://hiqfinland.fi/avoimet-tyopaikat/": keys[0]
        })
        self.assertEqual(key_url_dict, {
          keys[0]: { "url": "https://hiqfinland.fi/avoimet-tyopaikat/", "created_at": 1000 },
        })

        self.assertEqual(r.data, bytes("https://hiqfinland.fi/avoimet-tyopaikat/", encoding="utf-8"))
        self.assertEqual(r.status_code, 200)