#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path,os,logging,sh
from pydub import AudioSegment

class Ekho(object):
	logger = logging.getLogger("wechat")

	def __init__(self,words_audio_folder="words_audio"):
		super(Ekho, self).__init__()
		self.words_audio_folder = words_audio_folder
		
	def export_pronounces_wav(self, wavfilepath, words):
		return sh.ekho("-v", "Cantonese", "-o", wavfilepath, words)
	
	def get_pronounces_mp3(self, result, playback_speed=None):
		pronounce_list = result.pronounce_list
		words = result.words
		filename = ""
		for pronounce in pronounce_list:
			if pronounce:
				filename += pronounce
		if "" == filename:
			return None	
		filepath = os.path.join(self.words_audio_folder,filename)
		mp3filepath = filepath+".mp3"
		mp3_exist = os.path.isfile(mp3filepath)
		if mp3_exist:
			return mp3filepath
		else:
			wavfilepath = filepath+".wav"
			wav_exist = os.path.isfile(wavfilepath)
			if not wav_exist:
				self.export_pronounces_wav(wavfilepath, words)

			wavAudio = AudioSegment.from_wav(wavfilepath)
			wavAudio.export(mp3filepath, format="mp3")

			if playback_speed:
				mp3Audio = AudioSegment.from_wav(mp3filepath)
				mp3Audio = speedup(mp3Audio,playback_speed)
				mp3Audio.export(mp3filepath, format="mp3")
			return mp3filepath

def main():
	ekho = Ekho(".")
	r = ekho.export_pronounces_wav("test.wav",u"我喜欢你")
	print r

if __name__ == '__main__':
	main()
