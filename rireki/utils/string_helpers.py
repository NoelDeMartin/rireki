def str_studly(str):
    words = str.split(' ')

    return ''.join([w[0].upper() + w[1:].lower() for w in words])
