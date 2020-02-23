from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.functions import concat, col, lit


def strToType(str):
  if str == 'int':
    return IntegerType()
  elif str == 'double':
    return DoubleType()
  else:
    return StringType()

def spit_it_out(pds):
  ##### this will read in csv from local upload and spit out column and renamed original datasets #####
  varname_ids = []
  varname_xwalk = []

  for i,v in enumerate(pds.columns):
    vid = f'var_{str(i)}'
    varname_ids.append(vid)
    varname_xwalk.append((vid,v))

    pds = pds.withColumnRenamed(v, vid)


  headers = [['id', 'string'], ['varname','string']]
  schema = StructType([StructField(t[0], strToType(t[1]), True) for t in headers])

  varname_xwalk_rdd = sc.parallelize(varname_xwalk)
  varname_xwalk_df = sqlContext.createDataFrame(varname_xwalk_rdd, schema)

  return varname_xwalk_df, pds

def readin(ds_col_name, ds_name):
  col = spark.table(ds_col_name).select("*").toPandas()
  renvar_dict = dict(zip(col['id'], col['varname']))

  ds = spark.table(ds_name).select("*").toPandas()
  ds.rename(columns=renvar_dict, inplace=True)
  return ds
