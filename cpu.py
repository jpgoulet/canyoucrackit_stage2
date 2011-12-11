# virtual machine architecture
# ++++++++++++++++++++++++++++
#
# segmented memory model with 16-byte segment size (notation seg:offset)
#
# 4 general-purpose registers (r0-r3)
# 2 segment registers (cs, ds equiv. to r4, r5)
# 1 flags register (fl)

from instruction import Instruction
from exception import VMException

class Register(object):
   
   def __init__(self, cpu):
      super(Register, self).__init__()
      self.cpu = cpu
      
   def __getitem__(self, key):
      if type(key) is int:
         if key == 0:
            return self.cpu.r0
         elif key == 1:
            return self.cpu.r1
         elif key == 2:
            return self.cpu.r2
         elif key == 3:
            return self.cpu.r3
         elif key == 4:
            return self.cpu.cs
         elif key == 5:
            return self.cpu.ds
         
         raise VMException("Invalid register access")
      else:
         raise TypeError()
         
   def __setitem__(self, key, value):
      if type(key) is int:
         if key == 0:
            self.cpu.r0 = value
         elif key == 1:
            self.cpu.r1 = value
         elif key == 2:
            self.cpu.r2 = value
         elif key == 3:
            self.cpu.r3 = value
         elif key == 4:
            self.cpu.cs = value
         elif key == 5:
            self.cpu.ds = value
         else:
            raise VMException("Invalid register access")
      else:
         raise TypeError()
            

class CPU(object):
   
   def __init__(self):
      super(CPU, self).__init__()
      
      self.ip = 0x00
                                  
      self.r0 = 0x00
      self.r1 = 0x00
      self.r2 = 0x00
      self.r3 = 0x00
                    
      self.cs = 0x00
      self.ds = 0x10
                    
      self.fl = 0x00

      self.firmware = [0xd2ab1f05, 0xda13f110]
      
      #easy way to access registers using list index
      self.r = Register(self)

   def execute(self):
      try:
         while True:
            instruction = Instruction.load()
            instruction.execute()
            
      except VMException as e:
         print e
         
   def dump(self):
      print "********** Registers **********"
      print "r0: 0x{0:02X}\tr1: 0x{1:02X}".format(self.r0, self.r1)
      print "r2: 0x{0:02X}\tr3: 0x{1:02X}".format(self.r2, self.r3)
      print "cs: 0x{0:02X}\tds: 0x{1:02X}".format(self.cs, self.ds)
      print "ip: 0x{0:02X}\tfl: 0x{1:02X}".format(self.ip, self.fl)
      print ""    
      