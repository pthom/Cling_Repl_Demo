#!/usr/bin/env python3
import os
import os.path
import subprocess
import jupyter
import nbformat
import json
import shutil

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.realpath(THIS_DIR + "/../..")
NOTEBOOKS_DIR = MAIN_DIR + "/notebooks"
MARKDOWN_DIR = MAIN_DIR + "/markdown"
HTML_OUTPUT_DIR = MAIN_DIR + "/html_output"
NOTEBOOK_LOCALHOST = "http://localhost:8888"

def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def filename_to_output_dir(filename: str):
  src_dir = os.path.dirname(os.path.realpath(filename))
  dst_dir = "/sources_docker/" + "html_output" + src_dir.replace("/sources_docker", "")
  mkdirp(dst_dir)
  return dst_dir


def list_files_with_extension(extension:str, directory:str, add_directory:bool = True):
  all_files = os.listdir(directory)
  files = [ f for f in all_files if f.endswith(extension) ]
  files = sorted(files)
  if add_directory:
    result = [ "{}/{}".format(directory, f) for f in files ]
  else:
    result = [ "{}".format(f) for f in files ]
  return result


def find_notebooks():
  return list_files_with_extension(".ipynb", NOTEBOOKS_DIR)

def find_all_markdowns():
  result = []
  for root, dirs, files in os.walk(MARKDOWN_DIR):
    for file in files:
      if file.endswith(".md"):
        result.append(root + "/" + file)
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
  print("make_one_markdown_preview: " + notebook_file)
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


def copy_utilities():
  # copy reveal.js
  print("copy reveal.js")
  cmd = "cp -a {}/reveal.js {}/notebooks/".format(NOTEBOOKS_DIR, HTML_OUTPUT_DIR)
  subprocess.run(cmd, shell=True, check=True)
  print("copy images")
  cmd = "cp -a {}/images {}/markdown/".format(MARKDOWN_DIR, HTML_OUTPUT_DIR)
  subprocess.run(cmd, shell=True, check=True)
  cmd = "cp -a {}/data {}/notebooks/".format(NOTEBOOKS_DIR, HTML_OUTPUT_DIR)
  subprocess.run(cmd, shell=True, check=True)

def extract_notebook_infos(notebook_file: str):
  with open(notebook_file) as f:
    json_str = f.read()
  json_data = json.loads(json_str)
  cell_data_list = json_data["cells"][0]["source"]
  title = cell_data_list[0]
  title = title[2:] # skip "# "
  abstract = cell_data_list[1]
  return title, abstract


def make_one_notebook_links(notebook_file):
  title, abstract = extract_notebook_infos(notebook_file)
  base_filename = os.path.basename(notebook_file).replace(".ipynb", "")
  md_template = """
### {TITLE}
{ABSTRACT}
Choose between 4 ways to view this document:
* <a href="../../notebooks/{FILENAME}.html" target="_blank">Static page</a>
* <a href="../../notebooks/{FILENAME}.slides.html" target="_blank">As a slideshow</a>
* <a href="https://mybinder.org/v2/gh/pthom/Cling_Repl_Demo/master?filepath=notebooks%2F{FILENAME}.ipynb"
  target="_blank">Interactive notebook online</a>
  (Requires 1 minute to load : it is recommended to open this link in a separate tab)
* <a href="{NOTEBOOK_LOCALHOST}/notebooks/{FILENAME}.ipynb" target="_blank">Open notebook from you local clone of this repo</a>
"""
  md_code = md_template
  md_code = md_code.replace("{NOTEBOOK_LOCALHOST}", NOTEBOOK_LOCALHOST)
  md_code = md_code.replace("{FILENAME}", base_filename)
  md_code = md_code.replace("{ABSTRACT}", abstract)
  md_code = md_code.replace("{TITLE}", title)
  return md_code


def make_all_notebook_links():
  notebooks = find_notebooks()
  all_code = ""
  for notebook_file in notebooks:
    md_code = make_one_notebook_links(notebook_file)
    all_code = all_code + md_code
  dst_file = MARKDOWN_DIR + "/_gen.all_notebooks.md"
  with open(dst_file, "w") as f:
    f.write(all_code)

def copy_cpp_examples():
  for cpp_file in list_files_with_extension(".cpp", NOTEBOOKS_DIR):
    basename = os.path.basename(cpp_file)
    out_dir = filename_to_output_dir(cpp_file)
    shutil.copy(cpp_file, out_dir + "/" + basename)


def make_md_index():
  md_src_file = MARKDOWN_DIR + "/index.template.md"
  md_dst_file = MARKDOWN_DIR + "/_gen.index.md"
  with open(md_src_file, "r") as f:
    final_content = f.read()
  lines = final_content.split("\n")
  include_marker = ">>INCLUDE "
  final_content = ""
  for line in lines:
      if line.startswith(include_marker):
        included_file = line.replace(include_marker, "")
        with open(MARKDOWN_DIR + "/" + included_file, "r") as f:
          included_md = f.read()
        final_content = final_content + included_md
      else:
        final_content = final_content + line + "\n"
  with open(md_dst_file, "w") as f:
    f.write(final_content)


if __name__ == "__main__":
  os.environ["PATH"] = os.environ["PATH"] + os.pathsep + "/srv/conda/bin"
  mkdirp(HTML_OUTPUT_DIR)
  make_all_notebook_links()
  make_md_index()
  make_all_slideshows()
  make_all_md_previews()
  copy_utilities()
  copy_cpp_examples()
