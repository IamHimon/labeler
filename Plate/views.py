#encoding:utf-8
from django.shortcuts import render
#from imageSearchModel import search_img
import time,os
from django import forms
from django.http import HttpResponse
import json
import sys
from PIL import Image
reload(sys)
sys.setdefaultencoding('utf-8')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_IMG_DIR = "/car/static/upload/"
COUNTDIR = BASE_DIR+"/car/static/count.txt"
upload_path = BASE_DIR + BASE_IMG_DIR
DIR = BASE_DIR+"/car/static/upload/"
PlateDIR = BASE_DIR+"/car/static/plateTxt/"
ImgNameDIR = BASE_DIR+"/car/static/plateImg/"
carIndex = BASE_DIR+"/Plate/carIndex.txt"
'''
class plateForm(forms.Form):
    imgName = forms.CharField()
    plateImg = forms.FileField()
'''
carMap = {}
restImgCount = 0

with open(carIndex,'r')as f:
	carRest = f.readlines()


def handle_uploaded_file(f,ImgType,i):
   #newImageName = str(time.time()).split(".")[0]
   destination = open(BASE_DIR+BASE_IMG_DIR+str(i)+"."+ImgType, 'wb')
   for chunk in f.chunks():
      destination.write(chunk)
   destination.close()
   #return newImageName
def index(request):
      #return HttpResponse("Hello world ! ")
     #imgName = request.GET.get('url')
     #context['error'] = 'system exception'	
     return render(request, 'index.html')
def manage(request):
     imgList = []
     context = {}
     with open("plate.txt","a+") as f:
        lines = f.readlines()
        for line in lines:
          line = line.strip()
          arr = line.split(",")
          name = arr[0]
          path = DIR+name
          w,h = Image.open(path).size
          new_w = 500 * float(arr[3]) / w
          new_h = 500 * float(arr[4]) / h
           
          new_x = 500 * float(arr[1]) / w
          new_y = 500 * float(arr[2]) / h
          arr[1] = new_y
          print(arr[1])
          arr[2] = new_x
          arr[3] = new_w
          arr[4] = new_h
          imgList.append(arr)
     context['imgList'] = imgList   
     context['hello'] = "hello111"   
     #print(imgList)
     return render(request, 'manage.html',context)

def getCount():
    with open(COUNTDIR,"r") as f:
      lines = f.readlines()
      line = lines[0]
      count = int(line)+1
    with open(COUNTDIR,"wb") as f:
       f.write(str(count))
    return count
	

def sub(request):
     #return HttpResponse("Hello world ! ")
     #imgName = request.GET.get('url')
     #context['error'] = 'system exception'	
     '''
     if request.method == "POST":
        pf = plateForm(request.POST,request.FILES)
        if pf.is_valid():
            imgName = uf.cleaned_data['username']
            plateImg = uf.cleaned_data['headImg']
            return HttpResponse('upload ok!')
    '''
     with open(carIndex,'r') as f:
        lines = f.readlines()
        for line in lines:
           line = line.strip()
           arr = line.split(",")
           carMap[arr[0]] = arr[1]
     name = request.POST.get('name')
     x = request.POST.get('x')
     y = request.POST.get('y')
     w = request.POST.get('w')
     h = request.POST.get('h')
     x_b = str(int(x)+int(w))
     y_b = str(int(y)+int(h))  #改
     print(x_b)
     print(y_b)
     
     #print(request.FILES['file'])
     #imgType = request.FILES['file'].name.split(".")[1]
     #ImgName = request.FILES['file'].name.split(".")[0]
    
     #handle_uploaded_file(request.FILES['file'],imgType,i) //上传照片
     print("===>>>",x,y,w, h)
     print("===>>>",x,y,x_b, y_b)
     if(x !=None and y != None and x_b!= None and y_b != None):
        line = "1"+"\n"+x+","+y+","+x_b+","+y_b
        with open(PlateDIR+name.split(".")[0]+".txt","w") as f:
           f.write(line+"\n")
           ChangePlateState(carMap,name,"1")#处理成功
        return HttpResponse("1")
     else:
        return HttpResponse("0")


def ChangePlateState(carMap,name,state):
	with open(carIndex,'w') as f:
		for key, value in carMap.items():
			if(key == name):
				value = state
			f.write(key+","+value+"\n")#修改图片处理状态
	#print("长度-》》"+str(len(carMap)))
			


def delPlate(request):
	
	 carMap = {}
	 flag = False
	 ImgName = request.GET.get('ImgName')
	 print(request.GET)
	 print("ImgName=====>>>>>>"+ImgName)
	 with open(carIndex,'r') as f:
		lines = f.readlines()
	 for line in lines:
		line = line.strip()
		arr = line.split(",")
		if(ImgName == arr[0]):
			flag = True #找到需要删除图像
			continue
		carMap[arr[0]] = arr[1]
	 with open(carIndex,'w') as f:
		for key, value in carMap.items():
			f.write(key+","+value+"\n")#
	#不用从磁盘删除文件	
	
	 if(flag):
		#os.remove(ImgNameDIR+ImgName)
		print("删除成功！！！")
		return HttpResponse("1")
	 else:
		print("删除失败！！！")
		return HttpResponse("0")
def nextPage(request):
     #读取图像文件目录
	 import random
	 carMap = {}#所有
	 carMap_0 = {} #未处理
	 with open(carIndex,'r') as f:
		lines = f.readlines()
	 for line in lines:
		line = line.strip()
		arr = line.split(",")
		#print(arr)
		if(str(arr[1]) != "1"):#未处理
			carMap_0[arr[0]] = arr[1]
		carMap[arr[0]] = arr[1]
	 #print(str(len(carMap)))
	 if(len(carMap_0)!=0):
		name = random.sample(carMap_0, 1)[0]
		ChangePlateState(carMap,name,"2")#修改成2
		restImgCount = len(carMap_0)
		print(name+"   restImgCount:: "+str(restImgCount))
		return HttpResponse(name+":"+str(restImgCount))
	 else:
		return HttpResponse("9")
    

def getRestImgCount(carMap):
	count = 0
	with open(carIndex,'r')as f:
		lines = f.readlines()
	for line in lines:
		line = line.strip()
		arr = line.split(",")
		if(str(arr[1])!= "1"):
			count += 1
	return count
		
		
def getRestImgCountOnLoad(request):
	carMap = {}#所有
	carMap_0 = {} #未处理
	with open(carIndex,'r') as f:
		lines = f.readlines()
	for line in lines:
		line = line.strip()
		arr = line.split(",")
		#print(arr)
		if(str(arr[1]) != "1"):#未处理
			carMap_0[arr[0]] = arr[1]
	global restImgCount
	if(len(carMap_0)!=0):
		restImgCount = len(carMap_0)

	return HttpResponse(restImgCount)









