from ..base import ShopifyResource
from shopify import mixins
from .transaction import Transaction
from collections import Iterable


class Order(ShopifyResource, mixins.Metafields, mixins.Events):

    def close(self):
        self._load_attributes_from_response(self.post("close"))

    def open(self):
        self._load_attributes_from_response(self.post("open"))

    def cancel(self, **kwargs):
        self._load_attributes_from_response(self.post("cancel", **kwargs))

    def transactions(self):
        return Transaction.find(order_id=self.id)

    def capture(self, amount=""):
        return Transaction.create({"amount": amount, "kind": "capture", "order_id": self.id})

    def add_fulfillment(self, fulfillment):
        if self.is_new():
            raise ValueError("You can only add fulfillments to a resource that has been saved")

        fulfillment.attributes['order_id'] = self.id

        result = fulfillment.save()
        if result:
            if not isinstance(self.attributes.get('fulfillments'), Iterable):
                self.attributes['fulfillments'] = []
            self.attributes['fulfillments'].append(fulfillment)

        return result
