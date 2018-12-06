#!/usr/bin/env python3
import os
import os.path
import subprocess
import jupyter
import nbformat

os.environ["PATH"] = os.environ["PATH"] + os.pathsep + "/srv/conda/bin"

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
NOTEBOOKS_DIR = THIS_DIR + "/../../examples/notebooks"


def file_with_extension(extension:str, directory:str, add_directory:bool = True):
  all_files = os.listdir(directory)
  files = [ f for f in all_files if f.endswith(extension) ]
  if add_directory:
    result = [ "{}/{}".format(directory, f) for f in files ]
  else:
    result = [ "{}".format(f) for f in files ]
  return result


def find_notebooks():
  return file_with_extension(".ipynb", NOTEBOOKS_DIR)

def find_md():
  result = file_with_extension(".md", NOTEBOOKS_DIR) + file_with_extension(".md", NOTEBOOKS_DIR + "/help")
  return result


def make_reveal_js_slideshow(notebook_file):
  base_cmd = "jupyter nbconvert --to slides {} --reveal-prefix=reveal.js --SlidesExporter.reveal_theme=serif --SlidesExporter.reveal_scroll=True"
  cmd = base_cmd.format(notebook_file)
  subprocess.run(cmd, shell=True, check=True)

def make_html_preview(notebook_file):
  base_cmd = "jupyter nbconvert --to html {}"
  cmd = base_cmd.format(notebook_file)
  subprocess.run(cmd, shell=True, check=True)


def make_all_slideshows():
  for f in find_notebooks():
    print("Making previews for {}".format(f))
    make_reveal_js_slideshow(f)
    make_html_preview(f)


def write_markdown_as_notebook(markdown_code: str, out_ipynb_filename):
  nb = nbformat.v4.new_notebook()
  nb['cells'] = [nbformat.v4.new_markdown_cell(markdown_code)]
  with open(out_ipynb_filename, 'w') as f:
      nbformat.write(nb, f)


def make_one_markdown_preview(notebook_file):
  with open(notebook_file) as f:
    markdown_code = f.read()
  tmp_notebook = notebook_file + ".ipynb"
  write_markdown_as_notebook(markdown_code, tmp_notebook)
  make_html_preview(tmp_notebook)
  os.remove(tmp_notebook)


def make_all_md_previews():
  for f in find_md():
    print("Making Markdown previews for {}".format(f))
    make_one_markdown_preview(f)


if __name__ == "__main__":
  # make_all_slideshows()
  make_all_md_previews()
