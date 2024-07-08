import requests

def obtener_coordenadas(ciudad):
    # Función para obtener coordenadas de una ciudad (simulada)
    ciudades = {
        'santiago': '-33.4489,-70.6693',  # Santiago, Chile
        'ovalle': '-30.5987,-71.2048',    # Ovalle, Chile
        'buenos aires': '-34.6037,-58.3816',  # Buenos Aires, Argentina
        'mendoza': '-32.8895,-68.8458'   # Mendoza, Argentina
        # Agrega más ciudades según sea necesario
    }

    ciudad = ciudad.lower()
    if ciudad in ciudades:
        return ciudades[ciudad]
    else:
        return None

def obtener_instrucciones_ruta(origen, destino, vehiculo, api_key):
    # Configuración de la solicitud a la API de GraphHopper para obtener instrucciones de ruta
    url = 'https://graphhopper.com/api/1/route'
    params = {
        'point': [origen, destino],
        'vehicle': vehiculo,
        'locale': 'es',
        'key': api_key,
        'instructions': True  # Solicitar instrucciones detalladas
    }

    # Realizar la solicitud GET a la API de GraphHopper
    response = requests.get(url, params=params)

    # Procesar la respuesta JSON
    if response.status_code == 200:
        data = response.json()
        distancia_km = data['paths'][0]['distance'] / 1000.0
        distancia_millas = distancia_km / 1.60934
        duracion_segundos = data['paths'][0]['time']
        duracion_minutos = duracion_segundos / 60.0
        instrucciones = data['paths'][0]['instructions']

        narrativa_viaje = f"Viaje desde {origen.split(',')[0]} a {destino.split(',')[0]} en {vehiculo}. " \
                          f"Distancia aproximada: {distancia_km:.2f} km ({distancia_millas:.2f} millas). " \
                          f"Duración aproximada: {duracion_minutos:.2f} minutos."

        print(f"Distancia en kilómetros: {distancia_km:.2f} km")
        print(f"Distancia en millas: {distancia_millas:.2f} mi")
        print(f"Duración del viaje: {duracion_minutos:.2f} minutos")
        print(f"Narrativa del viaje: {narrativa_viaje}")

        print("\nInstrucciones de ruta:")
        for idx, instruccion in enumerate(instrucciones, 1):
            print(f"{idx}. {instruccion['text']}")

    else:
        print(f"Error al realizar la solicitud: {response.status_code} - {response.text}")

if __name__ == "__main__":
    api_key = 'd26d85da-5cfb-4d94-8371-5626eb7eddf9'

    while True:
        # Solicitar ciudad de origen
        ciudad_origen = input("Ingrese la ciudad de origen (o 's' para salir): ").strip().lower()
        if ciudad_origen == 's':
            break

        # Obtener coordenadas de la ciudad de origen
        coordenadas_origen = obtener_coordenadas(ciudad_origen)
        if coordenadas_origen is None:
            print(f"No se encontraron coordenadas para {ciudad_origen}. Intente de nuevo.")
            continue

        # Solicitar ciudad de destino
        ciudad_destino = input("Ingrese la ciudad de destino: ").strip().lower()
        if ciudad_destino == 's':
            break

        # Obtener coordenadas de la ciudad de destino
        coordenadas_destino = obtener_coordenadas(ciudad_destino)
        if coordenadas_destino is None:
            print(f"No se encontraron coordenadas para {ciudad_destino}. Intente de nuevo.")
            continue

        # Solicitar tipo de vehículo
        vehiculo = input("Ingrese el tipo de vehículo (car, foot, bike, etc.): ").strip().lower()

        # Obtener instrucciones de ruta detalladas
        obtener_instrucciones_ruta(coordenadas_origen, coordenadas_destino, vehiculo, api_key)

    print("¡Gracias por usar el programa!")
