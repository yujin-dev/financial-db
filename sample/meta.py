from sqlalchemy import create_engine, MetaData, Table, Column, Float, TIMESTAMP, Integer, VARCHAR

def create_table(addr):

   meta = MetaData()

   Table(
      'sample_price', meta, 
      Column('time', TIMESTAMP, primary_key = True), 
      Column('symbol', VARCHAR),
      Column('price', Float),
      Column('day_volume', Integer),
   )

   engine = create_engine(addr, echo = True)
   meta.create_all(engine)