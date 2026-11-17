
import requests
import pandas as pd
from datetime import datetime, timezone

API_URL = "https://api.tfl.gov.uk/BikePoint"

def fetch_bike_data():
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def transform_bike_data(data):
    records = []

    for station in data:
        properties = {
            p["key"]: p["value"]
            for p in station.get("additionalProperties", [])
        }

        records.append({
            "station_id": station["id"],
            "station_name": station["commonName"],
            "latitude": station["lat"],
            "longitude": station["lon"],
            "bikes_available": properties.get("NbBikes"),
            "empty_docks": properties.get("NbEmptyDocks"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    df = pd.DataFrame(records)

    for column in ["bikes_available", "empty_docks"]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    return df


def main():
    data = fetch_bike_data()
    df = transform_bike_data(data)

    print(f"Retrieved {len(df)} stations")
    print(df.head())


if __name__ == "__main__":
    main()
