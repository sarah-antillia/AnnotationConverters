#  Copyright (c) 2022 Antillia.com TOSHIYUKI ARAI. ALL RIGHTS RESERVED.
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

# COCO2TFRecordConverter.py

# See: https://github.com/tensorflow/models/blob/master/research/object_detection/dataset_tools/create_coco_tf_record.py

# See: https://github.com/MetaPeak/tensorflow_object_detection_create_coco_tfrecord

import os
import sys
from pycocotools.coco import COCO
import shutil
import tensorflow as tf

import dataset_util

from ConfigParser import ConfigParser
from LabelMapCreator import LabelMapCreator
from LabelMapReader import LabelMapReader
from YAMLCreator import YAMLCreator

import traceback
import pprint

class COCO2TFRecordConverter:

  def __init__(self,
            annotation,
            images_dir, 
            label_map_pbtxt, 
            output_dir, 
            dataset="train", 
            filename="foo.tfrecord"):
    self.annotations_file = annotation
    self.images_dir      = images_dir
    self.label_map_pbtxt = label_map_pbtxt 
    self.output_dir      = output_dir 
    self.dataset         = dataset
 
    self.filename        = filename
    reader = LabelMapReader()
    self.label_map_dic, classes = reader.read(self.label_map_pbtxt)
    print("==== label_map_dic {}".format(self.label_map_dic))


  def run(self):
    # load total coco data
    coco_data = self.load_coco_dataset(
                       self.annotations_file, shuffle_img=False)
    total_dataset = len(coco_data)

    print("== total dataset {}".format(total_dataset))

    tfrecord_dir = os.path.join(self.output_dir, self.dataset)
    if os.path.exists(tfrecord_dir) == False:
      os.makedirs(tfrecord_dir)
      
    tfrecord_path = os.path.join(tfrecord_dir, self.filename)

    print("==== tfrecord {}".format(tfrecord_path))

    with tf.io.TFRecordWriter(tfrecord_path) as tfrecord_writer:
      for image_data in coco_data:
        if image_data:
          example = self.convert_to_tf_example(image_data, 
                                    self.label_map_dic)
          tfrecord_writer.write(example.SerializeToString())


  def load_coco_dataset(self, annotations_file, shuffle_img = True):
    coco = COCO(annotations_file)
    print("--- annotations_filepath {}".format(annotations_file))
    img_ids = coco.getImgIds() 
    cat_ids = coco.getCatIds()
    print("--- len img_ids {}".format(len(img_ids)))
    if shuffle_img:
      shuffle(img_ids)

    coco_data = []
    W_SHRINK = 1.0 # float(512)/float(1280)
    H_SHRINK = 1.0 # float(512)/float(720)

    #for index, img_id in enumerate(img_ids):
    for img_id in img_ids:
      
      img_info   = {}
      bboxes     = []
      labels     = []
      img_detail = coco.loadImgs(img_id)[0]
      pprint.pprint(img_detail)
      pic_height = img_detail['height']
      pic_width  = img_detail['width']
      filename   = ""
      try:
        filename = img_detail['file_name']
        filename = os.path.basename(filename)
        print("--- filename {}".format(filename))
      except Exception as ex:
        traceback.print_exc()
      
      pic_height = int(float(pic_height)*H_SHRINK)
      pic_width  = int(float(pic_width)*W_SHRINK)
      ann_ids = coco.getAnnIds(imgIds=img_id,catIds=cat_ids)
      anns = coco.loadAnns(ann_ids)  
      for ann in anns: 
        bboxes_data = ann['bbox']
        bboxes_data[0] = float(bboxes_data[0])*W_SHRINK #Xmin
        bboxes_data[1] = float(bboxes_data[1])*H_SHRINK #Ymin
        bboxes_data[2] = float(bboxes_data[2])*W_SHRINK #width
        bboxes_data[3] = float(bboxes_data[3])*H_SHRINK #height
        bboxes_data = [bboxes_data[0]/float(pic_width), bboxes_data[1]/float(pic_height),\
        bboxes_data[2]/float(pic_width), bboxes_data[3]/float(pic_height)]
        # the format of coco bounding boxs is [Xmin, Ymin, width, height]
        print("---- {}".format(bboxes_data))
        bboxes.append(bboxes_data)
        labels.append(ann['category_id'])

      img_path = os.path.join(self.images_dir, img_detail['file_name'])
      print("--- img_path {}".format(img_path))
      img_bytes = 0
      try:
        img_bytes = tf.io.gfile.GFile(img_path,'rb').read()
        #if img_bytes >0:
        img_info['pixel_data'] = img_bytes
        img_info['height'] = pic_height
        img_info['width'] = pic_width
        img_info['bboxes'] = bboxes
        img_info['labels'] = labels
        img_info['id']     = img_id
        img_info['filename']  = filename

      except Exception as ex:
        print(ex)

      coco_data.append(img_info)
    return coco_data



  def convert_to_tf_example(self, image_data, label_map_dic):
    """Convert python dictionary format data of one image to tf.Example proto.
    Args:
    img_data: infomation of one image, inclue bounding box, labels of bounding box,\
    height, width, encoded pixel data.
    label_map_dic: dictionary of the following format:
    Returns:
    xample: The converted tf.Example
    """

    bboxes   = image_data['bboxes']
    filename = image_data['filename']

    classes_text = []

    for label in image_data['labels']:      
      print("---- label {}".format(label))
      name = label_map_dic[label]
      print("---- name {}".format(name))
      classes_text.append(name.encode('utf8'))
    print("--- classes_text {}".format(classes_text))
    xmin, xmax, ymin, ymax = [], [], [], []

    for bbox in bboxes:
      xmin.append(bbox[0])
      xmax.append(bbox[0] + bbox[2])
      ymin.append(bbox[1])
      ymax.append(bbox[1] + bbox[3])

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/id': dataset_util.int64_feature(image_data['id']),
        'image/filename':dataset_util.bytes_feature(filename.encode('utf8')),

        'image/height': dataset_util.int64_feature(image_data['height']),
        'image/width': dataset_util.int64_feature(image_data['width']),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(image_data['labels']),
        'image/encoded': dataset_util.bytes_feature(image_data['pixel_data']),
        'image/format': dataset_util.bytes_feature('jpeg'.encode('utf-8')),
    }))
    return example

#
# python COCO2TFRecordConverter.py coco2tfrecord_converter.conf

if __name__ == "__main__":

  config_ini  = ""
  try:
    if len(sys.argv) == 2:
      config_ini = sys.argv[1]
    else:
      raise Exception("Invalid argument")

    parser  = ConfigParser(config_ini)
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

    targets = ["train", "valid"]
    for target in targets:
      images_dir  = parser.get(target, "images_dir")
      annotation  = parser.get(target, "annotation")
      if os.path.exists(images_dir) == False:
        raise Exception("Not found " + images_dir)
      
      if os.path.exists(annotation) == False:
        raise Exception("Not found " + annotation)
 
      filename = target + ".tfrecord"
      converter = COCO2TFRecordConverter(
                                 annotation,
                                 images_dir,
                                 label_map_pbtxt,
                                 tfrecord_dir,
                                 dataset  = target, 
                                 filename = filename)
      converter.run()
  except:
    traceback.print_exc()

