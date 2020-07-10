from Classes.Fields import Fields

class First_name(Fields):

	def extract(self , line):
		name="-1"
		if ("Pren" in line or "preno" in line or "Prenom" in line or "Pre" in line):
			name = line.split(":")[len(line.split(":"))-1]
		names= name.split(" ")
		fname= ""
		l = len(names)
		j = 0
		while(j<l):
			word=names[j]
			#cleaning unnecessary words and spaces from the line
			if("Pren" in word or "preno" in word or "Prenom" in word or "Pre" in word):
				names[j]=""
			if(names[j]==""):
				names.pop(j)
				j=j-1
				l=l-1
			else:
				if ("-1" not in names[j]):
					#clean the unnecessary caracters from the extracted name(s)
					for i in range(len(names[j])):
						if ((names[j][i]<'a'or names[j][i]>'z') and (names[j][i]<'A'or names[j][i]>'Z') and (names[j][i] != '-')):
							word=word.replace(names[j][i],"")
					if word != "":
						fname = fname + word + " "
				else:
					name = "-1"
			j=j+1
		if fname =="":
			fname = "-1"
		if (fname !="-1"):
			if(fname[0]==" "):
				fname=fname.replace(fname[0],"")
			l=len(fname)
			i=l-1
			while(i<l):
				if((fname[i]<'a' or fname[i]>'z') and (fname[i]<'A' or fname[i]>'Z')):
					fname=fname[:i]
					l=len(fname)
					i=l-1
				else:
					break

		return self.set_field(fname)

	def word_to_mrz(self):
		result = ""
		for i in range(14):
			if i > len(self):
				result +="<"
			elif self[i] =="-":
				result += "<"
			elif self[i] == " ":
				result+="<<"
			else:
				result += self[i]
		return result[:14].upper()