import fitz






def pdf_convertion(input_file, output):
    doc = fitz.open(input_file)
    page = doc.loadPage(0) #number of page
    pix = page.getPixmap()
    input_file = output
    pix.writePNG(input_file)
