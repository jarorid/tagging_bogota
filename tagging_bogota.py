# load librarys
import geopandas as gpd
import matplotlib.pyplot as plt
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

# Let’s first enable shapely.speedups which makes some of the spatial queries running faster.
import shapely.speedups
shapely.speedups.enable()

def main():

	print('Started program taggin bogota')

	# load files
	# File with geopints with commerces points 
	data = gpd.read_file("data/establecimientos-comerciales-2016.kml", driver='KML')
	data.head()
	# Filepath to KML file with location polygon (localidades)
	polys = gpd.read_file("data/poligonos-localidades.kml", driver='KML')
	polys.head()
	# Filepath to KML file with municipality polygon (municipio)
	municipalities = gpd.read_file("data/scat.kml", driver='KML')
	municipalities.head()

	# Tag localidad
	print('Started taggin localidad')
	commerce_within(data, polys, 'localidad')
	
	# Tag municipio
	print('Started taggin municipios')
	commerce_within(data, municipalities, 'municipio')

	# Save data
	data.to_file("output/comercios_etiquetados.geojson", driver='GeoJSON')


# Fuction identification location 
def commerce_within(data, polys, column_name):
    locations = set(polys['Name'])
    #n = 0
    for l in locations:
        polygon = polys.loc[polys['Name']== l]
        polygon.reset_index(drop=True, inplace=True)
        pip_mask = data.within(polygon.loc[0, 'geometry'])
        data.loc[pip_mask.index,column_name] = l
    return data[column_name]



if __name__ == '__main__':
	main()