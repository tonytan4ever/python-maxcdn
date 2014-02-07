from requests_oauthlib import OAuth1Session
from urllib import urlencode

class MaxCDN(object):

    def __init__(self, company_alias, key, secret,
            server="rws.maxcdn.com", secure_connection=True, **kwargs):
        self.company_alias = company_alias
        self.server = server
        self.secure_connection = secure_connection

        self.client = OAuth1Session(key,
                client_secret=secret)

    @property
    def _connection_type(self):
        if self.secure_connection:
            return "https"
        return "http"

    def _get_url(self, uri):
        if not uri.startswith("/"): uri = "/"+uri

        return "%s://%s/%s%s" % (self._connection_type,
                self.server, self.company_alias, uri)

    def _get_content_length(self, data):
        if data:
            return len(urlencode(data, True).replace("+", "%20"))
        return 0

    def _get_content_length_header(self, data):
        return {"Content-Length": str(self._get_content_length(data))}

    def _response_as_json(self, method, uri, debug=False,
            debug_json=False, debug_request=False, override_headers=False,
            *args, **kwargs):

        headers = {"User-Agent": "Python MaxCDN API Client"}

        if debug:
            print "Making %s request to %s\n" % (method.upper(),
                    self._get_url(uri))

        data = kwargs.pop("data", None)

        if override_headers:
            headers.update(self._get_content_length_header(data))

        response = getattr(self.client, method)(self._get_url(uri),
                headers=headers, data=data, *args, **kwargs)

        if debug_request:
            return response

        if not debug_json:
            try:
                if response.status_code not in xrange(100, 401):
                    raise Exception("%d: %s" % (response.status_code,
                        response.json["error"]["message"]))

            except TypeError:
                raise Exception("%d: No Error information supplied by the server" % (
                    response.status_code))

        return response.json()

    def get(self, uri, **kwargs):
        return self._response_as_json("get", uri, **kwargs)

    def post(self, uri, data={}, **kwargs):
        return self._response_as_json("post", uri, data=data, **kwargs)

    def put(self, uri, data={}, **kwargs):
        if not kwargs.has_key("override_headers"):
            kwargs["override_headers"] = True
        return self._response_as_json("put", uri, data=data, **kwargs)

    def patch(self, uri, data={}, **kwargs):
        return self._response_as_json("patch", uri, data=data, **kwargs)

    def delete(self, uri, **kwargs):
        return self._response_as_json("delete", uri, **kwargs)

    def purge(self, zone_id, file_or_files=None, **kwargs):
        if file_or_files is not None:
            return self.delete("/zones/pull.json/%s/cache" % (zone_id,),
                    data={"files": file_or_files}, **kwargs)

        return self.delete("/zones/pull.json/%s/cache" % (zone_id,), **kwargs)

