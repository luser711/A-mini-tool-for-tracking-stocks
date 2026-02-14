#价格追踪
import akshare as ak
import pandas
import matplotlib.pyplot as plt
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy

class PriceTracker:
    def __init__(self):
        self.board_index_20days = self.store_20d_board_index().copy()
        self.board_data_ma = {}
    
    def sector_track(self):
        #满足avg5>avg10 and avg10>avg20的板块
        #计算 ma    
        for v in self.board_index_20days:
            data_length = len(self.board_index_20days[v])
            self.board_data_ma[v] = BoardMAData(
                ma5= numpy.sum((self.board_index_20days[v][data_length-15:-1]))/5 ,
                ma10= numpy.sum((self.board_index_20days[v][data_length-10:-1]))/10,
                ma20= numpy.sum((self.board_index_20days[v][data_length-20:-1]))/20, 
                today= datetime.today().strftime('%Y%m%d'),
                today_index= self.board_index_20days[v][-1]
            )
        return self.board_data_ma    
                
                

    def stock_track(self):
        #满足avg10>=avg20的个股
        pass
    def draw_price_graph(self):
        #画出给出的价格走势图，均线也需要
        pass
    
    def store_20d_board_index(self):
        #获取近20日的价格
        index_20d = {}
        industy_name = ak.stock_board_industry_name_ths()
        
        for n in (industy_name['name']):
            
            try:
                #ak.stock...返回的是dataframe类型， dataframe 包含series 类似于列表或者数组
                index_20d[n] = ak.stock_board_industry_index_ths(
                                    symbol= n,
                                    start_date= ((datetime.today()-timedelta(days=28)).strftime('%Y%m%d')),
                                    end_date= datetime.today().strftime('%Y%m%d')
                                    )['收盘价'].values 
                                    
            except Exception as e:
                print(f"error{e}")                       
        return index_20d
    

@dataclass
class BoardMAData:
    ma5: float
    ma10: float
    ma20: float
    today_index: float
    today: str
  
  
if __name__ == '__main__':
    pt = PriceTracker()
    print(pt.board_index_20days)
    board_ma = pt.sector_track() 
    print(board_ma)
