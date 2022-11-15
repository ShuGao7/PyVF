__author__ = 'Shu Gao'
#Vertical Feature Delineation by Arcpy
import arcpy
from arcpy import env
from arcpy.sa import *
import numpy as np

################################Input##########################
env.workspace=" " #The workspace should be a Geodatabase (output.gdb)
arcpy.CheckOutExtension("spatial")
env.overwriteOutput = True
InTRH="TRH.tif"#This input is a target recognition result (dh) ("dh.tif")
InTRR="TRR.tif"#This input is a target recognition result (R) ("r.tif")
InWSB_P=" "#input watershed boundary ("Watershed_Boundary.shp") Polygone file

WSBuffer=env.workspace+"//"+"WBDBuffer.shp"#"Watershed_Boundary_buffer"
InWSB_L=env.workspace+"//"+"WBD.shp"#Watershed boundary ("Watershed_Boundary.shp") Polyline file
PVFL=env.workspace+"//"+"PVF"#Potential Vertical Feature Line
VFL=env.workspace+"//"+"VF"
TR="TR.tif"

###############################################################

min_dh=   #0.5
min_r=   #3

arcpy.FeatureToLine_management(InWSB_P,InWSB_L)
HsetNull=SetNull(InTRH,in_false_raster_or_constant=InTRH,where_clause="Value < %s"%min_dh) #If the value of dh is smaller than the defined min_dh, the cell will be set as Nodata.
HsetNull.save ("HsetNull.tif")
RsetNull=SetNull(InTRR,in_false_raster_or_constant=1.0,where_clause="Value < %s"%min_r) #If the value of r is smaller than the defined min_r, the cell will be set as Nodata.
RsetNull.save ("RsetNull.tif")
TR=HsetNull*RsetNull
TR.save ("TR")

##############################################################
arcpy.Buffer_analysis(in_features=InWSB_L,out_feature_class=WSBuffer, buffer_distance_or_field="30 meters",line_side="FULL",line_end_type="FLAT",dissolve_option="NONE",method="PLANAR") #watershed boundary buffer
PVFR=ExtractByMask(TR,WSBuffer)#Potential Vertical Feature Raster
PVFR.save("PVFR.tif")
IntPVF=Int(PVFR)#Convert PVFR to int format from float
IntPVF.save("Int_PVFR.tif")
max_thickness= 30  #30
ThVF=Thin(IntPVF,"NODATA","NO_FILTER","SHARP", max_thickness )#Thined Vertical Feature Rasters. It will be change after finishing the new thin method
ThVF.save("THVF")
arcpy.RasterToPolyline_conversion(ThVF, PVFL, "ZERO",simplify="NO_SIMPLIFY" )
