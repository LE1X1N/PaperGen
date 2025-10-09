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


def parse_main_body_titles(structure: dict):
    titles = []

    for chapter in structure["chapters"]:
        if "sections" not in chapter:
            titles.append(chapter["title"])

        else:
            for section in chapter["sections"]:
                if "subsections" not in section:
                    titles.append(f"{section['title']}")
                else:
                    for subsection in section["subsections"]:
                        titles.append(f"{subsection['title']}")
    return titles