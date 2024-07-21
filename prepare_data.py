
import os
import sys

# New classes added
classes = ["OBSERVABLE_PROP","UNIT_SHORT","UNIT_LONG"]

# units in long format
unit_long_arr_frequency = ["hertz", "kilohertz", "megahertz", "gigahertz"]
unit_long_arr_time = ["second", "millisecond", "microsecond", "nanosecond"]
unit_long_arr_mass = ["gram", "grams", "ton", "tons", "kilograms", "kilogram"]
unit_long_arr_temperature = ["celsius", "degree celsius", "celsius", "degree celsius"]
unit_long_arr_percent = ["percent"]
unit_long_arr_length = ["meter", "kilometer", "millimeter", "nanometer", "micrometer"]
unit_long_arr_acceleration = ["g-force"]
unit_long_arr_humidity = []



# units in short format
unit_short_frequency = ["hz", "khz", "mhz", "ghz"]
unit_short_time = ["s", "ms", "µs", "ns"]
unit_short_mass = ["g", "kg", "t"]
unit_short_temperature = ["°C"]
unit_short_percent = ["%"]
unit_short_arr_length = ["m", "km", "mm", "nm", "µm"]
unit_short_arr_acceleration = ["g", "gs"]
unit_short_arr_humidity = []


# oberservable properties
property_frequency = ["frequency"]
property_time = ["time", "times"]
property_mass = ["mass", "weight", "weights", "weighs"]
property_temperature = ["temp", "temps", "temperature", "temperatures"]
property_percent = []
property_length = ["distance", "length"]
property_acceleration = ["acceleration","accelerationx", "accelerationy", "accelerationz"]
property_humidity = ["humidity", "humid"]



# Generate Array
unit_long_arr = unit_long_arr_frequency + unit_long_arr_time + unit_long_arr_mass + unit_long_arr_temperature + unit_long_arr_percent +\
    unit_long_arr_length + unit_long_arr_acceleration + unit_long_arr_humidity 
    
unit_short_arr = unit_short_frequency + unit_short_time + unit_short_mass + unit_short_temperature + unit_short_percent + unit_short_arr_length +\
    unit_short_arr_acceleration + unit_short_arr_humidity
    
property_arr = property_frequency + property_time + property_mass + property_temperature + property_percent +\
    property_length + property_acceleration + property_humidity

def get_word_type(word, sentence):     
    for propertyElement in property_arr:
        if propertyElement in word:
            return "OBSERVABLE_PROP"
        
    for unit_long in unit_long_arr:
        if unit_long in word:
            return "UNIT_LONG"
        
    for unit_short in unit_short_arr:
        if unit_short in word:
            return "UNIT_SHORT"
        
    print("Error detecting type!")
    print(f"Sentence: {sentence}")
    print(f"Word: {word}")
    sys.exit()


def find_word_indexes(sentence, word_arr):
    #print("sentence:", sentence, "word", word_arr)
    if len(word_arr) == 1:
        word = word_arr[0]
        # Determine Type
        word_type = get_word_type(word, sentence)
        # Get index
        start_index = sentence.find(word)
        if start_index == -1:
            # Word not found in sentence
            print(f"Word: {word} not found in:")
            print(sentence)
            sys.exit()
        end_index = start_index + len(word)
        #input([sentence, {"entities":[[start_index,end_index, word_type]]}])
        return [sentence, {"entities":[[start_index,end_index, word_type]]}]

    else:
        word_indexes = []

        # iterate over all words
        for word in word_arr:
            # Determine Type
            word_type = get_word_type(word, sentence)
            # Get index
            start_index = sentence.find(word)
            if start_index == -1:
                # Word not found in sentence
                print("Word not found in sentence!")
                print("Sentence:", sentence)
                print("Word:", word)
                sys.exit()
            end_index = start_index + len(word)
            word_indexes.append([start_index,end_index, word_type])
        
        #input([sentence, {"entities": word_indexes}])
        return [sentence, {"entities": word_indexes}]

def get_all_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths


def prepare_data(path):
    result_array = []
    file_paths = get_all_filepaths(path)
    for file_path in file_paths:
        print(f"Processing {file_path} ...")
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(";")
                reference_words = []
                for i in range(len(parts)):
                    if i == 0:
                        input_sentence = parts[0].strip()
                    else:
                        reference_words.append(parts[i].strip())

                result = find_word_indexes(input_sentence, reference_words)

                result_array.append(result)

    print("Preprocssing finished")
    return result_array
