class StorageFile:
  def __init__(self, bFile=None, fname=None):
    self.file = bFile if bFile is not None else None
    self.filename = fname if fname is not None else None

  def getFile(self):
    return self.file

  def setFile(self, bFile):
    self.file = bFile

  def getFile(self):
    return self.filename

  def setFile(self, fname):
    self.filename = fname