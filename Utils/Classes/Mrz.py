from Classes.Fields import Fields

class Mrz(Fields):
	def __init__(self, line = ""):
		Fields.__init__(self, line)

	def mean_length(words):
		mean_lengths=[]
		max_occur=0
		mean_length=0
		for word in words:
			if word != "-1":
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

	def mean_word(words, scores):
		mean_len = Mrz.mean_length(words)
		final_word = ""
		for i in range(mean_len):
			chars = Fields.score(i,mean_len,words,scores)
			print(chars)
			max_val=-1
			key=""
			for c in chars:
				if ((c == "<" or c=="(" or c == "[" or c == "{") and chars[c]>0.5):
					key = "<"
					break
				elif ((c == "S" or c == "C") and ( i-1 >= 0 and len(final_word) !=0) and (final_word[i-1] == "<")):
					key = "<"
					break
				elif chars[c]>=max_val:
					max_val=chars[c]
					key = c
			final_word = final_word + key
		return final_word
