from os.path import dirname

def getTemplateFolder(location=''):
    return dirname(__file__) + '/templates/' + location