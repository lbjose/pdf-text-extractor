# from docx import Document
from lxml import etree
from pathlib import Path

import logging
import json
import os
import argparse

doc = etree.XMLParser(recover=True)
top_thresh = 50


def convert_to_xml(input_filepath, output_filepath=""):
    """
        Takes a pdf file and coverts it to xml file and saves it.

        Params:
            - input_filepath
            - output_filepath
    """
    try:
        command = "pdftohtml -i -xml {0} {1}".format(input_filepath, output_filepath)
        os.system(command)
    except Exception as e:
        logging.error("PDF to XML conversion Error!", e)
        assert "Parsing Error"


def process_xml_data(input_filepath):
    """
        Takes the XML input file and returns the extracted data.

        Output Format::
            overall_data = {
                "page_no" : [List of sentences]
            }

        Params:
            - input_filepath (XML filepath)

        Return:
            - overall_data (dict of page-wise data)
    """
    tree = etree.parse(input_filepath, doc)
    xml_pages = tree.findall("page")
    page_wise_data = get_cord_font_text_data(xml_pages)
    overall_data = {}
    for pg_id, page_data in page_wise_data.items():
        if not page_data:
            continue
        ind = get_lowest_top(page_data)
        data, new_data = recursive_data_collection(page_data, ind, [])
        while data:
            ind = get_lowest_top(data)
            data, new_data = recursive_data_collection(data, ind, new_data)

        text = [each[-1] for each in new_data if each[-1].strip()]
        overall_data[pg_id] = text
    return overall_data


def get_cord_font_text_data(xml_pages):
    """
        Get page wise coordinate, font and text data.

        Params:
            - xml_pages (Parsed XML page data)

        Return:
            - page_wise_data (Parsed page wise font and text data)
    """
    page_wise_data = {}
    for ind, each_page in enumerate(xml_pages):
        page_wise_data[ind] = []
        for each in each_page:
            if each.tag == "fontspec":
                continue
            temp = [int(i) for i in each.values()[0:4]]
            txt = ""
            for tt in each.itertext():
                txt += tt
            temp.append(txt)
            page_wise_data[ind].append(temp)
    return page_wise_data


def recursive_data_collection(data, ind, new_data):
    """
        Collects text data recursively.
    """
    try:
        # thresh = data[ind][0]
        for inds, each in enumerate(data[ind:]):
            # if (thresh + top_thresh < each[0]):
            if inds == 0 or (abs(each[0] - last_thresh) <= top_thresh):
                pass
            # elif (last_thresh + top_thresh < each[0]):
            else:
                break
            last_index = inds + ind
            last_thresh = each[0]
            # last_left = each[1]
            new_data.append(each)
        data = data[:ind] + data[last_index + 1:]
    except Exception as e:
        logging.error(e)
    return data, new_data


def get_lowest_top(page_data):
    """
        Given a page's coordinate data, it returns the height's top most value.

        Params:
            - page_data (Coordinate data of a page)

        Return:
            - ind (lowest top value)
    """
    temp = [i[0] for i in page_data]
    min_top = min(temp)
    ind = temp.index(min_top)

    for i, each in enumerate(page_data):
        if abs(min_top - each[0]) <= 5 and each[1] < page_data[ind][1]:
            # if each[1] < data[ind][1]:
            ind = i
            break
    return ind


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, help='Input Path', required=True)
    parser.add_argument('--output_path', type=str, help='Output path')
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    path = os.path.dirname(input_path)
    xml_output_path = f"{path}/convert.xml" if path else "convert.xml"
    convert_to_xml(input_path, xml_output_path)
    data = process_xml_data(xml_output_path)
    output_path = f"{output_path}/convert.json" if output_path else "convert.json"
    with open(output_path, "w") as fw:
        json.dump(data, fw, indent=4)
