import asyncio
import websockets
from collections import deque
import traceback
import re

# Lista para almacenar las conexiones activas
active_connections = set()

# Cola para el buffer de mensajes
message_buffer = deque(maxlen=50)

def get_route(data):
    return "Test"

async def handler(websocket, path):
    # Agrega la conexión a la lista
    active_connections.add(websocket)

    # Muestra un mensaje cuando un nuevo usuario se conecta
    print(f"USUARIOS CONECTADOS ACTUALES: {len(active_connections)}")

    try:
        while True:
            data = await websocket.recv()

            if not isinstance(data, str) or not re.match(r'^[a-zA-Z0-9áéíóúüñ\s.,\'"-]+$', data):
                print("Input no es una cadena segura.")
                continue

            result = get_route(data)
            reply = f"Ruta optima para la consulta {data}: {result}"
            print(reply)

            # Almacena el mensaje en el buffer
            message_buffer.append(reply)

            # Envía la respuesta al cliente
            await websocket.send(reply)
    except websockets.exceptions.ConnectionClosedOK:
            print("El cliente ha cerrado la conexión de manera normal.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Error al manejar la conexión: {e}")
        # Envia un mensaje de rechazo al cliente
        refusal_message = "Conexión rechazada: error en el servidor"
        await websocket.send(refusal_message)
    finally:
        # Elimina la conexión de la lista cuando el usuario se desconecta
        active_connections.remove(websocket)
        print(f"USUARIOS CONECTADOS ACTUALES: {len(active_connections)}")


# Función para arrancar el servidor
start_server = websockets.serve(handler, "localhost", 8000)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print("Se ha solicitado apagar el servidor.")
except Exception as e:
    print(f"Error inesperado en el servidor: {e}")
    traceback.print_exc()
finally:
    print("Servidor apagado.")
