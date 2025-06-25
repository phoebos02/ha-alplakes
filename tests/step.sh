#!/bin/bash

set -e  # Exit on error

echo "Step 1: Set parameters"
lake="zurich"
depth="0.35"
latitude="47.25686"
longitude="8.69893"
echo "  lake: $lake"
echo "  depth: $depth"
echo "  latitude: $latitude"
echo "  longitude: $longitude"
echo

echo "Step 2: Set 'start' to today 09:00 UTC"
today=$(date -u +"%Y%m%d")
start="${today}0900"
echo "  start: $start"
echo

echo "Step 3: Set 'end' to today 12:00 UTC"
end="${today}1200"
echo "  end: $end"
echo

echo "Step 4: Construct URL"
url="https://alplakes-api.eawag.ch/simulations/point/delft3d-flow/$lake/$start/$end/$depth/$latitude/$longitude?variables=temperature"
echo "  url: $url"
echo

echo "Step 5: Fetch data with curl"
curl -v "$url"
echo

echo "Step 6: (Optional) Pretty-print JSON result (requires jq)"
if command -v jq > /dev/null; then
    curl -s "$url" | jq
else
    echo "jq not found, skipping pretty-print"
fi
