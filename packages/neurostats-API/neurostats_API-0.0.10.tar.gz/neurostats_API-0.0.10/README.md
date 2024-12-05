# neurostats_API

- [檔案架構](#檔案架構)
- [使用方法](#使用方法)
    - [下載](#下載)
    - [價值投資](#得到最新一期的評價資料與歷年評價)
    - [財務分析-重要指標](#財務分析-重要指標)
    - [月營收表](#回傳月營收表)
    - [損益表](#損益表)
    - [資產負債表](#資產負債表)
    - [現金流量表](#現金流量表)
    - [版本紀錄](#版本紀錄)


## 檔案架構

```
├── neurostats_API
│   ├── __init__.py
│   ├── cli.py
│   ├── main.py
│   ├── fetchers
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── balance_sheet.py
│   │   ├── cash_flow.py
│   │   ├── finance_overview.py
│   │   ├── profit_lose.py
│   │   ├── tech.py
│   │   ├── value_invest.py
│   ├── tools
│   │   ├── balance_sheet.yaml
│   │   ├── cash_flow_percentage.yaml
│   │   ├── finance_overview_dict.yaml
│   │   ├── profit_lose.yaml
│   │   └── seasonal_data_field_dict.txt
│   └── utils
│       ├──__init__.py
│       ├── data_process.py
│       ├── datetime.py
│       ├── db_client.py
│       └── fetcher.py
├──  test
│    ├── __init__.py
│    └── test_fetchers.py
├── Makefile
├── MANIFEST.in
├── README.md
├── requirement.txt
├── setup.py

```
- `neurostats_API`: 主要的package運行內容
   - `fetchers`: 回傳service內容的fetcher檔案夾
      - `base.py`: 基本架構
      - `value_invest.py`: iFa.ai -> 價值投資
      - `finance_overview.py`: iFa.ai -> 財務分析 -> 重要指標
      - `tech.py`: iFa.ai -> 技術指標
   - `tools`: 存放各種設定檔與資料庫index對應領域的dictionary
   - `utils`: 
      - `fetcher.py`: Service的舊主架構, 月營收, 損益表, 資產負債表, 資產收益表目前在這裡
      - `data_process.py`: config資料的讀取
      - `datetime.py`: 時間格式，包括日期,年度,月份,日,季度

## 下載
```
pip install neurostats-API
```
### 確認下載成功
```Python 
>>> import neurostats_API
>>> print(neurostats_API.__version__)
0.0.10
```

### 得到最新一期的評價資料與歷年評價
``` Python
from neurostats_API.utils import ValueFetcher, DBClient
db_client = DBClient("<連接的DB位置>").get_client()
ticker = "2330" # 換成tw50內任意ticker
fetcher = ValueFetcher(ticker, db_client)
data = stats_fetcher.query_data()
```

#### 回傳(2330為例)
```Python
{
    "ticker": 股票代碼,
    "company_name": 公司中文名稱,
    "daily_data":{
    ## 以下八個是iFa項目
        "P_E": 本益比,
        "P_B": 股價,
        "P_FCF": 股價自由現金流比,
        "P_S": 股價營收比,
        "EV_EBIT: ,
        "EV_EBITDA": ,
        "EV_OPI": ,
        "EV_S"; 
    ## 以上八個是iFa項目
        "close": 收盤價,
    }

    "yearly_data": pd.DataFrame (下表格為範例)
        year    P_E       P_FCF   P_B        P_S     EV_OPI    EV_EBIT   EV_EBITDA       EV_S
    0   107  16.68   29.155555  3.71  11.369868  29.837201  28.798274  187.647704  11.107886
    1   108  26.06   67.269095  5.41  17.025721  50.145736  47.853790  302.526388  17.088863
    2   109  27.98   95.650723  7.69  22.055379  53.346615  51.653834  205.847232  22.481951
    3   110  27.83  149.512474  7.68  22.047422  55.398018  54.221387  257.091893  22.615355
    4   111  13.11   48.562021  4.25  11.524975  24.683850  24.226554   66.953260  12.129333
    5   112  17.17  216.371410  4.59  16.419533  40.017707  37.699267  105.980652  17.127656
    6  過去4季    NaN -24.929987   NaN  4.300817      83.102921   55.788996 -1073.037084  7.436656
}
```
> 這裡有Nan是因為本益比與P/B等資料沒有爬到最新的時間

### 回傳月營收表
``` Python
from neurostats_API.fetchers import MonthRevenueFetcher, DBClient
db_client = DBClient("<連接的DB位置>").get_client()
ticker = "2330" # 換成tw50內任意ticker
fetcher = MonthRevenueFetcherFetcher(ticker, db_client)
data = fetcher.query_data()
```

#### 回傳
```Python
{
        "ticker": "2330",
        "company_name": "台積電",
        "month_revenue":
        year                 2024  ...        2014
        month                      ...
        grand_total  2.025847e+09  ...         NaN
        12                    NaN  ...  69510190.0
        ...                   ...  ...         ...
        2            1.816483e+08  ...  46829051.0
        1            2.157851e+08  ...  51429993.0

        "this_month_revenue_over_years":
        year                             2024  ...        2015
        revenue                  2.518727e+08  ...  64514083.0
        revenue_increment_ratio  3.960000e+01  ...       -13.8
        ...                               ...  ...         ...
        YoY_5                    1.465200e+02  ...         NaN
        YoY_10                            NaN  ...         NaN

        "grand_total_over_years":
        year                                 2024  ...          2015
        grand_total                  2.025847e+09  ...  6.399788e+08
        grand_total_increment_ratio  3.187000e+01  ...  1.845000e+01
        ...                                   ...  ...           ...
        grand_total_YoY_5            1.691300e+02  ...           NaN
        grand_total_YoY_10                    NaN  ...           NaN


}
```
- `'ticker'`: 股票代碼
- `'company_name'`: 公司名稱 
- `'month_revenue'`: 歷年的月營收以及到今年最新月份累計的月營收表格 
- `'this_month_revenue_over_years'`: 今年這個月的月營收與歷年同月份的營收比較
- `'grand_total_over_years'`: 累計至今年這個月的月營收與歷年的比較

> 大部分資料(成長率)缺失是因為尚未計算，僅先填上已經有的資料


### 財務分析: 重要指標
對應https://ifa.ai/tw-stock/2330/finance-overview
```Python
from neurostats_API.fetchers import FinanceOverviewFetcher, DBClient
db_client = DBClient("<連接的DB位置>").get_client()
ticker = "2330"
fetcher = FinanceOverviewFetcher(ticker = "2330", db_client = db_client)
data = fetcher.query_data()
```

#### 回傳
型態為Dict:
```Python
{
        ticker: str #股票代碼,
        company_name: str #公司名稱,
        seasonal_data: Dict # 回傳資料
}
```

以下為seasonal_data目前回傳的key的中英對應(中文皆參照iFa.ai)

markdown
複製程式碼
| 英文                                | 中文                          |
|-----------------------------------|-----------------------------|
|**財務概況**|
| revenue                           | 營業收入                     |
| gross_profit                      | 營業毛利                     |
| operating_income                  | 營業利益                     |
| net_income                        | 淨利                        |
| operating_cash_flow               | 營業活動之現金流              |
| invest_cash_flow                  | 投資活動之淨現金流             |
| financing_cash_flow               | 籌資活動之淨現金流             |
|**每股財務狀況**|
| revenue_per_share                 | 每股營收                     |
| gross_per_share                   | 每股營業毛利                  |
| operating_income_per_share        | 每股營業利益                  |
| eps                               | 每股盈餘(EPS)                |
| operating_cash_flow_per_share     | 每股營業現金流                |
| fcf_per_share                     | 每股自由現金流                |
| debt_to_operating_cash_flow       | 每股有息負債                  |
| equity                            | 每股淨值                     |
|**獲利能力**|
| roa                               | 資產報酬率                    |
| roe                               | 股東權益報酬率                 |
| gross_over_asset                  | 營業毛利÷總資產               |
| roce                              | ROCE                        |
| gross_profit_margin               | 營業毛利率                    |
| operation_profit_rate             | 營業利益率                    |
| net_income_rate                   | 淨利率                       |
| operating_cash_flow_profit_rate   | 營業現金流利潤率               |
|**成長動能**|
| revenue_YoY                       | 營收年成長率                  |
| gross_prof_YoY                    | 營業毛利年成長率               |
| operating_income_YoY              | 營業利益年成長率               |
| net_income_YoY                    | 淨利年成長率                  |
|**營運指標**|
| dso                               | 應收帳款收現天數               |
| account_receive_over_revenue      | 應收帳款佔營收比率             |
| dio                               | 平均售貨天數                  |
| inventories_revenue_ratio         | 存貨佔營收比率                |
| dpo                               | 應付帳款付現日天數             |
| cash_of_conversion_cycle          | 現金循環週期                  |
| asset_turnover                    | 總資產週轉率                  |
| applcation_turnover               | 不動產、廠房及設備週轉率        |
|**財務韌性**|
| current_ratio                     | 流動比率                     |
| quick_ratio                       | 速動比率                     |
| debt_to_equity_ratio              | 負債權益比率                  |
| net_debt_to_equity_ratio          | 淨負債權益比率                |
| interest_coverage_ratio           | 利息保障倍數                  |
| debt_to_operating_cash_flow       | 有息負債÷營業活動現金流         |
| debt_to_free_cash_flow            | 有息負債÷自由現金流            |
| cash_flow_ratio                   | 現金流量比率                  |
|**資產負債表**|
| current_assets                    | 流動資產                     |
| current_liabilities               | 流動負債                     |
| non_current_assets      | 非流動資產                    |
| non_current_liabilities| 非流動負債                    |
| total_asset                       | 資產總額                     |
| total_liabilities                 | 負債總額                     |
| equity                            | 權益                        |

#### 以下數值未在回傳資料中，待資料庫更新 
|英文|中文|
|---|----|
|**成長動能**|
| operating_cash_flow_YoY | 營業現金流年成長率             |
| fcf_YoY  | 自由現金流年成長率             |
| operating_cash_flow_per_share_YoY | 每股營業現金流年成長率          |
| fcf_per_share_YoY | 每股自由現金流年成長率          |

### 損益表
```Python
from neurostats_API.fetchers import ProfitLoseFetcher, DBClient
db_client = DBClient("<連接的DB位置>").get_client()
fetcher = ProfitLoseFetcher(db_client)
ticker = "2330" # 換成tw50內任意ticker
data = fetcher.query_data()
```
   
#### 回傳
因項目眾多，不列出詳細內容，僅列出目前會回傳的項目
```Python
{
        "ticker": "2330"
        "company_name": "台積電"
        # 以下皆為pd.DataFrame
        "profit_lose":  #損益表,
        "grand_total_profit_lose": #今年度累計損益表,
        # 營業收入
        "revenue": # 營收成長率
        "grand_total_revenue": # 營收累計成場濾
        # 毛利
        "gross_profit": # 毛利成長率
        "grand_total_gross_profit": # 累計毛利成長率
        "gross_profit_percentage": # 毛利率
        "grand_total_gross_profit_percentage" # 累計毛利率
        # 營利
        "operating_income": # 營利成長率
        "grand_total_operating_income": # 累計營利成長率
        "operating_income_percentage": # 營利率
        "grand_total_operating_income_percentage": # 累計營利率
        # 稅前淨利
        "net_income_before_tax": # 稅前淨利成長率
        "grand_total_net_income_before_tax": # 累計稅前淨利成長率
        "net_income_before_tax_percentage": # 稅前淨利率
        "grand_total_net_income_before_tax_percentage": # 累計稅前淨利率
        # 本期淨利
        "net_income": # 本期淨利成長率
        "grand_total_net_income": # 累計本期淨利成長率
        "net_income_percentage": # 本期淨利率
        "grand_total_income_percentage": # 累計本期淨利率
        # EPS
        "EPS":  # EPS
        "EPS_growth":  # EPS成長率
        "grand_total_EPS": # 累計EPS
        "grand_total_EPS_growth": # 累計EPS成長率
}
```

### 資產負債表
``` Python
from neurostats_API.fetchers import BalanceSheetFetcher, DBClient
db_client = DBClient("<連接的DB位置>").get_client()
ticker = "2330" # 換成tw50內任意ticker
fetcher = BalanceSheetFetcher(ticker, db_client)

stats_fetcher.query_data()
```

#### 回傳
```Python
{
        "ticker": "2330"
        "company_name":"台積電"
        "balance_sheet":
                2024Q2_value  ...  2018Q2_percentage
        流動資產                   NaN  ...                NaN
        現金及約當現金       1.799127e+09  ...              30.79
        ...                    ...  ...                ...
        避險之衍生金融負債－流動           NaN  ...               0.00
        負債準備－流動                NaN  ...               0.00

        "total_asset":
        2024Q2_value  ...  2018Q2_percentage
        資產總額  5.982364e+09  ...             100.00
        負債總額  2.162216e+09  ...              27.41
        權益總額  3.820148e+09  ...              72.59


        "current_asset":
                2024Q2_value  ...  2018Q2_percentage
        流動資產合計  2.591658e+09  ...               46.7

        "non_current_asset":
                2024Q2_value  ...  2018Q2_percentage
        非流動資產合計  3.390706e+09  ...               53.3

        "current_debt":
                2024Q2_value  ...  2018Q2_percentage
        流動負債合計  1.048916e+09  ...              22.55

        "non_current_debt":
                2024Q2_value  ...  2018Q2_percentage
        非流動負債合計  1.113300e+09  ...               4.86

        "equity":
        2024Q2_value  ...  2018Q2_percentage
        權益總額  3.820148e+09  ...              72.59

}
```
- `'ticker'`: 股票代碼
- `'company_name'`: 公司名稱 
- `'balance_sheet'`: 歷年當季資場負債表"全表" 
- `'total_asset'`: 歷年當季資產總額 
- `'current_asset'`: 歷年當季流動資產總額
- `'non_current_asset'`: 歷年當季非流動資產
- `'current_debt'`: 歷年當季流動負債
- `'non_current_debt'`: 歷年當季非流動負債
- `'equity'`:  歷年當季權益

### 現金流量表
``` Python
from neurostats_API.fetchers import CashFlowFetcher
db_client = DBClient("<連接的DB位置>").get_client()
ticker = 2330 # 換成tw50內任意ticker
fetcher = StatsFetcher(ticker, db_client)

stats_fetcher.query()
```
#### 回傳
```Python
{
        "ticker": "2330"
        "company_name": "台積電"
        "cash_flow":
                        2023Q3_value  ...  2018Q3_percentage
        營業活動之現金流量－間接法                  NaN  ...                NaN
        繼續營業單位稅前淨利（淨損）         700890335.0  ...           0.744778
        ...                            ...  ...                ...
        以成本衡量之金融資產減資退回股款               NaN  ...                NaN
        除列避險之金融負債∕避險 之衍生金融負債           NaN  ...          -0.000770

        "CASHO":
                        2023Q3_value  ...  2018Q3_percentage
        營業活動之現金流量－間接法              NaN  ...                NaN
        繼續營業單位稅前淨利（淨損）     700890335.0  ...           0.744778
        ...                        ...  ...                ...
        持有供交易之金融資產（增加）減少           NaN  ...           0.001664
        負債準備增加（減少）                 NaN  ...                NaN

        "CASHI":
                                2023Q3_value  ...  2018Q3_percentage
        投資活動之現金流量                        NaN  ...                NaN
        取得透過其他綜合損益按公允價值衡量之金融資產   -54832622.0  ...           0.367413
        ...                              ...  ...                ...
        持有至到期日金融資產到期還本                   NaN  ...                NaN
        取得以成本衡量之金融資產                     NaN  ...                NaN

        "CASHF":
                        2023Q3_value  ...  2018Q3_percentage
        籌資活動之現金流量                      NaN  ...                NaN
        短期借款減少                         0.0  ...                NaN
        ...                            ...  ...                ...
        以成本衡量之金融資產減資退回股款               NaN  ...                NaN
        除列避險之金融負債∕避險 之衍生金融負債           NaN  ...           -0.00077
}
```
- `'ticker'`: 股票代碼
- `'company_name'`: 公司名稱 
- `'cash_flow'`: 歷年當季現金流量表"全表" 
- `'CASHO'`: 歷年當季營運活動之現金流量
- `'CASHI'`: 歷年當季投資活動之現金流量
- `'CASHF'`: 歷年當季籌資活動之現金流量

> 大部分資料缺失是因為尚未計算，僅先填上已經有的資料


## 版本紀錄
### 0.0.10
- 更新指標的資料型態: 單位為千元乘以1000之後回傳整數

- 處理銀行公司在finanace_overview會報錯誤的問題(未完全解決，因銀行公司財報有許多名稱不同，目前都會顯示為None)

### 0.0.9
- 更新指標的資料型態: 單位為日, %, 倍轉為字串