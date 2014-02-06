import mock
import unittest
from maxcdn import MaxCDN
import requests_netdna as requests

################################################################################
# Mock as needed.
def mock_response_as_json(method, uri, **kwargs):
    pass

def mock_request(method, url, *args, **kwargs):
    pass

class Response(object):
    def __init__(self, code=200, json={'foo':'bar'}):
        self.status_code = code
        self.json = json

def response(**kwargs):
    return Response(**kwargs)
#
################################################################################

class MaxCDNTests(unittest.TestCase):

    def setUp(self):
        self.alias  = 'test_alias'
        self.key    = 'test_key'
        self.secret = 'test_secret'
        self.server = 'rws.example.com'
        self.maxcdn = MaxCDN(self.alias, self.key, self.secret, server=self.server)

        # back up _response_as_json for later use
        self.was_response_as_json = self.maxcdn._response_as_json

        self.maxcdn._response_as_json = mock.create_autospec(mock_response_as_json,
                                                                return_value={ 'foo': 'bar' })

    def test_init(self):
        self.assertTrue(self.maxcdn)
        self.assertEqual(self.maxcdn.company_alias, self.alias)

    def test_connection_type(self):
        self.assertEqual(self.maxcdn._connection_type, 'https')

        max = MaxCDN(self.alias, self.key, self.secret, secure_connection=False)
        self.assertEqual(max._connection_type, 'http')

    def test_get_url(self):
        self.assertEqual(self.maxcdn._get_url('/foo.json'),
                            'https://rws.example.com/test_alias/foo.json')

        max = MaxCDN(self.alias, self.key, self.secret, server=self.server,
                        secure_connection=False)

        self.assertEqual(max._get_url('/foo.json'), 'http://rws.example.com/test_alias/foo.json')

    def test_get_content_length(self):
        self.assertEqual(self.maxcdn._get_content_length(None), 0)
        self.assertEqual(self.maxcdn._get_content_length('foo bar bah'), 11)

    def test_get_content_length_header(self):
        self.assertEqual(self.maxcdn._get_content_length_header(None), {'Content-Length': '0'})
        self.assertEqual(self.maxcdn._get_content_length_header('foo bar bah'),
                                                                    {'Content-Length': '11'})

    def test_get_content_length(self):
        self.assertEqual(self.maxcdn._get_content_length(None), 0)
        self.assertEqual(self.maxcdn._get_content_length('foo bar bah'), 11)

    def test_get(self):
        self.assertEqual(self.maxcdn.get('/get.json'), { 'foo': 'bar' })
        self.maxcdn._response_as_json.assert_called_with('get', '/get.json')

    def test_post(self):
        self.assertEqual(self.maxcdn.post('/post.json'), { 'foo': 'bar' })
        self.maxcdn._response_as_json.assert_called_with('post', '/post.json', data={})

        self.maxcdn.post('/post.json', data={ "bah": "boo" })
        self.maxcdn._response_as_json.assert_called_with('post', '/post.json',
                                                            data={ "bah": "boo" })

    def test_put(self):
        self.assertEqual(self.maxcdn.put('/put.json'), { 'foo': 'bar' })
        self.maxcdn._response_as_json.assert_called_with('put', '/put.json', override_headers=True,
                                                            data={})

        self.maxcdn.put('/put.json', data={ "bah": "boo" })
        self.maxcdn._response_as_json.assert_called_with('put', '/put.json', override_headers=True,
                                                            data={ "bah": "boo" })

        self.maxcdn.put('/put.json', data={ "bah": "boo" }, override_headers=False)
        self.maxcdn._response_as_json.assert_called_with('put', '/put.json', data={ "bah": "boo" },
                                                            override_headers=False)

    def test_patch(self):
        self.assertEqual(self.maxcdn.patch('/patch.json'), { 'foo': 'bar' })
        self.maxcdn._response_as_json.assert_called_with('patch', '/patch.json', data={})

        self.maxcdn.patch('/patch.json', data={"patch":"data"})
        self.maxcdn._response_as_json.assert_called_with('patch', '/patch.json',
                                                            data={"patch":"data"})

    def test_delete(self):
        self.assertEqual(self.maxcdn.delete('/delete.json'), { 'foo': 'bar' })
        self.maxcdn._response_as_json.assert_called_with('delete', '/delete.json')

    def test_purge(self):
        self.assertEqual(self.maxcdn.purge(12345), { 'foo': 'bar' })
        self.maxcdn._response_as_json.assert_called_with('delete', '/zones/pull.json/12345/cache')

        self.assertEqual(self.maxcdn.purge(12345, '/master.css'), { 'foo': 'bar' })
        self.maxcdn._response_as_json.assert_called_with('delete', '/zones/pull.json/12345/cache',
                                                            data={ 'files': '/master.css' })

        self.assertEqual(self.maxcdn.purge(12345, ['/master.css', '/other.css']), { 'foo': 'bar' })
        self.maxcdn._response_as_json.assert_called_with('delete', '/zones/pull.json/12345/cache',
                                                            data={ 'files': ['/master.css', '/other.css'] })


    def test_response_as_json_basics(self):
        self.maxcdn._response_as_json = self.was_response_as_json

        # cover the basics
        for meth in [ 'get', 'post', 'put', 'patch', 'delete' ]:
            requests.Session.request = mock.create_autospec(mock_request,
                                                            return_value=response(json={ 'res': meth }))

            self.assertEqual(getattr(self.maxcdn, meth)('/%s.json' % meth), { 'res': meth })

    def test_response_as_json_with_data(self):
        self.maxcdn._response_as_json = self.was_response_as_json
        for meth in [ 'post', 'put', 'patch' ]:
            requests.Session.request = mock.create_autospec(mock_request,
                                                            return_value=response(json={ 'res': meth }))

            self.assertEqual(getattr(self.maxcdn, meth)('/%s.json' % meth, data={'req': meth}),
                                                            { 'res': meth })

    def test_response_as_json_with_files(self):
        self.maxcdn._response_as_json = self.was_response_as_json
        for meth in [ 'post', 'put', 'patch' ]:
            requests.Session.request = mock.create_autospec(mock_request,
                                                            return_value=response(json={ 'res': meth }))

            self.assertEqual(getattr(self.maxcdn, meth)('/%s.json' % meth, data={'req': meth}),
                                                            { 'res': meth })

    def test_response_as_json_pruge(self):
        self.maxcdn._response_as_json = self.was_response_as_json
        requests.Session.request = mock.create_autospec(mock_request, return_value=response(json={ 'res': 'delete' }))

        self.assertEqual(self.maxcdn.purge(12345), { 'res': 'delete' })

