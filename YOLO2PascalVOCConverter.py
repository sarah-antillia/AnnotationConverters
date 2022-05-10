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
# YOLO2PascalVOCConverter.py

import os
import sys
import shutil
from tkinter import W
# pip install lxml
from lxml import etree
from lxml.etree import Element, SubElement, tostring

from PIL import Image

import glob
import argparse
import json
import traceback
sys.path.append("../../")

from ConfigParser import ConfigParser

# classes_file is a text file which contains all classes(labels)
# Example classes.txt
"""
Bicycles_Only
Bumpy_Road
Buses_Priority
Centre_Line
Closed_To_Pedestrians
Crossroads
Dangerous_Wind _Gusts
Directions_Indicator
Falling_Rocks
Keep_Left
...
"""

class YOLO2PascalVOCConverter:
  # Constructor
  def __init__(self, classes_file):
    self.classes_file = classes_file
    self.classes = []
    with open(classes_file, "r") as f:
      all_class_names = f.readlines()
      for class_name in all_class_names:
        class_name = class_name.strip()
        if class_name.startswith("#") ==False:
          self.classes.append(class_name)
    print("==== classes {}".format(self.classes))

  def getClassName(self, class_id):
    name = None
    if class_id >=0 and class_id <len(self.classes):
      name = self.classes[class_id]
    return name
 
  def getAnnotations(self, annotation_file):
    annotations = None
    if os.path.exists(annotation_file) == False:
      raise Exception("Not found annotation file {}".format(annotation_file))
    with open(annotation_file, "r") as f:
      annotations  = f.readlines()
    return annotations


  def run(self, dataset_name, images_dir, output_dir):
    # The dataset_dir(train, valid, or test) contains both something_image.jpg and something_image.txt , and so on.
   
    # We assume the following folder structure:
    # dataset_dir/
    #  +- image1.jpg
    #  +- image1.txt  (YOLO format annotation file to image1.jpg)
    #  ...
    #  ...
    #  +- imageN.jpg
    #  +- imageN.txt  (YOLO format annotation file to imageN.jpg)
    #       
    pattern     = images_dir + "/*.jpg"
    image_files = glob.glob(pattern)

    for image_file in image_files:
      root = etree.Element("annotation")

      print("==== YOLO2XMLConverter.run() processing  image_file {}".format(image_file))
        
      image = Image.open(image_file)
      image_name    = os.path.basename(image_file)
      xml_filename  = image_name.replace(".jpg", ".xml")
      width, height = image.size
      depth         = image.layers
 
      folder         = Element("folder")
      folder.text    = "./"
      root.append(folder)

      filename       = Element("filename")
      filename.text  = str(image_name)
      root.append(filename)

      path           = Element("path")
      dir             =images_dir.split("/")[0]
      print("---- dir {}".format(dir))
      path.text      = str(dir)
      root.append(path)

      source         = Element("source")
      database       = SubElement(source, "database")         
      database.text  = str(dataset_name)
      annotation     = SubElement(source, "annotation")         
      annotation.text  = "PASCAL VOC2007"

      root.append(source)

      size           = Element("size")
      nwidth         = SubElement(size, "width")
      nwidth.text    = str(width)
      nheight        = SubElement(size, "height")
      nheight.text   = str(height)
      ndepth         = SubElement(size, "depth")
      ndepth.text    = str(depth)
      root.append(size)
 
      segmented      = Element("segmented")
      segmented.text = "0"
      root.append(segmented)

      output_imagefile = os.path.join(output_dir, image_name)
      shutil.copy2(image_file, output_imagefile)

      annotation_file = image_file.replace(".jpg", ".txt")
      self.append_object_elements(root, annotation_file, width, height)
      xml_tree = etree.tostring(root, pretty_print=True, encoding='UTF-8')

      output_xmlfile = os.path.join(output_dir, xml_filename)
      with open(output_xmlfile, 'w', encoding="utf-8") as f:
        f.write(xml_tree.decode('utf-8'))

      output_classes_file = os.path.join(output_dir, "classes.txt")
      shutil.copy2(self.classes_file, output_classes_file)

  def append_object_elements(self, root, annotation_file, width, height):    
      width  = float(width)
      height = float(height)

      annotations = self.getAnnotations(annotation_file)

      for annotation in annotations:
        # YOLO annotatiion  - (class_id, x_center, y_center, r_width, r_height)
        # where class_id starts from 0, and x_center, y_center, r_width, r_height are float, and in range [0.0, 1.0]
        # relative coordinate of boundingbox: (x_center, y_center, r_width, r_height)   
        class_id, x_center, y_center, r_width, r_height = annotation.split(" ")
        class_id = int(class_id)
        x_center      = float(x_center) 
        y_center      = float(y_center) 
        r_width       = float(r_width)
        r_height      = float(r_height)
            
        real_x_center = int(x_center * width)
        real_y_center = int(y_center * height)

        real_width    = int(r_width   * width)
        real_height   = int(r_height  * height)

        x_min         = real_x_center - int(real_width/2)
        y_min         = real_y_center - int(real_height/2)
        x_max         = x_min + real_width
        y_max         = y_min + real_height
        class_name    = self.getClassName(class_id)
        object_element= self.create_object_element(class_name, x_min, y_min, x_max, y_max)
        root.append(object_element)

  def create_object_element(self, label, x_min, y_min, x_max, y_max):
    object         = Element("object")
    name           = SubElement(object, "name")
    name.text      = str(label)
 
    pose           = SubElement(object, "pose")
    pose.text      = "Unspecified"
 
    truncated      = SubElement(object, "truncated")
    truncated.text = "0"
 
    difficult      = SubElement(object, "difficult")
    difficult.text = "0"
 
    bndbox         = SubElement(object, "bndbox")
         
    xmin           = SubElement(bndbox, "xmin")
    xmin.text      = str(x_min)
    ymin           = SubElement(bndbox, "ymin")
    ymin.text      = str(y_min)
    xmax           = SubElement(bndbox, "xmax")
    xmax.text      = str(x_max)
    ymax           = SubElement(bndbox, "ymax")
    ymax.text      = str(y_max)
    return object

# python YOLO2PascalVOCConverter.py  ./yolo2pascalvoc_conf 
# Example:
# python YOLO2PascalVOCConverter.py  ./Japanese_Signals/yolo2pascalvoc_conf 

if __name__ == '__main__':
  config_ini   = ""
  try:
    if len(sys.argv) == 2:
      config_ini   = sys.argv[1]
    else:
      raise Exception("Invalid argment")

    DATASET  = "dataset"
    parser   = ConfigParser(config_ini)
    dataset_name = parser.get(DATASET, "name") 
    classes_file = parser.get(DATASET, "classes")

    targets = ["train", "valid"]
    for target in targets:
      #images_dir = directory containing both images and annotation files.
      #YOLO_somewhere/train or YOLO_somewhere/valid
      images_dir = parser.get(target, "images_dir")

      output_dir  = parser.get(target, "output_dir")
      
      if os.path.exists(images_dir) == False:
        raise Exception("Not found images_dir  :{}".format(images_dir))

      if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)

      converter = YOLO2PascalVOCConverter(classes_file)
      converter.run(dataset_name, images_dir, output_dir)

  except:
    traceback.print_exc()
  
