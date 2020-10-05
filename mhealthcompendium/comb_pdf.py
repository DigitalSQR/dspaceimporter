from PyPDF2 import PdfFileReader, PdfFileWriter
import re
import os

contents_re = re.compile(r"([\w,\s\(\)\/\&:\-!\?]+)\s*\.+\s*(\d+)")
all_caps = ''
def mkdir(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        pass

def get_table_of_contents(file_path, pages=[], offset=0, last=0):
    folder = file_path.split('-', 2)[0]
    mkdir(folder)
    with open(f"compendium_volumes/{file_path}", 'rb') as f:
        pdf = PdfFileReader(f)
        with open(f"compendium_volumes/{file_path}_index", 'w') as index:
            for page in pages:
                index.writelines(pdf.getPage(page).extractText().split('\n'))
        with open(f"compendium_volumes/{file_path}_index", "r") as index:
            contents = re.findall(contents_re, index.read())

        # open index file for writing_table_of_contents
        toc = open(f"compendium_volumes/{file_path}_index", "w")
        last_page = False

        for i in range(len(contents)):
            title, pg = contents[i]
            if i+1 < len(contents):
                nxt_title, nxt_page = contents[i+1]
            if re.match(r"annex.*", nxt_title.lower()) or i+1 == len(contents):
                nxt_page = last
                last_page = True
            title = title.strip().replace("/", "-")
            toc.write(f"{title} -- {pg.strip()}\n")
            with open(f"{folder}/{title}.pdf", "wb") as pdf_out:
                pdf_writer = PdfFileWriter()
                for p in range(int(pg)+offset, int(nxt_page)+offset):
                    pdf_writer.addPage(pdf.getPage(p))
                pdf_writer.write(pdf_out)
            if last_page:
                break
        toc.close()

def find_article_file():
    

if __name__ == "__main__":
    files = [
        {"name": "vol_1-mhealthcompendiumupdated_final.pdf", "pages": [4,5], "offset": 3, "last": 77},
        {"name": "vol_2-usaid_mhealth_compendium_vol._2_us_letter_web.pdf", "pages": [7,8], "offset": 9, "last": 72},
        {"name": "vol_3-mhealth_compendium_volume_3_a4_english.pdf", "pages": [7,8], "offset": 9, "last": 68},
        {"name": "vol_4-usaid_mhealth_compendium_vol._4_final.pdf.pdf", "pages": [7,8], "offset": 9, "last": 84},
        {"name": "vol_5-mhealthvol5_final_15jun15_webv.pdf", "pages": [6,7], "offset": 9, "last": 104},
        {"name": "vol_6-2016_mhealth_31may16_final.pdf", "pages": [8], "offset": 9, "last": 74}
        ]

    for file in files:
        get_table_of_contents(file['name'], file['pages'], file['offset'], file['last'])