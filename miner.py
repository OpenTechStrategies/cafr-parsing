

import glob, json, ntpath, os, re
import xml.etree.cElementTree as ET
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
    """Opens a pdf document, converts it to text, and returns that text."""

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
    outfile = ntpath.basename(pdf_path) + ".txt"

    outfp = file(outfile, 'w')

    # Set up pdfminer objects
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

    with open(outfile) as myFile:
        file_text = myFile.read()

    os.remove(outfile)

    return file_text


def load_templates(template_directory):
    """Loads all templates located from the specified directory. Returns the list of templates."""
    files = glob.glob(template_directory + "/*.txt")
    templates = []
    for file in files:
        template = parse_template(file)
        templates.append(template)
    return templates


def parse_template (template_path):
    """Takes in a specific template path, converts it to a python object, and returns that object."""
    with open(template_path) as myFile:
        template_text = myFile.read()



    template = json.loads(template_text)
    return template


def invoke_template(template, text):
    """Takes a template and raw text, returns structured data."""
    result = []

    split_text = re.split(template["anchor"], text)

    # If the split shows more than 2, the anchor isn't unique
    # If the split shows less than 2, the anchor wasn't found
    if(len(split_text) != 2):
        return result

    text_lines = split_text[1].splitlines()[0:len(template["lines"])]


    # Go through each line of the template and perform a match
    for i, template_line in enumerate(template["lines"]):

        # Skip any template lines that don't have an object to map to
        if template_line == {}:
            continue

        # Set up a fresh copy of the result object for this line
        result_line = template_line.copy()
        target_line = text_lines[i].strip()

        # Parse out the integer value
        value = int("0" + "".join(re.findall(r'\d+', target_line)))

        # Is this a negative number
        if len(target_line) > 0 and (target_line[0] == "-" or (target_line[0] == "(" and target_line[-1] == ")")):
            value *= -1

        # Set the value for the mapped object based on the value in the cafr
        result_line["value"] = value
        result.append(result_line)

    return result


def process_pdf(pdf_path):
    """Takes a pdf path and attempts to extract all possible tables from it"""

    # TODO: This shouldn't be invoked every time
    templates = load_templates("templates")
    text = generate_pdf_text(pdf_path)

    for template in templates:

        # Don't invoke a template that doesn't apply to this file
        if not re.match(template["file_pattern"], ntpath.basename(pdf_path)):
            continue

        # Parse the file with this template
        result = invoke_template(template, text)

        # Move along if the template didn't have a match
        if result == "":
            continue

        # Write the resulting output
        outfile_path = "results/" + os.path.splitext(ntpath.basename(pdf_path))[0] + "-" + template["type_code"] + ".json"
        with open(outfile_path, "w") as outfile:
            outfile.write(json.dumps(result))


# NOTE: This method does NOT BELONG HERE (Just getting a first version written)
def generate_xbrl_output(json_result):
    """Takes a JSON string and generates an XBRL document from it"""
    root = ET.Element("xbrl", {
        "xmlns":"http://www.xbrl.org/2003/instance",
        "xmlns:xbrli":"http://www.xbrl.org/2003/instance",
        "xmlns:link":"http://www.xbrl.org/2003/linkbase" ,
        "xmlns:xlink":"http://www.w3.org/1999/xlink" ,
        "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance" ,
        "xmlns:xbrldi":"http://xbrl.org/2006/xbrldi" ,
        "xmlns:cafr":"http://www.xbrlsite.com/DigitalFinancialReporting/Metapattern/RollUp" ,
        "xmlns:iso4217":"http://www.xbrl.org/2003/iso4217" ,
        "xsi:schemaLocation":"http://xbrl.org/2006/xbrldi http://www.xbrl.org/2006/xbrldi-2006.xsd"
    })

    xsdLink = ET.SubElement(root, "link:schemaRef", {
        "xlink:href":"cafr-2015-04-20.xsd"
    })

    baseContext = ET.SubElement(root, "context", {
        "id":"baseContext"
    })
    baseContextEntity = ET.SubElement(baseContext, "entity")
    baseContextEntityIdentifier = ET.SubElement(baseContext, "identifier", {
        "scheme": "http://www.opentechstrategies.com"
    })
    baseContextEntityIdentifier.text = "CAFR"

    moneyUnit = ET.SubElement(root, "unit", {
        "id": "U-Monetary"
    });
    moneyUnitMeasure = ET.SubElement(moneyUnit, "measure")
    moneyUnitMeasure.text = "iso4217:USD"

    for i, json_fact in enumerate(json_result):
        concept = fact["xbrl_concept"]
        value = fact["value"]
        dimensions = fact["xbrl_dimensions"]
        xml_fact = ET.SubElement(root, "cafr:" + concept, {
            "contextRef": "baseContext",
            "unitRef": "U-Monetary",
            "decimals": "INF"
        })
        xml_fact.text = value

    tree = ET.ElementTree(root)
    tree.write("test.xml")

## For now you can test this code by uncommenting and picking a file path
#process_pdf("data/AL_cafr2010.pdf")
generate_xbrl_output([])