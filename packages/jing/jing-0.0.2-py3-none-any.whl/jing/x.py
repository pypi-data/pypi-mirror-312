#!/usr/bin/env python
# -*- encoding: utf8 -*-

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)

class X:
    def __init__(self, _market="cn", _date="", _code="", _rule="") -> None:
        self.market = _market
        self.date = _date
        self.rule = _rule
        self.dataCenter = util.Data()

        if len(_code) > 0:
            self.list = pd.DataFrame({'code':[_code]})
        else:
            self.list = self.dataCenter.list(market=_market)

    def run(self, _lookBack=0):
        for i, row in self.list.iterrows():
            code = row['code']
            print("--", code)
            self.runOne(code, _lookBack)

    def runOne(self, _code, _lookBack=0):
        self.one = self.dataCenter.one(_code, self.date, self.market)
        if len(self.one) < 400:
            logger.debug("[%s] -- bye", _code)
            return

        self.ref = util.Ref(self.one)
        self.rules(_code)

        for i in range(_lookBack):
            logger.debug('='*100)
            self.ref.df = self.ref.df.iloc[1:,]
            # logger.debug(self.ref.df.head(3))
            self.rules(_code)

    def rules(self, _code):
        r = Rule(_code, self.ref, self.rule)
        r.run()
        # r.ruleMa50Ma200()
        # logger.debug('-' * 100)
        # r.rulePriceBreakout()
        # logger.debug('-' * 100)

class Regression:
    def __init__(self) -> None:
        pass

    def breakoutList(self):
        rule = "priceBreakout"
        l = [
            ["2024-01-19", "SMCI", rule],
            ["2023-10-27", "DECK", rule],
            ["2023-11-30", "CRM", rule],
        ]
        return l

    def ma50Ma200List(self):
        rule = "ma50ma200"
        l = [
            [ "2023-10-30", "NFLX", rule],
            [ "2023-11-07", "CRM", rule ],
            [ "2024-01-10", "MDB", rule ],
            [ "2023-11-01", "AMD", rule ],
            [ "2023-11-02", "UBER", rule ],
        ]
        return l

    def volumeBreakoutList(self):
        rule = "volumeBreakout"
        l = [
            ["2023-05-24", "ANF", rule],
            ["2024-01-19", "SMCI", rule],
        ]
        return l

    def runOne(self, _list):
        for one in _list:
            dt   = one[0]
            code = one[1]
            rule = one[2]
            print(dt, code, rule)
            x = X("us", dt, code, rule)
            x.run()

    def run(self):
        l = self.breakoutList()
        self.runOne(l)

        l = self.ma50Ma200List()
        self.runOne(l)

        l = self.volumeBreakoutList()
        self.runOne(l)

class Rule:
    def __init__(self, _code, _ref, _ruleName) -> None:
        self.code = _code
        self.ref = _ref
        self.ruleName = _ruleName
        self.map = {
            "ma50ma200": self.ruleMa50Ma200,
            "priceBreakout": self.rulePriceBreakout,
            "volumeBreakout": self.ruleVolumeBreakout,
        }

    def run(self):
        if len(self.ruleName) == 0:
            logger.debug('=' * 100)
            for r, afunc in self.map.items():
                logger.debug('-' * 100)
                logger.debug("rule[%s]", r)
                afunc()
            return

        # rule is specified
        if self.ruleName not in self.map.keys():
            logger.error("rule [%s] does not exist", self.ruleName)
            return

        thefunc = self.map[self.ruleName]
        if not callable(thefunc):
            logger.error('error: [%s] not callable', self.ruleName)
            return

        logger.debug('=' * 100)
        thefunc()
        

    def ruleMa50Ma200(self):
        self.map['ma50ma200'] = self.ruleMa50Ma200
        code = self.code
        ref = self.ref
        dt = ref.date(0)

        logger.debug("[%s][%s] len: %d", code, dt, ref.len())

        # Rule1: break up ma50
        if ref.close(0) > ref.ma50(0) and ref.close(1) < ref.ma50(1):
            logger.info("[%s][%s] break up ma50, nice", code, dt)
            pass
        else:
            logger.debug("[%s][%s] not break up ma50, bye", code, dt)
            #logger.debug(ref.df.head(5))
            return

        # Rule2: ma200 ascending many days!
        trend = util.Trend()
        per, rate = trend.ascendPercentile(ref.Ma200())
        #logger.debug("[%s] ma200: per: %s, rate: %s", code, per, rate)
        if per >= 98 and rate > 20:
            logger.info("[%s][%s] ma200 asceding[%s, %s], nice", code, dt, per, rate)
            pass
        else:
            logger.debug("[%s][%s] ma200 not asceding[%s, %s], bye", code, dt, per, rate)
            return

        # Rule3: ma50 is always upper than ma200
        per, rate, start = trend.ascendCross(ref.Ma50(), ref.Ma200())
        #logger.debug("[%s] ma50 : per: %s, rate: %s, start: %s", code, per, rate, start)
        if per >= 98 and rate > 25:
            logger.info("[%s][%s] ma50 keeps upper[%s, %s], nice", code, dt, per, rate)
        else:
            logger.debug("[%s][%s] ma50 not keeps uppers[%s, %s], bye", code, dt, per, rate)
            return

        # Rule4: ma50 is not far away from ma200
        rate = 100 * (ref.ma50(0) / ref.ma200(0) - 1)
        #logger.debug("[%s] near: rate: %s", code, rate)
        # Rate:
        # - NFLX: 5.7%
        # - AMD: 5.7
        if rate > 2 and rate < 15:
            logger.info("[%s][%s] ma50 is near to ma200 [%s], nice", code, dt, rate)
        else:
            logger.debug("[%s][%s] ma50 is not near to ma200 [%s], bye", code, dt, rate)
            return

        # Rule5: close-price once is near to ma200
        n = 50
        minRate = trend.approach(ref.Close(), ref.Ma200(), n)
        if minRate < 10 and minRate > -10:
            logger.info("[%s][%s] close is near to ma200 [%s], nice", code, dt, minRate)
        else:
            logger.debug("[%s][%s] close is not near to ma200[%s], bye", code, dt, minRate)
            return

        logger.info("[%s][%s] ruleMa50Ma200 bingo", code, dt)

    # price breakout
    def rulePriceBreakout(self):
        code = self.code
        ref = self.ref
        dt = ref.date(0)

        logger.debug("[%s][%s] len: %d", code, dt, ref.len())

        # Rule0: rate & vr
        rate = 100 * (ref.close(0) / ref.close(1) - 1)
        vr   = ref.vol(0) / ref.vma50(0)
        if rate >= 9 and vr >= 4:
            logger.info("[%s][%s] rate[%s], vr[%s], nice", code, dt, rate, vr)
            pass
        else:
            logger.debug("[%s][%s] rate[%s], vr[%s] doesn't match, bye", code, dt, rate, vr)
            return

        trend = util.Trend()
        # Rule1: price breakout
        n = 200
        b = trend.breakout(ref.Close(), n)
        if b:
            logger.info("[%s][%s] breakout %d days, nice", code, dt, n)
            pass
        else:
            logger.debug("[%s][%s] not breakout", code, dt)
            return

        # Rule2: close is near to ma200
        n = 50
        near = trend.approach(ref.Close(), ref.Ma200(), n)
        if near < 20:
            logger.info("[%s][%s] approaching[%s], nice", code, dt, near)
        else:
            logger.debug("[%s][%s] approaching", code, dt)
            return

        # Rule3: ma200 ascending many days!
        trend = util.Trend()
        per, rate = trend.ascendPercentile(ref.Ma200())
        #logger.debug("[%s] ma200: per: %s, rate: %s", code, per, rate)
        if per >= 99 and rate > 20:
            logger.info("[%s][%s] ma200 asceding[%s, %s], nice", code, dt, per, rate)
            pass
        else:
            logger.debug("[%s][%s] ma200 not asceding[%s, %s], bye", code, dt, per, rate)
            return

        # Rule4: ma50 is always upper than ma200
        per, rate, start = trend.ascendCross(ref.Ma50(), ref.Ma200())
        #logger.debug("[%s] ma50 : per: %s, rate: %s, start: %s", code, per, rate, start)
        if per >= 99 and rate > 25:
            logger.info("[%s][%s] ma50 keeps upper[%s, %s], nice", code, dt, per, rate)
        else:
            logger.debug("[%s][%s] ma50 not keeps uppers[%s, %s], bye", code, dt, per, rate)
            return

        # Rule5: ma50 is not far away from ma200
        rate = 100 * (ref.ma50(0) / ref.ma200(0) - 1)
        if rate > 2 and rate < 20:
            logger.info("[%s][%s] ma50 is near to ma200 [%s], nice", code, dt, rate)
        else:
            logger.debug("[%s][%s] ma50 is not near to ma200 [%s], bye", code, dt, rate)
            return

        logger.info("[%s][%s] rulePriceBreakout bingo", code, dt)

    # volume breakout
    def ruleVolumeBreakout(self):
        code = self.code
        ref = self.ref
        dt = ref.date(0)

        logger.debug("[%s][%s] len: %d", code, dt, ref.len())

        # Rule1: rate & vr
        rate = 100 * (ref.close(0) / ref.close(1) - 1)
        vr   = ref.vol(0) / ref.vma50(0)
        if rate >= 30 and vr >= 6:
            logger.info("[%s][%s] rate[%s], vr[%s], nice", code, dt, rate, vr)
            pass
        else:
            logger.debug("[%s][%s] rate[%s], vr[%s] doesn't match, bye", code, dt, rate, vr)
            return

        trend = util.Trend()
        # Rule2: price breakout
        n = 50
        b = trend.breakout(ref.Close(), n)
        if b:
            logger.info("[%s][%s] breakout %d days, nice", code, dt, n)
            pass
        else:
            logger.debug("[%s][%s] not breakout", code, dt)
            return

        # Rule3: close was near to ma200
        n = 50
        near = trend.approach(ref.Close(), ref.Ma200(), n)
        if near < 20:
            logger.info("[%s][%s] approaching[%s], nice", code, dt, near)
        else:
            logger.debug("[%s][%s] approaching", code, dt)
            return

        # Rule3: ma200 ascending many days!
        trend = util.Trend()
        per, rate = trend.ascendPercentile(ref.Ma200(), 50)
        #logger.debug("[%s] ma200: per: %s, rate: %s", code, per, rate)
        if per >= 90 and rate > 5:
            logger.info("[%s][%s] ma200 asceding[%s, %s], nice", code, dt, per, rate)
            pass
        else:
            logger.debug("[%s][%s] ma200 not asceding[%s, %s], bye", code, dt, per, rate)
            return

        # Rule4: ma50 is always upper than ma200
        per, rate, start = trend.ascendCross(ref.Ma50(), ref.Ma200(), 100, 50)
        #logger.debug("[%s] ma50 : per: %s, rate: %s, start: %s", code, per, rate, start)
        if per >= 99 and rate > 5:
            logger.info("[%s][%s] ma50 keeps upper[%s, %s], nice", code, dt, per, rate)
        else:
            logger.debug("[%s][%s] ma50 not keeps uppers[%s, %s], bye", code, dt, per, rate)
            return

        # Rule5: ma50 is not far away from ma200
        rate = 100 * (ref.ma50(0) / ref.ma200(0) - 1)
        if rate > 2 and rate < 20:
            logger.info("[%s][%s] ma50 is near to ma200 [%s], nice", code, dt, rate)
        else:
            logger.debug("[%s][%s] ma50 is not near to ma200 [%s], bye", code, dt, rate)
            return

        logger.info("[%s][%s] ruleVolumeBreakout bingo", code, dt)


if __name__=="__main__":
    logger = util.initLogger("x.log")
    util.loggerStdout()
    logger.debug("hello, X")
    # x = X("us", "2023-10-30")

    # ma50 - ma200
    # x = X("us", "2023-10-30", "NFLX")
    # x = X("us", "2023-11-07", "CRM")
    # x = X("us", "2024-01-10", "MDB")
    # x = X("us", "2023-11-01", "AMD")
    # x = X("us", "2023-11-02", "UBER")
    # x = X("us", "2024-01-29", "CVNA") # fail
    # x = X("us", "2024-02-23", "CVNA")
    # x.run()

    # breakout
    # x = X("us", "2024-01-19", "SMCI") # breakout

    #x = X("us", "2024-01-21")
    #x.run(10)

    # r = Regression()
    # r.run()

    # x = X("us", "2023-05-24", "ANF", "volumeBreakout")
    # x = X("us", "2024-01-19", "SMCI", "volumeBreakout")
    # x.run()
    #x = X("us", "2024-02-16")

    x = X("us", "2024-05-25")
    x.run(5)

