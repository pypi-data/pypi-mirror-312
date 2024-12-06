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
import threading
import logging
import bstack_utils.bstack1lll1ll111_opy_ as bstack1lll111ll_opy_
from bstack_utils.helper import bstack1l1llll1l_opy_
logger = logging.getLogger(__name__)
def bstack111l1llll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1l1l1ll11_opy_(context, *args):
    tags = getattr(args[0], bstack111l_opy_ (u"ࠩࡷࡥ࡬ࡹ္ࠧ"), [])
    bstack1l1l1111l1_opy_ = bstack1lll111ll_opy_.bstack1111lll11_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1l1111l1_opy_
    try:
      bstack11ll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1llll_opy_(bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳ်ࠩ")) else context.browser
      if bstack11ll1lllll_opy_ and bstack11ll1lllll_opy_.session_id and bstack1l1l1111l1_opy_ and bstack1l1llll1l_opy_(
              threading.current_thread(), bstack111l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪျ"), None):
          threading.current_thread().isA11yTest = bstack1lll111ll_opy_.bstack1lll111111_opy_(bstack11ll1lllll_opy_, bstack1l1l1111l1_opy_)
    except Exception as e:
       logger.debug(bstack111l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬြ").format(str(e)))
def bstack1111lll1l_opy_(bstack11ll1lllll_opy_):
    if bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪွ"), None) and bstack1l1llll1l_opy_(
      threading.current_thread(), bstack111l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ှ"), None) and not bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫဿ"), False):
      threading.current_thread().a11y_stop = True
      bstack1lll111ll_opy_.bstack1l11lllll_opy_(bstack11ll1lllll_opy_, name=bstack111l_opy_ (u"ࠤࠥ၀"), path=bstack111l_opy_ (u"ࠥࠦ၁"))