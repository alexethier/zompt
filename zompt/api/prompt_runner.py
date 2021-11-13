import json
import os
import sys
import logging
from prompt_toolkit import prompt
from zompt.input.prompt.selection_prompt import SelectionPrompt
from zompt.input.prompt.input_prompt import InputPrompt
from zfind.api.core_find import Find
from zompt.api.finder_core import FinderRefactor
from zompt.api.rename.renamer_core import RenamerRefactor
from zompt.api.entries import Entries
from zompt.input.prompt.prompt_helper import PromptHelper
from zompt.run.runner_helper import RunnerHelper

class PromptRunner:

  def __init__(self, loader):
    self._prompt_helper = PromptHelper()
    self._loader = loader
    self._runner_helper = RunnerHelper()

    self._preview_files = []
    self._preview_extended = True

  def _preview(self, use_previous=False):

    if(not use_previous):
     
      self._preview_files = [] 
      self._preview_extended = True
      find = Find()

      # Provide user a preview of matched files
      file_filter_tokens = self._loader.get_file_filter_tokens()
      file_matches = find.find(".", file_filter_tokens, only_files=True)

      try:
        for i in range(0,7):
          file_match = next(file_matches)
          #if(file_match is None):
          #  self._preview_extended = False
          #  break
          self._preview_files.append(file_match)
      except StopIteration:
        self._preview_extended = False

      # Check one additional file to see if the sequence stops or continues
      if(self._preview_extended):
        last_match = next(file_matches)
        if(last_match is None):
          self._preview_extended = False

    print("The following files may be edited:")
    for file_match in self._preview_files:
      print(file_match)
    if(self._preview_extended):
      print("... (continued)")
    print()

  def _prompt_file_filters(self):

    add_file_filter_prompt = SelectionPrompt("Add a filter to only edit certain files? (use arrow keys to select)", ["no","yes"])
    add_filter = add_file_filter_prompt.run()

    while True and add_filter == "yes":
      self._prompt_helper.clear()
      self._preview(True)
      file_filter_inclusive_prompt = SelectionPrompt("Is this filter including or excluding matches? (use arrow keys to select)", ["include","exclude"])
      selection = file_filter_inclusive_prompt.run()
      output_text = file_filter_inclusive_prompt.get_stdout_text()
      self._prompt_helper.clear()
      self._preview(True)
      print(output_text)
      print()
      input_key = ""
      if(selection == "exclude"):
        input_key = input_key + "e"

      file_filter_text_prompt = InputPrompt("Input token to match against: ")
      token_text = file_filter_text_prompt.run()

      valid = self._loader.load_file_filter_token(input_key, token_text)
      if(not valid):
        print("Invalid rule: " + input_key + " was not added.")

      self._prompt_helper.clear()
      self._preview()
      continue_prompt = SelectionPrompt("Add another rule? (use arrow keys to select)", ["no","yes"])
      continue_selection = continue_prompt.run()
      if(continue_selection == "no"):
        break

  def _prompt_zompt_tokens(self):

    self._prompt_helper.clear()

    continue_prompt_text = None
    while True:

      if(continue_prompt_text is not None or len(self._loader.get_find_tokens()) == 0):

        if(continue_prompt_text is not None):
          self._prompt_helper.clear()
          print("Current find tokens: " + ", ".join(self._loader.get_find_tokens()))
          print()
          print(continue_prompt_text)
          print()
          
        zompt_find_prompt = InputPrompt("Input token to find: ")
        find_token_text = zompt_find_prompt.run()
        self._loader.add_find_token(find_token_text)


      self._prompt_helper.clear()
      print("Current find tokens: " + ", ".join(self._loader.get_find_tokens()))
      print()
      continue_prompt = SelectionPrompt("Add another token to find? (use arrow keys to select)", ["no","yes"])
      continue_selection = continue_prompt.run()
      continue_prompt_text = continue_prompt.get_stdout_text()
      if(continue_selection == "no"):
        break
      print()

    self._prompt_helper.clear()
    print("Current find tokens: " + ", ".join(self._loader.get_find_tokens()))
    print()

    continue_prompt_text = None
    while True:

      if(continue_prompt_text is not None or len(self._loader.get_replace_tokens()) == 0):

        if(continue_prompt_text is not None):
          self._prompt_helper.clear()
          print("Current find tokens: " + ", ".join(self._loader.get_find_tokens()))
          print("Current replace tokens: " + ", ".join(self._loader.get_replace_tokens()))
          print()
          print(continue_prompt_text)
          print()

        zompt_replace_prompt = InputPrompt("Input token to replace: ")
        replace_token_text = zompt_replace_prompt.run()
        self._loader.add_replace_token(replace_token_text)
 
      self._prompt_helper.clear()
      print("Current find tokens: " + ", ".join(self._loader.get_find_tokens()))
      print("Current replace tokens: " + ", ".join(self._loader.get_replace_tokens())) 
      print()
      continue_prompt = SelectionPrompt("Add another token to replace? (use arrow keys to select)", ["no","yes"])
      continue_selection = continue_prompt.run()
      continue_prompt_text = continue_prompt.get_stdout_text()
      if(continue_selection == "no"):
        break
      print()

  def generate_command(self):

    find_tokens = self._loader.get_find_tokens()
    replace_tokens = self._loader.get_replace_tokens()

    commands = []

    file_filter_tokens = self._loader.get_file_filter_tokens()
    for file_filter_token in file_filter_tokens:
      filter_command = "-g"
      if(not file_filter_token.is_inclusive()):
        filter_command = filter_command + "e"
      if(file_filter_token.is_regex()):
        filter_command = filter_command + "r"
      if(file_filter_token.is_filename_only()):
        filter_command = filter_command + "f"

      filter_text = file_filter_token.get_token()
      filter_command = filter_command + " " + filter_text
      commands.append(filter_command)

    for find_token in find_tokens:
      commands.append("-f " + find_token)
    
    for replace_token in replace_tokens:
      commands.append("-r " + replace_token)

    return " ".join(commands)

  def _run_zompt(self):

    entries = self._runner_helper.compute_zompt(self._loader)

    replacement_mapping = entries.get_replacement_mappings()
    edited_files = entries.get_files()

    self._prompt_helper.clear()

    print()
    command_text = self.generate_command()
    print("You can run the below command next time:")
    print("zompt -y " + command_text)

    edited_files = entries.get_files()
    entries = self._runner_helper.compute_zompt(self._loader) # This is called again in case any files were edited between prompts.

    if(len(edited_files) == 0):
      print()
      print("No changes detected.")
    else:
 
      # Note this list is different from the preview because it only contains files with matching tokens that will be replaced. 
      print()
      print("The following files will be edited: ")
      for i in range(0, len(edited_files)):
        print(edited_files[i])
        if(i > 7):
          print("... (continued)")
          break

      print()
      print("The following replacements are planned:")
      for find_text in replacement_mapping:
        replacement_text = replacement_mapping[find_text]
        print("    " + find_text + "  ->  " + replacement_text)

      print()

      apply_replacements = "yes"
      apply_prompt = SelectionPrompt("Apply changes? (use arrow keys to select)", ["yes","no"])
      apply_replacements = apply_prompt.run()

      print()
      if(apply_replacements == "yes"):
        self._runner_helper.apply_replacement(entries)
        print("Changes complete")
        print()

        cleanup_prompt = SelectionPrompt("Finalize Changes? (use arrow keys to select)", ["yes - delete backup files", "yes - keep backup files", "no - revert changes"])
        cleanup_action = cleanup_prompt.run()
        print()
        if(cleanup_action == "yes - delete backup files"):
          self._runner_helper.cleanup_backup(entries)
          print("Backup files removed.")
        elif(cleanup_action == "yes - keep backup files"):
          print("Backup files retained.")
        elif(cleanup_action == "no - revert changes"):
          self._runner_helper.revert_backup(entries)
          print("Files reverted.")

  def _run_rename(self):

    rename_action = "yes"
    if(not self._loader.is_skip_zompt()):
      print()
      rename_prompt = SelectionPrompt("Rename files?", ["yes", "no"])
      rename_action = rename_prompt.run()
    print()

    if(rename_action == "yes"):

      rename_map = self._runner_helper.find_rename_candidates(self._loader)
      renamer_zompt = RenamerRefactor()
      rename_operations = list(renamer_zompt.calculate(rename_map))

      if(len(rename_operations) > 0):
        print("The following file rename operations will be applied in order:")
        print()
        index = 1
        for name, rename in rename_operations:
          print(str(index) + ": " + name + " -> " + rename)
          index = index + 1
        print()

        rename_prompt = SelectionPrompt("Apply rename operations?", ["yes", "no"])
        rename_action = rename_prompt.run()
        if(rename_action == "yes"):
          renamer_zompt.apply(rename_operations)
          print()
          print("File renames complete!")
      else:
        print("No file renames found.")

  def run(self):

    try:
      self._prompt_helper.clear()
      print("Interactive mode enabled. Disable interactive mode with '-y'.")
      print()

      if(not self._loader.is_skip_zompt()):
        self._preview()
        self._prompt_file_filters()
        self._prompt_zompt_tokens()
        self._run_zompt()

      if(not self._loader.is_skip_rename()):
        if(self._loader.is_skip_zompt()):
          self._prompt_zompt_tokens()
        self._run_rename()

    except KeyboardInterrupt: 
      pass

    print()
    print("Bye!")
