def extract_title(markdown):
    for line in markdown.split("\n"):
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception("No title found in markdown file")
