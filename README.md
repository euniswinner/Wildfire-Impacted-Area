**Why this project is important**

Many geography graduates go on to work in public agencies and the 
insurance industry, where spatial risk assessment directly shapes 
real-world decisions. For example, major insurers such as State Farm 
and Allstate have pulled out of high wildfire risk ZIP codes in 
California, and risk mapping is central to how these decisions get made. 
I wanted to understand this process hands-on, so I built a wildfire 
risk map of California as part of my GIS coursework.

### Data
- **CAL FIRE Fire Perimeters Dataset** — historical wildfire boundaries 
  and burn zones across California
- **U.S. Census Bureau TIGER/Line Shapefiles** — county boundaries for 
  cross-regional comparison

### Method
1. **Dissolve:** Merged overlapping and fragmented wildfire perimeter 
   polygons using the `Dissolve` tool. This removed data redundancy 
   and significantly improved spatial processing speed.
2. **Spatial Join:** Calculated the cumulative burned area 
   (`SUM_Area_Acres`) within each county boundary by spatially joining 
   the dissolved fire perimeters to county polygons.
3. **Classification & Symbology:** Classified counties by total burned 
   acreage using a graduated color scheme (yellow → dark red). Darker 
   red indicates a higher concentration of historical fire activity — 
   this is the same logic institutions use to flag high-risk zones for 
   premium mapping and resource allocation.

**Tool:** ArcGIS Pro 3.7

### Reading the Map
Color intensity represents cumulative wildfire risk by county — the 
darker/redder the shading, the greater the historical burned area. 
Yellow and orange indicate lower-to-moderate risk; dark red marks the 
highest-risk counties.

### Challenges & Debugging
During the Spatial Join step, I initially got Null values in the 
`SUM_Area_Acres` field for every county. After troubleshooting, I 
found the issue was a coordinate system mismatch between the CAL FIRE 
and TIGER/Line datasets. Reprojecting both layers to a consistent 
coordinate system (and recalculating the area field via 
`Calculate Geometry` after the Dissolve step) resolved the issue and 
produced accurate cumulative acreage values per county.

### Findings
The classified map reveals a clear spatial pattern: counties with 
mountainous, heavily vegetated terrain show the highest cumulative 
wildfire risk (dark red), while low-elevation, agricultural areas 
like the Central Valley remain consistently low-risk (yellow). This 
aligns with what geographers would expect — forested mountain regions 
have more fuel load (dense vegetation), steeper terrain that makes 
firefighting access difficult, and drier conditions at higher 
elevations, all of which combine to increase fire risk. In contrast, 
flatter agricultural land has less continuous vegetation to sustain 
large fires and is far more accessible to suppression crews. This 
pattern reinforced for me that wildfire risk isn't random — it's 
directly tied to underlying physical geography, which is exactly the 
kind of relationship spatial analysis is built to reveal.

### Reflection
This project gave me a concrete sense of how spatial analysis 
translates into institutional decision-making — not just visualizing 
where fires occurred, but quantifying *how much* risk each region 
carries and why. A natural next step would be incorporating vegetation 
density and population data to build a more complete risk model, or 
comparing this against actual insurance non-renewal data to see how 
closely institutional decisions track the underlying geography.

### Why I'm Documenting This on GitHub
Coursera course assignments become inaccessible once a specialization 
ends, so I'm archiving my process and results here to preserve and 
build on this work over time.
