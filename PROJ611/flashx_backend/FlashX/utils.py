import os
from uuid import uuid1, uuid4


def uuid1_name():
    return str(uuid4()).replace('-', '')[:15]


# save upload file from a POST request and return file name
def upload_file(data, path):
    xt = data.name.split('.')[-1]
    temp = uuid1_name()+'.'+xt
    uploaded_file = open(os.path.join(path, temp), 'wb')
    uploaded_file.write(data.read())
    return [data.name, temp]


def download_file(file_name, path):
    if os.path.exists(os.path.join(path, file_name)):
        file = os.path.join(path, file_name)
        with open(file, 'rb') as f:
            contents = f.read()
        return contents
    else:
        return None


def remove_file(file_name, path):
    file = os.path.join(path, file_name)
    if os.path.exists(file):
        os.remove(file)
        return True
    else:
        return False