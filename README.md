# Sistema de Seguimiento de Tareas (Flask + MongoDB)

Aplicación de seguimiento de tareas utilizando microservicios Flask, una base de datos MongoDB/Docker y un cliente remoto en Python para el modo de escritorio..

## Arquitectura y Tecnologías
- **Backend:** Microservicio RESTful en Python con Flask.
- **Base de datos:** MongoDB ejecutándose en Docker.
- **Cliente remoto:** Interfaz de consola en Python 3 utilizando la librería `requests`.

## Estructura de Datos (MongoDB)
Colección `tareas`:
```json
{
  "_id": "0001",
  "rut": "11111111-1",
  "titulo": "Estudiar para test de entrada",
  "descripcion": "Repasar contenidos de bases de datos SQL y NoSQL",
  "completada": false
}
```

## Endpoints de la API
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/tareas` | Crea una tarea nueva asignando ID correlativo. |
| `GET` | `/tareas` | Lista todas las tareas (`?rut=<RUT>` como filtro opcional). |
| `PUT` | `/tareas/<id>` | Actualiza campos (`titulo`, `descripcion`, `completada`). |
| `DELETE`| `/tareas/<id>` | Elimina la tarea señalada. |

## Instrucciones de Ejecución

### 1. Iniciar BDD (Docker)
```bash
docker run -d --name mongo-tareas -p 27017:27017 -v mongo_data:/data/db mongo:latest
```

### 2. Configurar Entorno y Servidor
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 servidor.py
```

### 3. Ejecutar Cliente Remoto
En otra terminal con venv activo:
```bash
python3 cliente.py
```
