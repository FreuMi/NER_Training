python generate_spacy_data.py
python -m spacy init fill-config base_config.cfg config.cfg
python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./test.spacy --gpu-id 0