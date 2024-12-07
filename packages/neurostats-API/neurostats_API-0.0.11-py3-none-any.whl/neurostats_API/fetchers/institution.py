from .base import StatsFetcher
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor
import importlib.resources as pkg_resources
import yaml


class InstitutionFetcher(StatsFetcher):
    """
    iFa -> 交易資訊 -> 法人買賣

    包括: 
    1. 當日交易
    2. 一年內交易
    """

    def __init__(self, ticker, db_client):
        super().__init__(ticker, db_client)

    def prepare_query(self, start_date, end_date):
        pipeline = super().prepare_query()

        # target_query = {
        #     "date": date,
        #     "institution_trading": "$$target_season_data.institution_trading"
        # }

        pipeline.append({
            "$project": {
                "_id": 0,
                "ticker": 1,
                "company_name": 1,
                "daily_data": {
                    "$map": {
                        "input": {
                            "$filter": {
                                "input": "$daily_data",
                                "as": "daily",
                                "cond": {
                                    "$and": [{
                                        "$gte": ["$$daily.date", start_date]
                                    }, {
                                        "$lte": ["$$daily.date", end_date]
                                    }]
                                }
                            }
                        },
                        "as": "target_daily_data",
                        "in": "$$target_daily_data"
                    }
                }
            }
        })

        return pipeline

    def collect_data(self, start_date, end_date):
        pipeline = self.prepare_query(start_date, end_date)

        fetched_data = self.collection.aggregate(pipeline).to_list()

        return fetched_data[-1]

    def query_data(self):
        try:
            latest_time = StatsDateTime.get_latest_time(
                self.ticker, self.collection)['last_update_time']
            latest_date = latest_time['institution_trading'][
                'latest_date']
            date = latest_date.replace(hour=0,
                                       minute=0,
                                       second=0,
                                       microsecond=0)
        except Exception as e:
            print(
                f"No updated time for institution_trading in {self.ticker}, use current time instead"
            )
            date = datetime.now(self.timezone)
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)

            if (date.hour < 17):  # 拿不到今天的資料
                date = date - timedelta(days=1)

        start_date = date - timedelta(days=365)

        daily_data = self.collect_data(start_date, end_date=date)

        daily_data = sorted(daily_data['daily_data'],
                            key=lambda x: x['date'],
                            reverse=True)

        table_dict = self.process_data(daily_data)

        return table_dict

    def process_data(self, daily_data):
        table_dict = dict()

        latest_data = daily_data[0]
        yesterday_data = daily_data[1]

        # 交易價格與昨天交易
        price_dict = {
            "open": latest_data['open'],
            'close': latest_data['close'],
            'range': f"{latest_data['low']}-{latest_data['high']}",
            'volumn': latest_data['volume'] / 1000,
            'last_open': yesterday_data['open'],
            'last_close': yesterday_data['close'],
            'last_range': f"{yesterday_data['low']}-{yesterday_data['high']}",
            'last_volumn': yesterday_data['volume'] / 1000
        }
        # 一年範圍
        annual_lows = [data['low'] for data in daily_data]
        annual_highs = [data['high'] for data in daily_data]
        lowest = np.min(annual_lows).item()
        highest = np.max(annual_highs).item()

        price_dict['52weeks_range'] = f"{lowest}-{highest}"
        table_dict['price'] = price_dict

        # 發行股數 & 市值

        # 今日法人買賣
        table_dict['latest_trading'] = {
            "date":
            daily_data[0]['date'],
            "table":
            self.process_latest_trading(daily_data[0]['institution_trading'], daily_data[0]['volume'])
        }
        # 一年內法人
        annual_trading = [
            {
                **data['institution_trading'],
                "收盤價": int(data['close'])
            }
            for data in daily_data
        ]  # 將close也併入這個表格
        annual_dates = [data['date'] for data in daily_data]
        table_dict['annual_trading'] = self.process_annual_trading(
            annual_dates, annual_trading)
        
        return table_dict

    def process_latest_trading(self, latest_trading, volume):
        latest_table = {
            "foreign": self.default_institution_chart(),
            "mutual": self.default_institution_chart(),
            "prop": self.default_institution_chart(),
            "institutional_investor":self.default_institution_chart(),
        }

        for key in latest_trading.keys():
            if (key.find("外陸資") >= 0 or key.find("外資") >= 0):
                self.target_institution(latest_trading, latest_table['foreign'], key, volume)
            elif (key.find("自營商") >= 0):
                self.target_institution(latest_trading,latest_table['prop'], key, volume)
            elif (key.find("投信") >= 0):
                self.target_institution(latest_trading,latest_table['mutual'], key, volume)
            elif (key.find("三大法人") >= 0):
                self.target_institution(latest_trading,latest_table['institutional_investor'], key, volume)

        frames = []
        for category, trades in latest_table.items():
            temp_df = pd.DataFrame(trades).T
            temp_df['category'] = category
            frames.append(temp_df)
        
        latest_df = pd.concat(frames)
        latest_df = latest_df.reset_index().rename(columns={'index': 'type'})
        latest_df = latest_df[['type', 'category', 'stock', 'price', 'average_price', 'percentage']]

        return latest_df

    def process_annual_trading(self, dates, annual_tradings):
        dates = [date.strftime("%m/%d") for date in dates]
        return pd.DataFrame(annual_tradings, index=dates)

    def target_institution(self, old_table, new_table, key, volume):
        if (key.find("買進") >= 0):
            self.cal_institution(old_table, new_table['buy'], key, volume)
        elif (key.find("賣出") >= 0):
            self.cal_institution(old_table, new_table['sell'], key, volume)
        elif (key.find("買賣超") >= 0):
            self.cal_institution(old_table, new_table['over_buy_sell'], key, volume)
        
    def cal_institution(self, old_table, new_table, key, volume):
        new_table['stock'] = np.round(old_table[key] / 1000, 2).item()
        new_table['percentage'] = np.round((old_table[key] / volume) * 100, 2).item()
    
    def default_institution_chart(self):
        return {
            "buy": {
                "stock": 0,
                "price": 0,
                "average_price": 0,
                "percentage": 0
            },
            "sell": {
                "stock": 0,
                "price": 0,
                "average_price": 0,
                "percentage": 0
            },
            "over_buy_sell": {
                "stock": 0,
                "price": 0,
                "average_price": 0,
                "percentage": 0
            },
        }