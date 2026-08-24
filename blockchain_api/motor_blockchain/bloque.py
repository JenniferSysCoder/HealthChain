import time

from .registro_clinico import RegistroClinico


class Bloque:
    def __init__(self, pId=-1, pPrevHash=None):
        self.id = pId
        self.time_stamp = int(time.time() * 1000)
        self.previous_hash = pPrevHash
        self.a_registros = []
        self.nonce = -1
        self.hash = None

    def register(self, pNonce, pHash):
        if self.id > -1 and self.nonce < 0 and self.hash is None:
            self.nonce = pNonce
            self.hash = pHash
            return True
        return False

    def set_registro_clinico(self, pEntidad, pPaciente, pCategoria, pDatosCifrados):
        self.a_registros.append(
            RegistroClinico(
                len(self.a_registros), pEntidad, pPaciente, pCategoria, pDatosCifrados
            )
        )

    def set_registro_obj(self, pReg):
        self.a_registros.append(
            RegistroClinico(
                len(self.a_registros),
                pReg.get_entidad_emisora(),
                pReg.get_paciente_id(),
                pReg.get_categoria(),
                pReg.get_datos_cifrados(),
            )
        )

    def get_registro(self, pId):
        return self.a_registros[pId]

    def count_registros(self):
        return len(self.a_registros)

    def get_id(self):
        return self.id

    def get_nonce(self):
        return self.nonce

    def get_hash(self):
        return self.hash

    def get_previous_hash(self):
        return self.previous_hash

    def to_string(self):
        sCad = str(self.id) + str(self.time_stamp) + str(self.previous_hash)
        for reg in self.a_registros:
            sCad += reg.to_string()
        return sCad
