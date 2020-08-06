from Classes.Fields import Fields

class Mrz(Fields):

	def mean_length(words):
		mean_lengths=[]
		max_occur=0
		mean_length=0
		for word in words:
			if str(word) != "-1":
				mean_lengths.append(len(word))
		for length in mean_lengths:
			if(length == 36):
				return  length
			if(max_occur<mean_lengths.count(length)):
				max_occur=mean_lengths.count(length)
				mean_length = length
		if(isinstance(mean_length,str)):
			mean_length = 0
		return mean_length


	def synthax_check(self):
		if len(self) != 36 or self.field == "-1":
			print("Warning: Incorrect data")
			return False
		return True

	def mean_word( words, scores):
		mean_len = Mrz.mean_length(words)
		final_word = ""
		for i in range(mean_len):
			chars = Fields.score(i,mean_len,words,scores)
			print(chars)
			max_val=-1
			key=""
			for c in chars:
				if((c == "<" and chars[c]>2)):
					key = "<"
					break
				if ((c=="(" or c == "[" or c == "{")):
					key = "<"
					break
				elif ((c == "S" or c == "C" or c=="k" or c=="K" or c =="E") and ( i-1 >= 0 and len(final_word) !=0) and (final_word[i-1] == "<")):
					key = "<"
					break
				elif chars[c]>=max_val:
					max_val=chars[c]
					key = c
			final_word = final_word + key
		return final_word
