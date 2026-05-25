from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

LOCATIONS = [
    {
        "place_id": "ChIJTQ929KwuDogRD_8ndlex-p0",
        "name": "47th Street",
        "address": "205 E 47th St, Chicago"
    },
    {
        "place_id": "ChIJ81moTQAzDogRM_kPF4pi6_4",
        "name": "Kedzie",
        "address": "800 N Kedzie Ave, Chicago"
    },
    {
        "place_id": "ChIJ5f3f4PclDogRONXA5lZyr4g",
        "name": "87th Street",
        "address": "205 W 87th St, Chicago"
    }
]

def fetch_reviews_for_location(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,reviews",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "OK":
        print(f"Error fetching {place_id}: {data.get('status')}")
        return None

    result = data["result"]
    return {
        "rating": result.get("rating"),
        "total_ratings": result.get("user_ratings_total"),
        "reviews": result.get("reviews", [])
    }

def fetch_all_reviews():
    all_reviews = []
    summary = {
        "locations": [],
        "reviews": []
    }

    for location in LOCATIONS:
        data = fetch_reviews_for_location(location["place_id"])
        if not data:
            continue

        summary["locations"].append({
            "name": location["name"],
            "address": location["address"],
            "rating": data["rating"],
            "total_ratings": data["total_ratings"]
        })

        for review in data["reviews"]:
            all_reviews.append({
                "author": review.get("author_name"),
                "rating": review.get("rating"),
                "text": review.get("text"),
                "time": review.get("relative_time_description"),
                "location": location["name"]
            })

    # sort by rating descending so best reviews show first
    all_reviews = [r for r in all_reviews if r["rating"] >= 4]
    all_reviews.sort(key=lambda x: x["rating"], reverse=True)
    summary["reviews"] = all_reviews

    print(f"Total reviews fetched: {len(all_reviews)}")
    return summary

if __name__ == "__main__":
    result = fetch_all_reviews()
    #print(json.dumps(result, indent=2))
