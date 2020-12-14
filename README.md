# Simple server with REST-style API

## Implementation

The server is programmed with Python and the library Flask.

The server meets all the requirements listed in the "Details and limitations".

Coding the server was not a difficult task, and it took me about 1,5 hours.

The testing was the part that took me the most time, about 4,5 hours. I was not familiar with the unittest of Python and mocking the functions caused me some trouble. I had to take some time to study the unittest framework.


## Running the code

1. Create your virtual environment in the root folder
```
python3 -m venv venv
```
2. Start virtual environment
```
. venv/bin/activate
```
3. Load the requirements
```
pip install -r requirements.txt
```
4. Run the server with the command
```
python3 server.py
```

## Running the tests
```
python3 -m unittest
```

## Using the client program

1. Running the client program happens with the command
```
python3 client.py <url_type> <url>
```
The arguments url_type and url are mandatory, in that order.

2. To start using the server, run the command
```
python3 client.py shortened https://hiqfinland.fi/avoimet-tyopaikat
```
Any other url starting with http:// or https:// will work aswell.

The terminal now prints the response from the server, for example
```
Status: 200, message: http://localhost/61ec84e0f268c6d5
```

3. To get the original url from the server, run the command
```
python3 client.py original http://localhost/61ec84e0f268c6d5
```
The terminal will print the message
```
Status: 200, message: https://hiqfinland.fi/avoimet-tyopaikat/
```

