#!/usr/bin/env python3
import os
import os.path
import subprocess
import jupyter
import nbformat


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.realpath(THIS_DIR + "/../..")
NOTEBOOKS_DIR = MAIN_DIR + "/notebooks"
MARKDOWN_DIR = MAIN_DIR + "/markdown"
HTML_OUTPUT_DIR = MAIN_DIR + "/html_output"

def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def filename_to_output_dir(filename: str):
  src_dir = os.path.dirname(os.path.realpath(filename))
  dst_dir = "/sources_docker/" + "html_output" + src_dir.replace("/sources_docker", "")
  mkdirp(dst_dir)
  return dst_dir


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

def find_all_markdowns():
  result = file_with_extension(".md", MARKDOWN_DIR)
  return result


def make_reveal_js_slideshow(notebook_file):
  output_dir = filename_to_output_dir(notebook_file)
  print("outputdir = " + output_dir)
  base_cmd = """jupyter nbconvert --to slides {} \
    --output-dir={}
    --reveal-prefix=reveal.js \
    --SlidesExporter.reveal_theme=serif --SlidesExporter.reveal_scroll=True
   """
  cmd = base_cmd.format(notebook_file, output_dir)
  subprocess.run(cmd, shell=True, check=True)

def make_html_preview(notebook_file):
  output_dir = filename_to_output_dir(notebook_file)
  base_cmd = """jupyter nbconvert --to html {} \
    --output-dir={}
  """
  cmd = base_cmd.format(notebook_file, output_dir)
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
  for f in find_all_markdowns():
    print("Making Markdown previews for {}".format(f))
    make_one_markdown_preview(f)


if __name__ == "__main__":
  os.environ["PATH"] = os.environ["PATH"] + os.pathsep + "/srv/conda/bin"
  make_all_slideshows()
  make_all_md_previews()
