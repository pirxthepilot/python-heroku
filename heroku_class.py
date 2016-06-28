# Heroku Module
# For querying the Heroku API

import requests
import urllib
import json
import sys
import re


class Heroku:

    def __init__(self, baseurl, app_name, api_key, ca_cert=None):
        self.querybase = baseurl + '/apps/' + app_name
        self.headers = {"Content-Type": "application/json",
                        "Accept": "application/vnd.heroku+json; version=3",
                        "Authorization": "Bearer " + api_key}
        self.verify = True if ca_cert is None else ca_cert

    def query(self, method, uri, jsondata=None):
        try:
            # If no jsondata, it is a GET request
            if method == 'GET':
                response = requests.get(self.querybase + uri,
                                        headers=self.headers,
                                        verify=self.verify)
            if method == 'POST':
                response = requests.post(self.querybase + uri,
                                         data=jsondata,
                                         headers=self.headers,
                                         verify=self.verify)
            if method == 'DELETE':
                response = requests.delete(self.querybase + uri,
                                        headers=self.headers,
                                        verify=self.verify)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects) as e:
            print 'requests error: ' + str(e)
            sys.exit(1)
        self.http_error_check(response)
        return response.json()

    def list_dynos(self):
        req = self.query('GET', '/dynos')
        return json.dumps(req)

    def restart_all_dynos(self):
        req = self.query('DELETE', '/dynos')
        return json.dumps(req)

    def http_error_check(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print str(e)
            sys.exit(1)
