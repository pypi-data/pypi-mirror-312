import pandas as pd

class RealTimeData:
    def __init__(self, data: pd.DataFrame) -> None:
        self.__private_attribute = data
        self.TotalMatchVolume: int
        self.MarketStatus: str
        self.TradingDate: str
        self.ComGroupCode: str
        self.ReferencePrice: float
        self.OpenPrice: float
        self.ClosePrice: float
        self.HighestPrice: float
        self.LowestPrice: float
        self.PriceChange: float
        self.PercentPriceChange: float
        self.MatchVolume: int
        self.MatchValue: float
        self.TotalMatchValue: float
        self.TotalBuyTradeVolume: int
        self.TotalSellTradeVolume: int
        self.TotalDealVolume: int
        self.TotalDealValue: float
        self.ForeignBuyVolumeTotal: int
        self.ForeignBuyValueTotal: float
        self.ForeignSellVolumeTotal: int
        self.ForeignSellValueTotal: float
        
    def to_dataFrame(self) -> pd.DataFrame: ...
    




    


