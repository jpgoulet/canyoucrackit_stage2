class VMException(Exception):

   def __init__(self, value):
      super(VMException, self).__init__()
      self.value = value
      
   def __str__(self):
      return self.value