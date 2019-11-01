#!/usr/bin/env python
# coding: utf-8

# ## Exploratory Data Visualization

# In[3]:


import sqlite3
import pandas.io.sql as sql
import pandas as pd
import seaborn as sns
import geopandas as gdp
from shapely.geometry import Point,Polygon
import csv
import matplotlib.pyplot as plt
import gmaps


# ### Using SQL Querying & Data Storage

# In[8]:


#A script to create and import a .csv into sqlite3
'''con = sqlite3.connect("bikeshare.db")
cur = con.cursor()
cur.execute("CREATE TABLE bike_share (id INTEGER PRIMARY KEY,duration_sec int64(50),"
            "start_time datetime,end_time datetime,start_station_id int64,start_station_name varchar(255),start_station_latitude float(1,10),start_station_longitude float(1,10),end_station_id int64(50),end_station_name varchar(255),end_station_latitude float(1,10),end_station_longitude float(1,10),bike_id int64,user_type varchar(255),member_birth_year int,member_gender varchar(255),bike_share_for_all_trip varchar(255) );")

with open('201908-baywheels-tripdata.csv','r', encoding='utf-8') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['duration_sec'],i['start_time'],i['end_time'],i['start_station_id'],i['start_station_name'],i['start_station_latitude'],i['start_station_longitude'],i['end_station_id'],i['end_station_name'],i['end_station_latitude'],i['end_station_longitude'],i['bike_id'],i['user_type'],i['member_birth_year'],i['member_gender'],i['bike_share_for_all_trip']) for i in dr]

cur.executemany("INSERT INTO bike_share (duration_sec,start_time,end_time,start_station_id,start_station_name,start_station_latitude,start_station_longitude,end_station_id,end_station_name,end_station_latitude,end_station_longitude,bike_id,user_type,member_birth_year,member_gender,bike_share_for_all_trip) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db)
con.commit()'''


# <p>Let&rsquo;s check all of our data run a query and see if we have any duplicated user ID&rsquo;s</p>

# In[9]:


#Query all of our data
con = sqlite3.connect("bikeshare.db")
df = sql.read_sql('SELECT * from bike_share', con)
df


# In[5]:


#Check distinct ID
con = sqlite3.connect("bikeshare.db")
dupes = sql.read_sql('SELECT DISTINCT id from bike_share ', con)
dupes


# After doing a check we know there are no duplicated records both queries match (210563) rows

# In[11]:


#Checking our data types
df.dtypes


# In[12]:


#Check the shape of the data
df.shape


# In[13]:


#Fix the timestamp issue when converting to pandas.
df.start_time = pd.to_datetime(df.start_time)
df.end_time = pd.to_datetime(df.end_time)
df.dtypes


# <p>Run a query where birth_year is not null I want to explore the data based on gender.</p>

# In[14]:


#Query the data where birth_year not null
birth = sql.read_sql('SELECT * from bike_share where member_birth_year != "" ', con)
birth


# <p><strong>Question:</strong></p>
# <p>What genders are using the bike share program most?</p>

# In[15]:


#Query our data and store it into a pandas dataframe
gender = sql.read_sql('SELECT member_gender, COUNT(member_gender) as count FROM bike_share WHERE member_gender !="" GROUP BY member_gender ORDER BY COUNT(member_gender) DESC', con)
gender


# In[16]:


#create our bar chart and save it as a function
def sex():
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.set(style="whitegrid")
    
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(10, 5))
    
    # Plot the total crashes
    sns.set_color_codes("pastel")
    sns.barplot(x="member_gender", y="count", data=gender,label="Total", color="#79B8D5")
    
    plt.xlabel('')
    plt.ylabel('Frequency',rotation=0,fontsize=14,labelpad=60)
    plt.title("Bike Share Users Based On Sex",fontsize=17,pad=20);
    plt.xticks(rotation=-25,fontsize=14,ha='left');
    return plt.show()

sex()


# <p><strong>Observation:</strong></p>
# <p>Our population of users is predominantly male by a wide margin.</p>

# <p><strong>Question:</strong></p>
# <p>How many subscribed users do we have vs customers?</p>

# In[17]:


#Query our data and store it into a pandas dataframe
user = sql.read_sql('SELECT user_type, COUNT(user_type) as count FROM bike_share WHERE user_type !="" GROUP BY user_type ORDER BY COUNT(user_type) DESC', con)
user


# In[18]:


#create our bar chart and save it as a function.
def users():
    
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.set(style="whitegrid")
    
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(10, 5))
    
    # Plot the total crashes
    sns.set_color_codes("pastel")
    sns.barplot(x="user_type", y="count", data=user,label="Total", color="#1C84DB")
    
    plt.xlabel('')
    plt.ylabel('Frequency',rotation=0,fontsize=14,labelpad=60)
    plt.title("Bike Share Subcribers vs Non Subscribers",fontsize=17,pad=20)
    plt.xticks(rotation=-25,fontsize=14,ha='left');
    return plt.show()

users()


# <p><strong>Observation:</strong></p>
# <p>A large majority of our population has subscribed to the bike share program.</p>

# <p><strong>Question:</strong></p>
# <p>What are the top 20 bikes are being used the most?</p>

# In[19]:


#Query our data and store it into a pandas dataframe
pop_bike = sql.read_sql('SELECT bike_id, COUNT(bike_id) as count FROM bike_share WHERE bike_id !="" GROUP BY bike_id ORDER BY COUNT(bike_id) DESC', con)
pop_bike20 = pop_bike.head(20)
pop_bike20


# In[20]:


#create our bar chart
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")

# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(15, 10))

# Plot the total crashes
sns.set_color_codes("pastel")
sns.barplot(x="bike_id", y="count", data=pop_bike20,label="Total", color="#A4DF8C")

plt.xlabel('Bike ID',fontsize=16,labelpad=30)
plt.ylabel('Frequency',rotation=55,fontsize=16,labelpad=30)
plt.title('Most Frequently Used Bikes',fontsize=15,pad=20)
plt.margins(0.03)
#plt.savefig('name_here')


# <p><strong>Observation:</strong></p>
# <p>The top 20 bikes are being used relatively even with a few outliers.</p>

# <p><strong>What other visuals are we able to extract from our data?</strong></p>

# In[21]:


#Call our dataframe
df.head()


# Let’s make some histograms and scatter plots for areas of interest.

# In[22]:


#Age group using the bike share program
birth.hist(column='member_birth_year');


# In[23]:


#Age group using the bike share program
birth.plot(kind='scatter', x='member_birth_year', y='duration_sec');


# <p>Observation:</p>
# <li>According to the histogram and scatter plot we can state that the younger generation is using the program more frequently.</li>
# <li>Looks like some of the data is inaccurate. It is highly unlikely that people born in 1880 are using the program.</li>

# <p><strong>Question:</strong></p>
# <p>What bikes are being used this most?</p>

# In[24]:


#Which bikes are being used the most?
df.hist(column='bike_id');


# <p><strong>Observation:</strong></p>
# <p>This gives us a rough idea however further investigation is needed.</p>

# <p><strong>Question:</strong></p>
# <p>What is the relationship between bike_id and duration_sec?</p>

# In[25]:


#How long are bikes being used?
df.plot(kind='scatter', x='bike_id', y='duration_sec');


# <p><strong>Observation:</strong></p>
# <p>This gives us a rough idea however further investigation is needed.</p>

# <p><strong>Question:</strong></p>
# <p>Which start stations are being used the most?</p>

# In[26]:


#What beginning stations are popular?
df.hist(column='start_station_id');


# <p><strong>Observation:</strong></p>
# <ul>
# <li>The data is skewed left meaning the lower start station ID's are being used more frequently.</li>
# <li>This gives us a rough idea however further investigation is needed.</li>
# </ul>

# <p><strong>Question:</strong></p>
# <p>What is the relationship between our start stations and birth year?</p>

# In[27]:


#Start station vs member birth year
birth.plot(kind='scatter', x='start_station_id', y='member_birth_year');


# <p><strong>Observation:</strong></p>
# <p>More investigation is needed.</p>

# <p><strong>Question:</strong></p>
# <p>Which end stations are being used the most?</p>

# In[28]:


#End station hist
df.hist(column='end_station_id');


# <p><strong>Observation:</strong></p>
# <ul>
# <li>The data is skewed left meaning the lower start station ID's are being used more frequently.</li>
# <li>This gives us a rough idea however further investigation is needed.</li>
# </ul>

# <p><strong>Question:</strong></p>
# <li>What are the most popular start stations top 5?</li>
# <li>What are the least popular start stations top 5?</li>

# In[6]:


#Query our data and store it into a pandas dataframe
station = sql.read_sql('SELECT start_station_name, COUNT(start_station_name) as count FROM bike_share WHERE start_station_name !="" GROUP BY start_station_name ORDER BY COUNT(start_station_name) DESC', con)
pop_station = station.head(5)
unpop_station = station.tail(5)


# In[7]:


#popular stations
bar_pop_station = pop_station
bar_pop_station


# In[8]:


#unpopular stations
bar_unpop_station = unpop_station
bar_unpop_station


# In[17]:


def bar_pop_start_station():
    
    #create our bar chart for our most popular start stations.
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(13, 7))

    # Plot the total crashes
    sns.set_color_codes("pastel")
    sns.barplot(x="count", y="start_station_name", data=bar_pop_station, label="Total", color="#5F9C46")

    plt.xlabel('Frequency',fontsize=16,labelpad=30)
    plt.ylabel('Station',rotation=0,fontsize=16,labelpad=60)
    plt.title("Most Popular Starting Stations",fontsize=15,pad=20)
    plt.xticks(fontsize=11.5,ha='left');
    return plt.show()

bar_pop_start_station()


# In[14]:


def bar_least_pop():
    
    #create our bar chart
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(13, 7))
    
    # Plot the total crashes
    sns.set_color_codes("pastel")
    sns.barplot(x="count", y="start_station_name", data=bar_unpop_station, label="Total", color="#F54E3A")
    
    plt.xlabel('Frequency',fontsize=16,labelpad=30)
    plt.ylabel('Station',rotation=0,fontsize=16,labelpad=60)
    plt.title("Least Popular Starting Stations",fontsize=15,pad=20)
    plt.xticks(fontsize=13,ha='left')
    return plt.show();
bar_least_pop()


# <p><strong>Observation:</strong></p>
# <ul>
# <li>We notice there is a huge difference in usage between are most popular and least popular stations.</li>
# </ul>

# In[34]:


#View our data.
df.head()


# In[35]:


#make a box plot I am not really interested in this data
df.boxplot(by ='bike_share_for_all_trip', column =['bike_id'], grid = False) ;


# In[36]:


#Let's Check what other variables we can work with.
df.describe()


# In[96]:


#creating a matrix to give us some ideas of what we could potentially plot.
pd.plotting.scatter_matrix(df, figsize=(16,16));
#df.iloc[:, 0:2]


# In[37]:


#pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(16, 16), diagonal='kde');
#plt.show()


# ### <p>Observations within the scatter matrix:</p>
# <ol>
# <li>Member birth year is skewed right suggesting users are millennials and the younger generation are majority users of the program.</li>
# </ol>
# <ul>
# <li>Which age group is most prominent?</li>
# <li>What start stations are they using?</li>
# <li>What end stations are they using?</li>
# <li>Who uses the bike sharing more men vs women?</li>
# </ul>
# <p>I am more interested in the geographical data so I will continue to explore that.</p>

# ### Let’s take a look at where our bike share locations are on a map.

# In[38]:


#Query of our data
con = sqlite3.connect("bikeshare.db")
locations_df = sql.read_sql('SELECT DISTINCT start_station_id, start_station_longitude, start_station_latitude from bike_share', con)
locations_df


# <p>There is a way to use shape files for geographic plots. I sourced a few from open data resources.</p>

# In[39]:


#Read in our shape file
bay_area = gdp.read_file('shape/s7jc7v.shp')


# In[40]:


#Plot the shape file
fig,ax = plt.subplots(figsize = (15,15))
bay_area.plot(ax = ax);


# In[41]:


#read in some training data run a loop to Populate another column for our geometry library. 
crs = {'init': 'epsg:4326'}
geometry = [Point(xy) for xy in zip(locations_df["start_station_longitude"], locations_df["start_station_latitude"])]

locations_df = gdp.GeoDataFrame(locations_df,#Specify our data
                                crs = crs,#specify our coordinate reference system
                                geometry = geometry)#Specify the geometry list we created

locations_df


# In[42]:


#Plot our data
fig,ax = plt.subplots(figsize = (15,15))
bay_area.plot(ax = ax, alpha = 0.4)

locations_df.plot(ax = ax, markersize = 20, color = "green", marker = "o", label = "",alpha=0.99);
#plt.legend(prop={'size': 15})


# <p><strong>Observations:</strong></p>
# <p>There seems to be a problem with false geo data from some of our users.</p>
# <ul>
# <li>We'll filter out coordinates that are above -120</li>
# </ul>

# In[43]:


#Query our data and filter out undesired data
con = sqlite3.connect("bikeshare.db")
locations_df = sql.read_sql('SELECT DISTINCT start_station_id, start_station_longitude, start_station_latitude from bike_share where start_station_longitude <= -120 ', con)
locations_df


# In[44]:


#read in some training data run a loop to Populate another column for our geometry library. 
crs = {'init': 'epsg:4326'}
geometry = [Point(xy) for xy in zip(locations_df["start_station_longitude"], locations_df["start_station_latitude"])]

locations_df = gdp.GeoDataFrame(locations_df,#Specify our data
                                #crs = crs,#specify our coordinate reference system
                                geometry = geometry)#Specify the geometry list we created

locations_df


# In[45]:


def bay_area_map():
    
    fig,ax = plt.subplots(figsize = (10,10))
    bay_area.plot(ax = ax, alpha = 0.4)
    
    locations_df.plot(ax = ax, markersize = 20, color = "green", marker = "o", label = "Bike Share Locations",alpha=0.99)
    
    plt.xlabel('Longitude',rotation=0,fontsize=14,labelpad=20)
    plt.ylabel('Latitude',rotation=0,fontsize=14,labelpad=60)
    plt.title('Bay Area California Geographical',fontsize=15,pad=20)
    return plt.show()

bay_area_map()


# ### It looks as though we have a few participating cities.
# <p><strong>Observations:</strong></p>
# <ul>
# <li>Let&rsquo;s zoom in a check where our stations are within their borders.</li>
# <li>We'll start with San Francisco.</li>
# </ul>
# <p>&nbsp;</p>

# In[46]:


#Query our data for coordinates that fall within San Francisco's range
con = sqlite3.connect("bikeshare.db")
sanfran_df = sql.read_sql('SELECT DISTINCT start_station_id, start_station_longitude, start_station_latitude from bike_share where start_station_longitude between -122.52 and -122.35 and start_station_longitude like "-122%"', con)
sanfran_df


# In[47]:


#Import our shape file
sanfran_map = gdp.read_file('shape/sanfran_city/geo_export_b896081a-685e-4878-a962-38b650695c1a.shp')


# In[48]:


#Plot our shape file
fig,ax = plt.subplots(figsize = (15,15))
sanfran_map.plot(ax = ax);


# In[49]:


#read in some training data run a loop to Populate another column for our geometry library. 
crs = {'init': 'epsg:4326'}
geometry = [Point(xy) for xy in zip(sanfran_df["start_station_longitude"], sanfran_df["start_station_latitude"])]

sanfran_df = gdp.GeoDataFrame(sanfran_df,#Specify our data
                                #crs = crs,#specify our coordinate reference system
                                geometry = geometry)#Specify the geometry list we created

sanfran_df


# In[50]:


def sanfran_shape():
    
    #Plot our data
    fig,ax = plt.subplots(figsize = (10,10))
    sanfran_map.plot(ax = ax, alpha = 0.4)
    sanfran_df.plot(ax = ax, markersize = 20, color = "green", marker = "o", label = "Start Station Mil",alpha=0.99)
    
    plt.xlabel('Longitude',rotation=0,fontsize=14,labelpad=20)
    plt.ylabel('Latitude',rotation=0,fontsize=14,labelpad=60)
    plt.title('San Francisco',fontsize=15,pad=20)
    return plt.show()

sanfran_shape()
    


# <p><strong>Observation:</strong></p>
# <ul>
# <li>It looks as though most stations are to the east of center.</li>
# <li>Stations are highly concentrated.</li>
# </ul>

# <p><strong>Question:</strong></p>
# <ul>
# <li>What does Oakland look like when you plot the stations?</li>
# </ul>

# In[51]:


#Query our data coordinates within Oakland boundaries.
con = sqlite3.connect("bikeshare.db")
oakland_df = sql.read_sql('SELECT DISTINCT start_station_id, start_station_longitude, start_station_latitude from bike_share where start_station_longitude between -122.35 and -122.10 and start_station_longitude like "-122%"', con)
oakland_df


# In[52]:


#Import our shape file
streetmap = gdp.read_file('shape/oakland/geo_export_a8aad267-4123-4b77-b2b3-58eea2d8c754.shp')


# In[53]:


#Plot our shape file
fig,ax = plt.subplots(figsize = (15,15))
streetmap.plot(ax = ax);


# In[54]:


#read in some training data run a loop to Populate another column for our geometry library. 
crs = {'init': 'epsg:4326'}
geometry = [Point(xy) for xy in zip(oakland_df["start_station_longitude"], oakland_df["start_station_latitude"])]

oakland_df = gdp.GeoDataFrame(oakland_df,#Specify our data
                                #crs = crs,#specify our coordinate reference system
                                geometry = geometry)#Specify the geometry list we created

oakland_df


# In[55]:


#Plot our data
fig,ax = plt.subplots(figsize = (15,15))
streetmap.plot(ax = ax, alpha = 0.4)

oakland_df.plot(ax = ax, markersize = 20, color = "green", marker = "o", label = "Start Station Mil",alpha=0.99);


# <p><strong>Observations:</strong></p>
# <p>We&rsquo;ve run into a bit of a problem.</p>
# <ul>
# <li>There are a few cities surrounding Oakland with Start Stations.</li>
# <li>Finding it difficult to locate a shape files for that specific region.</li>
# <li>Is there another way?</li>
# </ul>

# ### Fortunately there is a library that connects with the Google Maps API.

# In[56]:


#Query our data for Oakland and surrounding area
con = sqlite3.connect("bikeshare.db")
oakland_df = sql.read_sql('SELECT distinct start_station_id, start_station_latitude, start_station_longitude from bike_share where start_station_longitude between -122.35 and -122.15 ', con)
oakland_df


# In[57]:


#Slice the geo data
oakland_df_geo = oakland_df[['start_station_latitude','start_station_longitude']]
oakland_df_geo


# In[58]:


#use gmaps with my api key to create a map.
gmaps.configure(api_key='secret')

#plot our data
locations = oakland_df_geo
fig = gmaps.figure(map_type='ROADMAP')
scatter_locations = gmaps.symbol_layer(locations,fill_color = "#2A65B1",stroke_color="#2A65B1",scale=2)
fig.add_layer(scatter_locations)
fig


# <p><strong>Observations:</strong></p>
# <ul>
# <li>Using gmaps is much more efficient for this application.</li>
# <li>We notice there are quite a few cities in the bay area that have excluded themselves from the program.</li>
# </ul>

# <p><strong>Question:</strong></p>
# <ul>
# <li>Where are the most popular start stations? (Top 10)</li>
# <li>Where are the least popular start stations? (Top 10)</li>
# </ul>

# In[59]:


#Query our data to find the most popular and least popular start stations.
station = sql.read_sql('SELECT start_station_latitude, start_station_longitude, start_station_name,  COUNT(start_station_name) as count FROM bike_share WHERE start_station_name !="" GROUP BY start_station_name ORDER BY COUNT(start_station_name) DESC', con)
pop_station = station.head(10)
unpop_station = station.tail(10)


# In[60]:


#top 10 popular stations
pop_station


# In[61]:


#Slice the data
pop_station_geo = pop_station[['start_station_latitude','start_station_longitude']]
pop_station_geo


# In[62]:


#use gmaps with my api key to create a map.
gmaps.configure(api_key='secret')

locations = pop_station_geo
fig = gmaps.figure(map_type='ROADMAP')
scatter_locations = gmaps.symbol_layer(locations,fill_color = "#2A65B1",stroke_color="#2A65B1",scale=2)
fig.add_layer(scatter_locations)
fig


# <p><strong>Observations:</strong></p>
# <ul>
# <li>Our top 10 most used stations are all in San Francisco.</li>
# <li>A large majority are on Market St.</li>
# </ul>

# <p><strong>Question:</strong></p>
# <ul>
# <li>What start station is used the most according to our data?</li>
# </ul>

# In[63]:


#Slice our number one start station.
most_pop = pop_station_geo[0:1]
most_pop


# In[64]:


#use gmaps with my api key to create a map.
gmaps.configure(api_key='secret')

locations = most_pop
fig = gmaps.figure(map_type='SATELLITE')
scatter_locations = gmaps.symbol_layer(locations,fill_color = "#FBFF02",stroke_color="#FBFF02",scale=5)
fig.add_layer(scatter_locations)
fig


# <p><strong>Observations:</strong></p>
# <ul>
# <li>Our most frequented start station is on Townsend St</li>
# <li>This makes a lot of sense, there is a very busy train station right beside the bike station.</li>
# </ul>

# <p><strong>Question:</strong></p>
# <ul>
# <li>Where are our least popular start location?</li>
# <li>What is the least popular start station?</li>
# </ul>

# In[65]:


unpop_station_geo = unpop_station[['start_station_latitude','start_station_longitude']]
unpop_station_geo


# In[66]:


#use gmaps with my api key to create a map.
gmaps.configure(api_key='secret')

locations = unpop_station_geo
fig = gmaps.figure(map_type='ROADMAP')
scatter_locations = gmaps.symbol_layer(locations,fill_color = "#2A65B1",stroke_color="#2A65B1",scale=2)
fig.add_layer(scatter_locations)
fig


# In[67]:


#Slice our least popular start station
least_pop = unpop_station_geo[9:10]
least_pop


# In[68]:


#use gmaps with my api key to create a map.
gmaps.configure(api_key='secret')

locations = least_pop
fig = gmaps.figure(map_type='ROADMAP')
scatter_locations = gmaps.symbol_layer(locations,fill_color = "#FBFF02",stroke_color="#FBFF02",scale=5)
fig.add_layer(scatter_locations)
fig


# ###### <p><strong>Observations:</strong></p>
# <ul>
# <li>Of the top 10 least used start stations San Jose has the most.</li>
# <li>The station used the least is located on 16th St San Francisco </li>
# <li>There is a station in Canada.</li>
# </ul>

# ## That’s odd why is there a station in Canada?

# In[69]:


#Slice our station located in canada
mont = unpop_station_geo[8:9]
mont


# In[70]:


#use gmaps with my api key to create a map.
gmaps.configure(api_key='secret')

locations = mont
fig = gmaps.figure(map_type='ROADMAP')
scatter_locations = gmaps.symbol_layer(locations,fill_color = "#FBFF02",stroke_color="#FBFF02",scale=5)
fig.add_layer(scatter_locations)
fig


# <p><strong>Observations:</strong></p>
# <ul>
# <li>There is a station in Montreal Canada.</li>
# <li>The station in Montreal Canada is the least popular station.</li>
# <li>You never know what you&rsquo;ll find in the data.</li>
# </ul>

# <p>Resources</p>
# <ul>
# <li><a href="https://towardsdatascience.com/geopandas-101-plot-any-data-with-a-latitude-and-longitude-on-a-map-98e01944b972">Using shape files for plotting.</a></li>
# <li><a href="https://www.geeksforgeeks.org/python-plotting-google-map-using-gmplot-package/">GMPLOT</a></li>
# <li><a href="https://pypi.org/project/gmaps/">GMAPS</a></li>
# <li><a href="https://wesmckinney.com/pages/book.html">Python for data analysis</a></li>
# </ul>
