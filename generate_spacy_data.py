import prepare_data
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import sys

# Define a function to create spaCy DocBin objects from the annotated data
def get_spacy_doc(data):
  # Create a blank spaCy pipeline
  nlp = spacy.blank('en')
  db = DocBin()

  cnt = 0
  
  # Iterate through the data
  for text, annot in tqdm(data):  
    doc = nlp.make_doc(text)
    annot = annot['entities']

    ents = []
    entity_indices = []

    # Extract entities from the annotations
    for start, end, label in annot:
      skip_entity = False
      for idx in range(start, end):
        if idx in entity_indices:
          skip_entity = True
          break
      if skip_entity:
        continue

      entity_indices = entity_indices + list(range(start, end))
      try:
        span = doc.char_span(start, end, label=label, alignment_mode='contract')
      except Exception as e:
        print(f"Exception: {e}")
        continue

      if span is None:
          # Log errors for annotations that couldn't be processed
          print(f"Error: Span is None for text: '{text}'")
          print(f"Start: {start}, End: {end}, Text Cut: '{text[start:end]}', Label: {label}")
          cnt += 1
          continue 
      else:
          ents.append(span)

    try:
      doc.ents = ents
      db.add(doc)
    except:
      pass
    
  if cnt != 0:
    print("Errors preparing data:", cnt)
  return db


# Load data
training_data = prepare_data.prepare_data("./training_data/")

# Generate Object
#data_dict = {}
#data_dict["classes"] = ["UNIT_SHORT","OBSERVABLE_PROP","UNIT_LONG"]
#data_dict["annotations"] = training_data

# Split data
train, test = train_test_split(training_data, test_size=0.15)

db = get_spacy_doc(train)
db.to_disk("./train.spacy")
print("Saved training data to train.spacy")


db = get_spacy_doc(test)
db.to_disk("./test.spacy")
print("Saved test data to test.spacy")
