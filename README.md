# pdf-text-extractor
pdf-text-extractor aims at extracting data from pdf using the pdf2text (Poppler) available in Ubuntu. 

This is mainly intended for extracting data from text based pdf with two or three columns, without getting the sentences mixed up.
We use pdf2text to extract data with xml as output file and then parses XML file and collects the sentences.

Run using the following command:
python temp.py --input_path input_file_path --output_path output_file_path
 
XML Parser Links
https://pypi.org/project/lxml/
https://lxml.de

Python version >= 3.5. Creating virtual env recommended.
Requirement file is added. Run the command pip install -r requirements.txt.

Also, install Poppler Utils.
sudo apt update
sudo apt install poppler-utils
