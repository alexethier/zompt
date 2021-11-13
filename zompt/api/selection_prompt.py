import os
import sys
import string
from os import system, name
from prompt_toolkit.key_binding import KeyBindings
from zompt.input.prompt.selector import Selector
from prompt_toolkit import prompt
import zompt.input.prompt.prompt_helper

class SelectionPrompt:

  def __init__(self, prompt_text, options):

    self._bindings = KeyBindings()

    self._suppress_keyboard()

    #self._bindings.add('a')(self._left_pressed)
    #self._bindings.add('d')(self._right_pressed)
    self._bindings.add('left')(self._left_pressed)
    self._bindings.add('right')(self._right_pressed)

    self._prompt_text = prompt_text
    self._selector = Selector(options) 

  def _suppress_keyboard(self):
    for char in string.printable:
      self._bindings.add(char)(self._pass)

  def _pass(self, event):
    pass

  def _right_pressed(self, event):

      self._selector.cursor_right()
      text = self._selector.render()
      sys.stdout.write("\r")
      sys.stdout.write(text)
      sys.stdout.flush()

  def _left_pressed(self, event):

      self._selector.cursor_left()
      text = self._selector.render()
      sys.stdout.write("\r")
      sys.stdout.write(text)
      sys.stdout.flush()

  #def clear(self):

  #  # for windows
  #  if name == 'nt':
  #      _ = system('cls')
  #  
  #  # for mac and linux(here, os.name is 'posix')
  #  else:
  #      _ = system('clear')

  def run(self):
    #prompt(self._prompt_text + os.linesep + os.linesep + "Selections:" + os.linesep + os.linesep + self._selector.render(), key_bindings=self._bindings)
    prompt(self._prompt_text + os.linesep + os.linesep + self._selector.render(), key_bindings=self._bindings)

    # Clear the screen
    # There is an issue where previous command output is incorrect, so clear the screen after each selection
    #self.clear()
    return self._selector.selection()

  def get_stdout_text(self):
    return self._prompt_text + os.linesep + os.linesep + self._selector.render()
