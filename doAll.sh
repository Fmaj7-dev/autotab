#/bin/bash
python main.py generate_dataset ../guitar_dataset/dataset/source/ ../guitar_dataset/dataset/notes/
python main.py process_dataset ../guitar_dataset/dataset/notes/
python main.py train
python main.py trainNN
# python main.py classify ../guitar_dataset/dataset/test/e2_9.wav
