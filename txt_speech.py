import re
import wave
import _thread
import time
import pyaudio

class TextToSpeech:
    CHUNK = 1024
    def __init__(self, words_pron_dict:str = 'words.txt'):
        self._l = {}
        self._load_words(words_pron_dict)

    def _load_words(self, words_pron_dict:str):
        with open(words_pron_dict, 'r') as file:
            for line in file:
                line = line.rstrip()
                if not line.startswith(';;;'):
                    key, val = line.split(',',2)
                    self._l[key] = re.findall(r"[A-Z\a-z\_]+",val)

    def get_pronunciation(self, str_input):
        list_pron = []
        for word in re.findall(r"[\w']+",str_input):
            if word in self._l:
                list_pron += self._l[word]
        print(list_pron)
        delay=0
        for pron in list_pron:
            _thread.start_new_thread(TextToSpeech._play_audio,(self, pron, delay))
            delay += 0.145

    def _play_audio(self, sound, delay):
        try:
            time.sleep(delay)
            wf = wave.open("sounds/"+sound+".wav", 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            data = wf.readframes(TextToSpeech.CHUNK)
            while data:
                stream.write(data)
                data = wf.readframes(TextToSpeech.CHUNK)
            stream.stop_stream()
            stream.close()
            p.terminate()
            return
        except:
            pass

    
    def spl_inp(self, str_input):
        self.str_input = str_input.upper()
        str_split = []

        cons = 'BCDFGHJKLMNPQRSTVWXYZ'
        vow = 'AEIOU'

        cur = 0
        nxt = 1
        
        while cur <= len(str_input) - 2:
            if str_input[cur] in cons and str_input[nxt] in vow:
                syl = ''+ str_input[cur] + str_input[nxt] + 'n'
                cur = nxt + 1
            elif str_input[cur] in cons and str_input[nxt] in cons: 
                syl = '' + str_input[cur] + 'n'
                cur = nxt
            elif str_input[cur] in vow:
                syl = '' + str_input[cur] + 'n'
                cur = nxt
            elif str_input[cur] in cons and str_input[nxt] not in cons and str_input[nxt] not in vow:
                syl = '' + str_input[cur] + 'n'
                cur = nxt
            str_split.append(syl)
            nxt = cur + 1
        return(str_split)

if __name__ == '__main__':
    tts = TextToSpeech()
    while True:
        tts.get_pronunciation(input('Enter a word or phrase: '))

        #tts.get_pronunciation(us_input)
