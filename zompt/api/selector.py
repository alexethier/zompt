class Selector:

  def __init__(self, options):
    self._index = 0
    self._options = options

    self._option_pad = 16
    for option in options:
      if len(option) + 7 > self._option_pad:
        self._option_pad = len(option) + 7

  def cursor_left(self):
    self._index = (self._index - 1) % len(self._options)

  def cursor_right(self):
    self._index = (self._index + 1) % len(self._options)

  def selection(self):
    return self._options[self._index]

  def render(self):

    padded_strings = []
    index = 0
    for option in self._options:
      padded_option_list = list("     " + option + "     ")
      if(index == self._index):
        padded_option_list[1] = "-"
        padded_option_list[2] = "-"
        padded_option_list[3] = ">"
        padded_option_list[4] = "["
        padded_option_list[-5] = "]"
      padded_strings.append("".join(padded_option_list))
      index = index + 1

    main_string = "   " + "".join(padded_strings)

    return main_string
