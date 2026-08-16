import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Cifrado:
    def __init__(self, pClave):
        try:
            hash_sha1 = hashlib.sha1(pClave.encode("utf-8")).digest()
            # Ajuste a 32 bytes para AES-256
            self.llave = hash_sha1.ljust(32, b"\0")[:32]

            self.o_cifrado = AES.new(self.llave, AES.MODE_ECB)
            self.o_descifrado = AES.new(self.llave, AES.MODE_ECB)
        except Exception:
            pass

    def cifrar_bloque(self, pBlk):
        try:
            pBlk.to_string()
            return
        except Exception:
            return

    def encriptar(self, pCadena):
        try:
            cipher = AES.new(self.llave, AES.MODE_ECB)
            ct_bytes = cipher.encrypt(pad(pCadena.encode("utf-8"), AES.block_size))
            return base64.b64encode(ct_bytes).decode("utf-8")
        except Exception:
            return None

    def desencriptar(self, pCadena):
        try:
            cipher = AES.new(self.llave, AES.MODE_ECB)
            ct_bytes = base64.b64decode(pCadena)
            pt_bytes = unpad(cipher.decrypt(ct_bytes), AES.block_size)
            return pt_bytes.decode("utf-8")
        except Exception:
            return None
