import sys
from zeys.api.detector import Detector

BACKSPACE_OUTPUT_CHAR='\b'
DELETE_OUTPUT=BACKSPACE_OUTPUT_CHAR + " " + BACKSPACE_OUTPUT_CHAR

class InputPrompt:

  def __init__(self):

    self._input_chars = []
    self._detector = Detector()

  def run(self):

    key_generator = self._detector.run()

    for key in key_generator:
      if(key == "enter"):
        return "".join(self._input_chars)
      elif(key == "esc"):
        pass
      elif(key == "delete"):
        # Delete / Backspace
        if(len(self._input_chars) > 0):
          self._input_chars.pop()
          sys.stdout.write(DELETE_OUTPUT)
          sys.stdout.flush()
      elif(len(key) > 1):
        pass
      else:
        sys.stdout.write(key)
        sys.stdout.flush()
        self._input_chars.append(key)
