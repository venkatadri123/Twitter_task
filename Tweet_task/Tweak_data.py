import os
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

os.chdir(os.path.dirname(os.path.realpath(__file__)))
keyword = input('Enter keyword: ')
print('Started'.center(100, '*'))
try:
    os.system(
        'python Tweat.py & python Streaming.py {}'.format(keyword))
except KeyboardInterrupt:
    os.system('pkill -9 python')