import json

def load_json(path):
    with open(path, "r", encoding='utf-8') as f:
        res = json.load(f)
    return res


def parse_section_titles(structure: dict):
    titles = []

    for chapter in structure["chapters"]:
        titles.append(chapter["title"])

        if "sections" in chapter:
            for section in chapter["sections"]:
                titles.append(section["title"])

                if "subsections" in section:
                        for subsection in section["subsections"]:
                             titles.append(subsection["title"]) 
    
    return titles