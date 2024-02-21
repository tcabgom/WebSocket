import asyncio
import websockets


async def send_message():
    # Dirección a la que mandar el mensaje del cliente simulado
    uri = "ws://localhost:8000"

    async with websockets.connect(uri) as websocket:
        #Introduces por la terminal el mensaje que quieres mandar
        message = input("Ingrese un mensaje para enviar al servidor: ")

        # Envía el mensaje al servidor
        await websocket.send(message)

        # Espera la respuesta del servidor
        response = await websocket.recv()
        #Imprimer en la terminal la respuesta
        print(f"Respuesta del servidor: {response}")


# Ejecuta el cliente
asyncio.get_event_loop().run_until_complete(send_message())
