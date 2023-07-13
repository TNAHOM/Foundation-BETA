import qrcode
from random import randint

def squash(dicts):
	fill = []
	ans_tf = []
	ans_other = []
	ans_ch = []
	for x, y in dicts.items():
		if y !='':
			if x[:6] == 'ans_tf':
				if y == 'true':
					ans_tf.append('T')
				elif y == 'false':
					ans_tf.append('F')
			# IF INPUT TEXT IS GIVEN
			elif x[:5] == 'other':
				ans_other.append(y.upper())
			elif x[:6] == 'ans_ch':
				ans_ch.append(y[0].upper())
			elif x[:4] == 'fill':
				fill.append(y.upper())
	# print(fill, 'fill')
	# print(ans_tf, 'tf')
	# print(ans_other, 'match')
	# print(ans_ch, 'choose')
	return fill, ans_tf, ans_other, ans_ch

def generate_qrcode(subject, side):
	qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, border=0, box_size=3)
	info = subject, side
	qr.add_data(info)
	qr.make(fit=True)
	
	img = qr.make_image()
	return img

def remove_stuff(original, removed):
	chosen = original.translate({ord(letter): None for letter in f"{removed}"})
	return chosen

def exam_code(code_list):
	while True:
		exam_id_list=''
		for x in range(5):
			exam_id_list+=str(randint(1, 5))
			
		exam_code_f = ''
		exam_code_f+=exam_id_list
		exam_code_f+='1'
		
		exam_code_b = ''
		exam_code_b += exam_id_list
		exam_code_b += '2'
		# print(len(code_list))
		print(int(exam_code_f), int(exam_code_b), type(code_list))
		if type(code_list) is list:
			if int(str(exam_code_f)[:-1]) not in code_list:
				return int(exam_code_f), int(exam_code_b)
		elif type(code_list) is int:
			print('------')
			if int(str(exam_code_f)[:-1]) != code_list:
				return int(exam_code_f), int(exam_code_b)
		# elif code_list
		