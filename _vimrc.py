from snake import *
import re

@key_map("<leader>C")
def toggle_snake_case_camel_case():
    """ toggles a word between snake case (some_function) and camelcase
    (someFunction) """
    word = get_word()

    # it's snake case
    if "_" in word:
        chunks = word.split("_")
        camel_case = chunks[0] + "".join([chunk.capitalize() for chunk in
            chunks[1:]])
        replace_word(camel_case)

    # it's camel case
    else:
        # split our word on capital letters followed by non-capital letters
        chunks = filter(None, re.split("([A-Z][^A-Z]*)", word))
        snake_case = "_".join([chunk.lower() for chunk in chunks])
        replace_word(snake_case)

colors = {"normal": """
1 0
2 0
3 0
4 0
5 0
6 0
7 0
""",
    "atom": """
6 1
7 1
4 3
7 3
7 4
7 5
7 6
"""}

max_nr = {"normal": 0, "atom": 0}
for tokentype, lines in colors.items():
    for line in lines.splitlines():
        if not line:
            continue
        if line.startswith("#"):
            continue
        fg, bg = line.split()
        command("hi! def _semhl%s%s ctermfg=%s ctermbg=%s" % (tokentype, max_nr[tokentype], fg, bg))
        max_nr[tokentype] = max_nr[tokentype] + 1

@key_map("<leader>S")
def toggle_semantic_highlight():
    buffer = get_current_buffer()
    lines = []

    blacklist = set(["defmodule", "do", "end", "def", "use"])
    command("syn keyword _ %s" % " ".join(blacklist))
    command("syn match comment \"\v#.*$\"")
    command("hi! link comment Comment")

    tokencount = {}
    for line in get_buffer_lines(buffer):
        if line.startswith("#"):
            continue
        line = re.sub("[ \.\t,;()\[\]{}=\"\'\|]+", " ", line).strip()
        for token in line.split():
            token = token.strip()
            if not token:
                continue
            if token in blacklist:
                continue
            if token.isdigit():
                continue
            tokencount[token] = tokencount.get(token, 0) + 1

    token2color = {}
    current = {"normal": 0, "atom": 0}
    for token, count in tokencount.items():
        if count <= 1:
            continue
        if token.startswith(":"):
            tokentype = "atom"
        else:
            tokentype = "normal"
        token2color[token] = "_semhl%s%s" % (tokentype, current[tokentype])
        current[tokentype] = (current[tokentype] + 1) % max_nr[tokentype]

    for token, color in token2color.items():
        command("syn keyword %s %s" % (color, token))
        lines.append("syn keyword %s %s" % (color, token))

    set_buffer_lines(buffer, lines)
