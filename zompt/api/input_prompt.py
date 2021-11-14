import tty
import sys
import termios
import os

class InputPrompt:

  def __init__(self):

    self._orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

    self._input_chars = []

#  def _clear_line(self):
#    sys.stdout.write("\r\x1b[K")
#
#  def _write(self):
#    self._clear_line()
#    sys.stdout.write(self._selector.render())
#    sys.stdout.flush()

  def run(self):

    try:
      while True:
        sys.stdout.flush()

        input_char = x=sys.stdin.read(1)[0]
        input_ord = ord(input_char)
        #print("AE: " + input_char + str(input_ord))
        if(input_ord == 10):
          sys.stdout.write(os.linesep)
          return "".join(self._input_chars)
        elif(input_ord == 27):
          pass
        elif(input_ord == 127):
          if(len(self._input_chars) > 0):
            self._input_chars.pop()
            sys.stdout.write('\b \b')
        else:
          sys.stdout.write(input_char)
          self._input_chars.append(input_char)
    finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._orig_settings)
