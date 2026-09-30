import requests

MC_URL_BASE = "http://127.0.0.1:5000/tareas"


def MC_mostrar_menu():
    print("\n" + "=" * 45)
    print("       SISTEMA DE SEGUIMIENTO DE TAREAS")
    print("=" * 45)
    print("1. Listar tareas (todas o por RUT)")
    print("2. Crear nueva tarea")
    print("3. Editar título y descripción de una tarea")
    print("4. Marcar tarea como completada")
    print("5. Eliminar tarea")
    print("6. Salir")
    return input("Seleccione una opción (1-6): ").strip()


def MC_listar_tareas():
    MC_rut = input("Ingrese RUT a filtrar (presione Enter para ver todas): ").strip()
    MC_params = {"rut": MC_rut} if MC_rut else {}

    try:
        MC_respuesta = requests.get(MC_URL_BASE, params=MC_params)
        if MC_respuesta.status_code == 200:
            MC_datos = MC_respuesta.json().get("tareas", [])
            if not MC_datos:
                print("\n[!] No existen tareas registradas.")
                return

            print(f"\nSe encontraron {len(MC_datos)} tarea(s):")
            for MC_t in MC_datos:
                MC_check = "[X] Completada" if MC_t["completada"] else "[ ] Pendiente"
                print("-" * 50)
                print(f"ID         : {MC_t['id']}")
                print(f"RUT Usuario: {MC_t['rut']}")
                print(f"Estado     : {MC_check}")
                print(f"Título     : {MC_t['titulo']}")
                print(f"Descripción: {MC_t['descripcion']}")
            print("-" * 50)
        else:
            print("Error:", MC_respuesta.json().get("error", "Error inesperado"))
    except requests.exceptions.ConnectionError:
        print("[!] No se pudo conectar con el microservicio Flask.")


def MC_crear_tarea():
    print("\n--- Nueva Tarea ---")
    MC_rut = input("RUT del usuario (ej: 12345678-9): ").strip()
    MC_titulo = input("Título de la tarea: ").strip()
    MC_descripcion = input("Descripción: ").strip()

    if not MC_rut or not MC_titulo:
        print("[!] El RUT y el título son campos obligatorios.")
        return

    MC_cuerpo = {
        "rut": MC_rut,
        "titulo": MC_titulo,
        "descripcion": MC_descripcion
    }

    try:
        MC_respuesta = requests.post(MC_URL_BASE, json=MC_cuerpo)
        if MC_respuesta.status_code == 201:
            print(f"[OK] {MC_respuesta.json().get('mensaje')}")
        else:
            print("[!] Error:", MC_respuesta.json().get("error"))
    except requests.exceptions.ConnectionError:
        print("[!] No se pudo conectar con el microservicio Flask.")


def MC_editar_tarea():
    print("\n--- Editar Tarea ---")
    MC_id = input("Ingrese el ID de la tarea a modificar: ").strip()
    MC_titulo = input("Nuevo título (deje vacío para no modificar): ").strip()
    MC_descripcion = input("Nueva descripción (deje vacío para no modificar): ").strip()

    MC_cuerpo = {}
    if MC_titulo:
        MC_cuerpo["titulo"] = MC_titulo
    if MC_descripcion:
        MC_cuerpo["descripcion"] = MC_descripcion

    if not MC_cuerpo:
        print("[!] No ingresó ningún campo para actualizar.")
        return

    try:
        MC_respuesta = requests.put(f"{MC_URL_BASE}/{MC_id}", json=MC_cuerpo)
        if MC_respuesta.status_code == 200:
            print(f"[OK] {MC_respuesta.json().get('mensaje')}")
        else:
            print("[!] Error:", MC_respuesta.json().get("error"))
    except requests.exceptions.ConnectionError:
        print("[!] No se pudo conectar con el microservicio Flask.")


def MC_marcar_completada():
    print("\n--- Marcar Tarea como Completada ---")
    MC_id = input("Ingrese el ID de la tarea: ").strip()
    if not MC_id:
        print("[!] Debe ingresar un ID.")
        return

    try:
        MC_respuesta = requests.put(f"{MC_URL_BASE}/{MC_id}", json={"completada": True})
        if MC_respuesta.status_code == 200:
            print(f"[OK] {MC_respuesta.json().get('mensaje')}")
        else:
            print("[!] Error:", MC_respuesta.json().get("error"))
    except requests.exceptions.ConnectionError:
        print("[!] No se pudo conectar con el microservicio Flask.")


def MC_eliminar_tarea():
    print("\n--- Eliminar Tarea ---")
    MC_id = input("Ingrese el ID de la tarea a eliminar: ").strip()
    if not MC_id:
        print("[!] Debe ingresar un ID.")
        return

    try:
        MC_respuesta = requests.delete(f"{MC_URL_BASE}/{MC_id}")
        if MC_respuesta.status_code == 200:
            print(f"[OK] {MC_respuesta.json().get('mensaje')}")
        else:
            print("[!] Error:", MC_respuesta.json().get("error"))
    except requests.exceptions.ConnectionError:
        print("[!] No se pudo conectar con el microservicio Flask.")


def MC_ejecutar_cliente():
    while True:
        MC_opcion = MC_mostrar_menu()
        if MC_opcion == '1':
            MC_listar_tareas()
        elif MC_opcion == '2':
            MC_crear_tarea()
        elif MC_opcion == '3':
            MC_editar_tarea()
        elif MC_opcion == '4':
            MC_marcar_completada()
        elif MC_opcion == '5':
            MC_eliminar_tarea()
        elif MC_opcion == '6':
            print("\nSaliendo del cliente.")
            break
        else:
            print("\n[!] Opción no válida. Intente nuevamente.")


if __name__ == '__main__':
    MC_ejecutar_cliente()
