from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException 
import os
import time
import uuid
from gtts import gTTS
import wave
import contextlib
import json
from shutil import copyfile
import time

class generateSpeech:
	def __init__(self,voice,text="Okay. NOUN 71: we used 30 and 37, four balls 1; NOUN 93: plus 00016, plus 00033, plus 00152; GET 00 48 15; check star 34. Over."):
		PITCH = {
			"CDR":"-0.44",
			"CC":"-0.5",
			"CMP":"-0.5",
			"LMP":"-0.37",
		}
		LANG = {
			"CDR":"en-ca",
			"CC":"en-us",
			"CMP":"en-ie",
			"LMP":"en-uk"

		}
		self.pitch = PITCH[voice] if voice in PITCH else "0"
		self.lang = LANG[voice] if voice in LANG else "en-us"
		self.filename = f"{uuid.uuid4().hex}.wav"
		self.text = text
		self.voice = voice

	def genSpeech(self,text):
		tts = gTTS(text, lang=self.lang)
		tts.save("temp.mp3")

	def getDuration(self,filename):
		with contextlib.closing(wave.open(filename,'r')) as f:
			frames = f.getnframes()
			rate = f.getframerate()
			duration = frames / float(rate)
		return duration

	def writeJSON(self):
		time.sleep(1)
		try:
			value = {
				"filename" : f"./Voice/{self.filename}",
				"author" : self.voice,
				"text" : self.text,
				"duration" : self.getDuration(f"./Voice/{self.filename}"),
			}
		except EOFError: #epic error handling time :)
			value = {
				"filename" : f"./Voice/{self.filename}",
				"author" : self.voice,
				"text" : self.text,
				"duration" : self.getDuration(f"./Voice/{self.filename}"),
			}
		with open("./Voice/data.json",encoding="utf-8") as f:
			data = json.load(f)
			data.append(value)
		with open("./Voice/data.json","w",encoding="utf-8") as f:
			json.dump(data,f, ensure_ascii=False, indent=4)

	def dlVoice(self):
		self.genSpeech(self.text)
		url = "https://voicechanger.io/voicemaker/#!/{%22effects%22:[{%22name%22:%22anonymous%22,%22params%22:{%22distortion%22:28,%22noiseMod%22:10,%22oscFreq%22:1}},{%22name%22:%22compressor%22,%22params%22:{%22threshold%22:-1,%22makeupGain%22:1,%22attack%22:1,%22release%22:0,%22ratio%22:4,%22knee%22:5,%22automakeup%22:1}},{%22name%22:%22astronaut%22,%22params%22:{%22distortion%22:119,%22lowPassFreq%22:2621,%22highPassFreq%22:470}},{%22name%22:%22pitchShift%22,%22params%22:{%22shift%22:"+self.pitch+"}}],%22version%22:1}"
		options = webdriver.ChromeOptions()
		options.add_argument("--ignore-certificate-errors")
		options.add_argument("--headless")
		options.add_argument("--test-type")
		options.add_argument("'--no-sandbox")
		options.add_experimental_option("prefs", {
					"profile.default_content_settings.popups": 0,
					"download.default_directory": os.getcwd()+"/",
					"directory_upgrade": True
				})
		options.add_experimental_option("excludeSwitches", ['enable-logging'])
		try:
			driver = webdriver.Chrome(options=options)
		except WebDriverException:
			return
		driver.get(url)
		upload = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/div[3]/div[1]/div/div[2]/div/div[1]/input")))
		upload.send_keys(os.getcwd()+"/temp.mp3")
		audio = WebDriverWait(driver,120).until(EC.element_to_be_clickable((By.XPATH,"//*[@id=\"output-audio-tag\"]")))
		WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id=\"download-output-audio-link\"]/button"))).click()
		while True:
			if os.path.exists("output.wav"):
				copyfile("output.wav",f"./Voice/{self.filename}")
				# os.remove("temp.mp3")
				break
		self.writeJSON()
		os.remove("output.wav")
		return f"./Voice/{self.filename}"

if __name__ == '__main__':
	model = generateSpeech("CDR",text="Roll's complete and the pitch is programed.")
	generate = model.dlVoice()
	# playsound(generate)