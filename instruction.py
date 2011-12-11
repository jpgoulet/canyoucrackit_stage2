# instruction encoding
# ++++++++++++++++++++
#
#           byte 1               byte 2 (optional)
# bits      [ 7 6 5 4 3 2 1 0 ]  [ 7 6 5 4 3 2 1 0 ]
# opcode      - - -             
# mod               -           
# operand1            - - - -
# operand2                         - - - - - - - -
#
# operand1 is always a register index
# operand2 is optional, depending upon the instruction set specified below
# the value of mod alters the meaning of any operand2
#   0: operand2 = reg ix
#   1: operand2 = fixed immediate value or target segment (depending on instruction)
#
# instruction set
# +++++++++++++++
# 
# Notes:
#   * r1, r2 => operand 1 is register 1, operand 2 is register 2
#   * movr r1, r2 => move contents of register r2 into register r1
# 
# opcode | instruction | operands (mod 0) | operands (mod 1)
# -------+-------------+------------------+-----------------
# 0x00   | jmp         | r1               | r2:r1
# 0x01   | movr        | r1, r2           | rx,   imm 
# 0x02   | movm        | r1, [ds:r2]      | [ds:r1], r2
# 0x03   | add         | r1, r2           | r1,   imm
# 0x04   | xor         | r1, r2           | r1,   imm 
# 0x05   | cmp         | r1, r2           | r1,   imm 
# 0x06   | jmpe        | r1               | r2:r1
# 0x07   | hlt         | N/A              | N/A
#
# flags
# +++++
# 
# cmp r1, r2 instruction results in:
#   r1 == r2 => fl = 0
#   r1 < r2  => fl = 0xff
#   r1 > r2  => fl = 1
# 
# jmpe r1
#   => if (fl == 0) jmp r1
#      else nop


######## Important modification #############
#
# Changed opcode definition to make it work
#
# opcode | instruction | operands (mod 0) | operands (mod 1)
# -------+-------------+------------------+-----------------
# 0x00   | jmp         | r1               | imm:r1

import vm
from exception import VMException

class Opcode(object):
   jmp = 0x00 
   movr = 0x01 
   movm = 0x02 
   add = 0x03 
   xor = 0x04 
   cmp = 0x05 
   jmpe = 0x06 
   hlt = 0x07
   

class Instruction(object):
   
  
   def __init__(self, byte1, byte2):
      super(Instruction, self).__init__()
      
      self.byte1 = byte1
      self.byte2 = byte2
      self.op1 = byte1 & 0x0F
      self.op2 = byte2
      
      self.opcode = byte1 >> 5
      self.mod = bool(byte1 & 0x10)
      
   def __str__(self):
      return "nop"
      
   def execute(self):
      pass
      
   @staticmethod   
   def load():
      byte1 = vm.mem.read(vm.cpu.cs, vm.cpu.ip)
      byte2 = vm.mem.read(vm.cpu.cs, vm.cpu.ip + 1)
      opcode = byte1 >> 5
      
      cs = vm.cpu.cs
      ip = vm.cpu.ip
      
      if not byte1 & 0x10 and opcode in [Opcode.jmp, Opcode.jmpe, Opcode.hlt]:
         vm.cpu.ip += 1
      else:
         vm.cpu.ip += 2
               
      instruction = None
            
      if opcode == Opcode.jmp:
         instruction = jmp_Instruction(byte1, byte2)
      elif opcode == Opcode.movr:
         instruction = movr_Instruction(byte1, byte2)
      elif opcode == Opcode.movm:
         instruction = movm_Instruction(byte1, byte2)
      elif opcode == Opcode.add:
         instruction = add_Instruction(byte1, byte2)
      elif opcode == Opcode.xor:
         instruction = xor_Instruction(byte1, byte2)
      elif opcode == Opcode.cmp:
         instruction = cmp_Instruction(byte1, byte2)
      elif opcode == Opcode.jmpe:
         instruction = jmpe_Instruction(byte1, byte2)
      elif opcode == Opcode.hlt:
         instruction = hlt_Instruction(byte1, byte2)
      else:
         raise VMException("Invalid opcode")
      
      #print "0x{0:02X}:0x{1:02X}".format(cs, ip), instruction
      
      return instruction
      
      
class jmp_Instruction(Instruction):
   
   def __init__(self, byte1, byte2):
      super(jmp_Instruction, self).__init__(byte1, byte2)
      
   def __str__(self):
      if self.mod:
         return "jmp $0x{0:02X}:r{1}".format(self.op2, self.op1)
      else:
         return "jmp r{0}".format(self.op1)
      
   def execute(self):
      vm.cpu.ip = vm.cpu.r[self.op1]
      
      if self.mod:
         vm.cpu.cs = self.op2


class movr_Instruction(Instruction):
   
   def __init__(self, byte1, byte2):
      super(movr_Instruction, self).__init__(byte1, byte2)
      
   def __str__(self):
      if self.mod:
         return "movr r{0}, $0x{1:02X}".format(self.op1, self.op2)
      else:
         return "movr r{0}, r{1}".format(self.op1, self.op2)
      
   def execute(self):
      if self.mod:
         vm.cpu.r[self.op1] = self.op2
      else:
         vm.cpu.r[self.op1] = vm.cpu.r[self.op2]

      
class movm_Instruction(Instruction):
   
   def __init__(self, byte1, byte2):
      super(movm_Instruction, self).__init__(byte1, byte2)
      
   def __str__(self):
      if self.mod:
         return "movm [ds:r{0}], r{1}".format(self.op1, self.op2)
      else:
         return "movm r{0}, [ds:r{1}]".format(self.op1, self.op2)
      
   def execute(self):
      if self.mod:
         vm.mem.write(vm.cpu.ds, vm.cpu.r[self.op1], vm.cpu.r[self.op2])
      else:
         vm.cpu.r[self.op1] = vm.mem.read(vm.cpu.ds, vm.cpu.r[self.op2])

      
class add_Instruction(Instruction):
   
   def __init__(self, byte1, byte2):
      super(add_Instruction, self).__init__(byte1, byte2)
      
   def __str__(self):
      if self.mod:
         return "add r{0}, $0x{1:02X}".format(self.op1, self.op2)
      else:
         return "add r{0}, r{1}".format(self.op1, self.op2)
      
   def execute(self):
      if self.mod:
         if vm.cpu.r[self.op1] + self.op2 > 0xFF:
            raise VMException("add overflow")
            
         vm.cpu.r[self.op1] = (vm.cpu.r[self.op1] + self.op2) & 0xFF
      else:
         if vm.cpu.r[self.op1] + vm.cpu.r[self.op2] > 0xFF:
            raise VMException("add overflow")
            
         vm.cpu.r[self.op1] = (vm.cpu.r[self.op1] + vm.cpu.r[self.op2]) & 0xFF
 
      
class xor_Instruction(Instruction):
   
   def __init__(self, byte1, byte2):
      super(xor_Instruction, self).__init__(byte1, byte2)
      
   def __str__(self):
      if self.mod:
         return "xor r{0}, $0x{1:02X}".format(self.op1, self.op2)
      else:
         return "xor r{0}, r{1}".format(self.op1, self.op2)
      
   def execute(self):
      if self.mod:            
         vm.cpu.r[self.op1] = vm.cpu.r[self.op1] ^ self.op2
      else:
         vm.cpu.r[self.op1] = vm.cpu.r[self.op1] ^ vm.cpu.r[self.op2]
      
      
class cmp_Instruction(Instruction):
   
   def __init__(self, byte1, byte2):
      super(cmp_Instruction, self).__init__(byte1, byte2)
      
   def __str__(self):
      if self.mod:
         return "cmp r{0}, $0x{1:02X}".format(self.op1, self.op2)
      else:
         return "cmp r{0}, r{1}".format(self.op1, self.op2)
      
   def execute(self):
      value1 = vm.cpu.r[self.op1]
      value2 = 0x00
      
      if self.mod:            
         value2 = self.op2
      else:
         value2 = vm.cpu.r[self.op2]
      
      if value1 == value2:
         vm.cpu.fl = 0x00
      elif value1 < value2:
         vm.cpu.fl = 0xff
      else:
         vm.cpu.fl = 0x01


class jmpe_Instruction(Instruction):
   
   def __init__(self, byte1, byte2):
      super(jmpe_Instruction, self).__init__(byte1, byte2)
      
   def __str__(self):
      if self.mod:
         return "jmpe r{1}:r{0}".format(self.op1, self.op2)
      else:
         return "jmpe r{0}".format(self.op1)
      
   def execute(self):
      if vm.cpu.fl == 0x00:
         vm.cpu.ip = vm.cpu.r[self.op1]
   
         if self.mod:
            vm.cpu.cs = vm.cpu.r[self.op2]


class hlt_Instruction(Instruction):
   
   def __init__(self, byte1, byte2):
      super(hlt_Instruction, self).__init__(byte1, byte2)
      
   def __str__(self):
      return "hlt"
      
   def execute(self):
      raise VMException("Program exited with flag 0x{0:02X}".format(vm.cpu.fl))














