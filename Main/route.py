import requests

def get_route_coordinates(start_lat, start_lon, end_lat, end_lon):
    base_url = 'http://router.project-osrm.org/route/v1/driving/'
    coordinates = f'{start_lon},{start_lat};{end_lon},{end_lat}'
    response = requests.get(f'{base_url}{coordinates}?geometries=geojson')
    if response.status_code == 200:
        data = response.json()
        if 'routes' in data and len(data['routes']) > 0 and 'geometry' in data['routes'][0]:
            geometry = data['routes'][0]['geometry']
            return geometry['coordinates']
        else:
            print("No se encontraron rutas entre los puntos proporcionados.")
    else:
        print("Error al obtener la ruta.")

# Ejemplo de uso


start_latitude = 38.9954097745552
start_longitude = -3.92764291249112



end_latitude = 38.9913293706391
end_longitude = -3.92801457577601

route_coordinates = get_route_coordinates(start_latitude, start_longitude, end_latitude, end_longitude)
if route_coordinates:
    print("Coordenadas de la ruta:")
    for coordinate in route_coordinates:
        print(coordinate)
