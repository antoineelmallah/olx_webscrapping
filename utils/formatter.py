import re
from datetime import datetime

def get_by_pattern_as_type(code_spipet, pattern, type):
    groups = re.findall(pattern, code_spipet)
    if not len(groups):
        return None
    return type(groups[0])

def get_code(code_snipet):
    return get_by_pattern_as_type(code_snipet, r'\D+(\d+)', str)

def get_creation_datetime(code_snipet):
    groups = re.findall(r'\D+(\d{2})/(\d{2})\D+(\d{2}):\s?(\d{2})', code_snipet)
    if not len(groups):
        return None
    day, month, hour, minute = ( int(val) for val in groups[0] )
    now = datetime.now()
    year = now.year if now.month >= month else now.year - 1
    return datetime(
        day=day,
        month=month,
        year=year,
        hour=hour,
        minute=minute
    )

def get_as_type(code_snipet, type):
    try:
        return type(code_snipet)
    except:
        return None

def get_gnv(code_snipet: str):
    if not code_snipet:
        return None
    if not len(code_snipet.strip()):
        return None
    if code_snipet.lower().startswith('n'):
        return False
    if code_snipet.lower().startswith('s'):
        return True
    return None

if __name__ == '__main__':
    formatted = get_creation_datetime('Publicado em 18/05 às 19: 22')
    print(formatted)