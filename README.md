# NetDNA REST Web Services Python Client

## Installation
`sudo pip install netdnarws`

## Usage
```python
from netdnarws import NetDNA

api = NetDNA("myalias", "consumer_key", "consumer_secret")

api.get("/account.json")
```

## Methods
It has support for GET, POST, PUT and DELETE ouath signed requests.

Every request can take an optional debug parameter.
```python
api.get("/account.json", debug=True)
# Will output
# Making GET request to http://rws.netdna.com/myalias/account.json
#{... API Returned Stuff ...}
```

For more information about what optional parameters this methods accept you
should check out [@kennethreitz](http://github.com/kennethreitz) library
[Requests](https://github.com/kennethreitz/requests).

## Initialization
For applications that don't require user authentication,
you can use the default initialization as the example above.

For applications that require user authentication, you can
initialize the API as follows.

```python
api = NetDNA("myalias", "consumer_key", "consumer_secret",
             token="user_token", token_secret="user_token_secret")
```

You can also send the optional parameter header_auth, which takes a boolean
to send the OAuth header in the body or URLEncoded.
