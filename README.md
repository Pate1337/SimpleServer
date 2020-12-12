# Simple server with REST-style API

## The task

Create simple server with a REST-style API consisting of two endpoints.

- First endpoint takes in any url as parameter and returns shortened url from which the original can be retrieved.
  - Example: https://hiqfinland.fi/avoimet-tyopaikat/  => http://localhost/agf4y0dmkgfs5xod

- Second endpoint returns the original url the from shortened version
  - Example: http://localhost/agf4y0dmkgfs5xod =>  https://hiqfinland.fi/avoimet-tyopaikat/

Details and limitations:

- Shortened urls must be unique
- Length of the unique key of the second endpoint is 16 characters. Unique key is the agf4y0dmkgfs5xod part of the example url.
- Shortened url is valid for 7 days
- Do not use a data storage which requires pre-installations to the computer running the code. E.g. do not use local mysql or mongodb to store the data.
- Write proper unit tests
- You can use any programming language you like
- Add source code to your personal online git repository
- Provide HiQ access for cloning the repository
- Provide instructions of how to run the code

Follow the instructions based on you best understanding and fill in the details as you see fit.

## Implementation

The server is programmed with Python and the library Flask.

The server meets all the requirements listed in the "Details and limitations".

Coding the server was not a difficult task, and it took me about 1,5 hours.

The testing was the part that took me the most time, about 4 hours. I was not familiar with the unittest of Python and mocking the functions caused me some trouble. I had to take some time to study the unittest framework.


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

