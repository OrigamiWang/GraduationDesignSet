import hashlib



def md5(key):
    md5 = hashlib.md5()
    md5.update(key.encode('utf-8'))
    return md5.hexdigest()

