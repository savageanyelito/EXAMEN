import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
geocode_url = "https://graphhopper.com/api/1/geocode?"
key = "97086bfd-4e2f-479e-aaa7-80c8494f975b"

def geocoding(location, key):
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    print("Geocoding API URL for " + location + ":\n" + url)
    if json_status == 200:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        country = json_data["hits"][0]["country"]
    else:
        lat = None
        lng = None
        country = None
    return json_status, lat, lng, country

def get_route(orig_coords, dest_coords, vehicle, key):
    url = route_url + urllib.parse.urlencode({
        "point": [f"{orig_coords[0]},{orig_coords[1]}", f"{dest_coords[0]},{dest_coords[1]}"],
        "vehicle": vehicle,
        "locale": "es",  
        "key": key
    }, doseq=True)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    while True:
        origen = input("Ingrese ciudad de origen (O presione 'S' para salir): ").strip()
        if origen.lower() == 's':
            break

        destino = input("Ingrese ciudad de destino (O presione 'S' para salir): ").strip()
        if destino.lower() == 's':
            break

        print("Medio de transporte: auto, bicicleta, a pie")
        vehicle_input = input("Ingrese su medio de transporte: ").strip().lower()

        vehicle_mapping = {
            "auto": "car",
            "bicicleta": "bike",
            "a pie": "foot"
        }

        if vehicle_input not in vehicle_mapping:
            print("Medio de transporte no válido. Intente nuevamente.")
            continue

        vehicle = vehicle_mapping[vehicle_input]

        orig_status, orig_lat, orig_lng, orig_country = geocoding(origen, key)
        dest_status, dest_lat, dest_lng, dest_country = geocoding(destino, key)

        if orig_status != 200 or dest_status != 200 or orig_lat is None or dest_lat is None:
            print("Error obteniendo la geocodificación de las ciudades. Intente nuevamente.")
            continue

        allowed_countries = ["Chile", "Argentina"]
        if orig_country not in allowed_countries:
            print(f"La ciudad de origen debe estar en Chile o Argentina. La ciudad '{origen}' está en {orig_country}. Intente nuevamente.")
            continue

        if dest_country not in allowed_countries:
            print(f"La ciudad de destino debe estar en Chile o Argentina. La ciudad '{destino}' está en {dest_country}. Intente nuevamente.")
            continue

        route_data = get_route((orig_lat, orig_lng), (dest_lat, dest_lng), vehicle, key)
        if route_data is None:
            print("Error obteniendo la ruta. Intente nuevamente.")
            continue

        distance_km = route_data['paths'][0]['distance'] / 1000
        distance_miles = distance_km * 0.621371
        time_sec = route_data['paths'][0]['time'] / 1000
        time_hrs = time_sec / 3600
        narrative = route_data['paths'][0]['instructions']

        print(f"\nDistancia: {distance_km:.2f} km ({distance_miles:.2f} millas)")
        print(f"Duración: {time_hrs:.2f} horas")
        print("Narrativa del viaje:")
        for step in narrative:
            print(f"{step['distance'] / 1000:.2f} km - {step['text']}")

if __name__ == "__main__":
    main()