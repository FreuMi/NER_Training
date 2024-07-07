# Training Script for SemWoT

This repository contains a training script for a Named Entity Recognition (NER) Model that detects Units in Natural Language Annotations within Web of Things (WoT) Thing Descriptions.

## How to Train the Model

### Step 1: Install Requirements

To train the model, first install the necessary dependencies listed in `requirements.txt` by running the following command:

```sh
pip install -r requirements.txt
```

### Step 2: Start the Training Process

After installing the requirements, you can start the training process using the prebuilt datasets with SpaCy. Execute the following command to start the training:

```sh
./start_train.sh
```

### Step 3: Adding Your Own Data

If you want to train the model with your own data, you need to generate the train.spacy and test.spacy files. Run the following script to create these files:

```sh
python3 generate_spacy_data.py
```

### Step 4: Using the Trained Model

After training, you can use the trained model for inference. Run the following command to perform inference:

```sh
python3 inference.py
```

# Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# License

This project is licensed under the AGPL-3.0 License.
