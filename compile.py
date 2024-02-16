import pathlib
import xml.etree.ElementTree as ET
from xml.dom import minidom


def asshex_from_int(val: int) -> str: return f"&H{val:08X}"


def asshex_to_int(val: str) -> int:
    if val.startswith("&H"):
        return int(val[2:], 16)
    return int(val)


def asstime_from_float(val: float) -> str:
    h = int(val) // 3600
    m = (int(val) // 60) % 60
    s = val % 60
    return f"{h}:{m:02d}:{s:05.02f}"


def asstime_to_float(val: str) -> float:
    h, m, s = val.split(":", 2)
    return int(h, 10) * 3600 + int(m, 10) * 60 + float(s)


def mkvchaptertime_from_float(val: float) -> str:
    h = int(val) // 3600
    m = (int(val) // 60) % 60
    s = val % 60
    return f"{h}:{m:02d}:{s:06.03f}"


class AssStyle:
    HEADERS = (
        'Name', 'Fontname', 'Fontsize', 'PrimaryColour', 'SecondaryColour', 'OutlineColour', 'BackColour', 'Bold',
        'Italic', 'Underline', 'StrikeOut', 'ScaleX', 'ScaleY', 'Spacing', 'Angle', 'BorderStyle', 'Outline', 'Shadow',
        'Alignment', 'MarginL', 'MarginR', 'MarginV', 'Encoding')

    def __init__(self, kv: dict[str, str]):
        self.data = kv

    def clone(self):
        return AssStyle(self.data.copy())

    def __str__(self):
        return f"Style: " + ",".join(self.data[k] for k in AssStyle.HEADERS)

    @property
    def name(self) -> str: return self.data["Name"]

    @name.setter
    def name(self, value: str): self.data["Name"] = value

    @property
    def font_name(self) -> str: return self.data["Fontname"]

    @font_name.setter
    def font_name(self, value: str): self.data["Fontname"] = value

    @property
    def font_size(self) -> int: return int(self.data["Fontsize"])

    @font_size.setter
    def font_size(self, value: int): self.data["Fontsize"] = str(value)

    @property
    def primary_color(self) -> int: return asshex_to_int(self.data["PrimaryColour"])

    @primary_color.setter
    def primary_color(self, value: int): self.data["PrimaryColour"] = asshex_from_int(value)

    @property
    def secondary_color(self) -> int: return asshex_to_int(self.data["SecondaryColour"])

    @secondary_color.setter
    def secondary_color(self, value: int): self.data["SecondaryColour"] = asshex_from_int(value)

    @property
    def back_color(self) -> int: return asshex_to_int(self.data["BackColour"])

    @back_color.setter
    def back_color(self, value: int): self.data["BackColour"] = asshex_from_int(value)

    @property
    def bold(self) -> bool: return int(self.data["Bold"]) != 0

    @bold.setter
    def bold(self, value: bool): self.data["Bold"] = '1' if value else '0'

    @property
    def italic(self) -> bool: return int(self.data["Italic"]) != 0

    @italic.setter
    def italic(self, value: bool): self.data["Italic"] = '1' if value else '0'

    @property
    def underline(self) -> bool: return int(self.data["Underline"]) != 0

    @underline.setter
    def underline(self, value: int): self.data["Underline"] = '1' if value else '0'

    @property
    def strikethrough(self) -> bool: return int(self.data["StrikeOut"]) != 0

    @strikethrough.setter
    def strikethrough(self, value: bool): self.data["StrikeOut"] = '1' if value else '0'

    @property
    def scale_x(self) -> float: return float(self.data["ScaleX"])

    @scale_x.setter
    def scale_x(self, value: float): self.data["ScaleX"] = f"{value:g}"

    @property
    def scale_y(self) -> float: return float(self.data["ScaleY"])

    @scale_y.setter
    def scale_y(self, value: float): self.data["ScaleY"] = f"{value:g}"

    @property
    def spacing(self) -> float: return float(self.data["Spacing"])

    @spacing.setter
    def spacing(self, value: float): self.data["Spacing"] = f"{value:g}"

    @property
    def angle(self) -> float: return float(self.data["Angle"])

    @angle.setter
    def angle(self, value: float): self.data["Angle"] = f"{value:g}"

    @property
    def border_style(self) -> int: return int(self.data["BorderStyle"])

    @border_style.setter
    def border_style(self, value: int): self.data["BorderStyle"] = str(value)

    @property
    def outline(self) -> float: return float(self.data["Outline"])

    @outline.setter
    def outline(self, value: float): self.data["Outline"] = f"{value:g}"

    @property
    def shadow(self) -> float: return float(self.data["Shadow"])

    @shadow.setter
    def shadow(self, value: float): self.data["Shadow"] = f"{value:g}"

    @property
    def alignment(self) -> int: return int(self.data["Alignment"])

    @alignment.setter
    def alignment(self, value: int): self.data["Alignment"] = str(value)

    @property
    def margin_l(self) -> int: return int(self.data["MarginL"])

    @margin_l.setter
    def margin_l(self, value: int): self.data["MarginL"] = str(value)

    @property
    def margin_r(self) -> int: return int(self.data["MarginR"])

    @margin_r.setter
    def margin_r(self, value: int): self.data["MarginR"] = str(value)

    @property
    def margin_v(self) -> int: return int(self.data["MarginV"])

    @margin_v.setter
    def margin_v(self, value: int): self.data["MarginV"] = str(value)

    @property
    def encoding(self) -> int: return int(self.data["Encoding"])

    @encoding.setter
    def encoding(self, value: int): self.data["Encoding"] = str(value)


class AssEvent:
    HEADERS = ('Layer', 'Start', 'End', 'Style', 'Name', 'MarginL', 'MarginR', 'MarginV', 'Effect', 'Text')

    def __init__(self, event_type: str, data: dict[str, str]):
        self.event_type = event_type
        self.data = data

    def clone(self):
        return AssEvent(self.event_type, self.data.copy())

    def __str__(self):
        return f"{self.event_type}: " + ",".join(self.data[k] for k in AssEvent.HEADERS)

    @property
    def layer(self) -> int: return int(self.data["Layer"])

    @layer.setter
    def layer(self, value: int): self.data["Layer"] = str(value)

    @property
    def start(self) -> float: return asstime_to_float(self.data["Start"])

    @start.setter
    def start(self, value: float): self.data["Start"] = asstime_from_float(value)

    @property
    def end(self) -> float: return asstime_to_float(self.data["End"])

    @end.setter
    def end(self, value: float): self.data["End"] = asstime_from_float(value)

    @property
    def style(self) -> str: return self.data["Style"]

    @style.setter
    def style(self, value: str): self.data["Style"] = value

    @property
    def name(self) -> str: return self.data["Name"]

    @name.setter
    def name(self, value: str): self.data["Name"] = value

    @property
    def margin_l(self) -> int: return int(self.data["MarginL"])

    @margin_l.setter
    def margin_l(self, value: int): self.data["MarginL"] = str(value)

    @property
    def margin_r(self) -> int: return int(self.data["MarginR"])

    @margin_r.setter
    def margin_r(self, value: int): self.data["MarginR"] = str(value)

    @property
    def margin_v(self) -> int: return int(self.data["MarginV"])

    @margin_v.setter
    def margin_v(self, value: int): self.data["MarginV"] = str(value)

    @property
    def effect(self) -> str: return self.data["Effect"]

    @effect.setter
    def effect(self, value: str): self.data["Effect"] = value

    @property
    def text(self) -> str: return self.data["Text"]

    @text.setter
    def text(self, value: str): self.data["Text"] = value


class Ass:
    def __init__(self, f: pathlib.Path | None = None):
        self.script_info: dict[str, str] = dict()
        self.style_header: list[str] = []
        self.event_header: list[str] = []
        self.styles: list[AssStyle] = []
        self.events: list[AssEvent] = []

        if f is None:
            return

        section: str | None = None
        header: list[str] | None = None
        with f.open("r", encoding="utf-8-sig") as fp:
            for line in fp:
                line = line.strip()
                if line == '' or line.startswith(';') or line.startswith('#'):
                    continue
                if line.startswith('[') and line.endswith(']'):
                    section = line[1:-1]
                    header = None
                    continue

                sep = line.find(':')
                if sep < 0:
                    raise RuntimeError("Invalid line")

                line_type = line[:sep]

                if line_type == 'Format':
                    if header is not None:
                        raise RuntimeError("Did not expect Format")

                    header = [x.strip() for x in line[sep + 1:].split(',')]
                    if section == 'V4+ Styles':
                        self.style_header = header
                    elif section == 'Events':
                        self.event_header = header
                    continue

                if section == 'Script Info':
                    self.script_info[line_type] = line[sep + 1:].strip()
                    continue

                if section == 'V4+ Styles':
                    self.styles.append(AssStyle(
                        dict(zip(header, (x.strip() for x in line[sep + 1:].split(',', len(header) - 1))))))
                elif section == 'Events':
                    self.events.append(AssEvent(
                        line_type,
                        dict(zip(header, (x.strip() for x in line[sep + 1:].split(',', len(header) - 1))))))

    def export(self) -> str:
        return "\n".join((
            "[Script Info]",
            *(f"{k}: {v}" for k, v in self.script_info.items()),
            "",
            "[V4+ Styles]",
            "Format: " + ", ".join(self.style_header),
            *(str(x) for x in self.styles),
            "",
            "[Events]",
            "Format: " + ", ".join(self.event_header),
            *(str(x) for x in self.events),
        ))


def resolve_xref(subtitles: dict[str, Ass]):
    for ass in subtitles.values():
        i = 0
        while i < len(ass.events):
            event = ass.events[i]
            if event.name != 'ref':
                i += 1
                continue
            ref_file, ref_key = event.effect.split('!', 1)
            ref_ass = ass if ref_file == '' else subtitles[ref_file]
            ref_lines = []
            for x in ref_ass.events:
                if x.effect != ref_key:
                    continue
                rl = event.clone()
                rl.event_type = x.event_type
                rl.name = x.name
                rl.effect = ''
                rl.text = x.text
                ref_lines.append(rl)
            ass.events[i:i + 1] = ref_lines
            i += 1


def generate_chapters(ass: Ass):
    data = []
    for event in ass.events:
        if event.event_type != "Comment" or event.name != "chapter":
            continue
        sep = event.text.find("-")
        d = {"start": event.start, "end": event.end, "name": event.text, "subchapters": []}
        if sep < 0:
            data.append(d)
        else:
            name = event.text[:sep]
            if not data or data[-1]["name"] != name:
                data.append({"name": event.text[:sep], "subchapters": []})
            data[-1]["subchapters"].append(d)

    chapters = ET.Element("Chapters")
    edition_entry = ET.SubElement(chapters, "EditionEntry")

    def add_chapter(parent, d):
        if d["subchapters"]:
            start = min(x["start"] for x in d["subchapters"])
            end = max(x["end"] for x in d["subchapters"])
        else:
            start, end = d["start"], d["end"]
        chapter_atom = ET.SubElement(parent, "ChapterAtom")
        ET.SubElement(chapter_atom, "ChapterTimeStart").text = mkvchaptertime_from_float(start)
        ET.SubElement(chapter_atom, "ChapterTimeEnd").text = mkvchaptertime_from_float(end)
        chapter_display = ET.SubElement(chapter_atom, "ChapterDisplay")
        ET.SubElement(chapter_display, "ChapterString").text = d["name"]
        ET.SubElement(chapter_display, "ChapterLanguage").text = "eng"
        for subc in d["subchapters"]:
            add_chapter(chapter_atom, subc)

    for c in data:
        add_chapter(edition_entry, c)

    reparsed = minidom.parseString(ET.tostring(chapters, "utf-8"))
    lines = reparsed.toprettyxml(indent="\t", encoding="utf-8").decode("utf-8").splitlines()
    lines.insert(1, '<!DOCTYPE Chapters SYSTEM "matroskachapters.dtd">')
    return "\n".join(lines)


def extract_title(ass: Ass, language_code: str):
    relevant = []
    for event in ass.events:
        if event.style == 'TitleEP':
            if not relevant:
                relevant.append(event)
            elif relevant[0].start == event.start and relevant[0].end == event.end:
                relevant.append(event)
    return ' '.join(x.text for x in relevant if x.name == language_code)


def extract_language(ass: Ass, language_code: str):
    new_ass = Ass()
    new_ass.script_info = {
        **ass.script_info,
        "Title": extract_title(ass, language_code),
    }
    new_ass.style_header = AssStyle.HEADERS
    new_ass.event_header = AssEvent.HEADERS
    new_ass.styles.extend(x.clone() for x in ass.styles)
    new_ass.events.extend(
        x.clone() for x in ass.events if
        (x.event_type == 'Dialogue' or (x.event_type == 'Comment' and language_code == 'ja'))
        and x.name == language_code)

    return new_ass


def __main__():
    dir_videos = pathlib.Path("./Videos")
    dir_subtitles = pathlib.Path("./Episodes")
    dir_subtitle_exports = pathlib.Path("./SubtitleExports")
    subtitles: dict[str, Ass] = {}

    for f in dir_subtitles.iterdir():
        if not f.name.endswith(".ass"):
            continue
        subtitles[f.name[:-4]] = Ass(f)

    resolve_xref(subtitles)

    # print(generate_chapters(subtitles["14"]))
    # print(extract_language(subtitles["14"], "en").export())

    for k, v in subtitles.items():
        (dir_subtitle_exports / "en" / f"{k}.ass").write_text(
            extract_language(v, "en").export(),
            encoding="utf-8-sig")
        (dir_subtitle_exports / "ko" / f"{k}.ass").write_text(
            extract_language(v, "ko").export(),
            encoding="utf-8-sig")
        (dir_subtitle_exports / "ja" / f"{k}.ass").write_text(
            extract_language(v, "ja").export(),
            encoding="utf-8-sig")
    return 0


if __name__ == "__main__":
    exit(__main__())
