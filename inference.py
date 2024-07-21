import ner

test_sentence = "The current temperature in celsius value."

result = ner.inference(test_sentence.lower())

if ner == None:
    print("No units found!")   

print(result)