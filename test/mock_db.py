class MockDatabase:
    """
    Mocks a DynamoDB with put item operation
    """
    def __init__(self, entries=None):
        if entries is None:
            entries = {}
        self.entries = entries

    def put_item(self, **kwargs):
        """
        Put an item into the mock DB
        :param kwargs: the generic params accepted by the DynamoDB put_item operation
        """
        self.entries.update({kwargs["item"]["uid"]: kwargs["item"]})

    def delete_item(self, **kwargs):
        """
        Delete an item from the mock DB
        :param kwargs: the generic params accepted by the DynamoDB delete_item operation
        """
        try:
            del self.entries[kwargs["item"]]
            return True
        except KeyError:
            return ValueError("Requested key does not exist")

    def get_item(self, **kwargs):
        """
        Get an item from the mock DB
        :param kwargs: the generic params accepted by the DynamoDB get_item operation
        """
        try:
            return self.entries[kwargs["item"]]
        except KeyError:
            return ValueError("Requested key does not exist")
