import xml.etree.ElementTree as ET
from zipfile import ZipFile
import os
import html
import re
import shutil


def create_directory(n):
    try:
        os.mkdir(n)
    except Exception:
        print(f"Couldn't create directory {n}")

items_zip = ZipFile('mhealthcompendium.zip', 'w')

tree = ET.parse('Tables_2019-Jul-16_1531.xml')
root = tree.getroot()
regex = re.compile(r"<(?:.*?/){7}(.*?)\s.*?>\s*(.*?)<")
href_regex = re.compile(r"href=(.*?)\s")
for row in root.findall('Row'):
    id = row.find("ID").text
    os.mkdir(f"item_{id}")
    title = row.find("ProjectTitle").text
    subject = row.find("Summary").text
    contributor = row.find("ContactInformation").text
    relation = row.find("ApplicationType").text
    attachment = html.unescape(row.find("CaseStudyLink").text)
    url = re.findall(href_regex, attachment)
    filename = re.findall(regex, attachment)
    print(f"Processing item {id}")
    # download file
    
    with open(f"item_{id}/contents", "w") as contents:
        contents.write(f"{filename[0][0]}\n")
    items_zip.write(f"item_{id}/contents")

    with open(f"item_{id}/collection", "w") as collection:
        collection.write("mhealthcompendium")
    items_zip.write(f"item_{id}/collection")

    with open(f"item_{id}/dublin_core.xml", "w") as dc:
        dc.write(f"""<dublin_core>
    <dcvalue element="title" qualifier="none" language="en">{title}.</dcvalue>
    <dcvalue element="subject">{subject}</dcvalue>
    <dcvalue element="contributor" qualifier="author">{contributor}</dcvalue>
    <dcvalue element="contributor" qualifier="author">Doarn, Charles R</dcvalue>
    <dcvalue element="date" qualifier="issued">2013-02-15</dcvalue>
    <dcvalue element="relation" qualifier="uri">{relation}</dcvalue>
</dublin_core>""")
    items_zip.write(f"item_{id}/dublin_core.xml")

    with open(f"item_{id}/metadata_dcterms.xml", "w") as dc:
        dc.write(f"""<dublin_core schema="dcterms">
    <dcvalue element="title" language="en">{title}.</dcvalue>
    <dcvalue element="subject">{subject}</dcvalue>
    <dcvalue element="contributor" qualifier="author">{contributor}</dcvalue>
    <dcvalue element="contributor" qualifier="author">Doarn, Charles R</dcvalue>
    <dcvalue element="date" qualifier="issued">2013-02-15</dcvalue>
    <dcvalue element="relation" qualifier="uri">{relation}</dcvalue>
</dublin_core>""")
    items_zip.write(f"item_{id}/metadata_dcterms.xml")

    shutil.rmtree(f"item_{id}")
items_zip.close()

