# **pdf-text-extractor**<br>

**pdf-text-extractor** aims at extracting data from pdf using the pdf2text (Poppler) available in Ubuntu. 

This is mainly intended for extracting data from text based pdf with two or three columns, without getting the sentences mixed up.<br>
We use pdf2text to extract content with xml as output file and then parsing that XML file to collect the content line by line.<br>

Run using the following command:<br>
```
python pdf_converter.py --input_path input_file_path --output_path output_file_path
```
 
For further reading about **XML Parser**<br>
https://pypi.org/project/lxml/<br>
https://lxml.de<br>

Python version>=3.5.<br>

## Installation
~~~bash
sudo apt update
sudo apt install poppler-utils
pip install -r requirements.txt
~~~
