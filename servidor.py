from flask import Flask, request, jsonify
from pymongo import MongoClient, ReturnDocument

MC_app = Flask(__name__)

# Conexión a MongoDB local
MC_cliente_mongo = MongoClient("mongodb://localhost:27017/")
MC_db = MC_cliente_mongo["gestion_tareas_db"]
MC_coleccion = MC_db["tareas"]
MC_contadores = MC_db["contadores"]


def MC_obtener_siguiente_id():
    """Genera un ID correlativo atómico formateado a 4 dígitos (0001, 0002, ...)."""
    MC_doc_contador = MC_contadores.find_one_and_update(
        {"_id": "tarea_id"},
        {"$inc": {"secuencia": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    MC_numero = MC_doc_contador["secuencia"]
    return f"{MC_numero:04d}"


def MC_formatear_tarea(MC_doc):
    """Convierte el documento BSON en un diccionario legible."""
    return {
        "id": MC_doc["_id"],
        "rut": MC_doc.get("rut", ""),
        "titulo": MC_doc.get("titulo", ""),
        "descripcion": MC_doc.get("descripcion", ""),
        "completada": MC_doc.get("completada", False)
    }


# 1. CREACIÓN: Agregar nueva tarea con ID correlativo (POST /tareas)
@MC_app.route('/tareas', methods=['POST'])
def MC_crear_tarea():
    MC_datos = request.get_json(silent=True) or {}
    MC_rut = MC_datos.get('rut', '').strip()
    MC_titulo = MC_datos.get('titulo', '').strip()
    MC_descripcion = MC_datos.get('descripcion', '').strip()

    if not MC_rut or not MC_titulo:
        return jsonify({"error": "El RUT y el título son obligatorios."}), 400

    MC_nuevo_id = MC_obtener_siguiente_id()

    MC_nueva_tarea = {
        "_id": MC_nuevo_id,
        "rut": MC_rut,
        "titulo": MC_titulo,
        "descripcion": MC_descripcion,
        "completada": False
    }

    MC_coleccion.insert_one(MC_nueva_tarea)

    return jsonify({
        "mensaje": "Tarea creada exitosamente",
        "tarea": MC_formatear_tarea(MC_nueva_tarea)
    }), 201


# 2. LISTADO: Obtener todas las tareas o filtrar por RUT (GET /tareas)
@MC_app.route('/tareas', methods=['GET'])
def MC_listar_tareas():
    MC_rut_filtro = request.args.get('rut')
    MC_filtro = {"rut": MC_rut_filtro} if MC_rut_filtro else {}

    MC_cursor = MC_coleccion.find(MC_filtro).sort("_id", 1)
    MC_lista_tareas = [MC_formatear_tarea(MC_doc) for MC_doc in MC_cursor]

    return jsonify({"tareas": MC_lista_tareas}), 200


# 3. ACTUALIZACIÓN: Modificar campos usando el ID formateado (PUT /tareas/<id>)
@MC_app.route('/tareas/<string:MC_id_tarea>', methods=['PUT'])
def MC_actualizar_tarea(MC_id_tarea):
    MC_datos = request.get_json(silent=True) or {}
    MC_campos_modificar = {}

    if "titulo" in MC_datos:
        MC_campos_modificar["titulo"] = MC_datos["titulo"].strip()
    if "descripcion" in MC_datos:
        MC_campos_modificar["descripcion"] = MC_datos["descripcion"].strip()
    if "completada" in MC_datos:
        MC_campos_modificar["completada"] = bool(MC_datos["completada"])

    if not MC_campos_modificar:
        return jsonify({"error": "No se enviaron campos válidos para actualizar."}), 400

    MC_resultado = MC_coleccion.update_one(
        {"_id": MC_id_tarea},
        {"$set": MC_campos_modificar}
    )

    if MC_resultado.matched_count == 0:
        return jsonify({"error": "Tarea no encontrada."}), 404

    MC_tarea_actualizada = MC_coleccion.find_one({"_id": MC_id_tarea})
    return jsonify({
        "mensaje": "Tarea actualizada correctamente",
        "tarea": MC_formatear_tarea(MC_tarea_actualizada)
    }), 200


# 4. ELIMINACIÓN: Borrar tarea por ID (DELETE /tareas/<id>)
@MC_app.route('/tareas/<string:MC_id_tarea>', methods=['DELETE'])
def MC_eliminar_tarea(MC_id_tarea):
    MC_resultado = MC_coleccion.delete_one({"_id": MC_id_tarea})

    if MC_resultado.deleted_count == 0:
        return jsonify({"error": "Tarea no encontrada."}), 404

    return jsonify({"mensaje": "Tarea eliminada exitosamente."}), 200


if __name__ == '__main__':
    MC_app.run(host='0.0.0.0', port=5000, debug=True)
