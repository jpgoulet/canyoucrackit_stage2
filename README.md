CanYouCrackIt - Stage2 Solution
===============================

This is the solution to the stage 2 of the [canyoucrackit][] challenge. I created a virtual machine using Python to load the data in memory and execute it. Emphasis has been put on code readability.

[canyoucrackit]:http://canyoucrackit.co.uk

To run
------

Simply run using Python the stage2.py file.

Output
------

The output is a simple memory dump where we can clearly see solution.

    0x1B:  AC 22 52 65 7E 27 2B 5A 12 61 0A 01 7A 6B 1D 67 	. . R e . . . Z . a . . z k . g 
    0x1C:  47 45 54 20 2F 64 61 37 35 33 37 30 66 65 31 35 	G E T   / d a 7 5 3 7 0 f e 1 5 
    0x1D:  63 34 31 34 38 62 64 34 63 65 65 63 38 36 31 66 	c 4 1 4 8 b d 4 c e e c 8 6 1 f 
    0x1E:  62 64 61 61 35 2E 65 78 65 20 48 54 54 50 2F 31 	b d a a 5 . e x e   H T T P / 1 
    0x1F:  2E 30 00 00 00 00 00 00 00 00 00 00 00 00 00 00 	. 0 . . . . . . . . . . . . . . 
    0x20:  37 7A 07 11 1F 1D 68 25 32 77 1E 62 23 5B 47 55 	7 z . . . . h . 2 w . b . . G U 
    
Debug
-----

There is a commented print in the instruction.py file located in the static method Instruction.load().

```python
print "0x{0:02X}:0x{1:02X}".format(cs, ip), instruction
```

Uncomment it and you will get a execution listing similar to this:

    0x00:0x00 movr r1, $0x04
    0x00:0x02 movr r3, $0xAA
    0x00:0x04 movm r0, [ds:r2]
    0x00:0x06 xor r0, r3
    0x00:0x08 movm [ds:r2], r0
    0x00:0x0A add r2, $0x01
    0x00:0x0C add r3, $0x01
    0x00:0x0E cmp r2, $0x50
    0x00:0x10 movr r0, $0x14
    0x00:0x12 jmpe r0
    0x00:0x13 jmp r1
    0x00:0x04 movm r0, [ds:r2]
    0x00:0x06 xor r0, r3
    0x00:0x08 movm [ds:r2], r0
