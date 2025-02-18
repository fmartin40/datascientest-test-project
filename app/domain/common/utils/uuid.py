import hashlib
import time

def generate_unique_id():
    timestamp = str(time.time()).encode('utf-8')
    return hashlib.sha256(timestamp).hexdigest()
