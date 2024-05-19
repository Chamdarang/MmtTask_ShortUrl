import hashlib
import base64
from os import urandom

# 구현 혹은 shortuuid패키지 사용
def url_encode(url: str):
    salt = urandom(32)
    hash_str = hashlib.sha256(url.encode()+salt).digest() # (가능한)안겹치는 유일한 값을 위해 해싱
    b64_str = base64.urlsafe_b64encode(hash_str).decode("utf-8").rstrip("=") # urlsafe
    return b64_str[:10] # 짧게 잘라서 리턴
