class Selector:

  def __init__(self, options):
    self._index = 0
    self._options = options

    self._option_pad = 16
    for option in options:
      if len(option) > self._option_pad:
        self._option_pad = len(option) + 7

  def cursor_left(self):
    self._index = (self._index - 1) % len(self._options)

  def cursor_right(self):
    self._index = (self._index + 1) % len(self._options)

#  def render(self):
#
#    output_strings = []
#
#    for i in range(0, len(self._options)):
#      if(i == self._index):
#        output_strings.append("-->[" + self._options[i] + "]")
#      else:
#        output_strings.append(self._options[i])
#
#    return " ".join(output_strings)

  def render(self):

    padded_strings = []
    for option in self._options:
      padded_strings.append(option.ljust(self._option_pad))

    init_pad = "        "
    main_string = list("        " + "".join(padded_strings).rstrip())
    start_index = (self._index) * self._option_pad + len(init_pad)
    end_index = start_index + len(self._options[self._index])
    main_string[start_index -1] = "["
    main_string[start_index -2] = ">"
    main_string[start_index -3] = "-"
    main_string[start_index -4] = "-"

    if(end_index < len(main_string)):
      main_string[end_index] = "]"
      # We need to overwrite the previous line completely so an extra space is needed to cover previous output
      return "".join(main_string) + " "
    else:
      return "".join(main_string) + "]"

  def selection(self):
    return self._options[self._index]
