import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from typing import Dict, Tuple
from geopy.geocoders import Nominatim

class RouteOptimizer:
    def __init__(self):
        # Embed API keys directly
        self.tomtom_api_key = "9vK7z3PIsb100N4rj06rBNCam4IxvCxq"
        self.aqicn_api_key = "a762497b89d6333ba596e9547d36ccd80299fad0"
        self.emission_factors = {
            'small_truck': 0.2,  # kg CO2 per km
            'medium_truck': 0.3,
            'large_truck': 0.4,
            'electric_vehicle': 0.0
        }
        self.geolocator = Nominatim(user_agent="route_optimizer")

    def get_coordinates(self, location: str) -> Tuple[float, float]:
        """Get coordinates for a given location."""
        try:
            geolocation = self.geolocator.geocode(location)
            if geolocation:
                return geolocation.latitude, geolocation.longitude
            else:
                st.error(f"Could not find coordinates for: {location}")
                return None, None
        except Exception as e:
            st.error(f"Geocoding error: {e}")
            return None, None

    def get_route(self, start: Tuple[float, float], end: Tuple[float, float]) -> Dict:
        """Fetch optimal route from TomTom API."""
        url = f"https://api.tomtom.com/routing/1/calculateRoute/{start[0]},{start[1]}:{end[0]},{end[1]}/json"
        params = {'key': self.tomtom_api_key, 'traffic': 'true'}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Error fetching route: {e}")
            return None

    def get_weather_data(self, lat: float, lon: float) -> Dict:
        """Fetch weather and air quality data."""
        url = f"http://api.waqi.info/feed/geo:{lat};{lon}/?token={self.aqicn_api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.warning(f"Weather data unavailable: {e}")
            return {'data': {'aqi': 50}}  # Default AQI value

    def calculate_emissions(self, distance: float, vehicle_type: str, weather_factor: float) -> float:
        """Calculate vehicle emissions."""
        base_emission = self.emission_factors[vehicle_type]
        return distance * base_emission * weather_factor

    def generate_report(self, route_data: Dict, weather_data: Dict, vehicle_type: str) -> Dict:
        """Generate a detailed report for the route."""
        if not route_data or 'routes' not in route_data:
            return {'distance': 0, 'duration': 0, 'emissions': 0, 'coordinates': []}

        route = route_data['routes'][0]
        distance = route['summary']['lengthInMeters'] / 1000  # Convert meters to km
        duration = route['summary']['travelTimeInSeconds'] / 3600  # Convert seconds to hours
        weather_factor = 1.2 if weather_data['data']['aqi'] > 100 else 1.0
        emissions = self.calculate_emissions(distance, vehicle_type, weather_factor)

        coordinates = []
        for leg in route['legs']:
            for point in leg['points']:
                coordinates.append([point['latitude'], point['longitude']])

        return {
            'distance': distance,
            'duration': duration,
            'emissions': emissions,
            'coordinates': coordinates
        }

def main():
    st.title("Dynamic Route Optimization for India")
    optimizer = RouteOptimizer()

    # Input selection
    st.subheader("Input Route Details")
    input_method = st.radio("Choose Input Method:", ["Enter Locations", "Enter Coordinates"])

    if input_method == "Enter Locations":
        start_location = st.text_input("Start Location", value="Delhi")
        end_location = st.text_input("End Location", value="Mumbai")
        start_coords = optimizer.get_coordinates(start_location)
        end_coords = optimizer.get_coordinates(end_location)
    else:
        start_lat = st.number_input("Start Latitude", value=28.6139)
        start_lon = st.number_input("Start Longitude", value=77.2090)
        end_lat = st.number_input("End Latitude", value=19.0760)
        end_lon = st.number_input("End Longitude", value=72.8777)
        start_coords = (start_lat, start_lon)
        end_coords = (end_lat, end_lon)

    vehicle_type = st.selectbox(
        "Select Vehicle Type:",
        list(optimizer.emission_factors.keys())
    )

    # Calculate route
    if st.button("Calculate Optimal Route"):
        if start_coords and end_coords:
            route_data = optimizer.get_route(start_coords, end_coords)
            weather_data = optimizer.get_weather_data(start_coords[0], start_coords[1])
            report = optimizer.generate_report(route_data, weather_data, vehicle_type)

            # Map visualization
            m = folium.Map(location=[start_coords[0], start_coords[1]], zoom_start=6)
            if report['coordinates']:
                folium.PolyLine(report['coordinates'], color="blue", weight=2).add_to(m)
                folium.Marker(start_coords, popup="Start").add_to(m)
                folium.Marker(end_coords, popup="End").add_to(m)

            # Display results
            st.subheader("Route Analysis")
            st.write(f"Distance: {report['distance']:.2f} km")
            st.write(f"Duration: {report['duration']:.2f} hours")
            st.write(f"Estimated Emissions: {report['emissions']:.2f} kg CO2")
            if weather_data['data']['aqi'] > 100:
                st.warning("High air pollution detected - emissions increased.")
            folium_static(m)
        else:
            st.error("Invalid input coordinates or locations.")

if __name__ == "__main__":
    main()
