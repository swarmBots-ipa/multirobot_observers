from influxdb import InfluxDBClient
import datetime
from tabulate import tabulate

def influxQueries(no_of_bots):
    client = InfluxDBClient(host='localhost',port = 8086)
    client.create_database('powerdb')
    client.get_list_database()
    client.switch_database('powerdb')
    #no_of_bots=4

    for i in range(no_of_bots):
        results=client.query('select * from powerdata_'+str(i))
        points = list(results.get_points())
        print(tabulate(points, headers='keys'))

