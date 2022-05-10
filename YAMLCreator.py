# Copyright 2022 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 
# 2022/05/10 copyright (c) antillia.com

# YAMLCreator.py

import os
import sys
import traceback

class YAMLCreator:

  def __init__(self, classes_file):
    self.classes = []
    with open(classes_file, "r") as file:
      for i in file.read().splitlines():
        #print(i)
        self.classes.append(i)  
    print(self.classes)
    
           
  def qt(self, label):
    line = "'" + label + "'"
    return line

  def create(self, label_map_yaml):
    NL = "\n"
    with open(label_map_yaml, "w") as f:
      for i in range(len(self.classes)):
        label   = self.classes[i]
        label   = self.qt(label)
        print("{} {}".format(i, label))
        ID      = "id: " 
        line =  str(i+1) + ": " + label + NL 
        f.write(line)
    print("--- Create {}".format(label_map_yaml))


if __name__ == "__main__":
  classes_file = "./classes160.txt"
  label_map_yaml = "./label_map.yaml"
  try:
    if os.path.exists(classes_file) == False:
      raise Exception("Not found "+ images_dir)
    yaml = YAMLCreator(classes_file)
    yaml.create(label_map_yaml)
    #bb.run(images_dir, output_dir)
    
  except:
    traceback.print_exc()

