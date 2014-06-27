import sublime
import sublime_plugin
import subprocess
import re
import os
import tempfile

# RUBY_METHOD_SEP_PATTERN = re.compile('[^.:]*$')
RUBY_METHOD_SEP_PATTERN = re.compile('((?<=\.).*$)|((?<=::).*$)')

class RsenseCompletions(sublime_plugin.EventListener):

    def get_project(self, view):
      fn = view.file_name()
      project = view.window().folders()
      if len(project) > 0:
        return project[0]
      elif fn is not None:
        return fn
      else:
        return ""

    def make_command(self, view, prefix, location, path):
      detect_proj = self.get_project(view)

      filestring = "--file=%s " % path

      if prefix:
        prefix_str = "--prefix=%s " % prefix
      else:
        prefix_str = ""

      loc_str = "--location=%s " % location
      return "".join([rsense_com, detect_proj, filestring, prefix_str, loc_str])

    def run_command(self, command_string):
      pipe = subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE)
      output, error = pipe.communicate()
      if error is not None:
        print(error)
      return output

    def _sanitize_output(self, output):
      return output.decode('utf-8')

    def _parse_output(self, output):
      lines = output.split("\n")
      line_parts = [line.split(" ", 5) for line in lines]
      return line_parts

    def clean_and_arrange(self, output):
      if output is None:
        return []

      completions = []
      parsed = self._parse_output(self._sanitize_output(output).strip())

      for line in parsed:
        if len(line) >= 5:
          show_string = line[1] + "\t" + line[3] + "\t" + line[4]
          compl = line[1]
          completions.append((show_string, compl))

      return completions

    # TODO: Filter completions for metadata returned by rsense.
    def get_completions(self, view, prefix, location, path):
      command_string = self.make_command(view, prefix, location, path)
      raw_output = self.run_command(command_string)
      return self.clean_and_arrange(raw_output)


    def is_ruby_scope(self, view, location):
      scopes = [
                "source.ruby - comment",
                "source.ruby.rspec - string - comment"
      ]
      match = False

      for scope in scopes:

        if view.match_selector(location, scope):
          match = True

      return match

    def on_query_completions(self, view, prefix, locations):

      if locations is None:
        return []

      location = locations[0]

      if not self.is_ruby_scope(view, location):
        return []

      row, col = view.rowcol(location)
      line_start_offset = location - col
      line_text = view.substr(sublime.Region(line_start_offset, location + 1))

      if not RUBY_METHOD_SEP_PATTERN.search(line_text):
        return []

      text = view.substr(sublime.Region(0, view.size()))

      if text is None:
        return []

      if view.settings().get("repl", False):
        #logger.debug("Rsense does not complete in SublimeREPL views")
        return

      return self.get_completions(view, prefix, location, tmp)

