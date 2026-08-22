import sys
from blockchain_api.motor_blockchain.cadena_bloques import BlockChain


def mostrar_menu():
    print("\n" + "=" * 45)
    print("      BLOCKCHAIN TESTER (Consola)")
    print("=" * 45)
    print("1. Iniciar/Crear Blockchain (Genesis)")
    print("2. Crear nuevo bloque")
    print("3. Agregar transacción al bloque actual")
    print("4. Minar bloque actual")
    print("5. Consultar balance de un usuario")
    print("6. Ver historial de transacciones / bloques")
    print("0. Salir")
    print("=" * 45)


def ejecutor_tester():
    bc = None
    bloque_creado = False
    transaccion_agregada = False

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                complejidad = int(
                    input("Nivel de complejidad de minería (1-6) [Ej: 4]: ")
                )
                caracter_clave = (
                    input("Carácter clave de minería [Ej: 0]: ")
                    .strip()
                    .lower()
                )
                if not caracter_clave:
                    caracter_clave = "0"

                # Instanciamos la clase BlockChain real
                bc = BlockChain(complejidad, caracter_clave)
                bc.create_genesis()
                genesis = bc.get_last_block()

                print("\n[+] Blockchain iniciada con éxito.")
                print(f"    Genesis Block Hash: {genesis.get_hash()}")
                print(f"    Timestamp: {genesis.time_stamp}")
                bloque_creado = False
                transaccion_agregada = False
            except Exception as e:
                print(f"\n[!] Error al iniciar la blockchain: {e}")

        elif opcion == "2":
            if not bc:
                print(
                    "\n[!] Primero debes iniciar la Blockchain (Opción 1)."
                )
                continue

            bc.create_block()
            ultimo = bc.get_last_block()
            print(f"\n[+] Nuevo bloque creado:")
            print(f"    ID: {ultimo.get_id()}")
            print(f"    Timestamp: {ultimo.time_stamp}")
            print(f"    Previous Hash: {ultimo.get_previous_hash()}")
            bloque_creado = True
            transaccion_agregada = False

        elif opcion == "3":
            if not bc or not bloque_creado:
                print(
                    "\n[!] Debes crear un bloque antes de agregar transacciones (Opción 2)."
                )
                continue

            sender = input("Sender (Emisor): ").strip().upper()
            receiver = input("Receiver (Receptor): ").strip().upper()
            try:
                amount = float(input("Amount (Monto): ").strip())
                # Usamos el método set_transaction_data de tu clase Bloque
                bc.get_last_block().set_transaction_data(
                    sender, amount, receiver
                )
                print(
                    f"\n[+] Transacción agregada: {sender} -> {receiver} (${amount})"
                )
                transaccion_agregada = True
            except ValueError:
                print("\n[!] Error: El monto debe ser un número válido.")

        elif opcion == "4":
            if not bc or not transaccion_agregada:
                print(
                    "\n[!] Debes agregar al menos una transacción antes de minar (Opción 3)."
                )
                continue

            print("\n[...] Minando bloque, por favor espera...")
            bc.mine_block()
            minado = bc.get_last_block()

            print("\n[--- Bloque Minado con Éxito ---]")
            print(f"    Nonce: {minado.get_nonce()}")
            print(f"    Hash:  {minado.get_hash()}")

            bloque_creado = False
            transaccion_agregada = False

        elif opcion == "5":
            if not bc:
                print(
                    "\n[!] Primero debes iniciar la Blockchain (Opción 1)."
                )
                continue

            cliente = input("Nombre del usuario/cliente: ").strip().upper()
            balance = bc.get_balance(cliente)
            print(f"\n[*] Balance para '{cliente}': ${balance}")

        elif opcion == "6":
            if not bc:
                print(
                    "\n[!] Primero debes iniciar la Blockchain (Opción 1)."
                )
                continue

            print("\n" + "=" * 50)
            print("         REPORTE DE LA CADENA DE BLOQUES")
            print("=" * 50)
            for i in range(bc.size()):
                blk = bc.get_block(i)
                print(f"Block ID: {blk.get_id()}")
                print(bc.transaction_report(i))
                print("-" * 50)

        elif opcion == "0":
            print("\nSaliendo del tester...")
            sys.exit(0)

        else:
            print("\nOpción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    ejecutor_tester()