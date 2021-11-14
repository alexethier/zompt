import sys
from zompt.api.arrow_selection_prompt import ArrowSelectionPrompt

class Runner:

  def __init__(self):
    pass;

  def run(self):

    if(len(sys.argv) < 2):
      print("No arguments given.")
      sys.exit(1)

    options = []
    for index in range(1, len(sys.argv)):
      arg = sys.argv[index]
      options.append(arg)

    arrow_selection_prompt = ArrowSelectionPrompt(options)
    selection = arrow_selection_prompt.run()
    print(selection)

def main():
  runner = Runner()
  runner.run()
