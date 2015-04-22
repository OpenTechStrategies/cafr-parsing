

import glob, json, ntpath, os, re
import xml.etree.cElementTree as ET
import itertools
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

    if(not os.path.isfile(outfile)):
        outfp = file(outfile, 'w')

        # Set up pdfminer objects
        rsrcmgr = PDFResourceManager(caching=caching)
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                                   imagewriter=imagewriter)
        
        fp = file(pdf_path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages, 
                                      caching=caching, check_extractable=False):
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

    # TODO: "10" is an arbitrary high number to ensure we extract enough lines
    # In reality, we need to extract the next value DURING the template iteration, but there isn't time to refactor this second
    # (Sorry.)
    text_lines = split_text[1].splitlines()[0:len(template["lines"]) * 10]

    # Extract lines with numeric values
    value_lines = []
    for text_line in text_lines:
        target_line = text_line.strip()

        numeric_line = "".join(re.findall(r'\d+', target_line))
        alpha_line = "".join(re.findall(r'[a-zA-Z]+', target_line))
        
        # We don't want any lines with words in them
        # We don't want any lines without numbers in them
        if(numeric_line == "" or alpha_line != ""):
            continue

        # Parse out the integer value
        value = int("0" + numeric_line)

        # Is this a negative number
        negcheck_line = re.findall(r'[\d()\-]', target_line)
        if len(negcheck_line) > 0 and (negcheck_line[0] == "-" or (negcheck_line[0] == "(" and negcheck_line[-1] == ")")):
            value *= -1

        value_lines.append(value)


    # Go through each line of the template and perform a match
    for i, template_line in enumerate(template["lines"]):

        # Skip any template lines that don't have an object to map to
        if template_line == {}:
            continue

        # Set up a fresh copy of the result object for this line
        result_line = template_line.copy()
        value = value_lines[i]

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
        json_result = invoke_template(template, text)

        # Move along if the template didn't have a match
        if json_result == "":
            continue

        # Convert to XBRL
        xbrl_result = generate_xbrl_tree(json_result)

        # Write the resulting output
        outfile_path = "results/" + os.path.splitext(ntpath.basename(pdf_path))[0] + "-" + template["type_code"] + ".xml"
        xbrl_result.write(outfile_path)


# TODO: This method does NOT BELONG HERE (Just getting a first version written)
# It is also actually really nasty; contexts are products of all possible combinations of the used dimensions
# This is the first method to get rewritten and pythonized
# TODO: This version only supports a SINGLE dimension.  The current taxonomy only uses a single dimension.

def generate_xbrl_tree(json_result):
    """Takes a JSON string and generates an XBRL document from it"""

    # Collect the dimensions used; each one will generate a context
    dimension_dict = {}
    for json_fact in json_result:
        dimensions = json_fact["xbrl_dimensions"]
        
        # Go through each specified dimension and store the value specified
        for dimension, member in dimensions.items():
            if(dimension not in dimension_dict):
                dimension_dict[dimension] = []
            if member not in dimension_dict[dimension]:
                dimension_dict[dimension].append(member)
    
    # Create one context element per dimension combination
    # contexts = []
    # for dimension, members in dimension_dict.items():
    #     new_contexts = []
    #     for member in members:
    #         new_contexts.append((dimension, member))

    #     if(contexts == []):
    #         contexts = new_contexts
    #     else:
    #         contexts = list(itertools.product(*[contexts, new_contexts]))

    # TODO: This just uses the first dimension, that's it.  This HAS to change eventually to use all dimensions.
    dimension_name = dimension_dict.keys()[0]
    dimension_members = dimension_dict[dimension_name]

    root = ET.Element("xbrl", {
        "xmlns":"http://www.xbrl.org/2003/instance",
        "xmlns:xbrli":"http://www.xbrl.org/2003/instance",
        "xmlns:link":"http://www.xbrl.org/2003/linkbase" ,
        "xmlns:xlink":"http://www.w3.org/1999/xlink" ,
        "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance" ,
        "xmlns:xbrldi":"http://xbrl.org/2006/xbrldi" ,
        "xmlns:cafr":"http://www.opentechstrategies.com/cafr-2015-04-20" ,
        "xmlns:iso4217":"http://www.xbrl.org/2003/iso4217" ,
        "xsi:schemaLocation":"http://xbrl.org/2006/xbrldi http://www.xbrl.org/2006/xbrldi-2006.xsd"
    })

    xsdLink = ET.SubElement(root, "link:schemaRef", {
        "xlink:href":"cafr-2015-04-20.xsd"
    })

    # Create one context per context item
    contexts = {}
    for member in dimension_members:
        contextId = "C-" + member
        contexts[member] = contextId

        context = ET.SubElement(root, "context", {
            "id": contextId
        })
        contextEntity = ET.SubElement(context, "entity")
        contextEntityIdentifier = ET.SubElement(contextEntity, "identifier", {
            "scheme": "http://www.opentechstrategies.com"
        })
        contextEntityIdentifier.text = "CAFR"
        contextPeriod = ET.SubElement(context, "period")
        contextPeriodInstant = ET.SubElement(contextPeriod, "instant")
        # TODO: Extract a date somehow
        contextPeriodInstant.text = "2015-04-21"
        contextScenario = ET.SubElement(context, "scenario")
        contextScenarioDimension = ET.SubElement(contextScenario, "xbrldi:explicitMember", {
            "dimension":"cafr:" + dimension_name
        })
        contextScenarioDimension.text = "cafr:" + member


    moneyUnit = ET.SubElement(root, "unit", {
        "id": "U-Monetary"
    });
    moneyUnitMeasure = ET.SubElement(moneyUnit, "measure")
    moneyUnitMeasure.text = "iso4217:USD"

    for json_fact in json_result:
        concept = json_fact["xbrl_concept"]
        value = json_fact["value"]
        dimensions = json_fact["xbrl_dimensions"]

        # TODO: This is flat out broken.  It assumes everything has dimension values for the same dimension (in our templates this will be true, but this can't be true forever)
        contextId = contexts[dimensions[dimension_name]]
        xml_fact = ET.SubElement(root, "cafr:" + concept, {
            "contextRef": contextId,
            "unitRef": "U-Monetary",
            "decimals": "INF"
        })
        xml_fact.text = str(value)

    tree = ET.ElementTree(root)
    return tree

def load_results_json(json_path):
    with open(json_path) as myFile:
        results_text = myFile.read()
    results_json = json.loads(results_text)
    return results_json


## For now you can test this code by uncommenting and picking a file path
process_pdf("data/ID_cafr2010.pdf")
process_pdf("data/ID_cafr2011.pdf")
process_pdf("data/ID_cafr2012.pdf")
process_pdf("data/ID_cafr2013.pdf")
process_pdf("data/ID_cafr2014.pdf")
process_pdf("data/NY_cafr2010.pdf")
process_pdf("data/NY_cafr2011.pdf")
process_pdf("data/NY_cafr2012.pdf")
process_pdf("data/NY_cafr2013.pdf")
process_pdf("data/NY_cafr2014.pdf")