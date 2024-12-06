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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11l11111l1_opy_, bstack11l111llll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l11111l1_opy_ = bstack11l11111l1_opy_
        self.bstack11l111llll_opy_ = bstack11l111llll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l1l1lll1_opy_(bstack111lllll1l_opy_):
        bstack111llll1ll_opy_ = []
        if bstack111lllll1l_opy_:
            tokens = str(os.path.basename(bstack111lllll1l_opy_)).split(bstack111l_opy_ (u"ࠢࡠࠤཱི"))
            camelcase_name = bstack111l_opy_ (u"ུࠣࠢࠥ").join(t.title() for t in tokens)
            suite_name, bstack111llllll1_opy_ = os.path.splitext(camelcase_name)
            bstack111llll1ll_opy_.append(suite_name)
        return bstack111llll1ll_opy_
    @staticmethod
    def bstack111lllll11_opy_(typename):
        if bstack111l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲཱུࠧ") in typename:
            return bstack111l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦྲྀ")
        return bstack111l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧཷ")