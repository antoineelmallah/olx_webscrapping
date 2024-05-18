import re
import math

def get_total_pages(main_content):
    pattern = r'(\d+) - (\d+) de ([0-9\.]+) resultados'
    matchs = [ re.search(pattern, p.text) for p in main_content.find_all('p') if re.search(pattern, p.text) ]
    if not len(matchs):
        return 0
    match = matchs[0]
    page_size = int(match.group(2))
    total_size = int(re.sub(r'\.', '', match.group(3)))
    print(page_size, '/', total_size)
    return math.ceil(total_size / page_size)
