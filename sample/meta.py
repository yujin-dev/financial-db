from sqlalchemy import create_engine, MetaData, Table, Column, Float, DateTime

def create_table(addr):

   meta = MetaData()

   Table(
      'prices_real_time', meta, 
      Column('time', DateTime, primary_key = True), 
      Column('symbol', Float),
      Column('price', Float),
      Column('day_volume', Float),
   )

   engine = create_engine(addr, echo = True)
   meta.create_all(engine)