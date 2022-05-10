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

# LabelMapCreator.py

import os
import sys
import traceback

class LabelMapCreator:

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

  def create(self, label_map_pbtxt):
    NL = "\n"
    with open(label_map_pbtxt, "w") as f:
      for i in range(len(self.classes)):
        label   = self.classes[i]
        label   = self.qt(label)
        print("{} {}".format(i, label))
        DISPLAY = "  display_name: "
        ID      = "  id: " 
        NAME    = "  name: "
        line = "item {" + NL + DISPLAY + label + NL  + ID  + str(i+1) + NL + NAME + label + NL + "}"  + NL
        f.write(line)
    print("--- Created {}".format(label_map_pbtxt))

    
if __name__ == "__main__":
  classes_file = "./classes86.txt"
  label_map_pbtxt = "./label_map.pbtxt"
  try:
    if os.path.exists(classes_file) == False:
      raise Exception("Not found "+ images_dir)
    bb = LabelMapCreator(classes_file)
    bb.create(label_map_pbtxt)
    #bb.run(images_dir, output_dir)
    
  except:
    traceback.print_exc()

