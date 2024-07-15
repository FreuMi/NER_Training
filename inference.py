import ner

test_sentence = "Vibration (KHz) - normal 1 kHz, +/- 2%"

result = ner.inference(test_sentence.lower())

if ner == None:
    print("No units found!")   

print(result)