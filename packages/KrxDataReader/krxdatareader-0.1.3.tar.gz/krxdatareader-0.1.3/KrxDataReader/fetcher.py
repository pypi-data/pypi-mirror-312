import requests
import datetime as dt


class KrxFetcher:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
            'Referer': 'http://data.krx.co.kr/',
        }
        self.url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    def fetch_base(self):
        """기본 정보 추출"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01901",
            "locale": "ko_KR",
            "mktId": "ALL",
            "share": "1",
            "csvxls_isNo": "false",
        }
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['OutBlock_1']
        except:
            return None

    def fetch_dividend(self):
        """배당 정보 추출"""
        data = {
            "bld": "dbms/MDC/STAT/issue/MDCSTAT20901",
            "locale": "ko_KR",
            "mktId": "ALL",
            "tboxisuCd_finder_comnm0_0": "전체",
            "isuCd": "ALL",
            "isuCd2": "ALL",
            "basYy": "2023",
            "indTpCd": "1",
            "share": "1",
            "money": "1",
            "csvxls_isNo": "true",
        }
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['output']
        except:
            return None

    def fetch_kospi_sector(self):
        """섹터 정보 추출"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03901',
            'locale': 'ko_KR',
            'mktId': 'STK',
            'trdDd': '20240730',
            'money': '1',
            'csvxls_isNo': 'false',
        }

        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['block1']
        except:
            return None

    def fetch_kosdaq_sector(self):
        """섹터 정보 추출"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03901',
            'locale': 'ko_KR',
            'mktId': 'KSQ',
            'segTpCd': 'ALL',
            'trdDd': '20240730',
            'money': '1',
            'csvxls_isNo': 'false',
        }
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['block1']
        except:
            return None

    def fetch_kospi_sell_trade(self, start_date, end_date):
        """코스피 매도 거래자 추출"""
        data = self._fetch_market_trade_data(start_date, end_date).copy()
        data['askBid'] = '1'
        data['mktId'] = 'STK'
        data['etf'] = 'EF'
        data['etn'] = 'EN'
        data['elw'] = 'EW'
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['output']
        except:
            return None

    def fetch_kospi_buy_trade(self, start_date, end_date):
        """코스피 매수 거래자 추출"""
        data = self._fetch_market_trade_data(start_date, end_date).copy()
        data['askBid'] = '2'
        data['mktId'] = 'STK'
        data['etf'] = 'EF'
        data['etn'] = 'EN'
        data['elw'] = 'EW'
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['output']
        except:
            return None

    def fetch_kosdaq_sell_trade(self, start_date, end_date):
        """코스닥 매도 거래자 추출"""
        data = self._fetch_market_trade_data(start_date, end_date).copy()
        data['askBid'] = '1'
        data['mktId'] = 'KSQ'
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['output']
        except:
            return None

    def fetch_kosdaq_buy_trade(self, start_date, end_date):
        """코스닥 매수 거래자 추출"""
        data = self._fetch_market_trade_data(start_date, end_date).copy()
        data['askBid'] = '2'
        data['mktId'] = 'KSQ'
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['output']
        except:
            return None

    def fetch_stock_buy_trade(self, lcode, start_date, end_date):
        """주식 매수 거래자 추출"""
        data = self._fetch_stock_trade_data(start_date, end_date)
        data['isuCd'] = lcode
        data['askBid'] = '2'
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['output']
        except:
            return None

    def fetch_stock_sell_trade(self, lcode, start_date, end_date):
        """주식 매도 거래자 추출"""
        data = self._fetch_stock_trade_data(start_date, end_date)
        data['isuCd'] = lcode
        data['askBid'] = '1'
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['output']
        except:
            return None

    def fetch_kospi_foreign_hold(self, start_date, end_date):
        data = self._fetch_market_foreign_hold_data(start_date, end_date)
        data['mktId'] = 'STK'
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['block1']
        except:
            return None

    def fetch_kosdaq_foreign_hold(self, start_date, end_date):
        data = self._fetch_market_foreign_hold_data(start_date, end_date)
        data['mktId'] = 'KSQ'
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['block1']
        except:
            return None

    def fetch_stock_foreign_hold(self, lcode, start_date, end_date):
        data = self._fetch_stock_foreign_hold_data(start_date, end_date)
        data['isuCd'] = lcode
        r = requests.post(self.url, data, headers=self.headers)
        try:
            return r.json()['output']
        except:
            return None
        

    def _fetch_stock_trade_data(self, start_date, end_date):
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02303',
            'locale': 'ko_KR',
            'inqTpCd': '2',
            'trdVolVal': '2',
            'strtDd': self._format_datetime(start_date).strftime("%Y%m%d"),
            'endDd': self._format_datetime(end_date).strftime("%Y%m%d"),
            'detailView': '1',
            'money': '3',
            'csvxls_isNo': 'false',
        }
        return data

    def _fetch_market_trade_data(self, start_date, end_date):
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02203',
            'locale': 'ko_KR',
            'inqTpCd': '2',
            'trdVolVal': '2',
            'strtDd': self._format_datetime(start_date).strftime("%Y%m%d"),
            'endDd': self._format_datetime(end_date).strftime("%Y%m%d"),
            'detailView': '1',
            'money': '3',
            'csvxls_isNo': 'false',
        }
        return data

    def _fetch_market_foreign_hold_data(self, start_date, end_date):
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03601',
            'locale': 'ko_KR',
            'segTpCd': 'ALL',
            'strtDd': self._format_datetime(start_date).strftime("%Y%m%d"),
            'endDd': self._format_datetime(end_date).strftime("%Y%m%d"),
            'share': '2',
            'money': '3',
            'csvxls_isNo': 'false',
        }
        return data

    def _fetch_stock_foreign_hold_data(self, start_date, end_date):
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03702',
            'locale': 'ko_KR',
            'searchType': '2',
            'mktId': 'ALL',
            'param1isuCd_finder_stkisu0_1': 'ALL',
            'strtDd': self._format_datetime(start_date).strftime("%Y%m%d"),
            'endDd': self._format_datetime(end_date).strftime("%Y%m%d"),
            'share': '1',
            'csvxls_isNo': 'false',
        }
        return data

    @staticmethod
    def _format_datetime(datetime_str):
        datetime_dt = dt.datetime.strptime(datetime_str, '%Y-%m-%d')
        return datetime_dt
