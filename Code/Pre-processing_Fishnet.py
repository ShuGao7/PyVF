__author__ = 'Shu Gao'

import arcpy
from arcpy import env
from arcpy.sa import *
import time
start_time = time.time()

arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True


inWorkspace=''
inRas=".tif"
TilesR  =".shp" #Recognition area (Fishnet)
BufferR= inWorkspace+"\\"+"Fishnet"+"_"+"Buffer"
BufferR_Ext=BufferR+".shp"
TilesE = inWorkspace+"\\"+"Effective_area"#effective area
TilesE_Ext=TilesE+".shp"
Max_r="" #the maximum r in the moving window (300 METER)

#Generate Effective Area
arcpy.Buffer_analysis(TilesR,BufferR ,Max_r , "FULL", "ROUND", "NONE")
arcpy.FeatureEnvelopeToPolygon_management(BufferR_Ext,TilesE,"SINGLEPART")

#Extract DEM for each recognition area and effective area

def PreP_Fishnet(inWorkspace,inTile, name):
    inWorkspace=str(inWorkspace)
    cursor=arcpy.da.SearchCursor(inTile,"SHAPE@")
    count=1
    total_count =str(1)
    for Mask in cursor:
        outRas=str(inWorkspace+"/"+name+"_"+total_count+".tif")
        outExtractByMask=ExtractByMask(inRas,Mask)
        outExtractByMask.save(outRas)
        arcpy.BuildPyramids_management(outRas)
        message="Finish the"+"\b"+total_count+"\b"+"tile"
        print(message)
        count=count+1
        total_count=str(count)

outRas_name_R="DEM_RecgArea" #name of the DEM in recognition area
outRas_name_E="DEM_EffArea" #name of the DEM in Effective area

PreP_Fishnet(inWorkspace,TilesR,outRas_name_R)
print("Finish all recognition tiles")

PreP_Fishnet(inWorkspace,TilesE_Ext,outRas_name_E)
print("Finish all effective tiles")


end_time = time.time()
temp = end_time-start_time
hours = temp//3600
temp = temp - 3600*hours
minutes = temp//60
seconds = temp - 60*minutes
print('%d:%d:%d' %(hours,minutes,seconds))





