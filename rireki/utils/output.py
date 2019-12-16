import click


def display_table(headers, rows, column_width=30):
    click.echo(format_table_row(map(lambda h: h.upper(), headers), column_width))

    for row in rows:
        click.echo(format_table_row(row, column_width))


def format_time(time):
    if time <= 60:
        return format_time_unit(time, 'second')

    time = time / 60
    if time <= 60:
        return format_time_unit(time, 'minute')

    time = time / 24
    if time <= 24:
        return format_time_unit(time, 'hour')

    return format_time_unit(time, 'day')


def format_time_unit(magnitude, name):
    if not magnitude == 1:
        name = name + 's'

    return '%s %s' % (str(magnitude), name)


def format_table_row(row, column_width):
    text = ''

    for cell_content in row:
        text = text + format_table_cell(cell_content, column_width)

    return text


def format_table_cell(content, column_width):
    if type(content) is not dict:
        return pad_text(content, column_width)

    text = pad_text(content['text'], column_width)

    if 'color' in content:
        text = click.style(text, fg=content['color'])

    return text


def pad_text(text, length, padding=' '):
    return (text + (padding * length))[:length]
