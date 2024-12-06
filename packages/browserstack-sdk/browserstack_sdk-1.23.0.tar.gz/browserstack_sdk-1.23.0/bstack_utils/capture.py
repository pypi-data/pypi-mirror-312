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
import builtins
import logging
class bstack11ll111l11_opy_:
    def __init__(self, handler):
        self._111l1l111l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111l1l11ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack111l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ၂"), bstack111l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫ၃"), bstack111l_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧ၄"), bstack111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭၅")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111l1l11l1_opy_
        self._111l11llll_opy_()
    def _111l1l11l1_opy_(self, *args, **kwargs):
        self._111l1l111l_opy_(*args, **kwargs)
        message = bstack111l_opy_ (u"ࠨࠢࠪ၆").join(map(str, args)) + bstack111l_opy_ (u"ࠩ࡟ࡲࠬ၇")
        self._log_message(bstack111l_opy_ (u"ࠪࡍࡓࡌࡏࠨ၈"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ၉"): level, bstack111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭၊"): msg})
    def _111l11llll_opy_(self):
        for level, bstack111l1l1111_opy_ in self._111l1l11ll_opy_.items():
            setattr(logging, level, self._111l1l1l11_opy_(level, bstack111l1l1111_opy_))
    def _111l1l1l11_opy_(self, level, bstack111l1l1111_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111l1l1111_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111l1l111l_opy_
        for level, bstack111l1l1111_opy_ in self._111l1l11ll_opy_.items():
            setattr(logging, level, bstack111l1l1111_opy_)