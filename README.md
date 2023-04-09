<h1> AnnotationConverters (Updated: 223/04/10) </h1>
This is a set of some annotatation format converters<br>
<li>
2023/04/10 Created <b>projects</b> folder and moved <b>Japanese_Signals</b> folder under the <b>projects</b> folder.
</li>
<li>
2023/04/10 Added new project <b>BUSI(Breast Ultrasound Images)</b> to <b>projects</b>.
</li>

<br>
<a href="#1">1 Usage</a><br>
<a href="#1.1">1.1 YOLO2TFRecordConverter</a><br>
<a href="#1.2">1.2 YOLO2COCOConverter</a><br>
<a href="#1.3">1.3 YOLO2PascalVOCConverter</a><br>
<a href="#2">2 Japanese_Signals</a><br>
<a href="#2.1">2.1 Convert YOLO to TFRecord</a><br>
<a href="#2.2">2.2 Convert YOLO to COCO</a><br> 
<a href="#2.3">2.3 Convert YOLO to PascalVOC</a><br>
<a href="#3">3 BUSI(Breast Ultrasound Images</a><br>
<a href="#3.1">3.1 Convert YOLO to TFRecord</a><br> 
<a href="#3.2">3.2 Convert YOLO to COCO</a><br>

<br>
<h2>
<a name="1">1 Usage </a> 
</h2>

<h3><a name="1.1">1.1 YOLO2TFRecordConverter</a></h3>
Usage:<br>
<pre>
>python YOLO2TFRecordConverter.py yolo2tfrecord_converter.conf
</pre>
<h3><a name="1.2">1.2 YOLO2COCOConverter</a></h3>
Usage:<br>
<pre>
python YOLO2COCOConverter.py yolo2coco_converter.conf
</pre>
<h3><a name="1.3">1.3 YOLO2PascalVOCConverter</a></h3>
Usage:<br>
<pre>
python YOLO2PascalVOCConverter.py yolo2pascalvoc_converter.conf
</pre>

<h2>
<a name="2">2 Japanese_Signals </a> 
</h2>
Change direcotory to <b>Japanese_Signals</b> under <b>./projects</b>.
<h3>
<a name="2.1">2.1 Convert YOLO to TFRecord </a> 
</h3>

Run the following bat file to convert YOLO to TFRecord.
<pre>
>./1_yolo2tfrecord.bat
</pre>
, where the bat file is the following.
<pre>
python ../../YOLO2TFRecordConverter.py ./yolo2tfrecord_converter.conf
</pre>
<pre>
; yolo2tfrecord_converter.conf
; 2023/04/10
[configs]
version      = "2.1"

[dataset]
name         = "jp_signals"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./classes.txt"

tfrecord_dir = "./TFRecord"

label_map_pbtxt = "./TFRecord/label_map.pbtxt"
label_map_yaml  = "./TFRecord/label_map.yaml"

[train]
images_dir   = "./YOLO/train"
anno_dir     = "./YOLO/train"

[valid]
images_dir   = "./YOLO/valid"
anno_dir     = "./YOLO/valid"
</pre>

<br>


<h3>
<a name="2.2">2.2 Convert YOLO to COCO </a> 
</h3>
Run the following bat file to convert YOLO to COCO.
<pre>
>./2_yolo2coco.bat
</pre>
, where the bat file is the following.
<pre>
python ../../YOLO2COCOConverter.py ./yolo2coco_converter.conf
</pre>
, where yolo2coco_converter.conf

<pre>
; yolo2coco_converter.conf
; 2023/04/10
[configs]
version      = "2.1"

[dataset]
name         = "jp_signals"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./classes.txt"

[train]
images_dir  = "./YOLO/train"
output_dir  = "./COCO/train"

[valid]
images_dir  = "./YOLO/valid"
output_dir  = "./COCO/valid"

[test]
images_dir  = "./YOLO/test"
output_dir  = "./COCO/test"
</pre>
<br>


<h3>
<a name="2.3">2.3 Convert YOLO to PascalVOC </a> 
</h3>
Run the following bat file to convert YOLO to PascalVOC.
<pre>
>./3_yolo2pascalvoc.bat
</pre>
, where the bat file is the following.
<pre>
python ../../YOLO2PascalVOCConverter.py ./yolo2pascalvoc_converter.conf
</pre>

<pre>
; yolo2pascalvoc_converter.conf
; 2023/04/10
[configs]
version      = "2.1"

[dataset]
name         = "jp_signals"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./classes.txt"

[train]
images_dir  = "./YOLO/train"
output_dir  = "./PascalVOC/train"

[valid]
images_dir  = "./YOLO/valid"
output_dir  = "./PascalVOC/valid"
</pre>

<!-- NEW BUSI
 -->

<h2>
<a name="3">3 BUSI(Breast Ultrasound Images)</a> 
</h2>
Change direcotory to <b>BUSI</b> under <b>./projects</b>.

<h3>
<a name="3.1">3.1 Convert YOLO to TFRecord </a> 
</h3>

Run the following bat file to convert YOLO to TFRecord.
<pre>
>./1_yolo2tfrecord.bat
</pre>
, where the bat file is the following.
<pre>
python ../../YOLO2TFRecordConverter.py ./yolo2tfrecord_converter.conf
</pre>
<pre>
 yolo2tfrecord_converter.conf
; 2023/04/10
[configs]
version      = "2.1"

[dataset]
name         = "BUSI"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./classes.txt"
tfrecord_dir = "./TFRecord"

label_map_pbtxt = "./TFRecord/label_map.pbtxt"
label_map_yaml  = "./TFRecord/label_map.yaml"

[train]
images_dir   = "./YOLO/train"
anno_dir     = "./YOLO/train"

[valid]
images_dir   = "./YOLO/valid"
anno_dir     = "./YOLO/valid"

</pre>

<br>


<h3>
<a name="3.2">3.2 Convert YOLO to COCO </a> 
</h3>
Run the following bat file to convert YOLO to COCO.
<pre>
>./2_yolo2coco.bat
</pre>
, where the bat file is the following.
<pre>
python ../../YOLO2COCOConverter.py ./yolo2coco_converter.conf
</pre>
, where yolo2coco_converter.conf

<pre>
; yolo2coco_converter.conf
; 2023/04/10
[configs]
version      = "2.1"

[dataset]
name         = "BUSI"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./classes.txt"

[train]
images_dir  = "./YOLO/train"
output_dir  = "./COCO/train"

[valid]
images_dir  = "./YOLO/valid"
output_dir  = "./COCO/valid"

[test]
images_dir  = "./YOLO/valid"
output_dir  = "./COCO/test"
</pre>
<br>


