#!/usr/bin/env python3
import os
import os.path
import subprocess
import jupyter
import nbformat
import json
import shutil
import copy

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.realpath(THIS_DIR + "/../..")
NOTEBOOKS_DIR = MAIN_DIR + "/notebooks"
MARKDOWN_DIR = MAIN_DIR + "/markdown"
HTML_OUTPUT_DIR = MAIN_DIR + "/html_output"
NOTEBOOK_LOCALHOST = "http://localhost:8888"

IGNORED_FOLDERS = [".ipynb_checkpoints"]

def is_ignored_folder(folder):
  matches = [folder.endswith(ignored_folder) for ignored_folder in IGNORED_FOLDERS ]
  has_one_match = any(matches)
  return has_one_match


def filename_without_ext(path_to_file):
  return os.path.splitext(path_to_file)[0]


def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def filename_to_output_dir(filename: str):
  src_dir = os.path.dirname(os.path.realpath(filename))
  dst_dir = "/sources_docker/" + "html_output" + src_dir.replace("/sources_docker", "")
  mkdirp(dst_dir)
  return dst_dir


def directory_files_with_extension(directory:str, extension:str, add_directory:bool = True):
  all_files = os.listdir(directory)
  files = [ f for f in all_files if f.endswith(extension) ]
  files = sorted(files)
  if add_directory:
    result = [ "{}/{}".format(directory, f) for f in files ]
  else:
    result = [ "{}".format(f) for f in files ]
  return result


def files_with_extension_recursive(directory: str, extension: str):
  result = []
  for current_dir, _, files in os.walk(directory, followlinks=True):
    if not is_ignored_folder(current_dir):
      for file in files:
        if file.endswith(extension):
          result.append(current_dir + "/" + file)
  return result



def find_notebooks(recurse: bool):
  if (recurse):
    return files_with_extension_recursive(NOTEBOOKS_DIR, ".ipynb")
  else:
    return directory_files_with_extension(NOTEBOOKS_DIR, ".ipynb")


def find_all_markdowns():
  return files_with_extension_recursive(MARKDOWN_DIR, ".md")


def shall_make_slideshow(notebook_file):
  with open(notebook_file) as f:
    metadata = json.load(f)["metadata"]
  if "output_slideshow" in metadata:
    if metadata["output_slideshow"]:
      print("shall_make_slideshow({}) => True", notebook_file)
      return True
  print("shall_make_slideshow({}) => False", notebook_file)
  return False


def make_notebook_slideshow(notebook_file):
  if not shall_make_slideshow(notebook_file):
    return
  output_dir = filename_to_output_dir(notebook_file)
  print("outputdir = " + output_dir)
  base_cmd = """jupyter nbconvert --to slides {} \
    --output-dir={} \
    --reveal-prefix=reveal.js \
    --SlidesExporter.reveal_theme=serif --SlidesExporter.reveal_scroll=True
   """
  cmd = base_cmd.format(notebook_file, output_dir)
  subprocess.run(cmd, shell=True, check=True)


def convert_notebook(notebook_file, export_format):
  output_dir = filename_to_output_dir(notebook_file)
  base_cmd = """jupyter nbconvert --to {} {} \
    --output-dir={}
  """
  cmd = base_cmd.format(export_format, notebook_file, output_dir)
  subprocess.run(cmd, shell=True, check=True)


def convert_notebook_to_html(notebook_file):
  convert_notebook(notebook_file, "html")


def make_all_notebook_previews():
  for f in find_notebooks(True):
    print("Making previews for {}".format(f))
    make_notebook_slideshow(f)
    convert_notebook_to_html(f)
    convert_notebook(f, "markdown")


def write_markdown_as_notebook(markdown_code: str, out_ipynb_filename):
  nb = nbformat.v4.new_notebook()
  nb['cells'] = [nbformat.v4.new_markdown_cell(markdown_code)]
  with open(out_ipynb_filename, 'w') as f:
      nbformat.write(nb, f)


def make_one_markdown_preview(notebook_file):
  print("make_one_markdown_preview: " + notebook_file)
  with open(notebook_file) as f:
    markdown_code = f.read()
  tmp_notebook = filename_without_ext(notebook_file) + ".ipynb"
  write_markdown_as_notebook(markdown_code, tmp_notebook)
  convert_notebook_to_html(tmp_notebook)
  os.remove(tmp_notebook)


def make_all_md_previews():
  for f in find_all_markdowns():
    print("Making Markdown previews for {}".format(f))
    make_one_markdown_preview(f)


def copy_utilities():
  # copy reveal.js
  print("copy reveal.js")
  cmd = "cp -a notebooks/reveal.js html_output/notebooks/"
  subprocess.run(cmd, shell=True, check=True)
  print("copy images")
  cmd = "cp -a notebooks/data html_output/notebooks/"
  subprocess.run(cmd, shell=True, check=True)
  cmd = "cp -a notebooks/data html_output/notebooks/"
  subprocess.run(cmd, shell=True, check=True)
  cmd = "cp -a markdown/images html_output/markdown/"
  subprocess.run(cmd, shell=True, check=True)
  cmd = "cp -a markdown/movies html_output/markdown/"
  subprocess.run(cmd, shell=True, check=True)


def notebook_collect_h1_titles(json_data):
  cells = json_data["cells"]
  h1_title_list = []
  for cell in cells:
    if cell["cell_type"] == "markdown":
      for line in cell["source"]:
        if line[:2] == "# ":
          line = line.replace("\n", "")
          h1_title_list.append(line)
  return h1_title_list

def notebook_make_toc(h1_title_list):
  html = """# Table of content
<table>
<tr><td>
<p style="text-align: left;">
__ITEMS__
</p>
</tr></td>
</table>
"""
  html_one = "   <a href=\"#__ANCHOR__\">__TITLE__</a><br/>\n"
  def title_to_anchor(title):
    anchor = title
    # anchor = anchor.lower()
    anchor = anchor.replace("# ", "")
    anchor = anchor.replace(" ", "-")
    anchor = anchor.replace(":", "")
    return anchor
  html_all = ""
  for h1_title in h1_title_list:
    h1_link_text = h1_title.replace("# ", "")
    anchor = title_to_anchor(h1_title)
    html_all = html_all + html_one.replace("__TITLE__", h1_link_text).replace("__ANCHOR__", anchor)
  html = html.replace("__ITEMS__", html_all)
  html_lines = html.split("\n")
  html_lines = list(map( lambda s : s + "\n", html_lines ))

  json_toc_cell =   {
   "cell_type": "markdown",
   "metadata": {},
   "source": []
  }
  json_toc_cell["source"] = html_lines
  return json_toc_cell


def notebook_add_toc_links_after_headers(notebook_cells_i):
  notebook_cells_o = copy.deepcopy(notebook_cells_i)
  toc_link = """\n<a href="#Table-of-content"><img src="https://img.shields.io/badge/%3C%20top-E7E7E7.svg" align="right"></a>\n"""
  for cell in notebook_cells_o:
    source_no_toc_link = [line for line in cell["source"] if "#Table-of-content" not in line]

    source_with_toc_link = []
    for line in source_no_toc_link:
      if line[:2] == "# " or line[:3] == "## ":
        source_with_toc_link.append(toc_link)
      source_with_toc_link.append(line)

    cell["source"] = source_with_toc_link

  return notebook_cells_o


# Table of content in a notebook
def make_notebook_toc(notebook_file: str):
  with open(notebook_file, "r") as f:
    json_str = f.read()
  json_data = json.loads(json_str)
  if "Table of content" in json_data["cells"][0]["source"][0]:
      json_data["cells"] = json_data["cells"][1:]
  h1_title_list = notebook_collect_h1_titles(json_data)
  json_toc_cell = notebook_make_toc(h1_title_list)
  json_data["cells"] = [ json_toc_cell ] + notebook_add_toc_links_after_headers(json_data["cells"])
  out = json.dumps(json_data, sort_keys=True, indent=1)
  with open(notebook_file, "w") as f:
    f.write(out)

def notebook_flag_wants_toc(notebook_file):
  with open(notebook_file, "r") as f:
    json_str = f.read()
  json_data = json.loads(json_str)
  if "toc" in json_data["metadata"]:
    aux = json_data["metadata"]["toc"]
    return aux
  return False


def make_all_notebook_tocs():
  notebooks = find_notebooks(True)
  for notebook_file in notebooks:
    if notebook_flag_wants_toc(notebook_file):
      make_notebook_toc(notebook_file)


def extract_notebook_infos(notebook_file: str):
  with open(notebook_file) as f:
    json_str = f.read()
  json_data = json.loads(json_str)
  cell_data_list = json_data["cells"][0]["source"]
  title = cell_data_list[0]
  title = title[2:] # skip "# "
  abstract = cell_data_list[1]
  return title, abstract

def remove_line_matching(text, what_to_match):
  lines = text.split("\n")
  lines = filter(lambda line : what_to_match not in line, lines)
  return "\n".join(lines)

def make_one_notebook_links(notebook_file):
  title, abstract = extract_notebook_infos(notebook_file)
  base_filename = os.path.basename(notebook_file).replace(".ipynb", "")
  md_template = """
### {TITLE}
{ABSTRACT}
View this document:
* <a href="../notebooks/{FILENAME}.slides.html" target="_blank">as a slideshow</a>(opens in a new window)
* <a href="../notebooks/{FILENAME}.html">as a static page</a>
* <a href="https://mybinder.org/v2/gh/pthom/Cling_Repl_Demo/master?filepath=notebooks%2F{FILENAME}.ipynb"
  target="_blank">as an interactive notebook online</a>
  (opens in a new window, may require 1 minute to load. Be patient!)
* <a href="{NOTEBOOK_LOCALHOST}/notebooks/{FILENAME}.ipynb" target="_blank">
  as a notebook on your local clone of this repo</a> (opens in a new window)
"""
  md_code = md_template
  md_code = md_code.replace("{NOTEBOOK_LOCALHOST}", NOTEBOOK_LOCALHOST)
  md_code = md_code.replace("{FILENAME}", base_filename)
  md_code = md_code.replace("{ABSTRACT}", abstract)
  md_code = md_code.replace("{TITLE}", title)
  if not shall_make_slideshow(notebook_file):
    md_code = remove_line_matching(md_code, "slideshow")
  return md_code


def make_all_notebook_links():
  notebooks = find_notebooks(False)
  all_code = ""
  for notebook_file in notebooks:
    md_code = make_one_notebook_links(notebook_file)
    all_code = all_code + md_code
  dst_file = MARKDOWN_DIR + "/_gen.all_notebooks.md"
  with open(dst_file, "w") as f:
    f.write(all_code)

def copy_cpp_examples():
  for cpp_file in directory_files_with_extension(NOTEBOOKS_DIR, ".cpp"):
    basename = os.path.basename(cpp_file)
    out_dir = filename_to_output_dir(cpp_file)
    shutil.copy(cpp_file, out_dir + "/" + basename)
  for cpp_file in directory_files_with_extension(NOTEBOOKS_DIR, ".h"):
    basename = os.path.basename(cpp_file)
    out_dir = filename_to_output_dir(cpp_file)
    shutil.copy(cpp_file, out_dir + "/" + basename)


def make_md_index():
  md_src_file = MARKDOWN_DIR + "/index.template.md"
  md_dst_file = MARKDOWN_DIR + "/index.md"
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
  files = files_with_extension_recursive(directory= NOTEBOOKS_DIR, extension= ".ipynb")
  print("{}".format(files))
  mkdirp(HTML_OUTPUT_DIR)
  make_all_notebook_tocs()
  make_all_notebook_links()
  make_md_index()
  make_all_notebook_previews()
  make_all_md_previews()
  copy_utilities()
  copy_cpp_examples()
