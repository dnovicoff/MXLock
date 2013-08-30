"""
File: settings.py
Purpose: Database and various login file manipulation settings
Copywrite: Sendwell 2013
"""

DBG_PGSQL_USER  = "mxlock"
DBG_PGSQL_PASS     = "mxlock" #"HulkSmash!" 
DBG_PGSQL_SERVER    = "192.168.0.227"  
DBG_PGSQL_DATABASE  = 'dns4new'
DBG_PGSQL_PORT = 3306

DBG_THREADS_RESOLVER = 1
DBG_THREADS_MEMCACHE = 3

DBG_READER = "async"
DBG_WRITER = "memcache"

DBG_RESOLVERS = "192.168.0.233 192.168.0.2"
DBG_TIMEOUT = 3
DBG_UDP = True
DBG_SINGLEPORT = False

DBG_GEODIRCOUNTRY4 = "/usr/share/GeoIP/GeoIP.dat"
DBG_GEODIRCOUNTRY6 = "/usr/share/GeoIP/GeoIPv6.dat"
DBG_GEODIRCITY4 = "/usr/share/GeoIP/GeoLiteCity.dat"

PGSQL_USER  = "hmsuser"
PGSQL_PASS     = "test123" #"HulkSmash!" 
PGSQL_SERVER    = "192.168.0.227"#192.168.69.19 
PGSQL_DATABASE  = 'hms'
PGSQL_PORT = 5432

GEN_FIFO_PATH = "/tmp/gen_fifo"
GEN_LOG_PATH = "/home/david/sendwell/pygenTNG/src/logs"
GEN_DATA_PATH = "/home/david/sendwell/pygenTNG/src/data"
MAILDUPE_MEMCACHED_PORT   =   11212
MAILDUPE_MEMCACHED_ADDRESS = "127.0.0.1"