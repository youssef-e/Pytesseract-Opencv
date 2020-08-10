
class Fields:
	def __init__(self, line = ""):
		"""Create a Fields objetc that contain a single string when the object is created"""
		self.field = line

	def __str__(self):
		return self.field

	def __len__(self):
		return len(self.field)

	def __contains__(self, nom):
		return nom in self.field

	def __getitem__(self, index):
		return self.field[index]

	def extract(self, line):
		pass

	def set_field(self, line):
		self.field = line
		return self

	def clean_alphanum(line,replacement = ""):
		word = line
		result =""
		for c in line:
			if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c != '<') and (c <'0' or c >'9')):
				word=word.replace(c,replacement)
		result = result + word
		return result

	def synthax_check(self):
		if len(self) < 2 or self.field == "-1":
			print("Warning: Incorrect data")
			return False
		return True

	def mean_length(words):
		mean_lengths=[]
		max_occur=0
		mean_length=0
		if len(mean_lengths) <= 1:
			mean_lengths = []
			for i,word in enumerate(words):
				if str(word) != "-1":
					mean_lengths.append(len(word))
		for length in mean_lengths:
			if(max_occur < mean_lengths.count(length)):
				max_occur = mean_lengths.count(length)
				mean_length = length
			if(isinstance(mean_length,str)):
				mean_length = 0
		return mean_length

	def score(i,mean_len,words, scores):
		chars={}
		for j,word in enumerate(words):
			if len(word) == mean_len:
					if j in scores:
						if word[i] in chars:
							chars[word[i]] += scores[j]
						else:
							chars[word[i]] = scores[j]

					else:
						if word[i] in chars:
							chars[word[i]] += 0.5
						else:
							chars[word[i]] = 0.5
		return chars

	def mean_word(words, scores):
		mean_len = Fields.mean_length(words)
		final_word = ""
		for i in range(mean_len):
			chars=Fields.score(i,mean_len,words,scores)
			print(chars)
			max_val=-1
			key=""
			for c in chars:
				if chars[c]>=max_val:
					max_val=chars[c]
					key = c
			final_word = final_word + key
		return final_word

	def word_to_mrz(self):
		return self.field