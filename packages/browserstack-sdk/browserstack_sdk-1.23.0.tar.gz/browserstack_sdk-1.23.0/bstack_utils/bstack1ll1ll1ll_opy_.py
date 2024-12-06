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
from collections import deque
from bstack_utils.constants import *
class bstack1l11l11ll1_opy_:
    def __init__(self):
        self._1lll11111ll_opy_ = deque()
        self._1lll1111l11_opy_ = {}
        self._1lll1111ll1_opy_ = False
    def bstack1lll1111l1l_opy_(self, test_name, bstack1lll111111l_opy_):
        bstack1lll111l11l_opy_ = self._1lll1111l11_opy_.get(test_name, {})
        return bstack1lll111l11l_opy_.get(bstack1lll111111l_opy_, 0)
    def bstack1lll1111lll_opy_(self, test_name, bstack1lll111111l_opy_):
        bstack1lll111lll1_opy_ = self.bstack1lll1111l1l_opy_(test_name, bstack1lll111111l_opy_)
        self.bstack1lll111l1l1_opy_(test_name, bstack1lll111111l_opy_)
        return bstack1lll111lll1_opy_
    def bstack1lll111l1l1_opy_(self, test_name, bstack1lll111111l_opy_):
        if test_name not in self._1lll1111l11_opy_:
            self._1lll1111l11_opy_[test_name] = {}
        bstack1lll111l11l_opy_ = self._1lll1111l11_opy_[test_name]
        bstack1lll111lll1_opy_ = bstack1lll111l11l_opy_.get(bstack1lll111111l_opy_, 0)
        bstack1lll111l11l_opy_[bstack1lll111111l_opy_] = bstack1lll111lll1_opy_ + 1
    def bstack11l1ll1l_opy_(self, bstack1lll111ll11_opy_, bstack1lll111l1ll_opy_):
        bstack1lll111ll1l_opy_ = self.bstack1lll1111lll_opy_(bstack1lll111ll11_opy_, bstack1lll111l1ll_opy_)
        event_name = bstack111l111ll1_opy_[bstack1lll111l1ll_opy_]
        bstack1lll11111l1_opy_ = bstack111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥᘙ").format(bstack1lll111ll11_opy_, event_name, bstack1lll111ll1l_opy_)
        self._1lll11111ll_opy_.append(bstack1lll11111l1_opy_)
    def bstack1l11l111ll_opy_(self):
        return len(self._1lll11111ll_opy_) == 0
    def bstack1ll11ll11_opy_(self):
        bstack1lll111l111_opy_ = self._1lll11111ll_opy_.popleft()
        return bstack1lll111l111_opy_
    def capturing(self):
        return self._1lll1111ll1_opy_
    def bstack1ll111111_opy_(self):
        self._1lll1111ll1_opy_ = True
    def bstack111l11l1l_opy_(self):
        self._1lll1111ll1_opy_ = False