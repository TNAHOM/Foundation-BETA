<<<<<<< HEAD
from random import randint
=======
>>>>>>> parent of 16ee675 (Removed the qrcode and exam code added)
import qrcode

def squash(dicts):
	true_f = []
	fill = []
	choose = []
	for x, y in dicts.items():
		if y !='':
			if x[:4] == 'true':
				true_f.append(y)
			elif x[:4] == 'fill':
				fill.append(y)
			elif x[:7]=='choose_':
				choose.append(y)
	return true_f, fill, choose

def generate_qrcode(subject):
	qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, border=0, box_size=4)
	qr.add_data(subject)
	qr.make(fit=True)
	
	img = qr.make_image()
	return img

def remove_stuff(original, removed):
	chosen = original.translate({ord(letter): None for letter in f"{removed}"})
	return chosen