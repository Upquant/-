#!/usr/bin/env python# -*- coding: utf-8 -*-from etasdk import *import numpy as np'''#本示例演示双均线策略，股票池为上证50#策略逻辑：#1.当5日均线上穿60日均线，买入#2.当5日均线下穿60日均线，卖出回测标的：上证50回测周期：20180702-20181101撮合周期：日K'''long_period = 60short_period = 5coefficient = 0.06# 初始化def onInitialize(api):    # 设置计算MACD需要的历史K线，为日K，最多历史上30根    api.setRequireBars(ETimeSpan.DAY_1, long_period)    # 设置安组回调模式，超时时间为 10S    api.setGroupMode(10000)    # 设计模拟盘Timer函数的定时回调    api.setTimerCycle(60000)    # 设置股票池为沪深300    api.setSymbolPool(instsets=["000016.IDX"])# 盘前运行，必须实现，用来设置当日关注的标的def onBeforeMarketOpen(api, tradeDate):    # 取出股票池    symbolPool = api.getSymbolPool()    # 备选买入清单    buy_list = []    # 卖出清单    sell_list = []    # 遍历股票池，分别获取5和60 的K线    for i, symbol in enumerate(symbolPool):        bars = api.getBarsHistory(symbol, ETimeSpan.DAY_1, long_period, priceMode=EPriceMode.FORMER, df=True,                                  fields=['close'])        if len(bars) == long_period:            bar_close_long = bars[0:long_period]            bar_close_short = bars[long_period - short_period:long_period]            long_mean = np.mean(np.array(bar_close_long['close']))  # 计算60日均线            short_mean = np.mean(np.array(bar_close_short['close']))  # 计算5日均线            # print data , symbol,short_mean,long_mean ,"|",(short_mean - long_mean) ,coefficient* long_mean            # 如果            buy_flag = True if (short_mean - long_mean) > coefficient * long_mean else False            if buy_flag:                buy_list.append(symbol)            else:                sell_list.append(symbol)    # 关注当前的buy_list即可，因为如果有持仓会自动关注    api.setFocusSymbols(buy_list)    # 获取当前持仓的标的，如果需要卖出，则平仓    position_symbols = api.getPositionSymbols()    # 输出当前交易日    LOG.INFO("[%s] buy list = [%s]", tradeDate, buy_list)    LOG.INFO("[%s] position_symbols list = [%s]", tradeDate, position_symbols)    # 如果买入列表的标的没有仓位则买入    for i, buy_symbol in enumerate(buy_list):        if buy_symbol not in position_symbols:            LOG.INFO("[%s] target position long 1000![%s]", tradeDate, buy_symbol)            api.targetPosition(symbol=buy_symbol, qty=1000)    # 卖出有卖出信号的标的    for i, pos_symbol in enumerate(position_symbols):        if pos_symbol in sell_list:            LOG.INFO("[%s] target position short 0![%s]", tradeDate, pos_symbol)            api.targetPosition(symbol=pos_symbol, qty=0)# Bar回调def onHandleData(api, bar):    pass# 定时器，模拟盘响应def onTimer(api):    pass# 策略终止时响应def onTerminate(api, exitInfo):    LOG.INFO("***************onTerminate*********")