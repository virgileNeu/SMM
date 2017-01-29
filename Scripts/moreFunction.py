import re
def check_date(date_string):
	#check if date is in "YYYY-MM-DD" format quickly
	return (len(date_string.split('-')) == 3)

#return a list of artists cleaned
def clean_artists(artists):
	result = []
	for s in artists:
		if(len(s) > 0):
			word_list = split_string(s)
			word_list = remove_parenthesis(word_list)
			word_list = remove_words(word_list)
			
			if(len(word_list) == 1):
				result.append(word_list[0])
			if(len(word_list) > 1):
				result.extend(word_list)
	return result
	
def split_string(string):
	result = []
	ss = string.split(',')
	for s in ss:
		tmp = s.strip('-.[\'\", +*?')
		
		if(len(tmp) >= 3):  #no groups with smaller name
			tmp2 = tmp.split('/')
			for w in tmp2:
				if(len(w) > 3):
					result.append(w.strip())
	return result
	
# remove parenthesis and text between them and check if balance parenthesis
# same with '[' and ']'
def remove_parenthesis(word_list):
	result = []
	for word in word_list:
		p_open = 0
		p_close = 0
		c_open = 0
		c_close = 0
		newword = ""
		for c in word:
			if(c == '('):
				p_open = p_open + 1
			elif(c == ')'):
				p_close = p_close + 1
			elif(c == '['):
				c_open = c_open + 1
			elif(c == ']'):
				c_close = c_close + 1
			elif(p_close == p_open and c_open == c_close):
				newword = newword + c
		newword = newword.strip() #remove spaces
		if(p_close <= p_open and c_close <= c_open and len(newword) > 3):
			result.append(newword) 
	return result

def remove_hours(string):
	pattern = r'\d{2}h\d{2}|\d{2}:\d{2}( - \d{2}:\d{2})?'
	t = re.search(pattern, string)
	res = string
	if(t!=None):
		try:
			res = string.replace(t.group(), '')
		except:
			print("Error on string : "+str(string))
	return res

def remove_words(word_list):
	forbidden_words = ["live", "CH", "UK", "DE", "TBA", "Chf", "Euro"]
	res = []
	for s in word_list:
		r = remove_hours(s)
		for f in forbidden_words:
			if f in r:
				r = r.replace(f, '')
		if(len(r) > 3):
			res.append(r.strip())
	return res

# return a tuple (address, location) 
def clean_location(address, location):
	resa = address
	resl = location
	if(len(location) == 0):
		#several possibilities:
		#1 <street>, <CP> <city>
		#2 <street>; <CP>, <city>
		#3 <street>, <CP> <city> (<canton>)
		#4 <canton>, <city>
		#5 <street>
		#6 <city>
		#7 <CP> <city>
		tmp = address.split(',')
		if(len(tmp) > 0): #1, 2, 3, 4
			if(tmp[0].contains(';')): #2
				tmp = tmp[1].split[',']
				resl = ' '.join(tmp[1:-1])
			else	:
				tmp = tmp[1]
				if(tmp[3].isdigit()): #1 3
					tmp = tmp.split(' ')
					if(tmp.contains('(') and tmp.contains(')')): #3
						resl = ' '.join(tmp[1:-2])
					else: #1
						resl = ' '.join(tmp[1:-1])
				else: #4
					resl = tmp
		elif(address[3].isdigit()): #7
			tmp = address.split(' ')
			resl = ' '.join(tmp[1, -1])
		elif(address[-1].isdigit()): #5
			return (None, None)
		#nothing to do for 6
	elif(location[0].isdigit()):
		resl = ' '.join(location.split(' ')[1:])
	elif(location[0:1]=='CP'):
		resl = location.split(' ')[-1]
	return (resa, resl)
