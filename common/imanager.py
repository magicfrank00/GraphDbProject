from abc import ABC


class Manager(ABC):
    def name(self):
        pass

    def order(self, retailer_id, product_id):
        pass

    def drop(self, id, label):
        pass
