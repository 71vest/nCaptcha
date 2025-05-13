from core.imports import Cipher, algorithms, modes, default_backend, os, base64, hmac, hashlib

class obfuscator:
    def __init__(self, key: bytes):
        self.key      = key
        self.hmac_key = key[:16]

    def obfuscate(self, id: str) -> str:
        iv        = os.urandom(16)
        cipher    = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        encrypted = cipher.encryptor().update(id.encode()) + cipher.encryptor().finalize()
        data      = iv + encrypted
        sig       = hmac.new(self.hmac_key, data, hashlib.sha256).digest()

        return base64.urlsafe_b64encode(data + sig).decode()

    def deobfuscate(self, encoded: str) -> str:
        try:
            decoded   = base64.urlsafe_b64decode(encoded.encode())
            data, sig = decoded[:-32], decoded[-32:]

            expected_sig  = hmac.new(self.hmac_key, data, hashlib.sha256).digest()
            if not hmac.compare_digest(expected_sig, sig):
                return None

            iv, encrypted = data[:16], data[16:]
            cipher        = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
            decrypted     = cipher.decryptor().update(encrypted) + cipher.decryptor().finalize()
            return decrypted.decode()
        
        except Exception:
            return None
