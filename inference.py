import spacy
import re

nlp = spacy.load(".output/model-best")

test_sentence = "Vibration (KHz) - normal 1 kHz, +/- 2%"


wikidata_base = "https://www.wikidata.org/wiki/"
qudt_base = "https://qudt.org/vocab/unit/"
nel_base = [
    {"short_unit": "Hz", "long_unit": "Hertz", "qudt_id": "HZ",
        "observerd_property": "frequency", "wikidata_id": "Q11652"},
    {"short_unit": "kHz", "long_unit": "Kilohertz", "qudt_id": "KiloHZ",
        "observerd_property": "frequency", "wikidata_id": "Q11652"},
    {"short_unit": "MHz", "long_unit": "Megahertz", "qudt_id": "MegaHZ",
        "observerd_property": "frequency", "wikidata_id": "Q11652"},
    {"short_unit": "GHz", "long_unit": "Gigahertz", "qudt_id": "GigaHZ",
        "observerd_property": "frequency", "wikidata_id": "Q11652"},
]


def perform_nel_unit_short(item):
    for nel_arr in nel_base:
        if nel_arr["short_unit"] == item:
            print("=====")
            print("FOUND:")
            print(f"short_unit: {nel_arr['short_unit']}, long_unit: {nel_arr['long_unit']}, qudt_id: {nel_arr['qudt_id']}, observerd_property: {nel_arr['observerd_property']}, wikidata_id: {nel_arr['wikidata_id']}")
            print("=====")

            break


def perform_nel_unit_long(item):
    for nel_arr in nel_base:
        if nel_arr["long_unit"] == item:
            print("=====")
            print("FOUND:")
            print(f"short_unit: {nel_arr['short_unit']}, long_unit: {nel_arr['long_unit']}, qudt_id: {nel_arr['qudt_id']}, observerd_property: {nel_arr['observerd_property']}, wikidata_id: {nel_arr['wikidata_id']}")
            print("=====")

            break


def perform_nel_property(item):
    # Assumes base unit, works if base unit is first entry in nel_base
    for nel_arr in nel_base:
        if nel_arr["observerd_property"] == item:
            print("=====")
            print("FOUND:")
            print(f"short_unit: {nel_arr['short_unit']}, long_unit: {nel_arr['long_unit']}, qudt_id: {nel_arr['qudt_id']}, observerd_property: {nel_arr['observerd_property']}, wikidata_id: {nel_arr['wikidata_id']}")
            print("=====")

            break

def remove_trailing_s(item):
    # Remove trailing s
    pattern = r'(?<!^.)s$'
    return re.sub(pattern, '', item)

def clear_number(item):
    # Remove number and whitespace
    pattern = r'[0-9\s\[\]\(\)\{\}]'
    return re.sub(pattern, '', item)


doc = nlp(test_sentence)
for ent in doc.ents:

    if ent.label_ == "UNIT_SHORT":
        unit = clear_number(ent.text)
        unit = remove_trailing_s(unit)
        perform_nel_unit_short(unit)

    elif ent.label_ == "UNIT_LONG":
        unit = clear_number(ent.text)
        unit = remove_trailing_s(unit)
        perform_nel_unit_long(unit)

    elif ent.label_ == "OBSERVABLE_PROP":
        unit = clear_number(ent.text)
        unit = remove_trailing_s(unit)
        perform_nel_property(unit)