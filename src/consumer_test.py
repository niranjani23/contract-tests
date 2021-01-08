import atexit
import unittest

from pact import Consumer, Provider

from src.provider_app import items

pact = Consumer('consumer_app').has_pact_with(Provider('provider_app'))
pact.start_service()
atexit.register(pact.stop_service)


class GetItemInfoContract(unittest.TestCase):
  def test_get_item(self):
    expected = {
      'name': 'Strawberries',
      'id': 1,
      'count': 2
    }

    (pact
     .given('Item exists')
     .upon_receiving('a request for Strawberries')
     .with_request('get', '/items')
     .will_respond_with(200, body=expected))

    with pact:
      result = items[0]

    self.assertEqual(result, expected)

class GetItemIdInfoContract(unittest.TestCase):
  def test_get_item_id(self):
    expected = {
      'name': 'Carrots',
      'id': 2,
      'count': 3.50
    }

    (pact
     .given('Item exists')
     .upon_receiving('a request for item id:2')
     .with_request('get', '/items/2')
     .will_respond_with(200, body=expected))

    with pact:
      result = items[1]

    self.assertEqual(result, expected)