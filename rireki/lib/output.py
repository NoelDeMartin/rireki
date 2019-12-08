import click


def display_table(headers, rows, column_width=20):
    click.echo(format_table_row(map(lambda h: h.upper(), headers), column_width))

    for row in rows:
        click.echo(format_table_row(row, column_width))


def format_table_row(row, column_width):
    text = ''

    for cell_content in row:
        text = text + format_table_cell(cell_content, column_width)

    return text


def format_table_cell(content, column_width):
    if type(content) is str:
        return pad_text(content, column_width)

    text = pad_text(content['text'], column_width)

    if 'color' in content:
        text = click.style(text, fg=content['color'])

    return text


def pad_text(text, length, padding=' '):
    return (text + (padding * length))[:length]
