__author__ = 'Shu Gao'
# Target Recognition Loop Method
#########################import modeules##########################
import arcpy
from arcpy import env
from arcpy.sa import *
import sys
import numpy as np
import math
import csv
import time


##################################################################

def VF(arr,R1,R2,r1, r2, n1,n2,IDX,I, H1, H2,h1,h2, dM1, dM2,M1,M2,o1,o2,n): #D:direction (i.e., A1, A2, B1, B2, ....);arr:arr[x][y]
	if (n==1):
		if((arr[x][y]>M1 or arr[x][y]>=M2) and (arr[x][y]>=M1 or arr[x][y]>M2)):#The aim is select this pixel is the heighest one of a symmetrical direction
			R1[x][y] = n1
			R2[x][y] = n2
			r1=R1[x][y]
			r2=R2[x][y]
			H1[x][y]=arr[x][y]-M1[0]
			H2[x][y]=arr[x][y]-M2[0]
			h1=H1[x][y]
			h2=H2[x][y]
			n1=n1+1
			n2=n2+1
			IDX=I

			return n1,n2, R1, R2, H1, H2, IDX, r1,r2,h1, h2,o1,o2
		else:
			R1[x][y] = n1
			R2[x][y] = n2
			r1=R1[x][y]
			r2=R2[x][y]
			H1[x][y]=arr[x][y]-M1[n-1]
			H2[x][y]=arr[x][y]-M2[n-1]
			h1=H1[x][y]
			h2=H2[x][y]
			n1=1
			n2=1
			IDX==0
			return n1,n2, R1, R2, H1, H2, IDX, r1,r2,h1, h2,o1,o2

	else:
		if(dM1>0.001 and dM2>0.001):
			R1[x][y] = n1
			R2[x][y] = n2
			r1=R1[x][y]
			r2=R2[x][y]
			H1[x][y]=arr[x][y]-M1[n-1]
			H2[x][y]=arr[x][y]-M2[n-1]
			h1=H1[x][y]
			h2=H2[x][y]
			n1=n1+1
			n2=n2+1
			IDX=I
			return n1,n2, R1, R2, H1, H2, IDX, r1,r2,h1, h2,o1,o2
		else:
			if (o1<5):
				R1, H1,o1, n1,r1,h1=checksides(R1,r1,n1,o1,H1,h1,dM1,M1)

			if (o2<5):
				R2, H2,o2, n2,r2,h2=checksides(R2,r2,n2,o2,H2,h2,dM2,M2)

			return n1, n2,R1, R2, H1, H2, IDX, r1,r2,h1, h2,o1,o2




def checksides(R,r,n,o,H,h,dM,M):#o:offset M:the difference of mean(n) and mean(n-1)
	if (dM>=0.001):
		R[x][y]=n
		r=R[x][y]
		H[x][y]=arr[x][y]-M[n-1]
		h=H[x][y]
		n=n+1
		o=1
		return R, H,o, n,r,h
	else:
		if (dM>=-0.1):
			o=o+1
			if (o<=5):
			   R[x][y]=n
			   r=R[x][y]
			   n=n+1
			   return R, H,o, n,r,h
			else:
				R[x][y]=n
				r=R[x][y]-5
				return R, H,o, n,r,h
		else:

			return R, H,o, n,r,h

def SearchFile(inRasPath, Prep_Path,name, format): #find the raster file and get the absolute path
	for files in os.listdir(inRasPath):
		filename=str(name+str(tag)+".tif")
		if filename in files and files.endswith(format):
			file= Prep_Path+"\\"+files
			return file


#*******Check out any necessary licenses
arcpy.CheckOutExtension("spatial")
start_time = time.time()

#*******Input & Output files

inWorkspace=' '
DEM=" "
Prep_Path='' #The path of DEMs after pre-precessing
OutputCSV=inWorkspace+"//"+"Attribute_Table"+".csv"
Count_Fishnet=1 #The value of the number of splitted tiles in pre-processing step.
tag=1


inRas=arcpy.Raster(DEM)#input raster
lowerLeft = arcpy.Point(inRas.extent.XMin,inRas.extent.YMin) #LL of Original DEM
row=inRas.width
col=inRas.height # The column of the DEM

xmin=inRas.extent.XMin #Minimum X of DEM
ymin=inRas.extent.YMin #Minimum Y of DEM
xmax=inRas.extent.XMax #Maximum X of DEM
ymax=inRas.extent.YMax #Maximum Y of DEM
arcpy.env.extent = arcpy.Extent(xmin,ymin,xmax,ymax)
LL=arcpy.Point(xmin,ymin)

arr = arcpy.RasterToNumPyArray(inRas,nodata_to_value=999)

row = len(arr)
col = len(arr[0])
Max_r=30
row_start=40 #This value should be larger than Max_r
col_start=40
Interval_row=200
Interval_col=200
i=(row-row_start)/Interval_row
j=(col-col_start)/Interval_col
tiles=min(i,j)



for i in range (row_start, row-Interval_row,Interval_row):
	for j in range (col_start, col-Interval_col,Interval_col):
		print i, j


		inRas_Ext=arcpy.Raster(DEM)#input raster
		arr = arcpy.RasterToNumPyArray(inRas,nodata_to_value=999)

		row = len(arr)
		col = len(arr[0])

		outH=str(inWorkspace+"\\"+"TR_h"+str(tag)+".tif")
		outR=str(inWorkspace+"\\"+"TR_r"+str(tag)+".tif")

		CellSize = inRas.meanCellWidth

		arr_r =np.zeros((row,col))
		HA1 =np.zeros((row,col))# h in A1 direction
		HA2 =np.zeros((row,col))# h in A2 direction
		HB1 =np.zeros((row,col))# h in B1 direction
		HB2 =np.zeros((row,col))# h in B2 direction
		HC1 =np.zeros((row,col))# h in C1 direction
		HC2 =np.zeros((row,col))# h in C2 direction
		HD1 =np.zeros((row,col))# h in D1 direction
		HD2 =np.zeros((row,col))# h in D2 direction

		arr_h =np.zeros((row,col))
		#arr_e =np.zeros((row,col))
		RA1=np.zeros((row,col))
		RA2=np.zeros((row,col))
		RB1=np.zeros((row,col))
		RB2=np.zeros((row,col))
		RC1=np.zeros((row,col))
		RC2=np.zeros((row,col))
		RD1=np.zeros((row,col))
		RD2=np.zeros((row,col))
		#################################################
		#Creating CSV files will make a longer time. If the users don't need the attribute table, this can be skipped.
		"""
		f = open(OutputCSV, 'wb') # Open the CSV file
		#f.write("x,y,r_A1,r_A2,H_A1,H_A2,r_B1,r_B2,H_B1,H_B2,r_C1,r_C2,H_C1,H_C2,r_D1,r_D2,H_D1,H_D2,w_A1,w_A2,w_B1,w_B2,w_C1,w_C2,w_D1,w_D2\n") # Set five columns in the CSV file
		f.write("x,y,r_A1,r_A2,H_A1,H_A2,r_B1,r_B2,H_B1,H_B2,r_C1,r_C2,H_C1,H_C2,r_D1,r_D2,H_D1,H_D2\n") # Set five columns in the CSV file
		fwriter=csv.writer(f)
		"""

		for x in range(i,i+Interval_row): # (x,y) is the location for raster cells
			for y in range(j,j+Interval_col):

				#print x
				A1=[]
				B1=[]
				C1=[]

				D1=[]
				A2=[]
				B2=[]
				C2=[]
				D2=[]

				MA1=[] #The mean elevation in A1 rings
				MB1=[]
				MC1=[]
				MD1=[]
				MA2=[]
				MB2=[]
				MC2=[]
				MD2=[]

				dha, dhb, dhc, dhd = 0, 0, 0, 0
				n, n1, n2, n3, n4 = 1, 1, 1, 1, 1
				na1, na2, nb1, nb2, nc1, nc2, nd1, nd2 = 1, 1, 1, 1, 1, 1, 1, 1
				oa1, oa2, ob1, ob2, oc1, oc2, od1, od2 = 1, 1, 1, 1, 1, 1, 1, 1
				ra1, ra2, rb1, rb2, rc1, rc2, rd1, rd2 = -999, -999, -999, -999, -999, -999, -999, -999 #output radius in A1 direction
				ha1, ha2, hb1, hb2, hc1, hc2, hd1, hd2 = -999, -999, -999, -999, -999, -999, -999, -999 #output dh in A1 direction
				ha1_, ha2_, hb1_, hb2_, hc1_, hc2_, hd1_, hd2_ = -999, -999, -999, -999, -999, -999, -999, -999
				ra1_, ra2_, rb1_, rb2_, rc1_, rc2_, rd1_, rd2_ = -999, -999, -999, -999, -999, -999, -999, -999

				dh_=-999
				n_=1
				row=[]
				Max_r=30 #It should be equal to the Max_r in Pre-processing.py dividing cell size.e.g., Max_r in pre-processing is 300m. The cell size of DEM is 10 meter. The Max_r in here is 30.
				while n<30 :
					for xx in range(-n, n+1):
						for yy in range(-n,n+1):
							a = math.atan2(yy,xx)
							xi = x + xx
							yj = y + yy
							Distance= math.sqrt((xx**2)+(yy**2))
							rlimit=n+0.5
							llimit=n-0.5
							if (llimit<Distance<rlimit):
								if(a>=math.pi*-7./8 and a<math.pi*-5./8) :
									B2.append(arr[xi][yj])
								elif(a>=math.pi*-5./8 and a<math.pi*-3./8):
									C2.append(arr[xi][yj])
								elif(a>=math.pi*-3./8 and a<math.pi*-1./8):
									D2.append(arr[xi][yj])
								elif(a>=math.pi*-1./8 and a<math.pi*1./8):
									A1.append(arr[xi][yj])
								elif(a>=math.pi*1./8 and a<math.pi*3./8):
									B1.append(arr[xi][yj])
								elif(a>=math.pi*3./8 and a<math.pi*5./8):
									C1.append(arr[xi][yj])
								elif(a>=math.pi*5./8 and a<math.pi*7./8):
									D1.append(arr[xi][yj])
								else:
									A2.append(arr[xi][yj])

					MA1.append(min(A1)) #the mean of the cells in A1 ring
					MA2.append(min(A2))
					MB1.append(min(B1))
					MB2.append(min(B2))

					MC1.append(min(C1))
					MC2.append(min(C2))
					MD1.append(min(D1))
					MD2.append(min(D2))


					if (n==1):
						dMA1=arr[x][y]-MA1[0]
						dMA2=arr[x][y]-MA2[0]
						dMB1=arr[x][y]-MB1[0]
						dMB2=arr[x][y]-MB2[0]
						dMC1=arr[x][y]-MC1[0]
						dMC2=arr[x][y]-MC2[0]
						dMD1=arr[x][y]-MD1[0]
						dMD2=arr[x][y]-MD2[0]


					else:
						dMA1=MA1[n-2]-MA1[n-1] #The difference of MA1 and arr[xi][yj]  (arr[xi][yi]-MA1)
						dMB1=MB1[n-2]-MB1[n-1]
						dMC1=MC1[n-2]-MC1[n-1]
						dMD1=MD1[n-2]-MD1[n-1]
						dMA2=MA2[n-2]-MA2[n-1]
						dMB2=MB2[n-2]-MB2[n-1]
						dMC2=MC2[n-2]-MC2[n-1]
						dMD2=MD2[n-2]-MD2[n-1]

					ID=0
					ID1=0
					ID2=0
					ID3=0
					ID4=0

					if (n<=n1):
						na1,na2, RA1, RA2, HA1,HA2, ID1, ra1,ra2,ha1,ha2,oa1,oa2=VF(arr,RA1,RA2,ra1,ra2,na1,na2,ID1,1,HA1,HA2,ha1,ha2,dMA1,dMA2,MA1,MA2,oa1,oa2,n)
						if (ha1>=ha1_):
							ha1=ha1
							ha1_=ha1
							ra1=ra1
							ra1_=ra1
						else:
							ha1=ha1_
							ra1=ra1_
						if (ha2>=ha2_):
							ha2=ha2
							ha2_=ha2
							ra2=ra2
							ra2_=ra2
						else:
							ha2=ha2_
							ra2=ra2_

					if (n<=n2):
						nb1,nb2, RB1, RB2, HB1,HB2, ID2, rb1,rb2,hb1,hb2,ob1,ob2=VF(arr,RB1,RB2,rb1,rb2,nb1,nb2,ID2,2,HB1,HB2,hb1,hb2,dMB1,dMB2,MB1,MB2,ob1,ob2,n)
						if (hb1>=hb1_):
							hb1=hb1
							hb1_=hb1
							rb1=rb1
							rb1_=rb1
						else:
							hb1=hb1_
							rb1=rb1_

						if (hb2>=hb2_):
							hb2=hb2
							hb2_=hb2
							rb2=rb2
							rb2_=rb2
						else:
							hb2=hb2_
							rb2=rb2_
					if (n<=n3):
						nc1,nc2, RC1, RC2, HC1,HC2, ID3, rc1,rc2,hc1,hc2,oc1,oc2=VF(arr,RC1,RC2,rc1,rc2,nc1,nc2,ID3,3,HC1,HC2,hc1,hc2,dMC1,dMC2,MC1,MC2,oc1,oc2,n)
						if (hc1>=hc1_):
							hc1=hc1
							hc1_=hc1
							rc1=rc1
							rc1_=rc1
						else:
							hc1=hc1_
							rc1=rc1_
						if (hc2>=hc2_):
							hc2=hc2
							hc2_=hc2
							rc2=rc2
							rc2_=rc2
						else:
							hc2=hc2_
							rc2=rc2_
					if (n<=n4):
						nd1, nd2,RD1, RD2, HD1,HD2, ID4, rd1,rd2,hd1,hd2,od1,od2=VF(arr,RD1,RD2,rd1,rd2,nd1,nd2,ID4,4,HD1,HD2,hd1,hd2,dMD1,dMD2,MD1,MD2,od1,od2,n)
						if (hd1>=hd1_):
							hd1=hd1
							hd1_=hd1
							rd1=rd1
							rd1_=rd1
						else:
							hd1=hd1_
							rd1=rd1_

						if (hd2>=hd2_):
							hd2=hd2
							hd2_=hd2
							rd2=rd2
							rd2_=rd2
						else:
							hd2=hd2_
							rd2=rd2_

					n1=max(na1,na2)
					n2=max(nb1,nb2)
					n3=max(nc1,nc2)
					n4=max(nd1,nd2)
					ID=max(ID1,ID2,ID3,ID4)
					n=max(n1,n2,n3,n4)
					dha=max(ha1,ha2)
					dhb=max(hb1,hb2)
					dhc=max(hc1,hc2)
					dhd=max(hd1,hd2)

					dh=max(ha1,ha2,hb1,hb2,hc1,hc2,hd1,hd2)

					if (dh>dh_):
						dh=dh
						dh_=dh
					else :
						dh=dh_

					if (ID!=0):
						arr_r[x][y]=n
						arr_h[x][y]=dh
					if (ID==0):
						break

				row=[x,y,ra1, ra2, ha1,ha2,rb1,rb2,hb1,hb2,rc1,rc2,hc1,hc2,rd1,rd2,hd1,hd2]
				#fwriter.writerow(row)

		H_h=np.array(arr_h)
		N=np.array(arr_r)

		myRaster_r = arcpy.NumPyArrayToRaster(N,LL,CellSize,CellSize,0)
		myRaster_mh = arcpy.NumPyArrayToRaster(H_h,LL,CellSize,CellSize,0)


		myRaster_mh.save(outH)
		myRaster_r.save(outR)

		tag=tag+1




		end_time = time.time()
		temp = end_time-start_time
		hours = temp//3600
		temp = temp - 3600*hours
		minutes = temp//60
		seconds = temp - 60*minutes
		print('%d:%d:%d' %(hours,minutes,seconds))


