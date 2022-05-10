<h1> AnnotationConverters </h1>
This is a set of some annotatation format converters<br>
<br>
<a href="#1">1 YOLO2TFRecordConverter</a><br>
<a href="#2">2 YOLO2COCOConverter</a><br>
<a href="#3">3 YOLO2PascalVOCConverter</a><br>
<br>
<h2><a name="1">1 YOLO2TFRecordConverter</a></h2>
Usage:<br>
<pre>
python YOLO2TFRecordConverter.py yolo2tfrecord_converter.conf
</pre>

Example<br>
<pre>
python ./YOLO2TFRecordConverter.py ./Japanese_Signals/yolo2tfrecord_converter.conf
</pre>
<pre>
; yolo2tfrecord_converter.conf
[configs]
version      = "2.0"

[dataset]
name         = "jp_signals"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./Japanese_Signals/classes.txt"

tfrecord_dir = "./Japanese_Signals/TFRecord"

label_map_pbtxt = "./Japanese_Signals/TFRecord/label_map.pbtxt"
label_map_yaml  = "./Japanese_Signals/TFRecord/label_map.yaml"

[train]
images_dir   = "./Japanese_Signals/YOLO/train"
anno_dir     = "./Japanese_Signals/YOLO/train"

[valid]
images_dir   = "./Japanese_Signals/YOLO/valid"
anno_dir     = "./Japanese_Signals/YOLO/valid"
</pre>

<br>
<h2><a name="2">2 YOLO2COCOConverter</a></h2>
Usage:<br>
<pre>
python YOLO2COCOConverter.py yolo2coco_converter.conf
</pre>

Example<br>
<pre>
python ./YOLO2COCOConverter.py ./Japanese_Signals/yolo2coco_converter.conf
</pre>

<pre>
; yolo2coco_converter.conf
[configs]
version      = "2.0"

[dataset]
name         = "jp_signals"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./Japanese_Signals/classes.txt"

[train]
images_dir  = "./Japanese_Signals/YOLO/train"
output_dir  = "./Japanese_Signals/COCO/train"

[valid]
images_dir  = "./Japanese_Signals/YOLO/valid"
output_dir  = "./Japanese_Signals/COCO/valid"
</pre>
<br>

<h2><a name="3">3 YOLO2PascalVOCConverter</a></h2>
Usage:<br>
<pre>
python YOLO2PascalVOCConverter.py yolo2pascalvoc_converter.conf
</pre>

Example<br>
<pre>
python ./YOLO2PascalVOCConverter.py ./Japanese_Signals/yolo2pascalvoc_converter.conf
</pre>

<pre>
; yolo2pascalvoc_converter.conf
[configs]
version      = "2.0"

[dataset]
name         = "jp_signals"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./Japanese_Signals/classes.txt"

[train]
images_dir  = "./Japanese_Signals/YOLO/train"
output_dir  = "./Japanese_Signals/PascalVOC/train"

[valid]
images_dir  = "./Japanese_Signals/YOLO/valid"
output_dir  = "./Japanese_Signals/PascalVOC/valid"

</pre>

