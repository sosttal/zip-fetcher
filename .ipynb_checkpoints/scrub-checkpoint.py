import re

pat = r'https://www.uio.no/studier/emner/matnat/ifi/IN3050/v25/weekly-exercises/[A-Za-z_0-9]+\.zip'

with open("scrub.html", "r") as page:
    extract = page.read()


extract = re.findall(pat,extract)

with open("zip.zap", "w") as out:
    for l in set(extract):
        out.write(l+"\n")
