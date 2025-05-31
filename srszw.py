import pypinyin as pypy
import pypinyin.contrib.tone_convert as pypytc
import json
import random as rd

# 加载配置文件
config = json.load(open("config.json", "r", encoding="utf-8"))
YunMuSplit = json.load(open(config["yunMuSpliting"], "r", encoding="utf-8"))
shengDiao = json.load(open(config["shengDiao"], "r", encoding="utf-8"))
zhengTiRenDu = json.load(open(config["zhengTiRenDu"], "r", encoding="utf-8"))
shengYun = json.load(open(config["shengYun"], "r", encoding="utf-8"))
kana = json.load(open("kana.json", "r", encoding="utf-8"))
charactors = []
for i in config["loaded_charactor_lists"]:
	charactors.append(json.load(open(i, "r")))
project = json.load(open(config["file"], "r", encoding="utf-8"))

def randLen():
	global config
	return (config["lengthRandom"]*2)*rd.random()-config["lengthRandom"]

def randPit():
	global config
	return (config["pitchRandom"]*2)*rd.random()-config["pitchRandom"]

def getShengYun(pinyin: str):
	"获取声韵"
	global config, YunMuSplit, zhengTiRenDu
	result = [None]
	try:
		result = zhengTiRenDu[pypytc.to_normal(pypytc.to_normal(pinyin))]
		return result
	except KeyError:
		# print("非整体认读音节")
		...
	result[0] = pypytc.to_initials(pinyin, strict=config["noYW"])
	# print(pinyin, pypytc.to_finals(pinyin, strict=True))
	result += YunMuSplit[pypytc.to_finals(pinyin.replace("ju","jv").replace("qu","qv").replace("xu","xv").replace("yu","yv")
		, strict=False)]
	# print(result)
	return result

def firstVowel(convertInfo: list):
	if type(convertInfo[1][0]) == dict:
		return convertInfo[1][1]
	else:
		return convertInfo[1][0]

def convertToMoras(convertInfo: list):
	"将声韵转换为日语音节"
	global kana
	result = []
	if convertInfo[0]:
		for i in range(len(convertInfo[0])):
			# print(convertInfo[0], i)
			result.append({})
			result[-1]["consonant"] = convertInfo[0][i][0]
			result[-1]["consonantLength"] = convertInfo[0][i][2] + randLen()
			if convertInfo[0][i][1]:
				result[-1]["vowel"] = convertInfo[0][i][1]
				result[-1]["vowelLength"] = convertInfo[0][i][3] + randLen()
			else:
				# print(convertInfo,i)
				result[-1]["vowel"] = firstVowel(convertInfo)[1]
				result[-1]["vowelLength"] = convertInfo[0][i][3] + randLen()\
					if convertInfo[0][i][3] else firstVowel(convertInfo)[3] + randLen()
			result[-1]["text"] = kana[result[-1]["consonant"]+result[-1]["vowel"]]
	if type(convertInfo[1][0]) == dict:
		loopTimes = convertInfo[1][0]["loop"]
	else:
		loopTimes = 1
		convertInfo[1] = [[]]+convertInfo[1]
	for i in range(loopTimes):
		for j in range(1, len(convertInfo[1])):
			if i==0 and j == 1 and convertInfo[0] and not convertInfo[0][-1][1]:
				continue
			if convertInfo[1][j][-1] == "Bridge" and not convertInfo[0]:
				continue
			result.append({})
			if convertInfo[1][j][0]:
				result[-1]["consonant"] = convertInfo[1][j][0]
				result[-1]["consonantLength"] = convertInfo[1][j][2] + randLen()
			result[-1]["vowel"] = convertInfo[1][j][1]
			result[-1]["vowelLength"] = convertInfo[1][j][3] + randLen()
			try:
				result[-1]["text"] = kana[result[-1]["consonant"]+result[-1]["vowel"]]
			except KeyError:
				result[-1]["text"] = kana[result[-1]["vowel"]]
	# print(result)
	return result

def convertToAccentPhraseWithoutPitch(sy: list):
	global shengYun
	convertInfo = [
		shengYun["shengmu"][sy[0]] if sy[0] else None,
		shengYun["yunmu"][sy[1]],
		shengYun["yunmu"][sy[2]],
		shengYun["yunmu"][sy[3]]
	]
	result = {}
	result["moras"] = convertToMoras(convertInfo[0:2])\
		+convertToMoras([None,convertInfo[2]])\
		+convertToMoras([None,convertInfo[3]])
	result["accent"] = 1
	result["isInterrogative"] = False
	# print(result)
	return result

def toneToPitch(tone: int, step: float):
	"声调转成音高"
	global shengDiao, config
	tone -= 1
	if step < 0.5:
		pitchStep = (shengDiao[tone][0] + (shengDiao[tone][1] - shengDiao[tone][0])*step*2 - 1)/4
		# print(f"{shengDiao[tone][0]}+({shengDiao[tone][0]}-{shengDiao[tone][1]})*{step}*2-1/4={pitchStep}")
	else:
		pitchStep = (shengDiao[tone][1] + (shengDiao[tone][2] - shengDiao[tone][1])*(step-0.5)*2 - 1)/4
	pitch = (((config["pitchRange"][1] - config["pitchRange"][0]) * pitchStep) + config["pitchRange"][0]) + randPit()
	# print(tone, pitch, step, pitchStep)
	return pitch

def addPauseMora(accentPhrase: list):
	"添加停顿"
	accentPhrase["pauseMora"] = {
		"text": "、",
		"vowel": "pau",
		"vowelLength": 0.3 + randLen(),
		"pitch": 0
	}
	return accentPhrase

def addPitch(moras: list, tone: int):
	"添加音高"
	global shengDiao, config
	result = moras
	for i in range(len(moras)):
		if tone == 5:
			# print(i, result[i])
			result[i]["vowelLength"] *= 0.6
			# print(result[i])
		step = (i) / (len(moras)-1)
		# print(i, len(moras)-1, step, tone)
		result[i]["pitch"] = toneToPitch(tone, step)
		#result[i]["pitch"] = 6.0 + randPit()
	return result

def ziToPinyin(zi: str):
	return (" ".join(pypy.lazy_pinyin(zi, style=pypy.Style.TONE3, strict=False, neutral_tone_with_five=True, tone_sandhi=True)))\
		.split(" ")

def generateKey():
	return "600a4233-{:0>4x}-{:0>4x}-{:0>4x}-{:0>12x}".format(rd.randint(0, 0xffff), rd.randint(0, 0xffff), rd.randint(0, 0xffff), rd.randint(0, 0xffffffffffff))

def converting(project: dict):
	global charactors
	vvproj = {}
	vvproj["appVersion"] = project["app_version"]
	vvproj["song"] = {"tpqn": 480,"tempos": [{"position": 0,"bpm": 120}],"timeSignatures": [{"measureNumber": 1,"beats": 4,"beatType": 4}],"tracks": {"725cfeb6-b161-49d3-b301-1042bceea90b": {"name": "無名トラック","singer": {"engineId": "074fc39e-678b-4c13-8916-ffca8d505d1d","styleId": 3002},"keyRangeAdjustment": -4,"volumeRangeAdjustment": 0,"notes": [],"pitchEditData": [],"solo": False,"mute": False,"gain": 1,"pan": 0}},"trackOrder": ["725cfeb6-b161-49d3-b301-1042bceea90b"]}
	vvproj["talk"] = {}
	talk = project["talk"]
	vvproj["talk"]["audioKeys"] = []
	vvproj["talk"]["audioItems"] = {}
	for i in talk:
		key = generateKey()
		vvproj["talk"]["audioKeys"].append(key)
		vvproj["talk"]["audioItems"][key] = {}
		vvproj["talk"]["audioItems"][key]["text"] = str(i["text"]["zi"])
		print(i)
		for j in charactors:
			try:
				charactorId = j[i["charactor"]]["id"]
				styleId = j[i["charactor"]]["styles"][i["style"]] if i["style"] else j[i["charactor"]]["normalstyle"]
				engineId = j["engine_id"]
				break
			except KeyError:
				print("未找到角色："+i["charactor"])
				continue
		vvproj["talk"]["audioItems"][key]["voice"] = {
			"engineId": engineId,
			"speakerId": charactorId,
			"styleId": styleId,
			"presetKey": generateKey()
		}
		vvproj["talk"]["audioItems"][key]["query"] = {
				"accentPhrases": [],
				"speedScale": i["speedScale"],
				"pitchScale": i["pitchScale"],
				"intonationScale": i["intonationScale"],
				"volumeScale": i["volumeScale"],
				"prePhonemeLength": i["prePhonemeLength"],
				"postPhonemeLength": i["postPhonemeLength"],
				"pauseLengthScale": i["pauseLengthScale"],
				"outputSamplingRate": 48000,
				"outputStereo": False,
				"kana": ""
			}
		accentPhrases = []
		if i["text"]["pinyin"]:
			pinyin = i["text"]["pinyin"].split(" ")
			print("使用拼音")
			print(pinyin)
		else:
			pinyin = ziToPinyin(i["text"]["zi"])
			print("使用汉字")
			print(i["text"]["zi"])
			print(pinyin)
		print("=================================================================================")
		for j in range(len(pinyin)):
			# print(pinyin[j], pinyin[j] in ",./<>?:;'\"[]{}!@#$%^&*()_+~`=-|\\，。《》？：；‘’“”【】！￥……（）——+｜\\·「」、")
			if pinyin[j] in ",./<>?:;'\"[]{}!@#$%^&*()_+~`=-|\\，。《》？：；‘’“”【】！￥……（）——+｜\\·「」、":
				addPauseMora(accentPhrases[-1])
			else:
				shengYun = getShengYun(pinyin[j])
				accentP = convertToAccentPhraseWithoutPitch(shengYun)
				accentP["moras"] = addPitch(accentP["moras"], int(pinyin[j][-1]))
				accentPhrases.append(accentP)
		vvproj["talk"]["audioItems"][key]["query"]["accentPhrases"] = accentPhrases
	return vvproj

def main():
	global config, project
	vvproj = converting(project)
	with open(config["output"], "w", encoding="utf-8") as f:
		json.dump(vvproj, f, ensure_ascii=False)
	return 0

if __name__ == "__main__":
	main()