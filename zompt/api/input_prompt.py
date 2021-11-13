from os import system, name
from prompt_toolkit import prompt

class InputPrompt:

  def __init__(self, prompt_text):
    self._prompt_text = prompt_text
    #self.clear()

  #def clear(self):
  #  
  #    # for windows
  #    if name == 'nt':
  #        _ = system('cls')
  #  
  #    # for mac and linux(here, os.name is 'posix')
  #    else:
  #        _ = system('clear')

  def run(self):
    text = prompt(self._prompt_text)

    # Clear the screen
    # There is an issue where previous command output is incorrect, so clear the screen after each selection
    #self.clear()
    return text
