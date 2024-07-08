import ner
        
test_sentence = "Frequency in kHz with +- 1%"

result = ner.inference(test_sentence)

if ner == None:
    print("No units found!")   

print(result[0])