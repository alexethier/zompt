from zompt.api.selector import Selector
import tty
import sys
import termios

class ArrowSelectionPrompt:

  def __init__(self, options):

    self._orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

    self._selector = Selector(options) 

  def _right_pressed(self):

    self._selector.cursor_right()
    self._write()

  def _left_pressed(self):

    self._selector.cursor_left()
    self._write()

  def _clear_line(self):
    sys.stdout.write("\r\x1b[K")

  def _write(self):
    self._clear_line()
    sys.stdout.write(self._selector.render())
    sys.stdout.flush()

  def run(self):

    self._write()

    try:
      while True:
        input_char = x=sys.stdin.read(1)[0]
        input_ord = ord(input_char)
        #print("You pressed: " + str(x) + " " + str(ord(x)))
        if(input_ord == ord('\n')):
          self._clear_line()
          sys.stdout.flush()
          return self._selector.selection()
        elif(input_ord == ord('[')):
          input_char2 = x=sys.stdin.read(1)[0]
          input_ord2 = ord(input_char2)
          #print("You pressed: " + str(x) + " " + str(ord(x)))
          if(input_ord2 == ord('C')):
            self._right_pressed()
          if(input_ord2 == ord('D')):
            self._left_pressed()
        elif(input_ord == ord('\x1b')):
          pass
    finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._orig_settings)
