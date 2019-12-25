import click

from datetime import datetime
from rireki.utils.array_helpers import array_map
from rireki.utils.string_helpers import str_pad


def display_table(headers, rows, min_column_width=14):
    headers = array_map(lambda h: h.upper(), headers)

    column_widths = __calculate_column_widths(headers, rows, min_column_width)

    click.echo(__format_table_row(headers, column_widths))

    for row in rows:
        click.echo(__format_table_row(row, column_widths))


def format_time(time, format):
    if format == 'date':
        return __format_time_date(time)
    elif format == 'interval':
        return __format_time_interval(time)


def __calculate_column_widths(headers, rows, min_column_width):
    column_widths = [min_column_width] * len(headers)

    column_widths = __fit_row_column_widths(headers, column_widths)

    for row in rows:
        columns_content = array_map(lambda cell: __render_cell_content(cell), row)
        column_widths = __fit_row_column_widths(columns_content, column_widths)

    return column_widths


def __fit_row_column_widths(columns_content, column_widths):
    for index, content in enumerate(columns_content):
        column_widths[index] = max(column_widths[index], len(content))

    return column_widths


def __format_time_interval(time):
    seconds = float(time)
    if seconds <= 60:
        return __format_time_unit(seconds, 'second')

    minutes = seconds / 60
    if minutes <= 60:
        return __format_time_unit(minutes, 'minute')

    hours = minutes / 60
    if hours <= 24:
        return __format_time_unit(hours, 'hour')

    days = hours / 24
    return __format_time_unit(days, 'day')


def __format_time_date(time):
    return datetime.fromtimestamp(time).strftime('%Y-%m-%d')


def __format_time_unit(magnitude, name):
    magnitude = int(magnitude)

    if not magnitude == 1:
        name = name + 's'

    return '%s %s' % (str(magnitude), name)


def __format_table_row(row, column_widths):
    text = ''

    for index, cell_content in enumerate(row):
        text = text + __format_table_cell(cell_content, column_widths[index])

    return text


def __format_table_cell(content, column_width):
    if type(content) is not dict:
        return str_pad(content, column_width)

    text = str_pad(content['text'], column_width)

    if 'color' in content:
        text = click.style(text, fg=content['color'])

    return text


def __render_cell_content(content):
    if type(content) is not dict:
        return content

    return content['text']
