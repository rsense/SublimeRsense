import sublime
import sublime_plugin
import subprocess
import re
import os
import tempfile
try:
    # Python 3
    import urllib.request as urllib_compat
    from urllib.error import HTTPError, URLError

except (ImportError):
    # Python 2
    import urllib2 as urllib_compat
    from urllib2 import HTTPError, URLError


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

    def make_command(self, view, text, location, path):
      textarr = text.split("\n")
      textstring = ""
      for t in textarr:
        textstring.join([t, "\n"])

      row, col = view.rowcol(location)
      locstring = "".join([str(row), ":", str(col)])

      rsense_com = "./rsense_completions.rb "

      detect_proj = self.get_project(view)

      proj_str = " --project=%s " % detect_proj

      filestring = " --filepath=%s " % path

      text_str = " --text='%s' " % text

      loc_str = " --location='%s' " % locstring
      return "".join([rsense_com, proj_str, filestring, text_str, loc_str])

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
      line_parts = [line.split(" ", 4) for line in lines]
      return line_parts

    def clean_and_arrange(self, output):
      if output is None:
        return []

      completions = []
      parsed = self._parse_output(self._sanitize_output(output).strip())

      for line in parsed:
        if len(line) >= 4:
          show_string = line[0] + "\t" + line[2] + "\t" + line[3]
          compl = line[0]
          completions.append((show_string, compl))

      return completions

    # TODO: Filter completions for metadata returned by rsense.
    def get_completions(self, view, text, location, path):
      command_string = self.make_command(view, text, location, path)
      raw_output = self.run_command(command_string)
      # print(raw_output.decode('utf-8'))
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

    def on_query_completions(self, view, text, locations):

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

      return self.get_completions(view, text, location, view.file_name())

