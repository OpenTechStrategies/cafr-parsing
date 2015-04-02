# This file contains helper methods to use pdfminer

## DISCLAIMER: This code is written to test ideas as fast as possible.
## This means that it is actually pretty terribly organized -- files are created in one method and deleted in another, nothing is encapsulated. Etc.
## Learn no lessons from this code (aside from how to perform the tasks being performed)
## Once a valid strategy is vetted and agreed on, the code will be refactored to follow actual best practices


import ntpath
import json
import re
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

def generate_pdf_text (pdf_path):
    """Open the pdf document, convert it to text, and return a filepath that contains the result"""

    # Set up input options
    password = ''
    pagenos = set()
    maxpages = 0

    # Set up output options
    imagewriter = None
    rotation = 0
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()

    # Set up the output file
    outfile = "parseme/processing/" + ntpath.basename(pdf_path) + ".txt"
    outfp = file(outfile, 'w')

    #
    rsrcmgr = PDFResourceManager(caching=caching)
    
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)
    
    fp = file(pdf_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                  maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
    fp.close()
    device.close()
    outfp.close()
    return outfile


def load_template (template_path):
    '''This takes in a table template and converts it to a python object'''
    with open("formats/AL_statewidenetassets.txt") as myFile:
        template_text = myFile.read()

    template = {
        'anchor': "",
        'lines': []
    }

    pieces = template_text.split("=====")
    template['anchor'] = pieces[0][:-1]
    template['lines'] = pieces[1].splitlines()

    for i, line in enumerate(template['lines']):
        if line == "" or line[0] != "{":
            template['lines'][i] = ""
        else:
            template['lines'][i] = json.loads(line)

    return template


def process_template(template, text):
    result = []

    searched_text = text.split(template['anchor'])
    if(len(searched_text) != 2):
        return result

    target_text = searched_text[1].splitlines()[0:len(template['lines'])]

    for i, template_line in enumerate(template['lines']):
        if template_line == "":
            continue
        result_line = template_line.copy()
        target_line = target_text[i].strip()
        value = int("0" + "".join(re.findall(r'\d+', target_line)))

        # Is this a negative number
        if len(target_line) > 0 and (target_line[0] == "-" or (target_line[0] == "(" and target_line[-1] == ")")):
            value *= -1

        result_line['value'] = value
        result.append(result_line)

    return result


pdf_file = "parseme/AL_cafr2010.pdf"
template_file = "formats/AL_statewidenetassets.txt"
# loaded_text = load_pdf_text(pdf_file)

with open("parseme/processing/AL_cafr2010.pdf.txt", "r") as myFile:
    loaded_text = myFile.read()

template = load_template(template_file)
result = process_template(template,loaded_text)

print(result)
