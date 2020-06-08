import psycopg2
import geopandas as gpd
from geopy.geocoders import Nominatim
address = "48 Tạ Quang Bửu Hai Bà Trưng Hà Nội"
geolocator = Nominatim()
location = geolocator.geocode(address)
lat = location.latitude
long = location.longitude
conn = psycopg2.connect(database = "bkx", user = "postgres", password = "kiena198", host = "localhost", port = "5432")
sql = "SELECT (route.geom) FROM (SELECT geom FROM pgr_fromAtoB('roads',"+str(long)+","+str(lat)+",105.84915, 21.00682) ORDER BY seq) AS route;"
df = gpd.GeoDataFrame.from_postgis(sql, conn, geom_col='geom' )
print(df['geom'])
df.to_file(r"/home/kien/Documents/httt địa lý/shp/route3.shp")
