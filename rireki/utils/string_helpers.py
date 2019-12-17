def str_studly(text):
    words = text.split(' ')

    return ''.join([w[0].upper() + w[1:].lower() for w in words])


def str_pad(text, length, padding=' '):
    return (text + (padding * length))[:length]
