README FILE FOR THE U.S. HISTORICAL CLIMATOLOGY NETWORK (U.S. HCN) MONTHLY DATA
Version 2

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

I. CONTENTS OF http://cdiac.ornl.gov/ftp/ushcn_v2_monthly


9641C_YYYYMM_F52.max.gz:     GZIP-compressed file of bias-adjusted mean monthly 
                             maximum temperatures (with estimates for missing
			     values)
9641C_YYYYMM_F52.min.gz:     GZIP-compressed file of bias-adjusted mean monthly 
                             minimum temperatures (with estimates for missing
			     values)
9641C_YYYYMM_F52.avg.gz:     GZIP-compressed file of the average of bias- 
                             adjusted mean monthly maximum and minimum 
			     temperatures (with estimates for missing values)
			     
9641C_YYYYMM_F52.pcp.gz:     GZIP-compressed file of total monthly precipitation 
                             (UNADJUSTED, but with estimates for missing 
			     values)

9641C_err_52d.max.gz:        GZIP-compressed file of the estimated uncertainty  
                             associated with the bias-adjusted mean monthly 
			     maximum temperatures (1 standard error) 
9641C_err_52d.min.gz:        GZIP-compressed file of the estimated uncertainty  
                             associated with the bias-adjusted mean monthly  
			     minimum temperatures (1 standard error) 

9641C_YYYYMM_tob.max.gz:     GZIP-compressed file of mean monthly maximum 
                             temperatures adjusted only for the time of 
			     observation bias
9641C_YYYYMM_tob.min.gz:     GZIP-compressed file of mean monthly minimum 
                             temperatures adjusted only for the time of 
			     observation bias
9641C_YYYYMM_tob.avg.gz:     GZIP-compressed file of the average of mean 
                             monthly maximum and minimum temperatures adjusted
			     only for the time of observation bias

9641C_YYYYMM_raw.max.gz:     GZIP-compressed file of unadjusted mean monthly 
                             maximum temperatures 
9641C_YYYYMM_raw.min.gz:     GZIP-compressed file of unadjusted mean monthly 
                             minimum temperatures
9641C_YYYYMM_raw.avg.gz:     GZIP-compressed file of the average of un- 
                             adjusted mean monthly maximum and minimum 
			     temperatures 

ushcn-stations.txt:          List of U.S. HCN stations and their coordinates

readme.txt:                  This file

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

II. FORMAT OF THE DATA FILES 

Each data file contains data for all HCN stations for one of the four 
meteorological variables (also known as data "elements"). 

Each record (line) in the files contains one year of 12 monthly values plus an 
annual value (note that the uncertainty estimates have no annual value).  
The values on each line include the following:

------------------------------
Variable   Columns   Type
------------------------------
STATION ID     1-6   Character
ELEMENT        7-7   Integer
YEAR          8-11   Integer
VALUE1       13-17   Integer
FLAG1        18-18   Character
VALUE2       20-24   Integer
FLAG2        25-25   Character
  .           .          .
  .           .          .
  .           .          .
VALUE13     97-101   Integer
FLAG13     102-102   Character
------------------------------

These variables have the following definitions:

ID         is the station identification code.  Please see "ushcn-stations.txt"
           for a complete list of stations and their metadata.
	   
ELEMENT    is the element code.  There are four values corresponding to the 
           element contained in the file:

           1 = mean maximum temperature (in tenths of degrees F)
           2 = mean minimum temperature (in tenths of degrees F)
	   3 = average temperature (in tenths of degrees F)
           4 = total precipitation (in hundredths of inches)

YEAR       is the year of the record.

VALUE1     is the value for January in the year of record (missing = -9999).

FLAG1      is the flag for January in the year of record.  There are
           five possible values:

           Blank = no flag is applicable;
	   
           E     = value is an estimate from surrounding values; no original 
	           value is available;
           I     = monthly value calculated from incomplete daily data (1 to 9 
	           days were missing);
           Q     = value is an estimate from surrounding values; the original 
	           value was flagged by the monthly quality control algorithms;
	   X     = value is an estimate from surrounding values; the original 
	           was part of block of monthly values that was too short to 
		   adjust in the temperature homogenization algorithm.

VALUE2     is the value for February in the year of record.

FLAG2      is the flag for February in the year of record.
  .
  .
  .
VALUE12    is the value for December in the year of record.

FLAG12	   is the flag for December in the year of record.

VALUE13    is the annual value (mean for temperature; total for precipitation)

FLAG13     is the flag for the annual value.
 
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

III. FORMAT OF "ushcn-stations.txt"

------------------------------
Variable   Columns   Type
------------------------------
COOP ID       1-6    Character
LATITUDE     8-15    Real
LONGITUDE   17-25    Real
ELEVATION   27-32    Real
STATE       34-35    Character
NAME        37-66    Character
COMPONENT 1 68-73    Character
COMPONENT 2 75-80    Character
COMPONENT 3 82-87    Character
UTC OFFSET  89-90    Integer
------------------------------

These variables have the following definitions:

COOP ID     is the U.S. Cooperative Observer Network station identification 
            code.  Note that the first two digits in the Coop Id correspond
            to the state. 

LATITUDE    is latitude of the station (in decimal degrees).

LONGITUDE   is the longitude of the station (in decimal degrees).

ELEVATION   is the elevation of the station (in meters, missing = -999.9).

STATE       is the U.S. postal code for the state.

NAME        is the name of the station location.

COMPONENT 1 is the Coop Id for the first station (in chronologic order) whose 
            records were joined with those of the HCN site to form a longer time
	    series.  "------" indicates "not applicable".
            
COMPONENT 2 is the Coop Id for the second station (if applicable) whose records 
            were joined with those of the HCN site to form a longer time series.
	    
COMPONENT 3 is the Coop Id for the third station (if applicable) whose records 
            were joined with those of the HCN site to form a longer time series.

UTC OFFSET  is the time difference between Coordinated Universal Time (UTC) and 
            local standard time at the station (i.e., the number of hours that 
	    must be added to local standard time to match UTC).  

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
