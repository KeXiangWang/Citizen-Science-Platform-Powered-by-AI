######### 调用有道api将中文翻译成英文 ###########
# seq 0 2 | xargs -I {} python dumpData.py --thread {}

######### 将多个结果合并 ########################
# python mergeData.py

######## 检索英文关键词,获取图片路径 ############
# python spider.py

######## 将图片路径list切分成10行一个 ###########
# mkdir -p list
# split -l 10 imgList.txt -d -a 2 list/imgList

######## 多进程下载图片 #########################
seq -f "%02g" 0 33 | xargs -P 10 -I {} python downImage.py --input list/imgList{} --output img

mv img/* ../static/project_image
