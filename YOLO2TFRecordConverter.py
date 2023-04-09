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

# YOLO2TFRecordConverter.py
# 
# 2022/05/10 copyright (c) antillia.com
# 2022/05/10 Modified filename to YOLO2TFRecordConverter.py

import os
import sys

import dataset_util

from PIL import Image
import tensorflow.compat.v1 as tf
import glob
import io
#import argparse
import shutil
import traceback
from ConfigParser import ConfigParser
from LabelMapCreator import LabelMapCreator
from YAMLCreator import YAMLCreator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  

class YOLO2TFRecordConverter:

  def __init__(self, images_dir, 
               yolo_anno_dir, 
               output_dir, 
               classes_file = "./classes.txt",
               dataset      = "train", 
               filename     = "foo.tfrecord"):
               
    self.images_dir    = images_dir
    self.yolo_anno_dir = yolo_anno_dir
    self.output_dir    = output_dir    #tfrecord/ foo.tfrecord
    self.dataset       = dataset
    self.filename      = filename
    self.class_map     = []

    if os.path.exists(classes_file) == False:
      raise Exception("No found " + classes_file)
      
    with open(classes_file, "r") as f:
      for line in f.readlines():
        self.class_map.append(line.strip("\n"))
        
    print("class_map {}".format(self.class_map))


  def create_tf_example(self, image_file, source_id):
    image_filepath = os.path.join(self.images_dir, image_file)
    
    filename = os.path.basename(image_file)
    print("--- filename {}".format(filename))
    
    # 2021/11/07: Try to use filename as source_id. 
    try:
      # The following line will cause an exception if the filename were a string something 
      # like uuid based name: 'ff290a59-462c-47a1-8a99-017a1b30e550_0_9224.jpg'
      # See also: google/automl/efficientdet/dataloader.py: line 342.
      source_id = tf.strings.to_number(filename)
    except Exception as ex:
      print(ex)

    if not os.path.exists(image_filepath):
      raise Exception("Not found " + image_file)
    with tf.gfile.GFile(image_filepath, 'rb') as fid:
      encoded_jpg = fid.read()

      encoded_jpg_io = io.BytesIO(encoded_jpg)
      image = Image.open(encoded_jpg_io)
      width, height = image.size
      image_format = b'jpg'

      xmins = []
      xmaxs = []
      ymins = []
      ymaxs = []
      classes_text = []
      classes = []
       
      source_id = str(source_id)
      name     = filename.split('.')[0]
      anno_txt_file = name + ".txt"
      anno_txt_filepath = os.path.join(self.yolo_anno_dir, anno_txt_file)
      
      if os.path.exists(anno_txt_filepath) == False:
        print("Not found annotation file {}".format(anno_txt_filepath))
        return
              
      with open(anno_txt_filepath, "r") as file:

        for row in file.readlines():
            
            # YOLO row format: row= (class_id, xcen, ycen, w, h)
         
            print(row)
            items = row.split(" ")
            
            class_id = items[0]
            xcen     = float(items[1])
            ycen     = float(items[2])
            w        = float(items[3])
            h        = float(items[4])
            xmin     = xcen - w/2
            ymin     = ycen - h/2
            xmax     = xmin + w
            ymax     = ymin + h
            
            xmins.append(xmin)
            xmaxs.append(xmax)
            ymins.append(ymin)
            ymaxs.append(ymax)
            
            classes_text.append(class_id.encode('utf-8'))
           
            # class_id may begins with 0
            class_id  = int(class_id)
            class_name = self.class_map[class_id].encode('utf-8')
            print("--- class_id {} class_name {}".format(class_id, class_name))
            
            #2021/11/03: Adding 1 to class_id.
            classes.append(class_id + 1)
            

        tf_example = tf.train.Example(features=tf.train.Features(feature={
            'image/height':             dataset_util.int64_feature(height),
            'image/width':              dataset_util.int64_feature(width),
            'image/filename':           dataset_util.bytes_feature(filename.encode('utf-8')),
            'image/source_id':          dataset_util.bytes_feature(source_id.encode('utf-8')),
            'image/encoded':            dataset_util.bytes_feature(encoded_jpg),
            'image/format':             dataset_util.bytes_feature(image_format),
            'image/object/bbox/xmin':   dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax':   dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin':   dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax':   dataset_util.float_list_feature(ymaxs),
            'image/object/class/text':  dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes),
        }))
        return tf_example


  def run(self):
    # self.dataset is "train" or "valid".
    
    tfrecord_dir = os.path.join(self.output_dir, self.dataset)
    if os.path.exists(tfrecord_dir) == False:
      os.makedirs(tfrecord_dir)
      
    tfrecord_path = os.path.join(tfrecord_dir, self.filename)

    image_files = os.listdir(self.images_dir)
    #print("--- {}".format(image_files))
   
    with tf.python_io.TFRecordWriter(tfrecord_path) as writer:
    
      source_id = 0    
      for image_file in image_files:
        if image_file.endswith(".jpg"):
           
          source_id += 1
          tf_example = self.create_tf_example(image_file, source_id)
          if tf_example != None:
            print("--- writing tf_example {}".format(image_file))
            
            writer.write(tf_example.SerializeToString())
          else:
            print("--- tf_example is None {}".format(image_file))
            raise Exception("== tf_example is None " + image_file)
        if image_file.endswith(".png"):
          print("Sorry, png files not supported")

          
usage = "python YOLO2TFRecordConverter.py yolo2tfrecord_creator.conf "

# python YOLO2TFRecordConverter.py ./yolo2tfrecord_converter.conf 
# Example:
# python YOLO2TFRecordConverter.py ./Japanese_Signals/yolo2tfrecord_converter.conf
# python YOLO2TFRecordConverter.py ./projects/BUSI/yolo2tfrecord_converter.conf

if __name__ == "__main__":
  config_ini = ""
  try:
    if len(sys.argv) == 2:
      config_ini     = sys.argv[1]
    else:
      raise Exception(usage)

    parser  = ConfigParser(config_ini)
    targets = ["train", "valid"]
    DATASET = "dataset"

    classes_file     = parser.get(DATASET, "classes")
    tfrecord_dir     = parser.get(DATASET, "tfrecord_dir")
    label_map_pbtxt  = parser.get(DATASET, "label_map_pbtxt")
    label_map_yaml   = parser.get(DATASET, "label_map_yaml")

    if os.path.exists(tfrecord_dir):
      shutil.rmtree(tfrecord_dir)

    if not os.path.exists(tfrecord_dir):
      os.makedirs(tfrecord_dir)

    labelmap_creator = LabelMapCreator(classes_file)
    labelmap_creator.create(label_map_pbtxt)

    yaml_creator     = YAMLCreator(classes_file)
    yaml_creator.create(label_map_yaml)

    for target in targets:
      images_dir  = parser.get(target, "images_dir")
      anno_dir    = parser.get(target, "anno_dir")
      output_dir  = parser.get(target, "output_dir")
      if os.path.exists(images_dir) == False:
        raise Exception("Not found " + images_dir)
      
      if os.path.exists(anno_dir) == False:
        raise Exception("Not found " + anno_dir)
       
      filename = target + ".tfrecord"
      
      converter = YOLO2TFRecordConverter(images_dir, 
                 anno_dir, 
                 tfrecord_dir, 
                 classes_file = classes_file,
                 dataset      = target, 
                 filename     = filename)
      converter.run()
        

  except:
    traceback.print_exc()
    