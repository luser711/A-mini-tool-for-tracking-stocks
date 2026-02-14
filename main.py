#价格追踪
import numpy
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='./price_tracker.log'  # 日志文件路径
)
logger = logging.getLogger(__name__)



import akshare as ak
import matplotlib.pyplot as plt
from dataclasses import dataclass
from datetime import datetime, timedelta
from pandas import  DataFrame

class PriceTracker:
    def __init__(self):
        #每次初始化都太久了...
        logger.info("Initializing...")
        self.board_index_20days = self.store_20d_board_index(self._get_board_index())
        self.board_data_ma = self.computing_board_data_ma()
        self.board_filtered = self.filter_sector()
        logger.info("Initializing is done.")
        
    def computing_board_data_ma(self):
        #计算 ma5, m10,20
        board_ma = {}
        board_index_20days = self.board_index_20days
        for v in board_index_20days:
                board_ma[v] = BoardMAData(
                ma5= numpy.mean(board_index_20days[v][-5:]),
                ma10= numpy.mean((board_index_20days[v][-10:])),
                ma20= numpy.mean((board_index_20days[v][-20:])), 
                today= datetime.today().strftime('%Y%m%d'),
                today_index= board_index_20days[v][-1]
            )
        return board_ma  
             
    def filter_sector(self):
        #满足avg5>avg10 and avg10>avg20的板块
        board_data_ma_copy = self.board_data_ma
        sector_filited = []
        for key in board_data_ma_copy:
            bkey = board_data_ma_copy[key]
            if bkey.ma10>= bkey.ma20 and bkey.ma5 >= bkey.ma10:
                sector_filited.append(key)   
        
        return sector_filited   
                
                

    def stock_track(self):
        #满足avg10>=avg20的个股
        pass
    def draw_price_graph(self):
        #画出给出的价格走势图，均线也需要
        pass
    
    def _get_board_index(self):
        industry_name = ak.stock_board_industry_name_ths()#Fixed: Spelling wrong industy--->industry
        return industry_name
        
    def store_20d_board_index(self,industry_name:DataFrame) -> dict:
        
        #函数应该高内聚，职责单一，这边把获取20日价格功能提取出来 ---> _get_board_index(self)
        
        #判断是否为dataframe 并且判断是否为空以避免没有必要的循环或者意外，增加安全性
        if isinstance(industry_name, DataFrame) and not industry_name['name'].empty:
                index_20d = {}  
                for n in (industry_name['name']):
                        if isinstance(n, str):
                                                
                                    try:
                                        #ak.stock...返回的是dataframe类型， dataframe 包含series 类似于列表或者数组
                                        index_20d[n] = ak.stock_board_industry_index_ths(
                                                                    symbol= n,
                                                                    start_date= ((datetime.today()-timedelta(days=28)).strftime('%Y%m%d')),
                                                                    end_date= datetime.today().strftime('%Y%m%d')
                                                                    )['收盘价'].values 
                                    except Exception as e:
                                        
                                        logger.error(f"获取板块{n} 数据失败{e}") # Fixed: More completed error output 
                        continue                                                #----and use logging moudle to record error
                return index_20d    
        else:
            logger.error(f"获取行业{industry_name}")                                       
        return {}
        

@dataclass
class BoardMAData:
    ma5: float
    ma10: float
    ma20: float
    today_index: float
    today: str
  
  
if __name__ == '__main__':
    pt = PriceTracker()
    print(pt.board_filtered)
