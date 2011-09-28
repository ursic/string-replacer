String replacer for HTML templating

Example usage:

    t = pytme.Template(<TEMPLATE_FILE_PATH> or <TEMPLATE_STRING>)

    # Insert single data point.
    t.insert('TITLE', 'Article title')

    # Insert repeater.
    t.insert('ARTICLE')

    # Write to file.
    t.write(<SAVE_TO_PATH>)

    # Get template string.
    t.get()