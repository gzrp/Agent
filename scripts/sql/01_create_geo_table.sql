CREATE TABLE IF NOT EXISTS geo_table (
   id TEXT PRIMARY KEY,
   name TEXT,
   address TEXT,
   location GEOMETRY,
   pcode INTEGER,
   adcode INTEGER,
   pname TEXT,
   cityname TEXT,
   type TEXT,
   typecode TEXT,
   adname TEXT,
   citycode INTEGER
);