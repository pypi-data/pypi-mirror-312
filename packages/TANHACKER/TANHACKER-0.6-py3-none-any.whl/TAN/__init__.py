import base64

class tanenc:
    def __init__(self, key: str):
        self.key = key

    def _xor_encrypt(self, data: str) -> bytes:
        key_bytes = self.key.encode()
        return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data.encode())])

    def _xor_decrypt(self, data: bytes) -> str:
        key_bytes = self.key.encode()
        return ''.join(chr(b ^ key_bytes[i % len(key_bytes)]) for i, b in enumerate(data))

    def encrypt(self, plaintext: str) -> str:
        f = input('SAVEFILE: ')
        xor_encrypted = self._xor_encrypt(plaintext)
        base64_encoded = base64.b64encode(xor_encrypted).decode()
        b = f'''importTAN 
t = {base64_encoded!r}
r = {self.key!r}
w = TAN.tanenc(r)
exec(compile(code:=w.decrypt(t), filename="", mode="exec"))'''
        with open(f'TAN_{f}','w') as j:
            j.write(b)
        return base64_encoded

    def decrypt(self, encrypted_text: str) -> str:
        base64_decoded = base64.b64decode(encrypted_text)
        return self._xor_decrypt(base64_decoded)
