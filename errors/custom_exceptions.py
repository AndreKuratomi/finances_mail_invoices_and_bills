class TooManyFilesError(Exception):
    """Class for customized error for more than one table provided."""
    def __init__(self):
        self.message = {"HEY! ONLY ONE TABLE IS ALLOWED!"}
        super().__init__(self.message)