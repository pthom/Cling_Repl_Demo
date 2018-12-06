#!/usr/bin/env python3
import os
import os.path
import subprocess
import jupyter
import nbformat
import json


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
    --output-dir={} \
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


def copy_reveal_js():
  # copy reveal.js
  print("copy_reveal_js")
  cmd = "cp -a {}/reveal.js {}/notebooks/".format(NOTEBOOKS_DIR, HTML_OUTPUT_DIR)
  subprocess.run(cmd, shell=True, check=True)

def extract_notebook_infos(notebook_file: str):
  with open(notebook_file) as f:
    json_str = f.read()
  json_data = json.loads(json_str)
  content = json_data["cells"][0]["source"][0]
  lines = content.split("\n")
  print("Content=" + content)
  title = lines[0][2:] # skip "# "
  abstract = lines[1]
  return title, abstract


def make_one_notebook_links(notebook_file):
  title, abstract = extract_notebook_infos(notebook_file)
  filename = os.path.basename(notebook_file)
  md_template = """
# {TITLE}
{ABSTRACT}
* <a href="{FILENAME}.html" target="_blank">Static page</a>
* <a href="/notebooks/{FILENAME}.ipynb" target="_blank">Open notebook from you local clone of this repo</a>
* <a href="{FILENAME}.slides.html" target="_blank">Slideshow</a>
* <a href="https://mybinder.org/v2/gh/pthom/Cling_Repl_Demo/master?filepath=notebooks%2F{FILENAME}.ipynb"
  target="_blank">Interactive notebook online</a>
  (Requires 1 minute to load : it is recommended to open this link in a separate tab)
"""
  md_code = md_template
  md_code = md_code.replace("{FILENAME}", filename)
  md_code = md_code.replace("{ABSTRACT}", abstract)
  md_code = md_code.replace("{TITLE}", title)
  return md_code


def make_all_notebook_links():
  notebooks = find_notebooks()
  all_code = ""
  for notebook_file in notebooks:
    md_code = make_one_notebook_links(notebook_file)
    all_code = all_code + md_code
  print(all_code)
  dst_file = MARKDOWN_DIR + "/0.all_notebooks.md"
  with open(dst_file, "w") as f:
    f.write(all_code)


if __name__ == "__main__":
  os.environ["PATH"] = os.environ["PATH"] + os.pathsep + "/srv/conda/bin"
  make_all_notebook_links()
  # make_all_slideshows()
  # make_all_md_previews()
  # copy_reveal_js()
