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
from browserstack_sdk.bstack11111lll1_opy_ import bstack1l1lllll11_opy_
from browserstack_sdk.bstack11l11l1l11_opy_ import RobotHandler
def bstack11l11ll1_opy_(framework):
    if framework.lower() == bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬጰ"):
        return bstack1l1lllll11_opy_.version()
    elif framework.lower() == bstack111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬጱ"):
        return RobotHandler.version()
    elif framework.lower() == bstack111l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧጲ"):
        import behave
        return behave.__version__
    else:
        return bstack111l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩጳ")