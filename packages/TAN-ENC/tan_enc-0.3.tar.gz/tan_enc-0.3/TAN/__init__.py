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
        xor_encrypted = self._xor_encrypt(plaintext)
        base64_encoded = base64.b64encode(xor_encrypted).decode()
        return base64_encoded

    def decrypt(self, encrypted_text: str) -> str:
        base64_decoded = base64.b64decode(encrypted_text)
        return self._xor_decrypt(base64_decoded)
