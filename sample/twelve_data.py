from meta import create_table
from twelvedata import TDClient
import psycopg2
from dump import Ingestion
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

class WebsocketPipeline(Ingestion):

    # batch size used to insert data in batches
    MAX_BATCH_SIZE=100
    
    def __init__(self, conn, table_name, columns):
        super().__init__(conn, table_name, columns)
        self.current_batch = []
        self.insert_counter = 0
        
    def _on_event(self, event):
        """This function gets called whenever there's a new data record coming
        back from the server.


        Args:
            event (dict): data record
        """
        if event["event"] == "price":
            # data record
            timestamp = datetime.utcfromtimestamp(event["timestamp"])
            data = (timestamp, event["symbol"], event["price"], event.get("day_volume"))


            # add new data record to batch
            self.current_batch.append(data)
            print(f"Current batch size: {len(self.current_batch)}")
            
            # ingest data if max batch size is reached then reset the batch
            if len(self.current_batch) == self.MAX_BATCH_SIZE:
                self._insert_values(self.current_batch)
                self.insert_counter += 1
                print(f"Batch insert #{self.insert_counter}")
                self.current_batch = []
    
    def start(self, symbols):
        """Connect to the web socket server and start streaming real-time data 
        into the database.

        Args:
            symbols (list of symbols): List of stock/crypto symbols
        """
        td = TDClient(apikey=os.environ.get("TWELVE_DATA_SECRET"))
        ws = td.websocket(on_event=self._on_event)
        ws.subscribe(symbols)
        ws.connect()
        ws.keep_alive()


if __name__ == "__main__":

    DB=os.environ.get("TS_DB")
    USER=os.environ.get("TS_USER")
    PWD=os.environ.get("TS_PASSWORD")
    create_table(f'postgresql://{USER}:{PWD}@localhost:5432/{DB}')
    # conn = psycopg2.connect(database=DB, 
    #                         host="localhost", 
    #                         user=USER, 
    #                         password=PWD,
    #                         port="5432")

    # symbols = ["BTC/USD", "ETH/USD", "MSFT", "AAPL"]
    # websocket = WebsocketPipeline(conn, "prices_real_time", ["time", "symbol", "price", "day_volume"])
    # websocket.start(symbols=symbols)