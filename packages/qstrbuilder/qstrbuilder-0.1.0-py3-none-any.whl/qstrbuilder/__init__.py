def build(number, width=None, precision=None):
    if width is None:
        swidth = ""
    else:
        assert isinstance(width, int) and width >= 0
        swidth = str(width)
    if precision is None:
        sprecision = ""
    else:
        assert isinstance(precision, int) and precision >= 0
        sprecision = "." + str(precision)
    template = "{:" + swidth + sprecision + "f}"
    result = template.format(number)
    return result
