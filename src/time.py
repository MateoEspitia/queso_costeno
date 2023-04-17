import traveltimepy as ttpy
import os
from datetime import datetime #for examples
#store your credentials in an environment variable
os.environ["TRAVELTIME_ID"] = 'ed191a6f'
os.environ["TRAVELTIME_KEY"] = '203c1dcf22210b47dc2b0c3733652af4'


locations = [
    {"id": "London center", "coords": {"lat": 51.508930, "lng": -0.131387}},
    {"id": "Hyde Park", "coords": {"lat": 51.508824, "lng": -0.167093}},
    {"id": "ZSL London Zoo", "coords": {"lat": 51.536067, "lng": -0.153596}}
]

departure_search = {
    "id": "departure search example",
    "departure_location_id": "London center",
    "arrival_location_ids": ["Hyde Park", "ZSL London Zoo"],
    "transportation": {"type": "driving"},
    "departure_time":  datetime.utcnow().isoformat(),
    "properties": ["travel_time", "distance", "route"]
}

arrival_search = {
    "id": "arrival  search example",
    "departure_location_ids": ["Hyde Park", "ZSL London Zoo"],
    "arrival_location_id": "London center",
    "transportation": {"type": "public_transport"},
    "arrival_time":  datetime.utcnow().isoformat(),
    "properties": ["travel_time", "distance", "route", "fares"],
    "range": {"enabled": True, "max_results": 1, "width": 1800}
}

out = ttpy.routes(
    locations=locations, departure_searches=departure_search, arrival_searches=arrival_search)