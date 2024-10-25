
from __future__ import absolute_import, division, print_function, unicode_literals

from urllib import request as urlrequest, parse as urlparse
import json


class DogAPI(object):
    def _api_request(self, endpoint):
        return json.loads(urlrequest.urlopen(
            urlparse.urljoin("https://dog.ceo/api/", endpoint)
        ).read().decode("utf-8"))

    def list(self):
        return self._api_request("breeds/list")

    def list_images(self, breed, subbreed=None):
        if subbreed is None:
            return self._api_request("breed/{}/images".format(breed))
        else:
            return self._api_request("breed/{}/{}/images".format(breed, subbreed))

    def random(self, breed=None, subbreed=None):
        if breed is None:
            return self._api_request("breeds/image/random".format(breed))
        if subbreed is None:
            return self._api_request("breed/{}/images/random".format(breed))
        else:
            return self._api_request("breed/{}/{}/images/random".format(breed, subbreed))


if __name__ == "__main__":
    from pprint import pprint
    from random import choice

    dogapi = DogAPI()
    breeds = dogapi.list()['message']
    pprint(dogapi.random(choice(breeds)))
    pprint(dogapi.list_images(choice(breeds)))
    pprint(dogapi.random())
    
