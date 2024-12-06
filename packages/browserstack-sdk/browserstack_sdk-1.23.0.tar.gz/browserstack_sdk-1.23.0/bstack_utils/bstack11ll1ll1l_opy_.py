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
import logging
import os
import threading
from bstack_utils.helper import bstack111lll11l_opy_
from bstack_utils.constants import bstack1111lllll1_opy_
logger = logging.getLogger(__name__)
class bstack1lll1lllll_opy_:
    bstack1ll1ll11111_opy_ = None
    @classmethod
    def bstack1lll1ll1ll_opy_(cls):
        if cls.on():
            logger.info(
                bstack111l_opy_ (u"ࠧࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠪ᠗").format(os.environ[bstack111l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢ᠘")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪ᠙"), None) is None or os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫ᠚")] == bstack111l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ᠛"):
            return False
        return True
    @classmethod
    def bstack1ll111llll1_opy_(cls, bs_config, framework=bstack111l_opy_ (u"ࠧࠨ᠜")):
        if bstack111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭᠝") in framework:
            return bstack111lll11l_opy_(bs_config.get(bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ᠞")))
        bstack1ll111l1lll_opy_ = False
        for fw in bstack1111lllll1_opy_:
            if fw in framework:
                bstack1ll111l1lll_opy_ = True
        return bstack111lll11l_opy_(bs_config.get(bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᠟"), bstack1ll111l1lll_opy_))
    @classmethod
    def bstack1ll111ll111_opy_(cls, framework):
        return framework in bstack1111lllll1_opy_
    @classmethod
    def bstack1ll11l1ll1l_opy_(cls, bs_config, framework):
        return cls.bstack1ll111llll1_opy_(bs_config, framework) is True and cls.bstack1ll111ll111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᠠ"), None)
    @staticmethod
    def bstack11ll1l1111_opy_():
        if getattr(threading.current_thread(), bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᠡ"), None):
            return {
                bstack111l_opy_ (u"ࠫࡹࡿࡰࡦࠩᠢ"): bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࠪᠣ"),
                bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᠤ"): getattr(threading.current_thread(), bstack111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᠥ"), None)
            }
        if getattr(threading.current_thread(), bstack111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᠦ"), None):
            return {
                bstack111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᠧ"): bstack111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᠨ"),
                bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᠩ"): getattr(threading.current_thread(), bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᠪ"), None)
            }
        return None
    @staticmethod
    def bstack1ll111ll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll1lllll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1l1lll1_opy_(test, hook_name=None):
        bstack1ll111l1ll1_opy_ = test.parent
        if hook_name in [bstack111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᠫ"), bstack111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᠬ"), bstack111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᠭ"), bstack111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᠮ")]:
            bstack1ll111l1ll1_opy_ = test
        scope = []
        while bstack1ll111l1ll1_opy_ is not None:
            scope.append(bstack1ll111l1ll1_opy_.name)
            bstack1ll111l1ll1_opy_ = bstack1ll111l1ll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll111ll1l1_opy_(hook_type):
        if hook_type == bstack111l_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣᠯ"):
            return bstack111l_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣᠰ")
        elif hook_type == bstack111l_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤᠱ"):
            return bstack111l_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨᠲ")
    @staticmethod
    def bstack1ll111l1l1l_opy_(bstack1l11l1111l_opy_):
        try:
            if not bstack1lll1lllll_opy_.on():
                return bstack1l11l1111l_opy_
            if os.environ.get(bstack111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧᠳ"), None) == bstack111l_opy_ (u"ࠣࡶࡵࡹࡪࠨᠴ"):
                tests = os.environ.get(bstack111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨᠵ"), None)
                if tests is None or tests == bstack111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᠶ"):
                    return bstack1l11l1111l_opy_
                bstack1l11l1111l_opy_ = tests.split(bstack111l_opy_ (u"ࠫ࠱࠭ᠷ"))
                return bstack1l11l1111l_opy_
        except Exception as exc:
            print(bstack111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨᠸ"), str(exc))
        return bstack1l11l1111l_opy_