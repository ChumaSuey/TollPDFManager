import re

def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    """
    return [ int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text) ]
