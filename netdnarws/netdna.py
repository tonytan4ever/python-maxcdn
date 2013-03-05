from __future__ import unicode_literals

import re
from requests import Request, Session
from oauthlib.oauth1 import Client, SIGNATURE_TYPE_QUERY, SIGNATURE_TYPE_BODY
from oauthlib.oauth1.rfc5849 import CONTENT_TYPE_FORM_URLENCODED


class NetDNA(object):

    def __init__(self, company_alias, key, secret,
                 server='rws.netdna.com', secure_connection=True, **kwargs):
        self.company_alias = company_alias
        self.server = server
        self.secure_connection = secure_connection
        self.client = Session()
        self.oauth_url = Client(key, client_secret=secret,
                                 signature_type=SIGNATURE_TYPE_QUERY, **kwargs)
        self.oauth_header = Client(key, client_secret=secret, **kwargs)
        self.oauth_body = Client(key, client_secret=secret,
                                  signature_type=SIGNATURE_TYPE_BODY, **kwargs)

    @property
    def _connection_type(self):
        if self.secure_connection:
            return "https"
        return "http"

    def _get_url(self, uri):
        return "%s://%s/%s%s" % (
                                  self._connection_type,
                                  self.server,
                                  self.company_alias,
                                  uri
                                )

    def _get_content_length(self, data):
        if data:
            return len(Request._encode_params(data))
        return 0

    def _get_content_length_header(self, data):
        return {'Content-Length': str(self._get_content_length(data))}

    def _normalize_signature(self, authorization, other):
        nonce_matcher = re.compile('oauth_nonce="?(\d+)"?')
        nonce = nonce_matcher.search(authorization).groups()[0]

        timestamp_matcher = re.compile('oauth_timestamp="?(\d+)"?')
        timestamp = timestamp_matcher.search(authorization).groups()[0]

        signature_matcher = re.compile('oauth_signature="?([%a-zA-Z0-9]+)"?')
        signature = signature_matcher.search(authorization).groups()[0]

        return other.replace(
                 nonce_matcher.search(other).groups()[0],
                 nonce
               ).replace(
                 timestamp_matcher.search(other).groups()[0],
                 timestamp
               ).replace(
                 signature_matcher.search(other).groups()[0],
                 signature
               ).replace('&&', '&')

    def _sign_request(self, url, method='GET', body=None, headers=None):
        signed_url = self.oauth_url.sign(url, method,
                                         body=body, headers=headers)[0]
        signed_headers = self.oauth_header.sign(url, method,
                                                body=body, headers=headers)[1]
        signed_body = self.oauth_body.sign(url, method,
                                           body=body, headers=headers)[2]

        auth = signed_headers['Authorization'] if body is None else signed_body

        signed_url = self._normalize_signature(auth, signed_url)
        signed_body = self._normalize_signature(auth, signed_body)
        signed_headers['Authorization'] = self._normalize_signature(
                                            auth,
                                            signed_headers['Authorization']
                                          )

        return signed_url, signed_headers, signed_body

    def _response_as_json(self, method, uri, debug=False,
          debug_json=False, debug_request=False, override_headers=False,
          *args, **kwargs):
        headers = None

        if debug:
            print "Making %s request to %s\n" % (method.upper(),
                                                 self._get_url(uri))
        data = kwargs.get('data', None)

        if override_headers:
             headers = self._get_content_length_header(data)

        if data and 'params' not in kwargs.keys():
            kwargs['params'] = data

        request = Request(
                    method.upper(),
                    self._get_url(uri),
                    headers=headers,
                    *args,
                    **kwargs
                  )

        prepared = request.prepare()

        signed_url, signed_headers, signed_body = \
          self._sign_request(
            prepared.url.replace('+', '%20'),
            method.upper(),
            prepared.body.replace('+', '%20') if prepared.body else None,
            prepared.headers
          )

        import ipdb; ipdb.set_trace()

        if prepared.body:
            prepared.body = prepared.body.replace('+', '%20')

        prepared.url = signed_url
        prepared.headers = signed_headers

        response = self.client.send(prepared)

        if debug_request:
            return response

        if not debug_json:
            try:
                if response.status_code not in xrange(100, 401):
                    raise Exception("%d: %s" % (
                                     response.status_code,
                                     response.json()['error']['message'])
                                   )
            except TypeError:
                raise Exception(
                  "%d: No Error information supplied by the server" % (
                  response.status_code,)
                )

        return response.json()

    def get(self, uri, **kwargs):
        return self._response_as_json("get", uri, **kwargs)

    def post(self, uri, data=dict(), **kwargs):
        return self._response_as_json("post", uri, data=data, **kwargs)

    def put(self, uri, data=dict(), **kwargs):
        return self._response_as_json("put", uri, data=data, **kwargs)

    def patch(self, uri, data=dict(), **kwargs):
        return self._response_as_json("patch", uri, data=data, **kwargs)

    def delete(self, uri, **kwargs):
        return self._response_as_json("delete", uri, **kwargs)
