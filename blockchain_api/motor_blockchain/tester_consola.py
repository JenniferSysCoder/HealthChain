import json
import sys

from blockchain_api.motor_blockchain.cadena_bloques import BlockChain
from blockchain_api.motor_blockchain.cifrado import Cifrado


def mostrar_menu():
    print("\n" + "=" * 50)
    print("      HEALTHCHAIN TESTER (Consola)")
    print("=" * 50)
    print("1. Iniciar/Crear Blockchain (Genesis)")
    print("2. Crear nuevo bloque")
    print("3. Agregar registro clínico al bloque actual")
    print("4. Minar bloque actual")
    print("5. Consultar historial médico de un paciente")
    print("6. Ver reporte de la cadena de bloques")
    print("0. Salir")
    print("=" * 50)


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
                    input("Carácter clave de minería [Ej: 0]: ").strip().lower()
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
                print("\n[!] Primero debes iniciar la Blockchain (Opción 1).")
                continue

            bc.create_block()
            ultimo = bc.get_last_block()
            print("\n[+] Nuevo bloque creado:")
            print(f"    ID: {ultimo.get_id()}")
            print(f"    Timestamp: {ultimo.time_stamp}")
            print(f"    Previous Hash: {ultimo.get_previous_hash()}")
            bloque_creado = True
            transaccion_agregada = False

        elif opcion == "3":
            if not bc or not bloque_creado:
                print(
                    "\n[!] Debes crear un bloque antes de agregar registros (Opción 2)."
                )
                continue

            entidad = input("Entidad Emisora (Hospital/Lab): ").strip().upper()
            paciente = input("ID del Paciente (Pasaporte/DUI): ").strip().upper()
            categoria = input("Categoría (Ej: Emergencia, Vacuna): ").strip().upper()

            print("\n[ Ingreso de Datos Clínicos ]")
            nombre = input("Nombre completo del paciente: ").strip()
            tipo_sangre = input("Tipo de Sangre y Rh [Ej: O+]: ").strip()
            alergias = input("Alergias severas [Ej: Penicilina]: ").strip()
            vacunas = input(
                "Vacunas internacionales [Ej: Covid, Fiebre Amarilla]: "
            ).strip()
            cronicas = input("Enfermedades crónicas [Ej: Asma]: ").strip()

            paquete_vital = {
                "nombre": nombre,
                "tipo_sangre": tipo_sangre,
                "alergias": alergias,
                "vacunas": vacunas,
                "cronicas": cronicas,
            }
            texto_plano = json.dumps(paquete_vital)

            # La clave será única por paciente
            llave_paciente = "clave_" + paciente.lower()

            try:
                motor_cifrado = Cifrado(llave_paciente)
                datos_cifrados = motor_cifrado.encriptar(texto_plano)

                if not datos_cifrados:
                    print(
                        "\n[!] Error: El módulo de cifrado falló al procesar los datos."
                    )
                    continue

                bc.get_last_block().set_registro_clinico(
                    entidad, paciente, categoria, datos_cifrados
                )
                print("\n[+] Registro clínico agregado y cifrado exitosamente.")
                transaccion_agregada = True
            except Exception as e:
                print(f"\n[!] Error al inyectar al bloque: {e}")

        elif opcion == "4":
            if not bc or not transaccion_agregada:
                print(
                    "\n[!] Debes agregar al menos un registro antes de minar (Opción 3)."
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
                print("\n[!] Primero debes iniciar la Blockchain (Opción 1).")
                continue

            cliente = input("ID del paciente a consultar: ").strip().upper()
            historial = bc.get_historial_paciente(cliente)

            print(
                f"\n[*] Historial médico para '{cliente}': {len(historial)} evento(s) encontrado(s)."
            )

            if len(historial) > 0:
                # Reconstruimos la llave del paciente para descifrar
                llave_paciente = "clave_" + cliente.lower()
                motor_cifrado = Cifrado(llave_paciente)

                for reg in historial:
                    print(f"\n    --- Registro ID: {reg.get_id()} ---")
                    print(f"    Categoría:    {reg.get_categoria()}")
                    print(f"    Hospital/Lab: {reg.get_entidad_emisora()}")
                    print(
                        f"    Hash Cifrado: {reg.get_datos_cifrados()[:40]}... (oculto)"
                    )

                    # ¡Aquí ocurre la magia de descifrar!
                    datos_descifrados = motor_cifrado.desencriptar(
                        reg.get_datos_cifrados()
                    )

                    if datos_descifrados:
                        try:
                            # Parseamos el JSON para imprimirlo con etiquetas claras
                            datos = json.loads(datos_descifrados)
                            print("    [+] Datos Médicos Revelados:")
                            print(
                                f"        - Paciente:              {datos.get('nombre', 'N/A')}"
                            )
                            print(
                                f"        - Tipo de Sangre:        {datos.get('tipo_sangre', 'N/A')}"
                            )
                            print(
                                f"        - Alergias Detectadas:   {datos.get('alergias', 'N/A')}"
                            )
                            print(
                                f"        - Vacunas Aplicadas:     {datos.get('vacunas', 'N/A')}"
                            )
                            print(
                                f"        - Enfermedades Crónicas: {datos.get('cronicas', 'N/A')}"
                            )
                        except json.JSONDecodeError:
                            print(f"    [+] Datos (Texto plano): {datos_descifrados}")
                    else:
                        print(
                            "    [!] Fallo de seguridad: No se pudo descifrar el registro."
                        )

        elif opcion == "6":
            if not bc:
                print("\n[!] Primero debes iniciar la Blockchain (Opción 1).")
                continue

            print("\n" + "=" * 50)
            print("         REPORTE DE LA CADENA DE BLOQUES")
            print("=" * 50)
            for i in range(bc.size()):
                blk = bc.get_block(i)
                print(f"Block ID: {blk.get_id()}")
                print(bc.registro_report(i))
                print("-" * 50)

        elif opcion == "0":
            print("\nSaliendo del tester...")
            sys.exit(0)

        else:
            print("\nOpción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    ejecutor_tester()
