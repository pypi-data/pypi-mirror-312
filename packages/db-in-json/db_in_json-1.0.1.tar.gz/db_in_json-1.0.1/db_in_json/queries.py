from .files import *
from uuid import uuid4

# Theses queries must be used in a collection class

def insert(self, data):
    """
    Insert data into your collection

    Args:
        data (any): The data you want to insert in your collection

    Returns:
        str: The uuid of your data in your collection
    """
    content = getFileJSON(self.db.file)
    while True:
        uuid = str(uuid4())
        if not (uuid in content[self.name]):
            content[self.name][uuid] = data
            setFileJSON(self.db.file, content)
            return uuid

def delete(self, condition):
    """
    Delete data from your collection based on a condition

    Args:
        condition (function): A function that returns True if the data should be deleted

    Returns:
        int: The number of data items deleted from your collection
    """
    content = getFileJSON(self.db.file)
    deletedCount = 0

    for uuid, data in list(content[self.name].items()):
        if condition(uuid, data):
            content[self.name].pop(uuid)
            deletedCount += 1

    setFileJSON(self.db.file, content)
    return deletedCount

def select(self, condition):
    """
    Select data from your collection based on a condition

    Args:
        condition (function): A function that returns True if the data should be selected

    Returns:
        list: A list formed like [{'uuid': uuid, 'data': data}, ...] (a list containing a dict with keys "uuid" and "data" for each element)
    """
    content = getFileJSON(self.db.file)
    selected_data = []

    for uuid, data in list(content[self.name].items()):
        if condition(uuid, data):
            selected_data.append({'uuid': uuid, 'data': data})

    return selected_data

def update(self, condition, new_data):
    """
    Update data in your collection based on a condition

    Args:
        condition (function): A function that returns True if the data should be updated
        new_data (any): The new data to be inserted in your collection

    Returns:
        int: The number of data items updated in your collection
    """
    content = getFileJSON(self.db.file)
    updatedCount = 0

    for uuid, data in list(content[self.name].items()):
        if condition(uuid, data):
            content[self.name][uuid] = new_data
            updatedCount += 1

    setFileJSON(self.db.file, content)
    return updatedCount
