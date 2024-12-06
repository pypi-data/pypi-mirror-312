# coding: UTF-8
import sys
bstack1111l1_opy_ = sys.version_info [0] == 2
bstack1l1l_opy_ = 2048
bstack11l1111_opy_ = 7
def bstack111l_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lllll_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1ll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack1l111l1_opy_ = bstack11lllll_opy_ % len (bstack1ll1_opy_)
    bstack1l1_opy_ = bstack1ll1_opy_ [:bstack1l111l1_opy_] + bstack1ll1_opy_ [bstack1l111l1_opy_:]
    if bstack1111l1_opy_:
        bstack1l111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l_opy_ - (bstack1llll1_opy_ + bstack11lllll_opy_) % bstack11l1111_opy_) for bstack1llll1_opy_, char in enumerate (bstack1l1_opy_)])
    else:
        bstack1l111l_opy_ = str () .join ([chr (ord (char) - bstack1l1l_opy_ - (bstack1llll1_opy_ + bstack11lllll_opy_) % bstack11l1111_opy_) for bstack1llll1_opy_, char in enumerate (bstack1l1_opy_)])
    return eval (bstack1l111l_opy_)
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1lll1ll111_opy_ as bstack1lll111ll_opy_
from browserstack_sdk.bstack1lll11ll1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11llllll1_opy_
class bstack1l1lllll11_opy_:
    def __init__(self, args, logger, bstack11l11111l1_opy_, bstack11l111llll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l11111l1_opy_ = bstack11l11111l1_opy_
        self.bstack11l111llll_opy_ = bstack11l111llll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l11l1111l_opy_ = []
        self.bstack11l1111l11_opy_ = None
        self.bstack11ll1l1l1_opy_ = []
        self.bstack11l11111ll_opy_ = self.bstack1lll1ll1_opy_()
        self.bstack1l1lll11l_opy_ = -1
    def bstack1l1l1ll11l_opy_(self, bstack11l111ll11_opy_):
        self.parse_args()
        self.bstack11l1111lll_opy_()
        self.bstack11l111l1l1_opy_(bstack11l111ll11_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11l1111111_opy_():
        import importlib
        if getattr(importlib, bstack111l_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨན"), False):
            bstack11l111lll1_opy_ = importlib.find_loader(bstack111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭པ"))
        else:
            bstack11l111lll1_opy_ = importlib.util.find_spec(bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧཕ"))
    def bstack11l1111ll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1lll11l_opy_ = -1
        if self.bstack11l111llll_opy_ and bstack111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭བ") in self.bstack11l11111l1_opy_:
            self.bstack1l1lll11l_opy_ = int(self.bstack11l11111l1_opy_[bstack111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧབྷ")])
        try:
            bstack11l111l1ll_opy_ = [bstack111l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪམ"), bstack111l_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬཙ"), bstack111l_opy_ (u"ࠪ࠱ࡵ࠭ཚ")]
            if self.bstack1l1lll11l_opy_ >= 0:
                bstack11l111l1ll_opy_.extend([bstack111l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬཛ"), bstack111l_opy_ (u"ࠬ࠳࡮ࠨཛྷ")])
            for arg in bstack11l111l1ll_opy_:
                self.bstack11l1111ll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11l1111lll_opy_(self):
        bstack11l1111l11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11l1111l11_opy_ = bstack11l1111l11_opy_
        return bstack11l1111l11_opy_
    def bstack1lll1ll1l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11l1111111_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11llllll1_opy_)
    def bstack11l111l1l1_opy_(self, bstack11l111ll11_opy_):
        bstack1l1ll1l111_opy_ = Config.bstack11llll1111_opy_()
        if bstack11l111ll11_opy_:
            self.bstack11l1111l11_opy_.append(bstack111l_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪཝ"))
            self.bstack11l1111l11_opy_.append(bstack111l_opy_ (u"ࠧࡕࡴࡸࡩࠬཞ"))
        if bstack1l1ll1l111_opy_.bstack11l111111l_opy_():
            self.bstack11l1111l11_opy_.append(bstack111l_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧཟ"))
            self.bstack11l1111l11_opy_.append(bstack111l_opy_ (u"ࠩࡗࡶࡺ࡫ࠧའ"))
        self.bstack11l1111l11_opy_.append(bstack111l_opy_ (u"ࠪ࠱ࡵ࠭ཡ"))
        self.bstack11l1111l11_opy_.append(bstack111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩར"))
        self.bstack11l1111l11_opy_.append(bstack111l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧལ"))
        self.bstack11l1111l11_opy_.append(bstack111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ཤ"))
        if self.bstack1l1lll11l_opy_ > 1:
            self.bstack11l1111l11_opy_.append(bstack111l_opy_ (u"ࠧ࠮ࡰࠪཥ"))
            self.bstack11l1111l11_opy_.append(str(self.bstack1l1lll11l_opy_))
    def bstack11l111ll1l_opy_(self):
        bstack11ll1l1l1_opy_ = []
        for spec in self.bstack1l11l1111l_opy_:
            bstack111l11lll_opy_ = [spec]
            bstack111l11lll_opy_ += self.bstack11l1111l11_opy_
            bstack11ll1l1l1_opy_.append(bstack111l11lll_opy_)
        self.bstack11ll1l1l1_opy_ = bstack11ll1l1l1_opy_
        return bstack11ll1l1l1_opy_
    def bstack1lll1ll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11l11111ll_opy_ = True
            return True
        except Exception as e:
            self.bstack11l11111ll_opy_ = False
        return self.bstack11l11111ll_opy_
    def bstack11lll11lll_opy_(self, bstack11l111l111_opy_, bstack1l1l1ll11l_opy_):
        bstack1l1l1ll11l_opy_[bstack111l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨས")] = self.bstack11l11111l1_opy_
        multiprocessing.set_start_method(bstack111l_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨཧ"))
        bstack1lll1l1l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lllllll1l_opy_ = manager.list()
        if bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ཨ") in self.bstack11l11111l1_opy_:
            for index, platform in enumerate(self.bstack11l11111l1_opy_[bstack111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧཀྵ")]):
                bstack1lll1l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11l111l111_opy_,
                                                            args=(self.bstack11l1111l11_opy_, bstack1l1l1ll11l_opy_, bstack1lllllll1l_opy_)))
            bstack11l111l11l_opy_ = len(self.bstack11l11111l1_opy_[bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཪ")])
        else:
            bstack1lll1l1l1_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11l111l111_opy_,
                                                        args=(self.bstack11l1111l11_opy_, bstack1l1l1ll11l_opy_, bstack1lllllll1l_opy_)))
            bstack11l111l11l_opy_ = 1
        i = 0
        for t in bstack1lll1l1l1_opy_:
            os.environ[bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ཫ")] = str(i)
            if bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪཬ") in self.bstack11l11111l1_opy_:
                os.environ[bstack111l_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ཭")] = json.dumps(self.bstack11l11111l1_opy_[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ཮")][i % bstack11l111l11l_opy_])
            i += 1
            t.start()
        for t in bstack1lll1l1l1_opy_:
            t.join()
        return list(bstack1lllllll1l_opy_)
    @staticmethod
    def bstack11l1111l_opy_(driver, bstack11l1111l1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ཯"), None)
        if item and getattr(item, bstack111l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭཰"), None) and not getattr(item, bstack111l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ཱࠧ"), False):
            logger.info(
                bstack111l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ིࠧ"))
            bstack111lllllll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1lll111ll_opy_.bstack1l11lllll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)