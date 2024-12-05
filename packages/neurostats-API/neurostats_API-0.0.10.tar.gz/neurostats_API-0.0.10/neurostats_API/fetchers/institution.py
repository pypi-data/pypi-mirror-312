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
        raise(NotImplementedError("InstitutionFetcher : Not done yet"))
        super().__init__(ticker, db_client)

    def prepare_query(self, start_date, end_date):
        pipeline = super().prepare_query()

        target_query = {
            "date": date,
            "institution_trading": "$$target_season_data.institution_trading"
        }


        pipeline.append({
            "$project": {
                "_id": 0,
                "ticker": 1,
                "company_name": 1,
                "profit_loses": {
                    "$map": {
                        "input": {
                            "$filter": {
                                "input": "$daily_data",
                                "as": "daily",
                                "cond": {
                                        "$and": [
                                        {"$gte": ["$$daily.date", start_date]},
                                        {"$lte": ["$$daily.date", end_date]}
                                    ]
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

    def collect_data(self, date):
        pipeline = self.prepare_query(date)

        fetched_data = self.collection.aggregate(pipeline).to_list()

        return fetch_data[-1]
    
    def query_data(self):
        try:
            latest_time = StatsDateTime.get_latest_time(
                self.ticker, self.collection)['last_update_time']
            latest_date = latest_time['daily_data']['institution_trading']['last_update']
            date = latest_date.replace(hour=0, minute=0, second=0, microsecond=0) 
        except Exception as e:
            print(f"No updated time for institution_trading in {self.ticker}, use current time instead")
            date = datetime.now(self.timezone)
            date = date.replace(hour=0, minute=0, second=0, microsecond=0) 

            if (date.hour < 17):  # 拿不到今天的資料
                date = date - timedelta(days=1)
        
        start_date = start_date - timedelta(days=365)

        daily_data = self.collect_data(date)

        daily_data = sorted(daily_data['daily_data'], key = lambda x : x['date'], reverse = True)

        self.process_data(self.ticker, daily_data)
    
    def process_data(self, daily_data):
        table_dict = dict()

        latest_data = daily_data[0] 
        yesterday_data = daily_data[1]

        # 交易價格與昨天交易
        table_dict = {
            "open": latest_data['open'],
            'close': latest_data['close'],
            'range': f"{latest_data['high']}-{latest_data['low']}",
            'volumn': latest_data['volumn'] / 1000

        }

        # 今日法人買賣

        # 一年內法人






        
