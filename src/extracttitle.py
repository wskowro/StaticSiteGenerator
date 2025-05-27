def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.strip().startswith("# "):  # ensure it's a single '#' followed by space
            return line.strip()[2:].strip()  # remove '# ' and extra spaces
    raise Exception("No h1 header found")
