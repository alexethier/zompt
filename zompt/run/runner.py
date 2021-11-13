import sys
from zompt.input.loader import Loader
from zompt.run.auto_runner import AutoRunner
from zompt.input.prompt.prompt_runner import PromptRunner

class Runner:

  def __init__(self):
    pass;

  def run(self):

    loader = Loader()
    continue_run = loader.run()
    if(not continue_run):
      sys.exit(1)

    child_runner = None
    if(loader.is_interactive()):
      child_runner = PromptRunner(loader)
    else:
      child_runner = AutoRunner(loader)

    child_runner.run()

def main():
  runner = Runner()
  runner.run()
