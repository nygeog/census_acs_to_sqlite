# Census ACS Data to SQLite (or CSV)

### The Problem 

Generally speaking, I've always found some aspects of getting and using US Census to be easy while other aspects of it hard. 

I generally use the US Census American Community Survey 5-year data. It has the finest geographic granularity, at the Census Block Group. However, not all variables are available a the the Census Block Group, so I usually default to Census Tract. 

For those of you who remember FactFinder or FactFinder2, it looks like the Census now is using the Data.Census.gov interface, so all that time learning FactFinder, was a bit of a waste. 

##### Census API

The US Census released an API and 

<add Census Python library> and credit as being super useful. 




### The Solution

I want it to be super easy for anyone - with even the most basic Python skills - to be able to get and use all of the US Census data. 

And while `.csv`'s are super easy to use and portable. So are **SQLite** files. 

#### Why SQLite? 

![sql lite banner](https://www.sqlite.org/images/sqlite370_banner.gif)

I've been somewhat over-enthuasiastic about SQLite files lately. There are two reasons for this. SQLite is the file format of the Geopackage - which for those of you GIS folks out there, this should be the file format that overtakes the Shapefile - and I've read and watched videos on [Datasette]() which uses SQLite as well. And Datasette's creator,  ---- , very convincingly explains why its such a great file format. 

> [There are over 1 trillion (1e12) SQLite databases in active use.](https://www.sqlite.org/mostdeployed.html)

First off, it's portable. 

Secondly, you can run SQL queries.  

It's not great for multiple users writing to a database, so you wouldn't want to use it in a high transactional database. However, most of the projects I work on, I just need to create the data one time or one user needs to update daily or weekly or at some cadence. It's usually not the case that more than one individual is inserting data at the same time. This may not work for your purposes but for most of my work and for this project it certainly does. And for creating a US Census database with all the US Census data you could ever want, you only need to generate it when the data is released. 

According to most documentation, for multi-user reading, it seems to be totally fine. <insert a link here>


So why not store all the Geography tables in one database. Well sure we could do that. However, I generally really only need to pick one Geographic granularity at a time. You can hop in and modify the code to write each year and geography level to one single database and there's really no reason I can think of not to do it that way. I just chose to do it this way. 





You can even create SQLite files in ArcGIS's ArcPy using: 

[`arcpy.CreateSQLiteDatabase_management('C:/data.sqlite', 'GEOPACKAGE_1.2')`](https://desktop.arcgis.com/en/arcmap/latest/tools/data-management-toolbox/create-sqlite-database.htm)

