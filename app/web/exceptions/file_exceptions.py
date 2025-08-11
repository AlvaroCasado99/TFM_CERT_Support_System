""" Excepciones propias sobre archivos """

class ValidationError(Exception):
    pass

class FileExtensionError(Exception):
    pass

class FileSizeError(Exception):
    pass

class ContentError(Exception):
    pass
