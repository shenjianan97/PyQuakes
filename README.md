# PyEarthquake
PyEarthquake is a Python wrapper for [USGS Earthquake Catalog API](https://earthquake.usgs.gov/fdsnws/event/1/) that manages data querying and result processing. PyEarthquake also integrates [Bing Map API](https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/find-a-location-by-query) to manage geolocation of events.

## List of deliverables
- Final report: ./final_report.pdf
- API documentation HTML, getting started and examples: ./docs/index.html
- Use case code (client code), and the comparison with the original API:  ./client
- Prototype implementation: ./src
- Unit tests: ./test

If you are having trouble finding these deliverables, please email us (because we for sure submitted everything!)

## Features of PyEarthquake
- Handles the HTTP requests, and the HTTP error. Only needs to focus on setting parameters and data processing.
- Supports setting the query parameters   
- Supports searching with multiple time periods with easy-to-understand time format.
- Supports searching with multiple locations with pre-defined location classes.
- Provides geocoding functionality so that users are able to search the location without finding the coordinates.
- Supports filtering, sorting and organizing the result.

## Getting Started
Follow the instructions of Bing Map to [get your own key](https://docs.microsoft.com/en-us/bingmaps/getting-started/bing-maps-dev-center-help/getting-a-bing-maps-key) and copy your Bing Map Key in key.txt file under src foler.

## How to use
The EarthquakeQuery class has to be imported to use the API.

Import other classes if you would like to search by time and location or set other parameters.

## Example
A typical usage to search a collection of results is:
```
query = EarthquakeQuery()
query.set_time([TimeFrame(datetime(2010, 1, 1), datetime(2015, 1, 1))])
query.set_max_depth(1.0)
result = query.search()
```

A typical usage to search a specific earthquake by its event id is:
```
event_id = "usc000lvb5"
result = EarthquakeQuery.search_by_event_id(event_id)
```
For more examples, please refer to the **client** folder. Several use cases are contained in the clinet folder with example codes. See the function without **original** suffix.

## Test
Tests are placed in the test folder.
Please cd into the folder and run each of the py files for testing.
