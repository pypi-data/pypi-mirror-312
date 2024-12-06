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
class bstack1ll1l1llll_opy_:
    def __init__(self, handler):
        self._1ll1l1llll1_opy_ = None
        self.handler = handler
        self._1ll1l1lllll_opy_ = self.bstack1ll1l1lll1l_opy_()
        self.patch()
    def patch(self):
        self._1ll1l1llll1_opy_ = self._1ll1l1lllll_opy_.execute
        self._1ll1l1lllll_opy_.execute = self.bstack1ll1l1lll11_opy_()
    def bstack1ll1l1lll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᙳ"), driver_command, None, this, args)
            response = self._1ll1l1llll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111l_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᙴ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1l1lllll_opy_.execute = self._1ll1l1llll1_opy_
    @staticmethod
    def bstack1ll1l1lll1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver