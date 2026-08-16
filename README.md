# HealthChain - API para Historial Médico con Blockchain

Este es un motor de Blockchain creado en Python usando Django. El objetivo del proyecto es guardar expedientes médicos de forma segura para que no puedan ser alterados. Usamos métodos de encriptación para asegurar que los diagnósticos y los datos de las consultas se mantengan privados entre el médico y el paciente.

Proyecto desarrollado por el equipo NinjaCode.

## Tecnologías que usamos

* Lenguaje principal: Python 3
* Backend y API: Django y Django REST Framework (DRF)
* Base de Datos: PostgreSQL
* Frontend: React con Vite
* Seguridad: Encriptación AES y SHA-256 (PyCryptodome)

## Lo que hace el sistema

* Minería de bloques: Un sistema de "Prueba de Trabajo" (PoW) que se encarga de validar y guardar los nuevos registros médicos.
* Privacidad de datos: Ocultamos el texto de los diagnósticos y tratamientos usando cifrado AES para que nadie sin autorización pueda leerlos.
* Historial seguro: Un registro de todas las consultas que recibe el paciente a lo largo del tiempo, el cual no se puede borrar ni modificar.
* Código ordenado: El sistema está dividido en módulos claros (Transacciones, Bloques, Cifrado) para que el código sea fácil de leer y mantener.

## Equipo NinjaCode

* Jennifer Tatiana Guerra Figueroa
* Gilberto José Menéndez Pérez
* Daniel Alexander Reyes Pérez

## Cómo probar el código

Incluimos un script de simulación para comprobar que el sistema genera los hashes correctamente, encripta la información del médico y mina el bloque sin errores. Para correr la prueba en tu computadora, solo tienes que ejecutar este comando en la terminal:

```bash
python manage.py test blockchain_api