#!/usr/bin/env python# -*- coding: utf-8 -*-from etasdk import *'''股票策略：买卖策略本策略是一个简单的买卖策略，主要是体现如何下单的。当没有持仓时就进行买入操作，当有持仓时，就进行卖出平仓操作回测标的：平安银行（000001.CS）回测周期：20180702-20181101撮合周期：日K更多详情请看帮助文档：http://quant.upchina.com/doc/first.html'''# 必要 ：整个回测/模拟/实盘前要做的操作def onInitialize(api):    # 必要：设置标的池，支持多级别的选择，提高数据缓存效率    api.setSymbolPool(symbols=["000001.CS"])    # 更多示例    # api.setSymbolPool(instsets=["000300.IDX","000016.IDX"])   #设置标的池沪深300和上证50的并集    # api.setSymbolPool(instsets=["CS.SET"])    #设置标的池为股票全部    # api.setSymbolPool(symbols=["IFZ0.CF"])    #设置标的池为IF的主力合约    # api.setSymbolPool(instsets=["IFZ0.CF"])   #设置标的池为IF的主力合约对应的标准合约    # 非必要：设计模拟盘Timer函数的定时回调，回测环境下无效，不调用默认为5000毫秒    api.setTimerCycle(60000)# 必要：每个交易日回测/模拟/实盘前要做的操作def onBeforeMarketOpen(api, trade_date):    # 必要：获取当个交易日需关注的股票    # 设置今天关注的股票，如果股票池中只有一只股票，则全部关注即可；股票池中股票过多时，需要先选股在设置部分关注以提高运行效率    symbolPool = api.getSymbolPool()    # 必要：关注股票，为后续相应行情onBar、onHandleData或者onTick等函数做准备    api.setFocusSymbols(symbolPool)# 必要：每天回测/交易 策略 两种方式回调  onbar/onHandleData# 用日K做回测，所以每天只会进入一次，收盘时响应此函数# 策略逻辑：第一天买入，第二天卖出；判断逻辑，如果当前有仓位，则平仓，如果当前没有仓位，则买入def onBar(api, bar):    symbolposition = api.getSymbolPosition(bar.symbol)     # 获取持仓标的信息    if symbolposition.posQty > 0:  # 如果持仓数大于0        # 平仓        LOG.INFO("target position zero!")  # 非必要： 输出日志        api.targetPosition(symbol=bar.symbol, qty=0)  # 卖出 ，symbol = 选中标的，数量变为0    else:        # 市价下单1000股        LOG.INFO("target position 1000!")  # 非必要： 输出日志        api.targetPosition(symbol=bar.symbol, qty=1000)  # 买入 symbol = 选中标的，直至持仓数达1000股# 定时器，模拟盘响应；回测时可忽略def onTimer(api):    pass# 策略终止时响应；运行终止时会调用一次,exitInfo返回值为终止消息def onTerminate(api, exitInfo):    LOG.INFO("***************onTerminate*********") # 输出日志