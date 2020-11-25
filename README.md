# PyVF [![DOI](https://zenodo.org/badge/316038076.svg)](https://zenodo.org/badge/latestdoi/316038076)

PyVF is an open-source program to extract significant vertical features (VFs) from a high-resolution, bare-earth LiDAR-DEM automatically.

## Definition
Vertical features are raised linear features such as roadbeds, railroads, levees, floodwalls, and natural features that alter the path of inundation (Bilskie et al., 2015).

## Flowchart
![image](https://github.com/ShuGao7/PyVF/blob/master/flowchart.png)

### Target Recognition
This process traversed each DEM cell and extracted all potential VF raster cells (i.e., high enough) based on terrain analysis for each DEM cell in eight directions by a iterative increasing size moving window method.

### Target Delineation
This process is to covert the potential VF raster cells into polyline combined with hydrologic analysis.


## Reference
Bilskie, M. V., Coggin, D., Hagen, S. C., & Medeiros, S. C. (2015). Terrain-driven unstructured mesh development through semi-automatic vertical feature extraction. Advances in Water Resources, 86, 102-118. doi:https://doi.org/10.1016/j.advwat


