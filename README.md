# Python Zompt
*zompt* is library for generating user input prompts for Python clis.

# Zompt features
* Text input prompt
* Multiple choice prompt (using arrow keys)

# Installation
```
pip install zompt
```

# Getting Started

## Input Prompt
The most simple example of the Input Prompt would look like this:
```
if __name__ == "__main__":
    print("Example prompt (type some text): ")
    input_prompt = InputPrompt()
    result = input_prompt.run()
    print()
    print("You typed: " + result)
```

## Multiple Choice Prompt
The most simple example of a mupltiple choice prompt would look like this:
```
if __name__ == "__main__":
    if(len(sys.argv) < 2):
      print("No arguments given, include at least two commandline arguments.")
      sys.exit(1)

    options = []
    for index in range(1, len(sys.argv)):
      arg = sys.argv[index]
      options.append(arg)

    print("Select an option (use arrow keys to change selection, press enter when done): ")
    arrow_selection_prompt = ArrowSelectionPrompt(options)
    result = arrow_selection_prompt.run()
    print()
    print()
    print("You selected: " + result)
```

# Philosophy
Sometimes for CLIs less is more. Providing users with a simplified prompting mechanism will help guide them through complex scenarios but with an easy to use interface.
