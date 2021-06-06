class ResultCollection:
	"""
	This is a class that represents an collection of earthquake events. An query can be a single event
	search or a ranged event search (i.e. difference between searching for a particular ID and a range
	of magnitudes). When the query specified a range of constraints, it will return a collection of
	earthquake events.

	This class accepts all the json data that the query generated, processes the data, and provides
	users all the necessary APIs for getting ordered, sorted and simplified results. The APIs are specially
	designed to include all functionality of the USGS API.

	Ordering types:
		The ResultCollection class supports multiple ordering types, all of them are represented in Strings

		- time: timestamp of the earthquake event
		- mag: short for magnitude, the magnitude of the earthquake
		- latitude: latitude of the epicenter
		- longitude: longitude of the epicenter
		- depth: depth of the epicenter

	Sample usage:
	::
		earthquake_query = EarthquakeQuery(time=None, Location=[rectangle, circle, geo_rectangle, geo_circle])
		result = earthquake_query.search()
		data1 = result.get_all_simplified_data(order_by="time")
		data2 = result.get_all_magnitudes(order_by="mag")

	"""
	def __init__(self, result_json_list):
		"""
		Constructor:
			Initialize the result object, remove all duplicating earthquakes when initializing

		:param result_json_list: list, the original list of json strings returned by all the requests
		                         made in the query
		"""
		self.json_raw = result_json_list
		self.json_combined = self._combine_json_list(result_json_list)

	def _combine_json_list(self, json_list: list):
		unique_results = self._combine_unique_results(json_list)
		combined_metadata = self._combine_metadata(json_list, len(unique_results))
		combined_bbox = self._combine_boundary_box(json_list)

		base_json = {"type": json_list[0]["type"],
					 "metadata": combined_metadata,
					 "features": unique_results,
					 "bbox": combined_bbox}

		return base_json

	def _combine_metadata(self, json_list: list, count: int):
		base_metadata = {"generated": [],
						 "url": [],
						 "title": json_list[0]["metadata"]["title"],
						 "status": 200,
						 "api": json_list[0]["metadata"]["api"],
						 "count": count}

		for data in json_list:
			base_metadata["generated"].append(data["metadata"]["generated"])
			base_metadata["url"].append(data["metadata"]["url"])

		return base_metadata

	def _combine_unique_results(self, json_list):
		result_id_set = set()
		unique_results = []

		for data in json_list:
			for result in data["features"]:
				ids = result["properties"]["ids"].strip(",").split(",")
				if any(x in result_id_set for x in ids):
					continue
				else:
					result_id_set.update(ids)
					unique_results.append(result)
		return unique_results

	def _combine_boundary_box(self, json_list):
		base_bbox = []
		for data in json_list:
			try:
				base_bbox.append(data["bbox"])
			except:
				continue
		return base_bbox

	def _get_sorted_results(self, order_by, descending):
		if order_by == "latitude":
			return sorted(self.json_combined["features"], key=lambda i: i["geometry"]["coordinates"][1], reverse=descending)
		if order_by == "longitude":
			return sorted(self.json_combined["features"], key=lambda i: i["geometry"]["coordinates"][0], reverse=descending)
		if order_by == "depth":
			return sorted(self.json_combined["features"], key=lambda i: i["geometry"]["coordinates"][2], reverse=descending)

		return sorted(self.json_combined["features"], key=lambda i: i["properties"][order_by], reverse=descending)

	def get_combined_json(self) -> dict:
		"""
		Get the combined raw json dict of the collection

		:return: dict, the raw json dict of the query
		"""
		return self.json_combined

	def get_metadata(self) -> dict:
		"""
		Get the combined metadata of the result collection

		:return: dict, a dictionary containing all metadata values
		"""
		return self.json_combined["metadata"]

	def get_boundary_box(self) -> list:
		"""
		Get the combined boundary box of the result collection.
		Combined boundary box means taking all max and min lat/long, and pick the extreme values.
		The updated combined boundary box should contain all the query regions.

		:return: list of coordinates, specifying the boundary box
		"""
		return self.json_combined["bbox"]

	def get_data_by_keys(self, keys:list, order_by="time", descending=True) -> dict:
		"""
		Get a simplified version of the results by specifying which keys the users wish to get.
		For example, if the user wants only the title, magnitude and time, he should pass the list
		["title", "mag", "time"] to this function.

		:param keys: list, list of keys. Each key should be present in the GeoJSON
		:param order_by: str, ordering type
		:param descending: bool, indicates whether the ordered data should be in descending order
		:return: dict, key value pairs of the result earthquake data
		"""
		to_return = []
		results = self._get_sorted_results(order_by, descending)

		for result in results:
			d = dict.fromkeys(keys)
			for key in keys:
				if key in result["properties"]:
					d[key] = result["properties"][key]
				if key in result["geometry"]:
					d[key] = result["geometry"][key]
				if key == "id":
					d[key] = result["id"]
			to_return.append(d)

		return to_return

	def get_all_earthquake_data(self, order_by="time", descending=True) -> list:
		"""
		Get all earthquakes data from the returned query

		:param order_by: str, ordering mode
		:param descending: bool, indicates whether it is in descending order
		:return: list, list of earthquakes in dict form
		"""
		return self._get_sorted_results(order_by, descending)

	def get_all_details_url(self, order_by="time", descending=True) -> list:
		"""
		Get all earthquake detailed data urls from the returned query

		:param order_by: str, ordering mode
		:param descending: bool, indicates whether it is in descending order
		:return: list of dicts, list of urls for detailed earthquake information
		"""
		to_return = []
		results = self._get_sorted_results(order_by, descending)

		for result in results:
			to_return.append({"title": result["properties"]["title"],
							  "ids": result["properties"]["ids"],
							  "detail": result["properties"]["detail"]})
		return to_return

	def get_all_simplified_data(self, order_by="time", descending=True) -> list:
		"""
		Get all earthquake data in a simplified term, keys will be title, coordinates, magnitude and depth

		:param order_by: str, ordering mode
		:param descending: bool, indicates whether it is in descending order
		:return: list, list of dicts representing the earthquakes
		"""
		to_return = []
		results = self._get_sorted_results(order_by, descending)

		for result in results:
			to_return.append({"title": result["properties"]["title"],
							  "mag": result["properties"]["mag"],
							  "time": result["properties"]["time"],
							  "coordinates": result["geometry"]["coordinates"]})
		return to_return

	def get_all_magnitudes(self, order_by="mag", descending=True) -> list:
		"""
		Get a list of earthquake magnitudes

		:param order_by: str, ordering mode
		:param descending: bool, indicates whether it is in descending order
		:return: list, list of earthquake magnitudes
		"""
		ordered = self._get_sorted_results(order_by, descending)
		return [x["properties"]["mag"] for x in ordered]

	def get_all_coordinates(self, order_by="time", descending=True) -> list:
		"""
		Get a list of earthquake coordinates

		:param order_by: str, ordering mode
		:param descending: bool, indicates whether it is in descending order
		:return: list, list of tuples representing coordinates
		"""
		ordered = self._get_sorted_results(order_by, descending)
		return [x["geometry"]["coordinates"][:2] for x in ordered]

	def get_all_3d_coordinates(self, order_by="time", descending=True) -> list:
		"""
		Get a list of earthquake coordinates, with the third dimension representing depth

		:param order_by: str, ordering mode
		:param descending: bool, indicates whether it is in descending order
		:return: list, list of 3-tuples representing coordinates
		"""
		ordered = self._get_sorted_results(order_by, descending)
		return [x["geometry"]["coordinates"] for x in ordered]

	def get_all_depths(self, order_by="time", descending=True) -> list:
		"""
		Get a list of earthquake depths

		:param order_by: str, ordering mode
		:param descending: bool, indicates whether it is in descending order
		:return: list, list of int representing depths
		"""
		ordered = self._get_sorted_results(order_by, descending)
		return [x["geometry"]["coordinates"][2] for x in ordered]
	
	def get_all_titles(self, order_by="time", descending=True) -> list:
		"""
		Get a list of earthquake event titles

		:param order_by: str, ordering mode
		:param descending: bool, indicates whether it is in descending order
		:return: list, list of titles
		"""
		ordered = self._get_sorted_results(order_by, descending)
		return [x["properties"]["title"] for x in ordered]

	def get_number_of_earthquakes(self) -> int:
		"""
		Get the total number of earthquakes in the query result

		:return: int, integer presenting the total number of earthquakes
		"""
		return len(self.json_combined["features"])
