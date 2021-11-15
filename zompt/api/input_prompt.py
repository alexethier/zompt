import tty
import sys
import termios
import os
import io

text = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12345678910!@#$%^&*()-=_+[]{}|`~:;"\'\\'
CHAR_MAP = {}
for char in text:
  CHAR_MAP[char] = None

DELETE_CHAR='\x7f'
ENTER_CHAR='\n'
ESC_CHAR='\x1b'
#BACKSPACE_OUTPUT_CHAR='\b'
#DELETE_OUTPUT=BACKSPACE_OUTPUT_CHAR + " " + BACKSPACE_OUTPUT_CHAR

class InputPrompt:

  def __init__(self):

    #self._orig_settings = termios.tcgetattr(sys.stdin)
    #tty.setcbreak(sys.stdin)

    self._input_chars = []


#  def _clear_line(self):
#    sys.stdout.write("\r\x1b[K")
#
#  def _write(self):
#    self._clear_line()
#    sys.stdout.write(self._selector.render())
#    sys.stdout.flush()

  def run(self):

    with io.open(sys.stdin.fileno(), 'rb', buffering=0, closefd=True) as std:

      while True:
        #sys.stdout.flush()

        input_obj = x=std.read(1)[0]
        input_char = chr(input_obj)
        if(input_char == ENTER_CHAR):
          #sys.stdout.write(os.linesep)
          return "".join(self._input_chars)
        elif(input_char == ESC_CHAR):
          pass
        elif(input_char == DELETE_CHAR):
          # Delete / Backspace
          if(len(self._input_chars) > 0):
            self._input_chars.pop()
            #sys.stdout.write(DELETE_OUTPUT)
        else:
          if(input_char in CHAR_MAP):
            #print(str(input_ord) + " " + str(input_char))
            #sys.stdout.write(input_char)
            self._input_chars.append(input_char)
