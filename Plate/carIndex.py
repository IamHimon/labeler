import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ImgNameDIR = BASE_DIR+"/car/static/hm_img/002/"

carList = os.listdir(ImgNameDIR)

with open("carIndex.txt","w") as f:
	for i in xrange(len(carList)):
		f.write(carList[i].strip()+','+'0'+'\n')
		
