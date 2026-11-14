import requests


def get_observations(lat, long):
    west  = long - 0.1
    east  = long + 0.1
    south = lat - 0.1
    north = lat + 0.1
    url = "https://api.daac.asf.alaska.edu/services/search/param"
    polygon = f"POLYGON(({west} {south}, {east} {south}, {east} {north}, {west} {north}, {west} {south}))"
    params = {
        "dataset": "NISAR",
        "processingLevel": "GCOV",
        "intersectsWith": polygon,
        "start": "2025-07-30",
        "end": "now",
        "output": "geojson",}

    response = requests.get(url, params=params)
    response.raise_for_status()
    features = response.json()["features"]

    groups = {}

    for f in features:
        prop = f["properties"]
        obs = (prop.get("pathNumber"), prop.get("frameNumber"), prop.get("flightDirection"))
        if obs not in groups:
            groups[obs] = []
        groups[obs].append(f)

    for obs, val in groups.items():
        val.sort(key=lambda f: f["properties"]["startTime"])
        print("Track/frame/direction:", obs, ":", len(val), "observations")

    for obs, val in groups.items():
        if len(val) < 2:
            continue
        print("\nGroup:", obs)
        for i in range(len(val) - 1):
            before = val[i]["properties"]["startTime"]
            after = val[i + 1]["properties"]["startTime"]
            print("  compare", before, "and", after)
    return groups


groups = get_observations(24.85837627940547, 55.71343188471354)
