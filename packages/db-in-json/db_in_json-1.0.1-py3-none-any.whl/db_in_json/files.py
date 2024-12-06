import json
import os

def doesFileExists(path):
    return os.path.isfile(path)

def getRawText(path):
    with open(path) as f:
        return f.read()

def getFileJSON(path):
    with open(path, 'r') as f:
        return json.load(f)

def setFileJSON(path, content):
    with open(path, 'w') as f:
        json.dump(content, f)