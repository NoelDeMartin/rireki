import click

from rireki.utils.string_helpers import str_pad


def display_table(headers, rows, min_column_width=10):
    headers = map(lambda h: h.upper(), headers)

    column_widths = calculate_column_widths(headers, rows, min_column_width)

    click.echo(format_table_row(headers, column_widths))

    for row in rows:
        click.echo(format_table_row(row, column_widths))


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


def calculate_column_widths(headers, rows, min_column_width):
    column_widths = [min_column_width] * len(headers)

    column_widths = fit_row_column_widths(headers, column_widths)

    for row in rows:
        columns_content = map(lambda cell: render_cell_content(cell), row)
        column_widths = fit_row_column_widths(columns_content, column_widths)

    return column_widths


def fit_row_column_widths(columns_content, column_widths):
    for index, content in enumerate(columns_content):
        column_widths[index] = max(column_widths[index], len(content))

    return column_widths


def format_time_unit(magnitude, name):
    if not magnitude == 1:
        name = name + 's'

    return '%s %s' % (str(magnitude), name)


def format_table_row(row, column_widths):
    text = ''

    for index, cell_content in enumerate(row):
        text = text + format_table_cell(cell_content, column_widths[index])

    return text


def format_table_cell(content, column_width):
    if type(content) is not dict:
        return str_pad(content, column_width)

    text = str_pad(content['text'], column_width)

    if 'color' in content:
        text = click.style(text, fg=content['color'])

    return text


def render_cell_content(content):
    if type(content) is not dict:
        return content

    return content['text']
