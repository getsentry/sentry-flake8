import json
import simplejson
from json import loads, load
from simplejson import JSONDecoder, JSONDecodeError, _default_encoder
import sentry.utils.json as good_json
from sentry.utils.json import JSONDecoder, JSONDecodeError


def bad_code():
    a = json.loads("''")
    b = simplejson.loads("''")
    c = loads("''")
    d = load()
