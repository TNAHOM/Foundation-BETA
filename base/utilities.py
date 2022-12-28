
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

