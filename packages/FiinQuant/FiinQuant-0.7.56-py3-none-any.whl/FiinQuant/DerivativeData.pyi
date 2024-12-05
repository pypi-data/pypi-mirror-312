import pandas as pd
class DerivativeData:
    def __init__(self, data) -> None: 
        self.__private_attribute: pd.DataFrame 
        self.TotalMatchVolume: int 
        self.MarketStatus: str 
        self.TradingDate: str 
        self.MatchType: str 
        self.ComGroupCode: str
        self.DerivativeCode: str 
        self.ReferencePrice: float 
        self.OpenPrice: float 
        self.ClosePrice: float 
        self.CeilingPrice: float 
        self.FloorPrice: float 
        self.HighestPrice: float 
        self.LowestPrice: float 
        self.MatchPrice: float 
        self.PriceChange: float 
        self.PercentPriceChange: float 
        self.MatchVolume: int 
        self.MatchValue: float 
        self.TotalMatchValue: float 
        self.TotalBuyTradeVolume: int 
        self.TotalSellTradeVolume: int 
        self.DealPrice: float 
        self.TotalDealVolume: int 
        self.TotalDealValue: float 
        self.ForeignBuyVolumeTotal: int
        self.ForeignBuyValueTotal: float
        self.ForeignSellVolumeTotal: int 
        self.ForeignSellValueTotal: float 
        self.ForeignTotalRoom: int 
        self.ForeignCurrentRoom: int
        self.OpenInterest: str 
    def to_dataFrame(self) -> pd.DataFrame: ...

    