import os

def file_path(tree_name):
  script_dir = os.path.dirname(__file__)
  rel_path = f"saved_trees\\{tree_name}"
  abs_file_path = os.path.join(script_dir, rel_path)
  return abs_file_path