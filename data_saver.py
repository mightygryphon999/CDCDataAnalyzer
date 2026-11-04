import json

from data_converter import DataConverter

converter = DataConverter()
states = converter.load_data()

with open("data.json", "w") as file:
    json.dump(
        [state.to_dict() for state in states],
        file,
        indent=4
    )