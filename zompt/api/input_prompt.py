import tty
import sys
import termios

class InputPrompt:

  def __init__(self, options):

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

    self._write()

    try:
      while True:
        input_char = x=sys.stdin.read(1)[0]
        input_ord = ord(input_char)
        if(input_ord == 10):
          return "".join(self._input_chars)
        elif(input_ord == 27):
          pass
        else:
          sys.stdout.write(input_char)
          self._input_chars.append(input_char)
    finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._orig_settings)
