def append_to_file(path, content):
    with open(path, 'a') as file:
        file.write("")
        file.write(content)
