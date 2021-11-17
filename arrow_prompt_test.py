from zompt.api.arrow_selection_prompt import ArrowSelectionPrompt
import sys

class Boot:

  def __init__(self):
    pass;

  def boot(self):

    if(len(sys.argv) < 2):
      print("No arguments given.")
      sys.exit(1)

    options = []
    for index in range(1, len(sys.argv)):
      arg = sys.argv[index]
      options.append(arg)

    sys.stdout.write("Example prompt: ")
    sys.stdout.flush()
    arrow_selection_prompt = ArrowSelectionPrompt(options)
    result = arrow_selection_prompt.run()
    print()
    print()
    print("Result: " + result)

if __name__ == "__main__":
  boot = Boot()
  boot.boot()
