# Load the Python Standard and DesignScript Libraries
import numpy as np
from tqdm import tqdm
filename= 'DEBENHAMS-ROAD-POINTS-LOCAL-M-v2.txt'
gridSize = 1
rangeFix = 0.05
data=[]
data=np.loadtxt(filename, delimiter=',')
maxvalues=np.max(data, axis=0)
minvalues=np.min(data, axis=0)
range1=minvalues.copy()
range2=range1+[gridSize, gridSize, 0]

done=False


pbar = tqdm(total=maxvalues[1]-minvalues[1])
fullgrid=[]
while not done:
	grid=[]
	grid=list(data[np.all(data[:,:2]>=range1[:2], axis=1) & np.all(data[:,:2]<range2[:2], axis=1)])
	if grid:
		fullgrid.append(grid)

	range1[0]=range2[0]
	range2[0]+=gridSize
	if range1[0]>maxvalues[0]:
		range1[0]=minvalues[0]
		range1[1]=range2[1]
		range2=range1+[gridSize, gridSize, 0]
		pbar.update(gridSize)
	if range1[1]>maxvalues[1]:
		done=True
	

OORValue=[] #Out of range value
def medianValue(a):
	n = len(a)
	index = n // 2
	if n % 2:
		return(sorted(a)[index])
	else:
		return(sum(sorted(a)[index - 1 :index + 1]) / 2)
def average(a):
	return(sum(a)/len(a))
#FeetToMm=304.8
#Trial
goodPoints = []
count=0
for count, x in enumerate(fullgrid):
	zValues =[]
	for z in x:
		zValues.append(z[2])
	highRange = medianValue(zValues) + rangeFix
	lowRange = medianValue(zValues) - rangeFix
	c=0
	for c, y in enumerate(zValues):
		if (highRange < y) or (lowRange > y):
			OORValue.append(fullgrid[count][c])
		else:
			goodPoints.append(fullgrid[count][c])
xPoint = []
yPoint = []
zPoint = []

result=np.asarray(goodPoints)

np.savetxt('output.txt', result, fmt='%.3f,%.3f,%.3f')



