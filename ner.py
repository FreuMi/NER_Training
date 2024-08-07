import spacy
import re

nlp = spacy.load("./output/model-best")

wikidata_base = "https://www.wikidata.org/wiki/"
qudt_base = "https://qudt.org/vocab/unit/"
nel_base = [
    # Frequency
    {"short_unit": "hz", "long_unit": ["hertz"], "qudt_id": "HZ",
        "observerd_property": ["frequency"], "wikidata_id": "Q11652"},
    {"short_unit": "khz", "long_unit": ["kilohertz"], "qudt_id": "KiloHZ",
        "observerd_property": ["frequency"], "wikidata_id": "Q11652"},
    {"short_unit": "mhz", "long_unit": ["megahertz"], "qudt_id": "MegaHZ",
        "observerd_property": ["frequency"], "wikidata_id": "Q11652"},
    {"short_unit": "ghz", "long_unit": ["gigahertz"], "qudt_id": "GigaHZ",
        "observerd_property": ["frequency"], "wikidata_id": "Q11652"},
    # Time
    {"short_unit": "s", "long_unit": ["second", "seconds"], "qudt_id": "SEC",
        "observerd_property": ["time", "times"], "wikidata_id": "Q11471"},
    {"short_unit": "ms", "long_unit": ["millisecond", "milliseconds"], "qudt_id": "MilliSEC",
        "observerd_property": ["time", "times"], "wikidata_id": "Q11471"},
    {"short_unit": "µs", "long_unit": ["microsecond", "microseconds"], "qudt_id": "MicroSEC",
        "observerd_property": ["time", "times"], "wikidata_id": "Q11471"},
    {"short_unit": "ns", "long_unit": ["nanosecond", "nanoseconds"], "qudt_id": "NanoSEC",
        "observerd_property": ["time", "times"], "wikidata_id": "Q11471"},
    # Mass
    {"short_unit": "g", "long_unit": ["gram", "grams"], "qudt_id": "GM",
        "observerd_property": ["mass", "weight", "weights", "weighs"], "wikidata_id": "Q11423"},
    {"short_unit": "kg", "long_unit": ["kilogram", "kilograms"], "qudt_id": "KiloGM",
        "observerd_property": ["mass", "weight", "weights", "weighs"], "wikidata_id": "Q11423"},
    {"short_unit": "t", "long_unit": ["ton", "tons"], "qudt_id": "TON_Metric",
        "observerd_property": ["mass", "weight", "weights", "weighs"], "wikidata_id": "Q11423"},
    # Temperature
    {"short_unit": "°C", "long_unit": ["celsius", "degree celsius", "degrees celsius"], "qudt_id": "DEG_C",
        "observerd_property": ["temperature", "temperatures", "temp", "temps"], "wikidata_id": "Q11466"},
    # Percent
    {"short_unit": "%", "long_unit": ["percent"], "qudt_id": "PERCENT",
        "observerd_property": [], "wikidata_id": "Q2499617"},
    # Distance
    {"short_unit": "m", "long_unit": ["meter", "meters"], "qudt_id": "M",
        "observerd_property": ["distance", "length"], "wikidata_id": "Q126017"},
    {"short_unit": "km", "long_unit": ["kilometer", "kilometers"], "qudt_id": "KiloM",
        "observerd_property": ["distance", "length"], "wikidata_id": "Q126017"},
    {"short_unit": "mm", "long_unit": ["millimeter", "millimeters"], "qudt_id": "MilliM",
        "observerd_property": ["distance", "length"], "wikidata_id": "Q126017"},
    {"short_unit": "µm", "long_unit": ["micrometer", "micrometers"], "qudt_id": "MicroM",
        "observerd_property": ["distance", "length"], "wikidata_id": "Q126017"},
    {"short_unit": "nm", "long_unit": ["nanometer", "nanometers"], "qudt_id": "NanoM",
        "observerd_property": ["distance", "length"], "wikidata_id": "Q126017"},
    # Acceleration
    {"short_unit": "g", "long_unit": ["g-force"], "qudt_id": "G",
        "observerd_property": ["acceleration", "accelerationx", "accelerationy", "accelerationz"], "wikidata_id": "Q11376"},
    {"short_unit": "Gs", "long_unit": ["g-force"], "qudt_id": "G",
        "observerd_property": ["acceleration", "accelerationx", "accelerationy", "accelerationz"], "wikidata_id": "Q11376"},
    # Humidity
    {"short_unit": "%", "long_unit": ["percent"], "qudt_id": "PERCENT",
        "observerd_property": ["humidity", "humid"], "wikidata_id": "Q2499617"},
]


def perform_nel_unit_short(item):
    if len(item) > 3:
        return perform_nel_unit_long(item)
    else:
        for nel_arr in nel_base:
                if  nel_arr["short_unit"] == item:
                    return nel_arr


def perform_nel_unit_long(input_item):
    item_split_arr = input_item.split(" ")
    
    for item in item_split_arr:   
        for nel_arr in nel_base:
            # Iterate over units
            for unit in nel_arr["long_unit"]:
                if unit == item:
                    return nel_arr


def perform_nel_property(item):
    # Assumes base unit, works if base unit is first entry in nel_base
    for nel_arr in nel_base:
        properties = nel_arr["observerd_property"] 
        for prop in properties:
            if prop.lower() == item or prop.lower() in item:
                return nel_arr

def clear_number(item):
    # Define patterns for numbers, whitespace, +, and - at the beginning and end
    pattern = r'^[0-9\s\[\]\(\)\{\}\+\-]+|[0-9\s\[\]\(\)\{\}\+\-]+$'
    # Use re.sub to replace the matched patterns with an empty string
    return re.sub(pattern, '', item)

def clear_brackets(input_string):
    brackets = "[](){}"
    for bracket in brackets:
        input_string = input_string.replace(bracket, "")
    return input_string

def remove_duplicates(found_elements, list_label):
    seen = set()
    filtered_elements = []
    filtered_elements_labels = []
    for i in range(len(found_elements)):
        item_qudt = found_elements[i]["qudt_id"]
        item = found_elements[i]
        label = list_label[i]
        if item_qudt not in seen:
            filtered_elements.append(item)
            filtered_elements_labels.append(label)
            seen.add(item_qudt)
    return filtered_elements, filtered_elements_labels

def filter_percent(found_elements, found_elements_labels):
    # Remove % if more then one unit is found
    filtered_elements = []
    filtered_elements_labels = []
    for i in range(len(found_elements)):
        element = found_elements[i]
        element_label = found_elements_labels[i]
        
        if element["short_unit"] != "%":
            filtered_elements.append(element)
            filtered_elements_labels.append(element_label)
    
    return filtered_elements, filtered_elements_labels


def filter_property(found_elements, found_elements_labels):
    # Remove property if more then one unit is found
    filtered_elements = []
    filtered_elements_labels = []
    for i in range(len(found_elements)):
        element = found_elements[i]
        element_label = found_elements_labels[i]
        
        if element_label != "OBSERVABLE_PROP":
            filtered_elements.append(element)
            filtered_elements_labels.append(element_label)
    
    return filtered_elements, filtered_elements_labels

def inference(sentence, mode="full"):
    sentence = sentence.lower()
    doc = nlp(sentence)
    found_elements = []
    found_elements_labels = []
    for ent in doc.ents:
        print("Working on:", "|", ent, "|", "with label", ent.label_)
        result = None
        if ent.label_ == "UNIT_SHORT":
            unit = clear_number(ent.text)
            unit = clear_brackets(unit)
            result = perform_nel_unit_short(unit.lower())

        elif ent.label_ == "UNIT_LONG":
            unit = clear_number(ent.text)
            unit = clear_brackets(unit)           
            result = perform_nel_unit_long(unit.lower())

        elif ent.label_ == "OBSERVABLE_PROP":
            if mode == "full":
                prop = clear_number(ent.text)
                prop = clear_brackets(prop)               
                result = perform_nel_property(prop.lower())
        
        if result != None:
            found_elements.append(result)
            found_elements_labels.append(ent.label_)
         
    
    found_elements, found_elements_labels = remove_duplicates(found_elements, found_elements_labels )
    # Filter percent if more than one unit is found
    if len(found_elements) > 1:
        found_elements, found_elements_labels = filter_percent(found_elements, found_elements_labels)

    # Filter unit detected from OBSERVABLE PROPERTY if more than on unit is found
    if len(found_elements) > 1:
        found_elements, found_elements_labels = filter_property(found_elements, found_elements_labels)
                
    # Check if still more than unit is found
    if len(found_elements) > 1:
        print("Error: more than one unit found")
        for i in range(len(found_elements)):
            element = found_elements[i]
            element_label = found_elements_labels[i]
            print(element, "with label", element_label)
        return None
    
    # Check if nothing is found
    elif len(found_elements) == 0:      
        return None
    else:
        # return result data:
        return found_elements[0]