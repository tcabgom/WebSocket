import asyncio
import websockets

async def send_message(uri, message):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Respuesta: {response}")

async def main():
    # Dirección a la que mandar el mensaje del cliente simulado
    uri = "ws://localhost:8000"

    # Número de clientes simulados
    num_clients = 10000

    # Mensaje a enviar
    message = "Destino de prueba"

    # Crear lista de tareas para simular múltiples clientes conectándose simultáneamente
    tasks = [send_message(uri, message) for _ in range(num_clients)]

    # Ejecutar las tareas simultáneamente
    await asyncio.gather(*tasks)

# Ejecutar el programa principal
asyncio.get_event_loop().run_until_complete(main())