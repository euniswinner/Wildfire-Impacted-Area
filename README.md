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
   
**Reason why I am Documenting on GitHub**
SInce completed course assignments can become inaccessible once the Coursera specialization ends, I wanted to create a permanent record of my learning journey, Documenting my analysis processes and results 
here on GitHub ensures my growth as a GIS analyst is preserved and continuously built upon. 
