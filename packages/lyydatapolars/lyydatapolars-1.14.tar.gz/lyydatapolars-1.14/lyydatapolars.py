import polars as pl
from datetime import datetime, timedelta
from tqdm import tqdm
import sys
import traceback
import lyybinary
import os
import pandas as pd
import time
import csv
from pytdx.params import TDXParams

import lyytools
import lyystkcode
import lyywmdf
import lyyztreason
from lyylog2 import log
import lyycfg
import lyyliutongz


pl.Config.set_tbl_rows(40)  # 设置显示行数为100
pl.Config.set_tbl_cols(20)   # 设置显示列数为10

api_dict = {}
signal_id_dict = {"昨日换手": 777, "昨日回头波": 776}  # ,"涨停原因":888
column_mapping = {"时间": "datetime", "代码": "code", "名称": "name", "开盘": "open", "今开": "open", "收盘": "close", "最新价": "close", "最高": "high", "最低": "low", "涨跌幅": "change_rate", "涨跌额": "change_amount", "成交量": "vol", "成交额": "amount", "振幅": "amplitude", "换手率": "turnover_rate"}

tdx_path = r"D:\Soft\_Stock\通达信金融终端(开心果交易版)V2024.09"

kline_type = {"5min":0,"15min":1,"30min":2,"60min":3,"day2":4,"week":5,"month":6,"1min":7,"1mink":8,"day":9,"season":10,"year":11}



def get_dict_all_code_guben():
    df_all_cache_file = r"D:\UserData\resource\data\df_all_info.pkl"
    df_all_info = pd.read_pickle(df_all_cache_file)
    dict_all_code_guben = df_all_info.set_index("code")["流通股本亿"].to_dict()
    return dict_all_code_guben


def update_cg_series(df, debug=False):
    """
    更新通达信chonggao二进制文件
    """
    if debug: print(f"     [update_cg_series] enter, len={len(df)} df = ",df)


    assert len(df) > 10000, "[update_cg_series] dataframe<1000 line，check it"

    df_grouped = df.group_by("code")

    for code, group_rows in df_grouped:
        code = code[0] if isinstance(code, tuple) else code
        market = lyystkcode.get_market(code)
        if debug: print(f"        [update_cg_series] code = [{code}], market = [{market}]")
        tdx_signal_file = os.path.join(tdx_path, rf"T0002\signals\signals_user_{999}", f"{market}_{code}.dat")

        db_last_date_int = lyybinary.get_lastdate_tdx_singnal(code, tdx_signal_file)
        if debug: print("     [update_cg_series] db_last_date_int=", db_last_date_int, "then try to filter new data")
        filtered_rows = group_rows.filter(pl.col("dayint") > db_last_date_int)
        
        if len(filtered_rows) == 0:
            if debug: print("     [update_cg_series] no new data, continue")
            continue
        else:
            data_dict = filtered_rows.select(["dayint", "chonggao"]).to_dict(as_series=False)
            if debug: print("     [update_cg_series] chonggao data_dict  at first=", data_dict)
            data_dict = dict(zip(data_dict["dayint"], data_dict["chonggao"]))
            if debug: print("     [update_cg_series] chonggao data_dict =", data_dict)

            if debug: print(tdx_signal_file, db_last_date_int, "db_last_date_int type=", type(db_last_date_int))

            lyybinary.add_data_if_new_than_local(tdx_signal_file, data_dict, db_last_date_int, debug=debug)

            if debug: print("       [update_cg_series] 写入文件成功")



def get_ztreason_df(debug=False):
    lyycfg.cfg.get_engine_conn()
    query = """SELECT * FROM (SELECT *,ROW_NUMBER() OVER (PARTITION BY code ORDER BY date DESC) AS rn FROM stock_jiucai WHERE date >= DATE_SUB(CURDATE(), INTERVAL 20 DAY)) AS subquery WHERE rn = 1 """
    result = pl.read_database(query, lyycfg.cfg.engine)
    if debug: print("[get_ztreason_df] 准备生成pl dataframe")
    result = result.with_columns([
        pl.col("code").cast(pl.Utf8).str.zfill(6),
        pl.lit(888).cast(pl.Int64).alias("signal_id"),
        pl.lit(0.000).alias("number"),
        (pl.col("plate_name").cast(pl.Utf8) + "：" + pl.col("reason").cast(pl.Utf8).str.replace("\n", "")).alias("text"),
        pl.col("code").map_elements(lyystkcode.get_market).alias("market")
    ])
    if debug: print("[get_ztreason_df] 准备生成选取列并返回,df.columns", result.columns) #df.columns ['id', 'date', 'code', 'name', 'plate_id', 'plate_name', 'plate_reason', 'reason', 'rn', 'signal_id', 'number', 'text', 'market']

    return_df = result.select(["market", "code", "signal_id", "text", "number"])
    if debug:
        print(return_df)
    return return_df



def add_liangbi_columns(df: pl.DataFrame, liutongdict, if_debug=False):
    """
    根据原有的成交量列和 liutongdict，添加“量比”和“昨量比”两列。
    参数：
    - df: 未分组的 DataFrame，包含至少以下列：'code', 'date', 'volume'
    - liutongdict: 字典，每个代码对应一个包含流通股数 'lt' 的字典
    返回：
    - 一个新的 DataFrame，包含原始数据和新增的 '量比' 和 '昨量比' 列
    """
    # 检查必要的列
    required_columns = ['code', 'date', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"DataFrame 中缺少必要的列：'{col}'")
    
    # 将 liutongdict 转换为 DataFrame，并合并到 df 中
    liutong_df = pl.DataFrame(
        {
            'code': list(liutongdict.keys()),
            'lt': [float(liutongdict[code]['lt']) for code in liutongdict]
        }
    )

    if if_debug:
        print("==========="*4)
        print("[add_liangbi_columns] df=", df)
        print("------------"*4)
        print("[add_liangbi_columns] liutong_df=", liutong_df)
        print("==========="*4)

    df = df.join(liutong_df, on='code', how='left')
    
    # 检查 'lt' 列是否有缺失值
    if df['lt'].null_count() > 0:
        missing_codes = df.filter(pl.col('lt').is_null())['code'].unique()
        raise ValueError(f"存在以下代码在 liutongdict 中没有对应的 'lt' 值：{missing_codes}")
    
    # 转换 'date' 列为日期类型（如果尚未转换）
    if df['date'].dtype != pl.Date:
        df = df.with_columns(pl.col('date').str.strptime(pl.Date, "%Y-%m-%d"))
    
    # 排序 DataFrame
    df = df.sort(['code', 'date'])
    if if_debug:
        print("[add_liangbi_columns] df.columns=", df.columns)
        print("接下来打印df")
        print(df)
        print("df打印完毕")
        d = {c: t for c, t in zip(df.columns, df.dtypes)}
        print("columns type dict:", d)

    # 计算 '量比' 和 '昨量比'
    df = df.with_columns([
        (pl.col('volume') / pl.col('lt')).alias('量比'),
        (pl.col('volume') / pl.col('lt')).shift(1).over('code').alias('昨量比')
    ])
    
    # 删除临时列（如有需要）
    if 'lt' in df.columns:
        df = df.drop('lt')
    
    return df

def get_limit_up_rate( stock_code, stock_name=None):

    code_left2 = stock_code[:2]

    if code_left2 == '60' or code_left2 == '00':    #判断是否主板
        if stock_name is not None and "st" in stock_name.lower(): #用方法1 判断是否包含 'ST'
            zt = 5.0
        elif stock_name is None and stock_code in lyyliutongz.st_list:  #用方法2 判断是否包含 'ST'
            zt = 5.0
        else:
            zt = 10.0
    elif code_left2 == '30' or code_left2 == '68':
        zt = 20.0
    elif code_left2 == "92" or code_left2 == "43" or code_left2 == "87" or code_left2 == "83" :
        zt = 30.0
    else:
        raise ValueError(f"[get_limit_up_rate] 股票代码不符合规则, code={stock_code}, name={stock_name}")
    return zt




def update_signal_txt(df, liutong_dict, debug=False):
    def gbk_encode_decode(s):
        return pl.Series(s.to_numpy().astype(str).tobytes().decode('utf-8').encode('gbk', errors='ignore').decode('gbk'))
    if debug:
        print("enter [update_signal_txt], input para len=", len(df))

    #df = df.with_columns([ pl.col("volume").shift(1).over("code").rolling_mean(window_size=5).alias("avg_volume_5d").round(0)])
    #df = df.with_columns([ (pl.col("volume") / pl.col("avg_volume_5d")).alias("volume_ratio").round(1)])
    #df = df.with_columns([ pl.struct(["code", "name"]).map_elements(lambda row: get_limit_up_rate(row["code"], row["name"]) , return_dtype=pl.Float64).alias("limit_up_rate")])
    

    #除以0.03的意思是，冲高达到3分之一涨停板幅度。这个为什么不是3而是0.03，主要是有些是使用百分数，而涨停板幅度用的小数。

    """
    df = df.with_row_count("row_number")

    filtered_df = df.filter(pl.col("code") == "000001")

    print("filtered_df.columns=", filtered_df)

    filtered_df = df.filter(    (pl.col("row_number") >= 313980) & (pl.col("row_number") <= 313990))    
    print("filtered_df.columns=", filtered_df)

    time.sleep(33333)
    """
    if debug: print("<><><><><><><><><>"*5)
    if debug: print("[update_signal_txt] df.columns=", df.columns)

    
    grouped_df = df.group_by("code").agg([
        pl.col("volume").last().round(0),
        pl.col("huitoubo").last().round(2),
        pl.col("chonggao").last().round(2),
        pl.col("chonggao_times").last(),

        pl.col("dayint").last(),
        pl.col("volume_ratio").last().round(1),

    ])


    df_reason = get_ztreason_df()
    if debug:
        print("apply code 666 to grouped_df")
        print(grouped_df.head(100), "----------------here is grouped df---------------")
    
    pbar = tqdm(range(len(grouped_df)), desc="update_chonggao_huitoubo_for_signal_txt")

    signal_data_list = []
    for row in grouped_df.iter_rows(named=True):
        pbar.update(1)

        code = row["code"]
        chonggao_times = row["chonggao_times"]
        market = lyystkcode.get_market(code)
        float_shares = float(liutong_dict[code]["lt"])*100 #流通股本
        turn_over = round(row["volume"]/float_shares,1) #换手率       
        huitoubo = row["huitoubo"]
        chonggao = round(row["chonggao"],2)
        量倍数 = round(row["volume_ratio"],1)

        zuoliangbi_dict = {            "market": market,            "code": code,            "signal_id": 661,            "text": "",            "number": 量倍数        }
        huitoubo_dict = {            "market": market,            "code": code,            "signal_id": 662,            "text": "",            "number": huitoubo        }
        turn_over_dict = {            "market": market,            "code": code,            "signal_id": 663,            "text": "",            "number": turn_over        }
        chonggao_dict = {            "market": market,            "code": code,            "signal_id": 664,            "text": "",            "number": chonggao        }        
        chonggao_times_dict = {            "market": market,            "code": code,            "signal_id": 665,            "text": "",            "number": chonggao_times        }        

        signal_data_list.extend([zuoliangbi_dict, huitoubo_dict, turn_over_dict, chonggao_dict, chonggao_times_dict])

        if debug: print("row=", row)


    df_merged = pl.concat([pl.DataFrame(signal_data_list), df_reason],  how="vertical").sort("signal_id")


    if debug:
        print("df_merged.columns=", df_merged.columns)
        print("df_merged=\n", df_merged)
    if debug:
        print("contact finished. Try to filter no gbk code")

    path = os.path.join(tdx_path, r"T0002/signals/extern_user.txt")
    write_pl_df_to_gbk_csv(df_merged, path)
    if debug:
        print("执行完成！df_merged=\n", df_merged)
    return df_merged

def write_pl_df_to_gbk_csv(df, file_path):
    with open(file_path, 'w', encoding='gbk', newline='') as f:
        writer = csv.writer(f, delimiter='|')        
        for row in df.rows():
            encoded_row = []
            for value in row:
                if isinstance(value, str):
                    # 对于字符串，我们需要确保它可以被 GBK 编码
                    try:
                        value.encode('gbk')
                    except UnicodeEncodeError:
                        value = value.encode('gbk', errors='ignore').decode('gbk')  # 如果无法编码，可以选择替换或忽略
                encoded_row.append(value)
            writer.writerow(encoded_row)
    print(f"文件已保存到: {file_path}")

def df_add_notfull(df, haveto_date, debug=False):
    now = datetime.now()
    today_date_int = now.year * 10000 + now.month * 100 + now.day
    
    df = df.with_columns([
        pl.col("day").str.replace("-", "").cast(pl.Int32).alias("dayint"),
        pl.lit(15).alias("notfull")
    ])
    
    if df["dayint"].max() == today_date_int and now.hour < 15:
        if debug:
            print(f"今天没收盘，要重点标记一下。today_time_hour={now.hour}, today_date_int={today_date_int}")
        df = df.with_columns(
            pl.when(pl.col("dayint") == today_date_int)
            .then(now.hour)
            .otherwise(pl.col("notfull"))
            .alias("notfull")
        )
    else:
        if debug:
            print("in df_add_notfull, 完美收盘无需牵挂", end="")
    return df

def convert_dict(item, code):
    new_dict = dict(item)
    new_dict['date'] = datetime.strptime(new_dict['date'], '%Y-%m-%d %H:%M')
    
    return new_dict


def 分钟线合成日K(df) -> pl.DataFrame:
    print("[分钟线合成日K] enter")
    所有分钟线 = df.clone()
    完美日K线 = 所有分钟线.groupby_dynamic("datetime", every="1d").agg([
        pl.col("open").first().alias("open"),
        pl.col("high").max().alias("high"),
        pl.col("low").min().alias("low"),
        pl.col("close").last().alias("close"),
        pl.col("volume").sum().alias("volume")
    ]).drop_nulls()

    完美日K线 = 完美日K线.with_columns(pl.col("datetime").dt.date())
    print("[分钟线合成日K] done")

    return 完美日K线

def 分钟线5合15(所有分钟线) -> pl.DataFrame:
    print("[分钟线5合15] enter")

    多分钟K线 = 所有分钟线.groupby_dynamic("day", every="30min").agg([
        pl.col("open").first().alias("open"),
        pl.col("high").max().alias("high"),
        pl.col("low").min().alias("low"),
        pl.col("close").last().alias("close"),
        pl.col("volume").sum().alias("volume"),
        pl.col("high").max().alias("tenmax")

    ])
    
    #.drop_nulls()
    daily_df = daily_df.with_columns(((pl.col('tenmax') / pl.col('close').shift(1) - 1) * 100).alias('chonggao'))
    
    多分钟K线 = 多分钟K线.with_columns([
        pl.col("day").dt.strftime("%H%M").alias("time"),
        pl.col("day").dt.date().alias("day")
    ])
    
    十点K线 = 多分钟K线.filter(pl.col("time") == "1000").select(["time", "day", "high"])
    print("[分钟线5合15] done")

    return 十点K线

def 多周期K线合并(完美日K线, 十点K线, debug=False) -> pl.DataFrame:
    多周期合成K线 = 完美日K线.join(十点K线[["day", "tenhigh"]], on="day")
    
    # 注意：这里的 MyTT.REF 需要替换为 Polars 的等效操作
    多周期合成K线 = 多周期合成K线.with_columns([
        ((pl.col("high") / pl.col("close").shift(1) - 1) * 100).round(2).alias("up"),
        ((pl.col("tenhigh") / pl.col("close").shift(1) - 1) * 100).round(2).alias("chonggao"),
        ((1 - pl.col("close") / pl.col("high")) * 100).round(2).alias("huitoubo")
    ])
    
    if debug:
        print("多周期合成K线=", 多周期合成K线.select("chonggao"))
    
    return 多周期合成K线


def get_and_format_wmdf_for_single_code(code, api, db_last_date_int, kline_n, debug=False):
    if debug: print(f"[get_and_format_wmdf_for_single_code] enter {code}, {api}, {db_last_date_int}, {kline_n}")
    
    try:
        wmdf_data = wmdf(api, code, kline_n, debug=debug)
        print(wmdf_data)
        assert wmdf_data is not None and not wmdf_data.is_empty(), "[assert] wmdf_data is None or empty"
        if debug:print("               [单代码Df], wmdf_data= ",wmdf_data)
    except Exception as e:
        print(f"               [get_and_format_wmdf_for_single_code]wmdf error: {e}")
        traceback.print_exc()

    wmdf_data = wmdf_data.with_columns(pl.lit(code).alias("code"))
    
    if debug: print(f"               [单代码Df]in function get_and_format_wmdf_for_single_code,{code} wmdf = \n", wmdf_data)
    #dayint列不需要所以注释掉。
    wmdf_data = wmdf_data.with_columns( pl.col('date').dt.strftime("%Y%m%d").cast(pl.Int32).alias('dayint') )    
    wmdf_data = wmdf_data.slice(1) #多取一行用于计算一些字段，然后删除
    
    if debug: print(               "[单代码Df]",wmdf_data.columns)    
    filtered_df = wmdf_data.filter(pl.col("date").dt.strftime("%Y%m%d").cast(pl.Int32) > db_last_date_int)
    return filtered_df


def get_new_wmdf_data(last_date_dict, code_api_dict, debug=False):
    """
    获取全部要更新的数据并格式化
    
    """
    
    df_to_concat_list = []
    code_name_dict = lyystkcode.get_code_name_dict()
    assert len(code_name_dict)>5000, "[get_new_wmdf_data] 代码和名称表少于5000条"

    pbar = tqdm(total=len(code_api_dict), desc="update wmdf closed")

    if debug: print("enter fun: lyydata.update_wmdf_closed")

    assert code_api_dict is not None and len(code_api_dict)>5000, "[assert] last_date_dict is None"

    for index, (code, api) in enumerate(code_api_dict.items()):
        pbar.update(1)
        db_last_date_int, 相差天数, kline_n = lyywmdf.calc_lastdate_kline_number(code, last_date_dict, debug=debug)
        assert db_last_date_int is not None, "[assert] db_last_date_int is None"
        assert 相差天数 is not None, "[assert] 相差天数 is None"
        assert kline_n is not None, "[assert] kline_n is None"

        if 相差天数 == 0:
            if debug:
                print("新", end="")
            continue

        if debug: print(f"code/type={code} {type(code)}, server_ip={api.ip}, dblast_date/type={db_last_date_int} {type(db_last_date_int)}, 相差天数={相差天数}, kline_n={kline_n}")
        if code is None or api is None or kline_n is None or db_last_date_int is None:
            print("code/api/kline_n/db_last_date_int is None, continue")
            continue

        df_single = get_and_format_wmdf_for_single_code(code, api, db_last_date_int, kline_n, debug=debug)
        assert df_single is not None or not df_single.is_empty(), "[assert] after get_and_format_wmdf_for_single_code, df_single is None or empty"
        df_single = df_single.with_columns(pl.lit(code_name_dict.get(code, "")).alias("name"))
        log("dfsingle=",df_single)
        if debug: print(df_single, "df_single")

        if debug: print(f"finish code={code}")
        if not df_single.is_empty():
            if debug: print("add df_single to df list")
            df_to_concat_list.append(df_single)
            if debug: print("finish add df_single to df list")
        else:
            if debug: log(f"{code}@{api.ip} df_single is empty")
    print("finish for loop")
        #wmdf_data = df_add_notfull(wmdf_data, today_date_int)





    #先把新下载的所有股票的数据合并，统一格式化，再统一添加到wmdf_closed中
    wmdf_new_all_codes = pl.concat(df_to_concat_list)


    # 获取当前时间
    current_hour = datetime.now().hour
    # 判断是否超过15点
    hour_value = 15 if current_hour >= 15 else current_hour
    # 修改 DataFrame
    wmdf_new_all_codes = wmdf_new_all_codes.with_columns(pl.lit(hour_value).alias('notfull'))
    wmdf_new_all_codes = wmdf_new_all_codes.with_columns( ((pl.col('high') - pl.col('close')) / pl.col('high') * 100).alias('huitoubo'))    

    wmdf_closed = pl.concat([wmdf_closed, wmdf_new_all_codes])


    pbar.close()
    if debug:
        print("return wmdf_closed")
    return wmdf_closed





def 通达信下载原始分钟K线(api, code_str, 要下载的K线数量, ktype='15min', start_index=0, debug=False) -> pl.DataFrame:
    """
    api.get_security_bars(self, category, market, code, start, count)
    """
    fun_name = sys._getframe().f_code.co_name
    t0 = datetime.now()
    if debug:
        print("函数名：", fun_name)
    
    市场代码 = lyystkcode.get_market(code_str)
    if debug: print(f"[通达信下载原始分钟K线] 市场代码={市场代码}，code_str={code_str},klinetype={kline_type[ktype]},要下载的K线数量={要下载的K线数量}")
    
    assert api is not None, "[assert] api is None"
    assert code_str is not None and code_str.isdigit(), "[assert] code_str is None"
    assert 市场代码 is not None and isinstance(市场代码, int) , "[assert] 市场代码 is None"
    assert 要下载的K线数量 is not None and 要下载的K线数量 > 0, "[assert] 要下载的K线数量 is None"
    assert ktype in kline_type.keys() and kline_type[ktype] >= 0, f"[assert] ktype={ktype} not in kline_type.keys()"
    assert start_index is not None and start_index >= 0, "[assert] start_index is None"
    
    # 限制单次下载的K线数量为800
    max_download = 800
    current_download = min(要下载的K线数量, max_download)
    
    if debug: print("[通达信下载原始分钟K线] kline_type=",kline_type[ktype], "market=",市场代码,"code_str=", code_str, "start_index=", start_index, "to_down=",current_download)
    
    if code_str == "830779":
        from pytdx.hq import TdxHq_API
        api = TdxHq_API()
        if api.connect('58.63.254.152', 7709):
            print("api.connect success")
            ordered_dict_data_list = api.get_security_bars(kline_type[ktype], 市场代码, code_str, start=start_index, count=current_download)
    else:    
        try:
            ordered_dict_data_list = api.get_security_bars(kline_type[ktype], 市场代码, code_str, start=start_index, count=current_download)
        except Exception as e:
            print(f"[通达信下载原始分钟K线] api.get_security_bars下载失败，code_str={code_str}, 市场代码={市场代码}, ktype={ktype}, start_index={start_index}, 要下载的K线数量={要下载的K线数量}, 异常信息：{e}")
            traceback.print_exc()
            return None
    print(f"[通达信下载原始分钟K线] ordered_dict_data_list={ordered_dict_data_list}")
    assert ordered_dict_data_list is not None and len(ordered_dict_data_list) > 0, "[assert] ordered_dict_data_list is None或者为空"
    if debug: print("[通达信下载原始分钟K线] 通达信获取到orderedDict，长度为",len(ordered_dict_data_list))

    df = pl.DataFrame(ordered_dict_data_list)
    if debug: print("[通达信下载原始分钟K线] v[lyydatapolars][通达信下载原始分钟K线]df=",df)
    
    df = df.with_columns([pl.col("datetime").str.to_datetime().alias("datetime"),pl.lit(code_str).alias("code")    ])

    # 如果还有更多数据需要下载
    if 要下载的K线数量 > max_download:
        remaining_klines = 要下载的K线数量 - max_download
        new_start_index = start_index + max_download
        
        # 递归调用以获取剩余的数据
        remaining_df = 通达信下载原始分钟K线(api, code_str, remaining_klines, ktype, new_start_index, debug)
        
        # 合并数据框
        df = pl.concat([df, remaining_df])

    if debug: print(f"[通达信下载原始分钟K线] {code_str}转换结束，df=<<<<<<<<<<", df,">>>>>>>>>>")
    assert df is not None and not df.is_empty(), "[通达信下载原始分钟K线] [assert] df is None or empty"
    return df

    """
    ┌───────┬───────┬───────┬───────┬──────────┬──────────────┬──────┬───────┬─────┬──────┬────────┬─────────────────────┬────────┐
    │ open  ┆ close ┆ high  ┆ low   ┆ vol      ┆ amount       ┆ year ┆ month ┆ day ┆ hour ┆ minute ┆ datetime            ┆ code   │
    │ ---   ┆ ---   ┆ ---   ┆ ---   ┆ ---      ┆ ---          ┆ ---  ┆ ---   ┆ --- ┆ ---  ┆ ---    ┆ ---                 ┆ ---    │
    │ f64   ┆ f64   ┆ f64   ┆ f64   ┆ f64      ┆ f64          ┆ i64  ┆ i64   ┆ i64 ┆ i64  ┆ i64    ┆ datetime[μs]        ┆ str    │
    ╞═══════╪═══════╪═══════╪═══════╪══════════╪══════════════╪══════╪═══════╪═════╪══════╪════════╪═════════════════════╪════════╡
    │ 33.36 ┆ 53.38 ┆ 53.38 ┆ 33.33 ┆ 1.6834e7 ┆ 6.52135552e8 ┆ 2024 ┆ 10    ┆ 11  ┆ 9    ┆ 45     ┆ 2024-10-11 09:45:00 ┆ 920019 │
    │ 53.38 ┆ 39.49 ┆ 55.55 ┆ 38.0  ┆ 7.118e6  ┆ 3.2936608e8  ┆ 2024 ┆ 10    ┆ 11  ┆ 10   ┆ 0      ┆ 2024-10-11 10:00:00 ┆ 920019 │
    │ 39.99 ┆ 41.49 ┆ 43.36 ┆ 39.0  ┆ 3.7078e6 ┆ 1.52029744e8 ┆ 2024 ┆ 10    ┆ 11  ┆ 10   ┆ 15     ┆ 2024-10-11 10:15:00 ┆ 920019 │
    │ 41.48 ┆ 38.63 ┆ 41.8  ┆ 38.5  ┆ 1.8737e6 ┆ 7.5719752e7  ┆ 2024 ┆ 10    ┆ 11  ┆ 10   ┆ 30     ┆ 2024-10-11 10:30:00 ┆ 920019 │
    │ 38.65 ┆ 42.44 ┆ 42.44 ┆ 38.65 ┆ 1.1459e6 ┆ 4.6079968e7  ┆ 2024 ┆ 10    ┆ 11  ┆ 10   ┆ 45     ┆ 2024-10-11 10:45:00 ┆ 920019 │
    │ …     ┆ …     ┆ …     ┆ …     ┆ …        ┆ …            ┆ …    ┆ …     ┆ …   ┆ …    ┆ …      ┆ …                   ┆ …      │
    │ 31.82 ┆ 31.99 ┆ 32.0  ┆ 31.6  ┆ 707900.0 ┆ 2.2508304e7  ┆ 2024 ┆ 10    ┆ 18  ┆ 14   ┆ 0      ┆ 2024-10-18 14:00:00 ┆ 920019 │
    │ 32.0  ┆ 31.68 ┆ 32.32 ┆ 31.6  ┆ 611700.0 ┆ 1.9473248e7  ┆ 2024 ┆ 10    ┆ 18  ┆ 14   ┆ 15     ┆ 2024-10-18 14:15:00 ┆ 920019 │
    │ 31.67 ┆ 31.66 ┆ 32.11 ┆ 31.3  ┆ 952700.0 ┆ 3.0152796e7  ┆ 2024 ┆ 10    ┆ 18  ┆ 14   ┆ 30     ┆ 2024-10-18 14:30:00 ┆ 920019 │
    │ 31.61 ┆ 30.51 ┆ 31.61 ┆ 30.5  ┆ 2.1979e6 ┆ 6.81242e7    ┆ 2024 ┆ 10    ┆ 18  ┆ 14   ┆ 45     ┆ 2024-10-18 14:45:00 ┆ 920019 │
    │ 30.51 ┆ 28.4  ┆ 30.51 ┆ 28.33 ┆ 3.0761e6 ┆ 9.0351896e7  ┆ 2024 ┆ 10    ┆ 18  ┆ 15   ┆ 0      ┆ 2024-10-18 15:00:00 ┆ 920019 │
    """



def 原始分钟df格式化(df, debug=False):

    if debug: print("[原始分钟df格式化]# 然后，我们创建日线数据，包括 chonggao")
    print(df)
    daily_df_0 = df.group_by(pl.col('datetime').dt.date().alias('date')).agg([
        pl.col('open').first().alias('open'),
        pl.col('high').max().alias('high'),
        pl.col('low').min().alias('low'),
        pl.col('close').last().alias('close'),
        pl.col('vol').sum().round(2).alias('volume'),
        pl.col('amount').sum().round(2).alias('amount'),
        pl.col('high').filter(
        (pl.col('datetime').dt.hour() < 10) |
        ((pl.col('datetime').dt.hour() == 10) & (pl.col('datetime').dt.minute() < 1))
    ).max().alias('tenmax')
    ])

    # 添加 'huitoubo' 列
    daily_df_0 = daily_df_0.with_columns( ((pl.col('high') / pl.col('close') - 1) * 100).round(2).alias('huitoubo') )
    if debug: print("daily_df_0=",daily_df_0)
    print("以datetime排序");
    daily_df = daily_df_0.sort('date')


    print("daily_df=",daily_df)

    #daily_df = daily_df.with_columns(pl.col('close').shift(1) .alias('refclose'))


    #daily_df = daily_df.with_columns(((pl.col('tenmax') / pl.col('close').shift(1) ) ).alias('trup'))

    daily_df = daily_df.with_columns(((pl.col('tenmax') / pl.col('close').shift(1) - 1) * 100).round(2).alias('chonggao'))

    if debug: print("[原始分钟df格式化]# # 确保 'date' 列是日期类型")
    daily_df = daily_df.with_columns([
        pl.col('date').cast(pl.Date)
    ])

    assert daily_df is not None and not daily_df.is_empty(), "[assert] daily_df is None or empty"
    assert set(daily_df.columns) == set(['date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'tenmax', 'chonggao', 'huitoubo']), "[assert] daily_df.columns is not correct, daily_df.columns="+str(daily_df.columns)+", should be ['date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'tenmax','chonggao']"
    if debug: print("[原始分钟df格式化]# # 完成日线数据创建 all done")
    if debug: print("daily_df=",daily_df.tail(3))
    return daily_df


def wmdf_get_and_format_for_single_code(api, stk_code_num, to_down_kline, server_ip=None, debug=False) -> pl.DataFrame:
    """
    通达信下载原始分钟K线，并转换为 Polars DataFrame wmdf格式。
    """
    if debug: print(f"函数名：{sys._getframe().f_code.co_name}: try to get wmdf")
    t0 = datetime.now()
    if debug:            print(f"准备开始下载原始K线，IP={api.ip}")
    
    
    df = 通达信下载原始分钟K线(api, stk_code_num, to_down_kline, debug=debug)
    if debug:print("通太下载成功，df=",df)
    assert df is not None and not df.is_empty(), "[assert] df is None or empty"

    time = datetime.now() - t0
    if time > timedelta(seconds=0.5):
        print(f"通达信下载原始K线下载时间过长,IP={api.ip} {time}")
        
    
    #    (f"[lyydatapolars] [wmdf], try to run 通达信下载原始分钟线 error。stk_code_num: {stk_code_num}, to_down_kline: {to_down_kline}, api: {api}, errorMsg = {e}")
    
    if debug:
        lyytools.测速(t0, "通达信下载原始K线")
    t1 = datetime.now()
    if debug: print(f"======================上原始下格式{len(df)}=================================================")
    if debug: print("=========小心准备格式化=========")
    print("<<<<<<<<<<<<<<<<<<<<<<",df,">>>>>>>>>>>>>>>>>>>>>>")

    wmdf = 原始分钟df格式化(df, debug=debug)
    print("**********************",wmdf,"%%%%%%%%%%%%%%%%%%%%%%%%%")

    if debug:print("=========格式化完毕=========wmdf=",wmdf)

    """
        ┌────────────┬───────┬────────┬───────┬────────┬───────────┬──────────┬──────────┐
        │ date       ┆ open  ┆ high   ┆ low   ┆ close  ┆ volume    ┆ amount   ┆ chonggao │
        │ date       ┆ f64   ┆ f64    ┆ f64   ┆ f64    ┆ f64       ┆ f64      ┆ f64      │
        ╞════════════╪═══════╪════════╪═══════╪════════╪═══════════╪══════════╪══════════╡
        │ 2024-10-11 ┆ 87.12 ┆ 245.0  ┆ 87.12 ┆ 178.01 ┆ 3.19155e7 ┆ 4.7085e9 ┆ 245.0    │
        │ 2024-10-14 ┆ 101.0 ┆ 155.9  ┆ 101.0 ┆ 109.95 ┆ 2.13822e7 ┆ 2.5199e9 ┆ 155.9    │
        │ 2024-10-15 ┆ 105.0 ┆ 115.44 ┆ 92.07 ┆ 96.73  ┆ 1.88241e7 ┆ 1.9225e9 ┆ 115.44   │
[wmdf_get_and_format_for_single_code][assert] line 642, wmdf.columns is not correct, current=('date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'tenmax', 'huitoubo', 'chonggao')

    """

    
    if debug:
        lyytools.测速(t1, "df格式转换")

    assert set(wmdf.columns) == {'date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'tenmax', 'huitoubo', 'chonggao'}, "[wmdf_get_and_format_for_single_code][assert] line 642, wmdf.columns is not correct, current="+str(tuple(wmdf.columns) )
    #assert len(wmdf)>2, "[wmdf][assert] wmdf.len < 2"    

    return wmdf





if __name__ == "__main__":
    # 初始化模拟环境
    api = MockAPI("127.0.0.1")
    code = "000001"
    code_api_dict = {code: api}

    # 创建初始的 wmdf_closed
    initial_data = {
        "code": [code],
        "dayint": [20230101],
        "open": [15.0],
        "high": [16.0],
        "low": [14.0],
        "close": [15.5],
        "volume": [5000],
        "name": ["示例股票"]
    }
    wmdf_closed = pl.DataFrame(initial_data)

    # 运行更新函数
    updated_wmdf = update_wmdf_closed(wmdf_closed, code_api_dict, debug=True)

    # 打印结果
    print("Updated WMDF:")
    print(updated_wmdf)

    # 显示统计信息
    print("\nStatistics:")
    print(updated_wmdf.describe())

    # 显示最新的几条记录
    print("\nLatest records:")
    print(updated_wmdf.tail(5))


