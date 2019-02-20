#------------如果你需要使用python调用OCR识别图像，再进行如下操作--------#
1、安装Tesseract-OCR引擎，注意要3.0以上才支持中文哦，按照提示安装就行，默认路径安装并修改环境变量。

2、解压已下载chi_sim.traindata字库。要有这个才能识别中文。将chi_sim.traindata 放到Tesseract-OCR项目的tessdata文件夹里面。

3.下载安装FireFox浏览器并安装下载相应的驱动（https://github.com/mozilla/geckodriver/releases/）

4.将下载下来的驱动放到python安装目录中的Script文件夹下，同时将Script文件夹加入环境变量中