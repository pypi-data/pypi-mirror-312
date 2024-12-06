from .files import *
from .queries import *

class DB(object):
    def __init__(self, file):
        """
        The DB object, linked to your JSON file

        Args:
            file (str): The JSON file containing your DB
        """
        assert type(file) == str, 'Your file path is not a string'
        self.file = file
        if not doesFileExists(file):
            with open(file, 'x') as f:
                f.write('{}')
        elif getRawText(file) == '':
            setFileJSON(file, {})

    def purge(self):
        """
        Purge the DB
        """
        setFileJSON(self.file, {})

    def getCollection(self, name):
        """
        Get the collection object, create the collection if does'nt exists

        Args:
            name (str): The name of the collection

        Returns:
            collection: The collection object
        """
        return self.collection(self, name)

    class collection(object):
        def __init__(self, db, name):
            """
            Initialize the collection object.

            Args:
                db (DB): The DB object to which this collection belongs.
                name (str): The name of the collection.
            """
            self.db = db
            self.name = name
            self.queries = {
                'insert': lambda data: insert(self, data),
                'delete': lambda condition: delete(self, condition),
                'select': lambda condition: select(self, condition),
                'update': lambda condition, data: update(self, condition, data)
            }

            content = getFileJSON(self.db.file)
            if not (name in content):
                content[name] = {}
                setFileJSON(self.db.file, content)

        def remove(self):
            """
            Remove your collection from the DB
            """
            content = getFileJSON(self.db.file)
            if self.name in content:
                content.pop(self.name)
            setFileJSON(self.db.file, content)

        def purge(self):
            """
            Remove all the content of the collection
            """
            content = getFileJSON(self.db.file)
            if self.name in content:
                content[self.name] = {}
            setFileJSON(self.db.file, content)