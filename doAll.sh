#/bin/bash

# split files and store them in train folder
python main.py generate_dataset ../guitar_dataset/source/ ../guitar_dataset/train/

# process all notes and store each as array
python main.py process_dataset ../guitar_dataset/train/

# train my own method
python main.py train

# train NN
python main.py trainNN

# example of running a test
# python main.py classify ../guitar_dataset/dataset/test/e2_9.wav

# analyze a song
#python main.py analyze ../guitar_dataset/songs/chispa.wav
