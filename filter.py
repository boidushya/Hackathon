import re

def filter(text):
	pattern = r"\n*\(GOSS NET \d+\) Tape \d+\/\d+ Page \d+"
	return re.sub(pattern,"",text)

def speaker(text):
	text = filter(text)
	pattern = r"((\d|\w){2}\s){4}(\w+)"
	match = re.match(pattern,text)
	if match:
		new = re.sub(pattern,f"{match.group(3)}:",text)
		return new
	else:
		return text

def filterTranscript():
	with open("./Transcripts/Apollo11.txt") as f:
		data = f.readlines()
		newData = [speaker(a.rstrip()) for a in data if a.strip()]
	with open("./Transcripts/Filtered/Apollo11.txt","w") as f:
		f.write("\n".join(newData))


def test():
	# text = "00 O0 08 19 CC"
	# match = re.match(r"((\d|\w){2}\s){4}(\w+)",text)
	# print(match.group(3))
	a = "           ".strip()
	if a:
		print("ok")
	else:
		print("uhhh")

if __name__ == '__main__':
# 	print(speaker("""
# 00 00 00 04 CDR
# Roger. Clock.

# 00 00 00 13 CDR
# Roger. We got a roll program.

# 00 00 00 15 CMP
# Roger. Roll.
# 		"""))
	filterTranscript()
	# test()
