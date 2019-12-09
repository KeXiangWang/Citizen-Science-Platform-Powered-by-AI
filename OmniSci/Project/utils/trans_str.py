

def transform(string):
    transformer = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        ' ': '&nbsp;',
    }
    for key, value in transformer.items():
        string = string.replace(key, value)

    return string
