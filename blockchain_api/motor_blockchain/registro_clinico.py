import time


class RegistroClinico:
    def __init__(self, pId, pEntidad, pPaciente, pCategoria, pDatosCifrados):
        self.id = pId
        self.time_stamp = int(time.time() * 1000)
        self.entidad_emisora = pEntidad
        self.paciente_id = pPaciente
        self.categoria = pCategoria
        self.datos_cifrados = pDatosCifrados

    def to_string(self):
        return (
            str(self.id)
            + str(self.time_stamp)
            + self.entidad_emisora
            + self.paciente_id
            + self.categoria
            + self.datos_cifrados
        )

    def get_id(self):
        return self.id

    def get_time_stamp(self):
        return self.time_stamp

    def get_entidad_emisora(self):
        return self.entidad_emisora

    def get_paciente_id(self):
        return self.paciente_id

    def get_categoria(self):
        return self.categoria

    def get_datos_cifrados(self):
        return self.datos_cifrados
