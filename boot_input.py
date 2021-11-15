from zompt.api.input_prompt import InputPrompt
import sys

class Boot:

  def __init__(self):
    pass;

  def boot(self):

    sys.stdout.write("Example prompt: ")
    sys.stdout.flush()
    input_prompt = InputPrompt()
    result = input_prompt.run()
    print()
    print("Result: " + result)

if __name__ == "__main__":
  boot = Boot()
  boot.boot()
