import sys
from zompt.api.selector import Selector
from zompt.api.detector import Detector

class ArrowSelectionPrompt:

  def __init__(self, options):

    self._detector = Detector()
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

    key_generator = self._detector.run()
    
    for key in key_generator:
      if(key == "enter"):
        #self._clear_line()
        sys.stdout.flush()
        return self._selector.selection()
      elif(key == "arrow-right"):
        self._right_pressed()
      elif(key == "arrow-left"):
          self._left_pressed()
      elif(len(key) > 0):
        pass
