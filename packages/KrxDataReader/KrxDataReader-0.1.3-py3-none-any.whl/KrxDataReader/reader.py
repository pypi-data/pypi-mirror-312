import time
import datetime as dt

import pandas as pd

from .fetcher import KrxFetcher

class KrxDataReader:
    def __init__(self) -> None:
        self.fetcher = KrxFetcher()
        self.base = self._get_base_df()
    
    
    def get_base_df(self):
        """ 기본 정보 """
        return self.base

    def get_dividend_df(self):
        """ 배당 관련 정보 """
        dividend = pd.DataFrame(self.fetcher.fetch_dividend())
        dividend_cols = [
            '종목코드','종목명','시장구분','사업연도','결산월','업종명','업종별배당률','주식배당','',
            '액면가','주당배당금','시가배당률','배당성향','기말주식수','총배당금액'
            ]
        dividend = dividend.iloc[:, : len(dividend_cols)]
        dividend.columns = dividend_cols
        dividend = dividend.drop(columns=[''])
        return dividend

    def get_kospi_sector_df(self):
        """ 코스피 업종 정보 """
        kospi_sector = pd.DataFrame(self.fetcher.fetch_kospi_sector())
        kospi_sector = kospi_sector.iloc[:,:-1]
        kospi_sector.columns = [
            '종목코드','종목명','시장구분','업종명','종가','대비','등락률','시가총액'
            ]
        return kospi_sector
        
    
    def get_kospi_buy_trade_df(self, start_date, end_date):
        """ 코스피 매수자 기관별 """
        date_ranges = self._split_date_ranges(start_date, end_date, 2)
        kospi_buy_trades = []
        for _start_date, _end_date in date_ranges:
            kospi_buy_trades.extend(self.fetcher.fetch_kospi_buy_trade(_start_date, _end_date))
            time.sleep(.5)
        kospi_buy_trade = pd.DataFrame(kospi_buy_trades)
        kospi_buy_trade.columns = [
            '날짜', '금융투자', '보험', '투신', '사모', '은행','기타금융', '연기금', '기타법인',
            '개인', '외국인','기타외국인', '전체'
            ]
        return kospi_buy_trade
    
    def get_kospi_sell_trade_df(self, start_date, end_date):
        """ 코스피 매도자 기관별 """
        date_ranges = self._split_date_ranges(start_date, end_date, 2)
        kospi_sell_trades = []
        for _start_date, _end_date in date_ranges:
            kospi_sell_trades.extend(self.fetcher.fetch_kospi_sell_trade(_start_date, _end_date))
            time.sleep(.5)
        kospi_sell_trade = pd.DataFrame(kospi_sell_trades)
        kospi_sell_trade.columns = [
            '날짜', '금융투자', '보험', '투신', '사모', '은행','기타금융', '연기금', '기타법인',
            '개인', '외국인','기타외국인', '전체'
            ]
        return kospi_sell_trade
    
    def get_kospi_foreign_hold_df(self, start_date, end_date):
        date_ranges = self._split_date_ranges(start_date, end_date, 2)
        kospi_foreign_holds = []
        for _start_date, _end_date in date_ranges:
            kospi_foreign_holds.extend(self.fetcher.fetch_kospi_foreign_hold(_start_date, _end_date))
            time.sleep(.5)
        kospi_foreign_hold = pd.DataFrame(kospi_foreign_holds)
        kospi_foreign_hold.columns = [
            '날짜','전체_시가총액','외국인_시가총액','외국인_시가총액_비율','전체_주식수','외국인_주식수','외국인_주식수_비율'
            ]
        return kospi_foreign_hold
        

    def get_kosdaq_sector_df(self):
        """ 코스닥 업종 정보 """
        kosdaq_sector = pd.DataFrame(self.fetcher.fetch_kosdaq_sector())
        kosdaq_sector = kosdaq_sector.iloc[:,:-1]
        kosdaq_sector.columns = [
            '종목코드','종목명','시장구분','업종명','종가','대비','등락률','시가총액'
            ]
        return kosdaq_sector

    def get_kosdaq_buy_trade_df(self, start_date, end_date):
        """ 코스닥 매수자 기관별 """
        date_ranges = self._split_date_ranges(start_date, end_date, 2)
        kosdaq_buy_trades = []
        for _start_date, _end_date in date_ranges:
            kosdaq_buy_trades.extend(self.fetcher.fetch_kosdaq_buy_trade(_start_date, _end_date))
            time.sleep(.5)
        kosdaq_buy_trade = pd.DataFrame(kosdaq_buy_trades)
        kosdaq_buy_trade.columns = [
            '날짜', '금융투자', '보험', '투신', '사모', '은행','기타금융', '연기금', '기타법인',
            '개인', '외국인','기타외국인', '전체'
            ]
        return kosdaq_buy_trade

    def get_kosdaq_sell_trade_df(self, start_date, end_date):
        """ 코스닥 매도자 기관별 """
        date_ranges = self._split_date_ranges(start_date, end_date, 2)
        kosdaq_sell_trades = []
        for _start_date, _end_date in date_ranges:
            kosdaq_sell_trades.extend(self.fetcher.fetch_kosdaq_sell_trade(_start_date, _end_date))
            time.sleep(.5)
        kosdaq_sell_trade = pd.DataFrame(kosdaq_sell_trades)
        kosdaq_sell_trade.columns = [
            '날짜', '금융투자', '보험', '투신', '사모', '은행','기타금융', '연기금', '기타법인',
            '개인', '외국인','기타외국인', '전체'
            ]
        return kosdaq_sell_trade

    def get_kosdaq_foreign_hold_df(self, start_date, end_date):
        date_ranges = self._split_date_ranges(start_date, end_date, 2)
        kosdaq_foreign_holds = []
        for _start_date, _end_date in date_ranges:
            kosdaq_foreign_holds.extend(self.fetcher.fetch_kosdaq_foreign_hold(_start_date, _end_date))
            time.sleep(.5)
        kosdaq_foreign_hold = pd.DataFrame(kosdaq_foreign_holds)
        kosdaq_foreign_hold.columns = [
            '날짜','전체_시가총액','외국인_시가총액','외국인_시가총액_비율','전체_주식수','외국인_주식수','외국인_주식수_비율'
            ]
        return kosdaq_foreign_hold

    def get_stock_buy_trade_df(self,stock_code, start_date, end_date):
        """ 종목 매수자 기관별 """
        lcode = self.scode_lcode_mapper[stock_code]
        date_ranges = self._split_date_ranges(start_date, end_date, 2)
        stock_buy_trades = []
        for _start_date, _end_date in date_ranges:
            stock_buy_trades.extend(self.fetcher.fetch_stock_buy_trade(lcode,_start_date, _end_date))
            time.sleep(.5)
        stock_buy_trade = pd.DataFrame(stock_buy_trades)
        stock_buy_trade.columns = [
            '날짜', '금융투자', '보험', '투신', '사모', '은행','기타금융', '연기금', '기타법인',
            '개인', '외국인','기타외국인', '전체'
            ]
        return stock_buy_trade
    
    def get_stock_sell_trade_df(self,stock_code, start_date, end_date):
        """ 종목 매도자 기관별 """
        lcode = self.scode_lcode_mapper[stock_code]
        date_ranges = self._split_date_ranges(start_date, end_date, 2)
        stock_sell_trades = []
        for _start_date, _end_date in date_ranges:
            stock_sell_trades.extend(self.fetcher.fetch_stock_sell_trade(lcode,_start_date, _end_date))
            time.sleep(.5)
        stock_sell_trade = pd.DataFrame(stock_sell_trades)
        stock_sell_trade.columns = [
            '날짜', '금융투자', '보험', '투신', '사모', '은행','기타금융', '연기금', '기타법인',
            '개인', '외국인','기타외국인', '전체'
            ]
        return stock_sell_trade
    
    def get_stock_foreign_hold_df(self, stock_code, start_date, end_date):
        lcode = self.scode_lcode_mapper[stock_code]
        date_ranges = self._split_date_ranges(start_date, end_date, 2)
        stock_foreign_holds = []
        for _start_date, _end_date in date_ranges:
            stock_foreign_holds.extend(self.fetcher.fetch_stock_foreign_hold(lcode, _start_date, _end_date))
            time.sleep(.5)
        stock_foreign_hold = pd.DataFrame(stock_foreign_holds)
        stock_foreign_hold = stock_foreign_hold.drop(columns=['FLUC_TP_CD'])
        stock_foreign_hold.columns = [
            '날짜','종가','대비','등락률','전체_주식수','외국인_주식수','외국인_주식수_비율','외국인_한도수량','외국인_한도소진율'
            ]
        return stock_foreign_hold

    def _get_base_df(self):
        """ 기본 정보 """
        base = pd.DataFrame(self.fetcher.fetch_base())
        base.columns = [
            '표준코드','단축코드','한글종목명','한글종목약명','영문종목명','상장일',
            '시장구분','증권구분','소속부','주식종류','액면가','상장주식수'
            ]
        self.scode_lcode_mapper = base.set_index('단축코드')['표준코드'].to_dict()
        return base
    
    def _split_date_ranges(self, start_date, end_date, years=2):
        start_date = self.fetcher._format_datetime(start_date)
        end_date = self.fetcher._format_datetime(end_date)
        ranges = []
        while start_date < end_date:
            range_end = start_date + dt.timedelta(days=years*365)
            if range_end > end_date:
                range_end = end_date
            ranges.append((start_date.strftime("%Y-%m-%d"), range_end.strftime("%Y-%m-%d")))
            start_date = range_end + dt.timedelta(days=1)
        return ranges