import moviepy.editor as mp
import re
import gpt_2_simple as gpt2
import moviepy.audio.fx.all as afx
import json
import random
from pydub import AudioSegment
from moviepy.video.tools.subtitles import SubtitlesClip
import os
from astronautVoice import generateSpeech

class generator:

	def __init__(self):
		collections = self.generate()
		for i in collections:
			model = generateSpeech(i["author"],i["text"])
			model.dlVoice()
		self.video()

	def getDict(self,text):
		dialog = []
		pattern = r"(\w+).*:\n(.*)"
		matches = re.finditer(pattern,text,re.MULTILINE)
		for match in matches:
			dialog.append({"author":match.group(1),"text":match.group(2)})
		return dialog

	def generate(self):
		sess = gpt2.start_tf_sess()
		gpt2.load_gpt2(sess,run_name="space")
		text = gpt2.generate(sess,run_name="space", return_as_list=True)[0]
		return self.getDict(text)

	def generateSRT(self,texts,durations):
		start = 0
		string = ""
		w = textwrap.TextWrapper(width=42,break_long_words=False,replace_whitespace=False)
		for i,text in enumerate(texts):
			text = "\n".join(w.wrap(text))
			shr = start // 3600
			start %= 3600 
			smn = start // 60
			start %= 60 
			ssc = start
			end = start+durations[i]
			ehr = end // 3600
			end %= 3600 
			emn = end // 60
			end %= 60 
			esc = end
			string += f"{i+1}\n{int(shr):02d}:{int(smn):02d}:{int(ssc):02d},000 --> {int(ehr):02d}:{int(emn):02d}:{int(esc):02d},000\n{text}\n\n"
			start = end
		with(open("subs.srt","w")) as f:
			f.write(string)

	def video(self):
		files = ["temp.mp3","overlay.mp3","noice.mp3","mixed_sounds.mp3","music.mp3","base.mp3","epic.mp4"]
		with open("./Voice/data.json") as f:
			coll = json.load(f)
		durations = []
		texts = [a["author"]+": "+a["text"] for a in coll]
		location = "./Assets/Audios/"+random.choice(os.listdir("./Assets/Audios"))
		baseAudio=[]
		for a in coll:
			pause = random.uniform(0,3)
			baseAudio.append(mp.AudioFileClip(a["filename"]))
			try:
				baseAudio.append(mp.AudioFileClip("./Assets/Audios/silence.wav").subclip(0,pause))
			except:
				pause = 0
			durations.append(a["duration"]+pause)
		self.generateSRT(texts,durations)
		epic = mp.concatenate_audioclips(baseAudio)
		totalDuration = epic.duration
		epic.write_audiofile("base.mp3")
		base = mp.AudioFileClip(location)
		start = random.randint(0,int(base.duration))
		base = base.set_start(start)
		base.subclip(start,start+totalDuration).volumex(0.1).audio_fadein(1).audio_fadeout(1).write_audiofile("noice.mp3")
		sound1 = AudioSegment.from_mp3("base.mp3")
		sound2 = AudioSegment.from_mp3("noice.mp3")
		output = sound1.overlay(sound2)
		output.export("mixed_sounds.mp3", format="mp3")
		audioclip = mp.AudioFileClip("mixed_sounds.mp3")
		clip = [mp.VideoFileClip("./Assets/Videos/"+a) for a in os.listdir("./Assets/Videos")]
		baseIndex = random.randint(0,len(clip))
		if clip[baseIndex].duration < totalDuration:
			mp.concatenate_videoclips([clip[baseIndex],clip[random.randchoice([a for i,a in enumerate(clip) if i!= baseIndex])]])
		else:
			clip = clip[baseIndex]
		generator = lambda txt: mp.TextClip(txt,color="yellow",font="Arial-Bold-Italic",fontsize=18,stroke_width=1,stroke_color="black")
		subtitles = SubtitlesClip("subs.srt", generator)
		final_clip = mp.CompositeVideoClip([clip, subtitles.set_pos(('center','bottom'))])
		final_clip.set_duration(sum(durations)).write_videofile("epic.mp4")
		video = final_clip.set_audio(audioclip).set_duration(totalDuration)
		video.write_videofile("nice.mp4")
		for file in files:
			os.remove(file)

if __name__ == '__main__':
	box = generator()