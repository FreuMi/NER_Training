import spacy
import re

nlp = spacy.load("./output/model-best")


wikidata_base = "https://www.wikidata.org/wiki/"
qudt_base = "https://qudt.org/vocab/unit/"
nel_base = [
    # Frequency
    {"short_unit": "Hz", "long_unit": ["hertz"], "qudt_id": "HZ",
        "observerd_property": ["frequency"], "wikidata_id": "Q11652"},
    {"short_unit": "kHz", "long_unit": ["kilohertz"], "qudt_id": "KiloHZ",
        "observerd_property": ["frequency"], "wikidata_id": "Q11652"},
    {"short_unit": "MHz", "long_unit": ["megahertz"], "qudt_id": "MegaHZ",
        "observerd_property": ["frequency"], "wikidata_id": "Q11652"},
    {"short_unit": "GHz", "long_unit": ["gigahertz"], "qudt_id": "GigaHZ",
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
    {"short_unit": "°C", "long_unit": ["celsius", "degree celsius"], "qudt_id": "DEG_C",
        "observerd_property": ["temperature", "temperatures", "temp", "temps"], "wikidata_id": "Q11466"},
    # Percent
    {"short_unit": "%", "long_unit": ["percent"], "qudt_id": "PERCENT",
        "observerd_property": [], "wikidata_id": ""},
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
]


def perform_nel_unit_short(item):
    for nel_arr in nel_base:
        if nel_arr["short_unit"] == item:

            return nel_arr


def perform_nel_unit_long(item):
    for nel_arr in nel_base:
        if nel_arr["long_unit"] == item:

            return nel_arr


def perform_nel_property(item):
    # Assumes base unit, works if base unit is first entry in nel_base
    for nel_arr in nel_base:
        properties = nel_arr["observerd_property"]
        for prop in properties:
            if prop == item:
                return nel_arr

def remove_trailing_s(item):
    # Remove trailing s
    pattern = r'(?<!^.)s$'
    return re.sub(pattern, '', item)

def clear_number(item):
    # Remove number and whitespace
    pattern = r'[0-9\s\[\]\(\)\{\}]'
    return re.sub(pattern, '', item)


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

def inference(sentence):
    doc = nlp(sentence)
    found_elements = []
    found_elements_labels = []
    for ent in doc.ents:
        #print("Working on:", ent, "with label", ent.label_)
        result = None
        if ent.label_ == "UNIT_SHORT":
            unit = clear_number(ent.text)
            result = perform_nel_unit_short(unit)

        elif ent.label_ == "UNIT_LONG":
            unit = clear_number(ent.text)
            result = perform_nel_unit_long(unit.lower())

        elif ent.label_ == "OBSERVABLE_PROP":
            prop = clear_number(ent.text)
            result = perform_nel_property(prop.lower())
        
        if result != None:
            found_elements.append(result)
            found_elements_labels.append(ent.label_)
            
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
            print(element, "with label", elment_label)
        return None
    # Check if nothing is found
    elif len(found_elements) == 0:
        return None
    else:
        # return result data:
        return found_elements[0]