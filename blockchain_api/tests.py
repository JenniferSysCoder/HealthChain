from django.test import TestCase

from .motor_blockchain.cadena_bloques import BlockChain


class TestMotorBlockchain(TestCase):
    def test_simulacion_financiera(self):
        print("\n" + "=" * 50)
        print(" INICIANDO PRUEBA DEL MOTOR BLOCKCHAIN FINANCIERO")
        print("=" * 50)

        mi_cadena = BlockChain(4, "0")

        print("\n[Paso 1] Creando Bloque Génesis con balance inicial...")
        mi_cadena.create_genesis_with_balance(1000.0, "Cliente_A")
        self.assertEqual(mi_cadena.size(), 1)
        print("✓ Bloque Génesis creado y minado.")

        print("\n[Paso 2] Creando Bloque 1...")
        mi_cadena.create_block()

        print("\n[Paso 3] Añadiendo transacciones (Transferencias)...")
        bloque_actual = mi_cadena.get_last_block()
        bloque_actual.set_transaction_data("Cliente_A", 250.0, "Cliente_B")
        bloque_actual.set_transaction_data("Cliente_B", 50.0, "Cliente_C")
        print("✓ 2 transacciones añadidas al bloque.")

        print("\n[Paso 4] Minando Bloque 1...")
        mi_cadena.mine_block()

        print("\n" + "=" * 50)
        print(" REPORTE FINAL DEL BLOQUE MINADO")
        print("=" * 50)
        print(f"Hash: {bloque_actual.get_hash()}")
        print(mi_cadena.transaction_report(1))

        print("\n--- BALANCES DE CUENTAS ---")
        print(f"Balance Cliente_A: ${mi_cadena.get_balance('Cliente_A')}")
        print(f"Balance Cliente_B: ${mi_cadena.get_balance('Cliente_B')}")
        print(f"Balance Cliente_C: ${mi_cadena.get_balance('Cliente_C')}")

        self.assertEqual(mi_cadena.size(), 2)
        print("\n✓ PRUEBA TÉCNICA SUPERADA CON ÉXITO")
