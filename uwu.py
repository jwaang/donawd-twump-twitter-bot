import subprocess
from random import randint as rand

# https://upli.st/l/list-of-all-ascii-emoticons
convertedSentence = ""
positive_emoji = ["xD", "XD", ":3", "xP", "XP", ":D", "c:", "C:", ">:]", ">:)", "(~‾▿‾)~", "ᕕ( ᐛ )ᕗ", "(☞ﾟヮﾟ)☞", "•ᴗ•", "(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧", "( ˘ ³˘)♥", "(◕‿◕✿)", "٩( ᐛ )و", "(๑>◡<๑)", "(•̀ᴗ•́)و ̑̑", "(҂◡_◡) ᕤ", "ツ"]
negative_emoji = [">.<", ">:[", ">:o", ">:O", ">:(", ">_<", "-.-", "-_-", "T_T", "ᕙ(⇀‸↼‶)ᕗ", "ಠ_ಠ", "(╯°□°）╯︵ ┻━┻", "ಥ_ಥ", "(ง •̀_•́)ง", "o(╥﹏╥)o", "t(-.-'t)", ".·´¯`(>▂<)´¯`·.", "(ᗒᗣᗕ)՞", "(งಠᗝಠ)ง", "ᕕ(ᗒДᗕ)ᕗ", "(ಥ﹏ಥ)", "◕︵◕", "୧༼ಠ益ಠ༽", "٩(๑`ȏ´๑)۶", "o(>< )o"]
neutral_emoji = [":O", ":o", "o.o", "o_O", "¯\_(ツ)_/¯", "༼ つ ◕_◕ ༽つ", "ԅ(≖‿≖ԅ)", "(☉ ϖ ☉) ", "(づ￣ ³￣)づ", "¯\_(⊙_ʖ⊙)_/¯", "OwO"]
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

def convertWord(word):
	global convertedSentence, alphabet
	converted = ""
	doubleT = doubleT_Presence = th_Presence = False
	if '@' in word:
		converted += word
	elif '#' in word:
		converted += word
	elif '&amp;' in word:
		converted += '&'
	elif 'http://' in word or 'https://' in word:
		converted += word
	else:
		for i in range(len(word)):
			if doubleT or th_Presence:
				doubleT = th_Presence = False
				continue
			elif ((word[i] == "L" or word[i] == "l") and not doubleT_Presence) or (word[i] == "R" or word[i] == "r"):
				converted += "W" if word[i].isupper() else "w"
			elif (word[i] == "T" or word[i] == "t") and ((word[i + (1 if i + 1 < len(word) else 0)] == "T" or word[i + (1 if i + 1 < len(word) else 0)] == "t")):
				converted += ((("D" if word[i].isupper() else "d") + ("D" if word[i + 1].isupper() else "d")) if i + 1 < len(word) else "t") if word[i].islower() else "T"
				doubleT = doubleT_Presence = True if i + 1 < len(word) else False
			elif (word[i] == "T" or word[i] == "t") and ((word[i + (1 if i + 1 < len(word) else 0)] == "H" or word[i + (1 if i + 1 < len(word) else 0)] == "h")):
				converted += (("F" if word[i].isupper() else "f") if i + 2 == len(word) else "t") if word[i].islower() else "T"
				th_Presence = True if i + 2 == len(word) else False
			else:
				converted += word[i]
	convertedSentence += ((converted[0] + "-" + converted[0:]) if (rand(1, 10) == 1 and converted[0] in alphabet) else converted) + " "
	return convertedSentence

def convert(sentence):
	global convertedSentence
	convertedSentence = ""
	words = sentence.split(" ")
	for i in words:
		convertWord(i)
	return convertedSentence
	# if sentiment == 'positive':
	# 	return convertedSentence + positive_emoji[rand(0, len(positive_emoji)-1)]
	# elif sentiment == 'negative':
	# 	return convertedSentence + negative_emoji[rand(0, len(negative_emoji)-1)]
	# else:
	# 	return convertedSentence + neutral_emoji[rand(0, len(neutral_emoji)-1)]