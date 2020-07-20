import fitz
import sys






def pdf_convertion(input_file, output):
	"""
	convert a pdf input file into a pn.

	"input_file" is the path to the pdf file to convert.
	"output" is the name of the output file and should contain the .png extention.
	"""
	doc = fitz.open(input_file)
	page = doc.loadPage(0) #number of page
	pix = page.getPixmap()
	input_file = output
	pix.writePNG(input_file)

def query_yes_no(question, default="yes"):
	"""
	Ask a yes/no question via input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is True for "yes" or False for "no".
	"""
	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	if default is None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")