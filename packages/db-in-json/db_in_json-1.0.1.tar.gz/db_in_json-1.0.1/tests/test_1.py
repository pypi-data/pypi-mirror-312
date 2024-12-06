import os
from db_in_json.main import DB

def test_1():
    db = DB('temp-DB.json')
    test = db.getCollection('test')
    inserted_uuid = test.queries['insert']('Some great data')
    selected_items = test.queries['select'](lambda uuid, data: True)

    assert inserted_uuid != None
    assert len(selected_items) == 1
    assert selected_items[0]['uuid'] == inserted_uuid

    test.queries['update'](lambda uuid, data: uuid == inserted_uuid, 'Another great data')
    selected_items = test.queries['select'](lambda uuid, data: uuid == inserted_uuid)

    assert selected_items[0]['data'] == 'Another great data'

    test.queries['delete'](lambda uuid, data: uuid == inserted_uuid)

    assert test.queries['select'](lambda uuid, data: True) == []

    os.remove('temp-DB.json')