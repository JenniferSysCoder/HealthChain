"""
Suite de pruebas para el proyecto HealthChain (blockchain médica).

Cómo correrlas:
    1. Activa tu venv (ya lo tienes activo en tu terminal).
    2. pip install pytest   (si no lo tienes ya instalado)
    3. Desde la RAÍZ del proyecto (proyecto_medico_bc), corre:
           pytest -v

Requiere que existan blockchain_api/__init__.py y
blockchain_api/motor_blockchain/__init__.py (aunque estén vacíos),
para que los imports relativos funcionen.
"""

import pytest

from blockchain_api.motor_blockchain.cadena_bloques import BlockChain
from blockchain_api.motor_blockchain.cifrado import Cifrado
from blockchain_api.motor_blockchain.sha256 import SHA256

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def bc():
    """Blockchain nueva, con complejidad baja (2) para que los tests corran rápido."""
    chain = BlockChain(2, "0")
    chain.create_genesis()
    return chain


# ---------------------------------------------------------------------------
# 1. Bloque génesis
# ---------------------------------------------------------------------------


class TestGenesis:
    def test_genesis_se_crea_correctamente(self, bc):
        assert bc.size() == 1
        genesis = bc.get_last_block()
        assert genesis.get_id() == 0
        assert genesis.get_hash() is not None

    def test_no_se_puede_crear_genesis_dos_veces(self, bc):
        # Ya hay un génesis (por el fixture); un segundo intento debe fallar
        assert bc.create_genesis() is False
        assert bc.size() == 1

    def test_genesis_cumple_la_dificultad(self, bc):
        genesis = bc.get_last_block()
        assert genesis.get_hash()[: bc.complexity] == bc.proof_of_work


# ---------------------------------------------------------------------------
# 2. Minería / prueba de trabajo
# ---------------------------------------------------------------------------


class TestMineria:
    def test_bloque_minado_tiene_hash_valido(self, bc):
        bc.create_block()
        bc.get_last_block().set_registro_clinico(
            "HOSPITAL_X", "P001", "CONSULTA", "cifrado_falso"
        )
        bc.mine_block()
        nuevo = bc.get_last_block()
        assert nuevo.get_hash() is not None
        assert nuevo.get_hash()[: bc.complexity] == bc.proof_of_work

    def test_get_proof_of_work_over_block_detecta_bloque_valido(self, bc):
        assert bc.get_proof_of_work_over_block(bc.get_last_block()) is True

    def test_previous_hash_del_nuevo_bloque_coincide_con_el_anterior(self, bc):
        hash_genesis = bc.get_last_block().get_hash()
        bc.create_block()
        nuevo = bc.get_last_block()
        assert nuevo.get_previous_hash() == hash_genesis


# ---------------------------------------------------------------------------
# 3. Integridad de la cadena (is_chain_valid)
# ---------------------------------------------------------------------------


class TestIntegridadCadena:
    def test_cadena_recien_creada_es_valida(self, bc):
        bc.create_block()
        bc.get_last_block().set_registro_clinico(
            "HOSPITAL_X", "P001", "CONSULTA", "abc"
        )
        bc.mine_block()

        es_valida, motivo = bc.is_chain_valid()
        assert es_valida is True

    def test_alterar_un_registro_invalida_la_cadena(self, bc):
        bc.create_block()
        bc.get_last_block().set_registro_clinico(
            "HOSPITAL_X", "P001", "CONSULTA", "abc"
        )
        bc.mine_block()

        # Alteramos el contenido del bloque DESPUÉS de minado
        registro = bc.get_last_block().get_registro(0)
        registro.categoria = "DATO_MANIPULADO"

        es_valida, motivo = bc.is_chain_valid()
        assert es_valida is False

    def test_romper_el_encadenamiento_invalida_la_cadena(self, bc):
        bc.create_block()
        bc.get_last_block().set_registro_clinico(
            "HOSPITAL_X", "P001", "CONSULTA", "abc"
        )
        bc.mine_block()

        # Rompemos el enlace manualmente, simulando un bloque insertado a la fuerza
        bc.get_last_block().previous_hash = "hash_falso_inventado"

        es_valida, motivo = bc.is_chain_valid()
        assert es_valida is False

    def test_cadena_vacia_no_es_valida(self):
        chain_vacia = BlockChain(2, "0")
        es_valida, motivo = chain_vacia.is_chain_valid()
        assert es_valida is False


# ---------------------------------------------------------------------------
# 4. add_proved_block: rechazo de bloques adulterados
# ---------------------------------------------------------------------------


class TestAddProvedBlock:
    def test_rechaza_bloque_con_hash_que_no_corresponde(self, bc):
        bc.create_block()
        bloque_falso = bc.get_last_block()
        bloque_falso.set_registro_clinico("HOSPITAL_X", "P001", "CONSULTA", "abc")
        # Le asignamos un hash/nonce inventado, sin minarlo de verdad
        bloque_falso.nonce = 123
        bloque_falso.hash = "hash_inventado_no_valido"

        assert bc.add_proved_block(bloque_falso) is False

    def test_acepta_bloque_correctamente_minado(self, bc):
        otra_chain = BlockChain(2, "0")
        otra_chain.create_genesis()
        otra_chain.create_block()
        otra_chain.get_last_block().set_registro_clinico(
            "HOSPITAL_X", "P002", "VACUNA", "xyz"
        )
        otra_chain.mine_block()
        bloque_valido = otra_chain.get_last_block()

        # Lo agregamos a una cadena nueva (independiente) que no lo tiene aún
        chain_receptora = BlockChain(2, "0")
        chain_receptora.create_genesis()
        assert chain_receptora.add_proved_block(bloque_valido) is True

    def test_rechaza_bloque_duplicado(self, bc):
        bc.create_block()
        bc.get_last_block().set_registro_clinico(
            "HOSPITAL_X", "P001", "CONSULTA", "abc"
        )
        bc.mine_block()
        bloque_existente = bc.get_last_block()

        # Intentar agregar un bloque con el mismo id que ya existe en la cadena
        assert bc.add_proved_block(bloque_existente) is False


# ---------------------------------------------------------------------------
# 5. Cifrado / descifrado de datos clínicos
# ---------------------------------------------------------------------------


class TestCifrado:
    def test_encriptar_y_desencriptar_da_el_texto_original(self):
        motor = Cifrado("clave_p001")
        texto_original = '{"nombre": "Juan Perez", "tipo_sangre": "O+"}'

        cifrado = motor.encriptar(texto_original)
        assert cifrado is not None
        assert cifrado != texto_original

        descifrado = motor.desencriptar(cifrado)
        assert descifrado == texto_original

    def test_desencriptar_con_llave_incorrecta_no_revienta_y_falla_controladamente(
        self,
    ):
        motor_correcto = Cifrado("clave_p001")
        cifrado = motor_correcto.encriptar("datos sensibles del paciente")

        motor_incorrecto = Cifrado("clave_p002_otra_llave")
        resultado = motor_incorrecto.desencriptar(cifrado)

        # No debe lanzar excepción; debe regresar None de forma controlada
        assert resultado is None

    def test_mismo_texto_plano_con_la_misma_llave_da_el_mismo_cifrado(self):
        # NOTA: esto documenta el comportamiento actual de AES-ECB (determinista).
        # Es justamente la debilidad de seguridad mencionada: dos registros
        # iguales generan el mismo texto cifrado, lo cual filtra información
        # (patrones repetidos). Se recomienda migrar a AES-CBC o AES-GCM con IV
        # aleatorio para que este test deje de cumplirse.
        motor = Cifrado("clave_p001")
        texto = "mismo contenido"
        assert motor.encriptar(texto) == motor.encriptar(texto)


# ---------------------------------------------------------------------------
# 6. Historial médico del paciente
# ---------------------------------------------------------------------------


class TestHistorialPaciente:
    def test_historial_vacio_si_paciente_no_existe(self, bc):
        historial = bc.get_historial_paciente("PACIENTE_INEXISTENTE")
        assert historial == []

    def test_historial_recupera_registros_de_varios_bloques(self, bc):
        bc.create_block()
        bc.get_last_block().set_registro_clinico(
            "HOSPITAL_A", "P001", "EMERGENCIA", "c1"
        )
        bc.mine_block()

        bc.create_block()
        bc.get_last_block().set_registro_clinico("HOSPITAL_B", "P001", "VACUNA", "c2")
        bc.get_last_block().set_registro_clinico("HOSPITAL_B", "P999", "VACUNA", "c3")
        bc.mine_block()

        historial_p001 = bc.get_historial_paciente("P001")
        assert len(historial_p001) == 2
        categorias = {r.get_categoria() for r in historial_p001}
        assert categorias == {"EMERGENCIA", "VACUNA"}


# ---------------------------------------------------------------------------
# 7. SHA256 (utilitario base)
# ---------------------------------------------------------------------------


class TestSHA256:
    def test_hash_es_deterministico(self):
        assert SHA256.generate_hash("hola") == SHA256.generate_hash("hola")

    def test_hash_cambia_con_el_contenido(self):
        assert SHA256.generate_hash("hola") != SHA256.generate_hash("hola.")

    def test_hash_tiene_64_caracteres_hex(self):
        h = SHA256.generate_hash("cualquier texto")
        assert len(h) == 64
        int(h, 16)  # no debe lanzar error: debe ser hexadecimal válido
