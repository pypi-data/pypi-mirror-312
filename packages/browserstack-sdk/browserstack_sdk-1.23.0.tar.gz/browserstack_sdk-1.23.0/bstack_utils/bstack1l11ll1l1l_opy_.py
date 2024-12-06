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
import json
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack111lll1111_opy_, bstack111lll111l_opy_, bstack1111ll11l_opy_, bstack11l1lll111_opy_, bstack1lllll1l1ll_opy_, bstack1111l1llll_opy_, bstack11111l11ll_opy_, bstack1ll11l111l_opy_
from bstack_utils.bstack1ll1ll11111_opy_ import bstack1ll1ll1111l_opy_
import bstack_utils.bstack1l1l111l_opy_ as bstack1l1l1l11l_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack1lll1lllll_opy_
import bstack_utils.bstack1lll1ll111_opy_ as bstack1lll111ll_opy_
from bstack_utils.bstack111111l11_opy_ import bstack111111l11_opy_
from bstack_utils.bstack11ll111l1l_opy_ import bstack11l1l1l1ll_opy_
bstack1ll1l11111l_opy_ = bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᛨ")
logger = logging.getLogger(__name__)
class bstack11ll111ll_opy_:
    bstack1ll1ll11111_opy_ = None
    bs_config = None
    bstack1l1lll1l11_opy_ = None
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l1lll1l11_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1lll1l11_opy_ = bstack1l1lll1l11_opy_
        try:
            cls.bstack1ll11ll1l11_opy_()
            bstack111lll11l1_opy_ = bstack111lll1111_opy_(bs_config)
            bstack111lll11ll_opy_ = bstack111lll111l_opy_(bs_config)
            data = bstack1l1l1l11l_opy_.bstack1ll11ll1lll_opy_(bs_config, bstack1l1lll1l11_opy_)
            config = {
                bstack111l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᛩ"): (bstack111lll11l1_opy_, bstack111lll11ll_opy_),
                bstack111l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᛪ"): cls.default_headers()
            }
            response = bstack1111ll11l_opy_(bstack111l_opy_ (u"ࠨࡒࡒࡗ࡙࠭᛫"), cls.request_url(bstack111l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩ᛬")), data, config)
            if response.status_code != 200:
                bstack1ll11l1lll1_opy_ = response.json()
                if bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ᛭")] == False:
                    cls.bstack1ll11ll1l1l_opy_(bstack1ll11l1lll1_opy_)
                    return
                cls.bstack1ll11l1ll11_opy_(bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᛮ")])
                cls.bstack1ll1l1111l1_opy_(bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᛯ")])
                return None
            bstack1ll11lll1ll_opy_ = cls.bstack1ll11ll11ll_opy_(response)
            return bstack1ll11lll1ll_opy_
        except Exception as error:
            logger.error(bstack111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦᛰ").format(str(error)))
            return None
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def stop(cls, bstack1ll11ll1ll1_opy_=None):
        if not bstack1lll1lllll_opy_.on() and not bstack1lll111ll_opy_.on():
            return
        if os.environ.get(bstack111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᛱ")) == bstack111l_opy_ (u"ࠣࡰࡸࡰࡱࠨᛲ") or os.environ.get(bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᛳ")) == bstack111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᛴ"):
            logger.error(bstack111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᛵ"))
            return {
                bstack111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᛶ"): bstack111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᛷ"),
                bstack111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᛸ"): bstack111l_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭᛹")
            }
        try:
            cls.bstack1ll1ll11111_opy_.shutdown()
            data = {
                bstack111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᛺"): bstack1ll11l111l_opy_()
            }
            if not bstack1ll11ll1ll1_opy_ is None:
                data[bstack111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧ᛻")] = [{
                    bstack111l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ᛼"): bstack111l_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪ᛽"),
                    bstack111l_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭᛾"): bstack1ll11ll1ll1_opy_
                }]
            config = {
                bstack111l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ᛿"): cls.default_headers()
            }
            bstack1111lll1ll_opy_ = bstack111l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩᜀ").format(os.environ[bstack111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢᜁ")])
            bstack1ll11llll1l_opy_ = cls.request_url(bstack1111lll1ll_opy_)
            response = bstack1111ll11l_opy_(bstack111l_opy_ (u"ࠪࡔ࡚࡚ࠧᜂ"), bstack1ll11llll1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111l_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥᜃ"))
        except Exception as error:
            logger.error(bstack111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤᜄ") + str(error))
            return {
                bstack111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᜅ"): bstack111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᜆ"),
                bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᜇ"): str(error)
            }
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1ll11ll11ll_opy_(cls, response):
        bstack1ll11l1lll1_opy_ = response.json()
        bstack1ll11lll1ll_opy_ = {}
        if bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"ࠩ࡭ࡻࡹ࠭ᜈ")) is None:
            os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᜉ")] = bstack111l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᜊ")
        else:
            os.environ[bstack111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᜋ")] = bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"࠭ࡪࡸࡶࠪᜌ"), bstack111l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᜍ"))
        os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᜎ")] = bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᜏ"), bstack111l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᜐ"))
        if bstack1lll1lllll_opy_.bstack1ll11l1ll1l_opy_(cls.bs_config, cls.bstack1l1lll1l11_opy_.get(bstack111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬᜑ"), bstack111l_opy_ (u"ࠬ࠭ᜒ"))) is True:
            bstack1ll11ll111l_opy_, bstack11111111_opy_, bstack1ll1l111l11_opy_ = cls.bstack1ll11l1llll_opy_(bstack1ll11l1lll1_opy_)
            if bstack1ll11ll111l_opy_ != None and bstack11111111_opy_ != None:
                bstack1ll11lll1ll_opy_[bstack111l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᜓ")] = {
                    bstack111l_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰ᜔ࠪ"): bstack1ll11ll111l_opy_,
                    bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦ᜕ࠪ"): bstack11111111_opy_,
                    bstack111l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭᜖"): bstack1ll1l111l11_opy_
                }
            else:
                bstack1ll11lll1ll_opy_[bstack111l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᜗")] = {}
        else:
            bstack1ll11lll1ll_opy_[bstack111l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ᜘")] = {}
        if bstack1lll111ll_opy_.bstack111l1ll1ll_opy_(cls.bs_config) is True:
            bstack1ll11l11lll_opy_, bstack11111111_opy_ = cls.bstack1ll11llllll_opy_(bstack1ll11l1lll1_opy_)
            if bstack1ll11l11lll_opy_ != None and bstack11111111_opy_ != None:
                bstack1ll11lll1ll_opy_[bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᜙")] = {
                    bstack111l_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪ᜚"): bstack1ll11l11lll_opy_,
                    bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ᜛"): bstack11111111_opy_,
                }
            else:
                bstack1ll11lll1ll_opy_[bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᜜")] = {}
        else:
            bstack1ll11lll1ll_opy_[bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᜝")] = {}
        if bstack1ll11lll1ll_opy_[bstack111l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᜞")].get(bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᜟ")) != None or bstack1ll11lll1ll_opy_[bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᜠ")].get(bstack111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᜡ")) != None:
            cls.bstack1ll11llll11_opy_(bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"ࠧ࡫ࡹࡷࠫᜢ")), bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᜣ")))
        return bstack1ll11lll1ll_opy_
    @classmethod
    def bstack1ll11l1llll_opy_(cls, bstack1ll11l1lll1_opy_):
        if bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᜤ")) == None:
            cls.bstack1ll11l1ll11_opy_()
            return [None, None, None]
        if bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᜥ")][bstack111l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᜦ")] != True:
            cls.bstack1ll11l1ll11_opy_(bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᜧ")])
            return [None, None, None]
        logger.debug(bstack111l_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᜨ"))
        os.environ[bstack111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᜩ")] = bstack111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᜪ")
        if bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"ࠩ࡭ࡻࡹ࠭ᜫ")):
            os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᜬ")] = bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠫ࡯ࡽࡴࠨᜭ")]
            os.environ[bstack111l_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᜮ")] = json.dumps({
                bstack111l_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᜯ"): bstack111lll1111_opy_(cls.bs_config),
                bstack111l_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᜰ"): bstack111lll111l_opy_(cls.bs_config)
            })
        if bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᜱ")):
            os.environ[bstack111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᜲ")] = bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᜳ")]
        if bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ᜴ࠫ")].get(bstack111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭᜵"), {}).get(bstack111l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ᜶")):
            os.environ[bstack111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ᜷")] = str(bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᜸")][bstack111l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ᜹")][bstack111l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ᜺")])
        return [bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠫ࡯ࡽࡴࠨ᜻")], bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ᜼")], os.environ[bstack111l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ᜽")]]
    @classmethod
    def bstack1ll11llllll_opy_(cls, bstack1ll11l1lll1_opy_):
        if bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᜾")) == None:
            cls.bstack1ll1l1111l1_opy_()
            return [None, None]
        if bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᜿")][bstack111l_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᝀ")] != True:
            cls.bstack1ll1l1111l1_opy_(bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᝁ")])
            return [None, None]
        if bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᝂ")].get(bstack111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᝃ")):
            logger.debug(bstack111l_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᝄ"))
            parsed = json.loads(os.getenv(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᝅ"), bstack111l_opy_ (u"ࠨࡽࢀࠫᝆ")))
            capabilities = bstack1l1l1l11l_opy_.bstack1ll11lll1l1_opy_(bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᝇ")][bstack111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᝈ")][bstack111l_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᝉ")], bstack111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᝊ"), bstack111l_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᝋ"))
            bstack1ll11l11lll_opy_ = capabilities[bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᝌ")]
            os.environ[bstack111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᝍ")] = bstack1ll11l11lll_opy_
            parsed[bstack111l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᝎ")] = capabilities[bstack111l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᝏ")]
            os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᝐ")] = json.dumps(parsed)
            scripts = bstack1l1l1l11l_opy_.bstack1ll11lll1l1_opy_(bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᝑ")][bstack111l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᝒ")][bstack111l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᝓ")], bstack111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭᝔"), bstack111l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࠪ᝕"))
            bstack111111l11_opy_.bstack111llll1l1_opy_(scripts)
            commands = bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᝖")][bstack111l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ᝗")][bstack111l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵ࠭᝘")].get(bstack111l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᝙"))
            bstack111111l11_opy_.bstack111ll11111_opy_(commands)
            bstack111111l11_opy_.store()
        return [bstack1ll11l11lll_opy_, bstack1ll11l1lll1_opy_[bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ᝚")]]
    @classmethod
    def bstack1ll11l1ll11_opy_(cls, response=None):
        os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᝛")] = bstack111l_opy_ (u"ࠩࡱࡹࡱࡲࠧ᝜")
        os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ᝝")] = bstack111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ᝞")
        os.environ[bstack111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᝟")] = bstack111l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᝠ")
        os.environ[bstack111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᝡ")] = bstack111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᝢ")
        os.environ[bstack111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᝣ")] = bstack111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᝤ")
        os.environ[bstack111l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᝥ")] = bstack111l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᝦ")
        cls.bstack1ll11ll1l1l_opy_(response, bstack111l_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨᝧ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1111l1_opy_(cls, response=None):
        os.environ[bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᝨ")] = bstack111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᝩ")
        os.environ[bstack111l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᝪ")] = bstack111l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᝫ")
        os.environ[bstack111l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᝬ")] = bstack111l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ᝭")
        cls.bstack1ll11ll1l1l_opy_(response, bstack111l_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᝮ"))
        return [None, None, None]
    @classmethod
    def bstack1ll11llll11_opy_(cls, bstack1ll11lll11l_opy_, bstack11111111_opy_):
        os.environ[bstack111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᝯ")] = bstack1ll11lll11l_opy_
        os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᝰ")] = bstack11111111_opy_
    @classmethod
    def bstack1ll11ll1l1l_opy_(cls, response=None, product=bstack111l_opy_ (u"ࠤࠥ᝱")):
        if response == None:
            logger.error(product + bstack111l_opy_ (u"ࠥࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠧᝲ"))
        for error in response[bstack111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᝳ")]:
            bstack111111l11l_opy_ = error[bstack111l_opy_ (u"ࠬࡱࡥࡺࠩ᝴")]
            error_message = error[bstack111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᝵")]
            if error_message:
                if bstack111111l11l_opy_ == bstack111l_opy_ (u"ࠢࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉࠨ᝶"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111l_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࠤ᝷") + product + bstack111l_opy_ (u"ࠤࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢ᝸"))
    @classmethod
    def bstack1ll11ll1l11_opy_(cls):
        if cls.bstack1ll1ll11111_opy_ is not None:
            return
        cls.bstack1ll1ll11111_opy_ = bstack1ll1ll1111l_opy_(cls.bstack1ll11ll1111_opy_)
        cls.bstack1ll1ll11111_opy_.start()
    @classmethod
    def bstack11l1l1ll11_opy_(cls):
        if cls.bstack1ll1ll11111_opy_ is None:
            return
        cls.bstack1ll1ll11111_opy_.shutdown()
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1ll11ll1111_opy_(cls, bstack11l1ll11l1_opy_, bstack1ll1l1111ll_opy_=bstack111l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ᝹")):
        config = {
            bstack111l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ᝺"): cls.default_headers()
        }
        response = bstack1111ll11l_opy_(bstack111l_opy_ (u"ࠬࡖࡏࡔࡖࠪ᝻"), cls.request_url(bstack1ll1l1111ll_opy_), bstack11l1ll11l1_opy_, config)
        bstack111l1lll11_opy_ = response.json()
    @classmethod
    def bstack11l1l11111_opy_(cls, bstack11l1ll11l1_opy_, bstack1ll1l1111ll_opy_=bstack111l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ᝼")):
        if not bstack1l1l1l11l_opy_.bstack1ll11lll111_opy_(bstack11l1ll11l1_opy_[bstack111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ᝽")]):
            return
        bstack1ll11lll1_opy_ = bstack1l1l1l11l_opy_.bstack1ll1l111111_opy_(bstack11l1ll11l1_opy_[bstack111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᝾")], bstack11l1ll11l1_opy_.get(bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ᝿")))
        if bstack1ll11lll1_opy_ != None:
            if bstack11l1ll11l1_opy_.get(bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬក")) != None:
                bstack11l1ll11l1_opy_[bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ខ")][bstack111l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪគ")] = bstack1ll11lll1_opy_
            else:
                bstack11l1ll11l1_opy_[bstack111l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫឃ")] = bstack1ll11lll1_opy_
        if bstack1ll1l1111ll_opy_ == bstack111l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ង"):
            cls.bstack1ll11ll1l11_opy_()
            cls.bstack1ll1ll11111_opy_.add(bstack11l1ll11l1_opy_)
        elif bstack1ll1l1111ll_opy_ == bstack111l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ច"):
            cls.bstack1ll11ll1111_opy_([bstack11l1ll11l1_opy_], bstack1ll1l1111ll_opy_)
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack11l11l1l1_opy_(cls, bstack11l11llll1_opy_):
        bstack1ll11l1l11l_opy_ = []
        for log in bstack11l11llll1_opy_:
            bstack1ll11lllll1_opy_ = {
                bstack111l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧឆ"): bstack111l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬជ"),
                bstack111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪឈ"): log[bstack111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫញ")],
                bstack111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩដ"): log[bstack111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪឋ")],
                bstack111l_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨឌ"): {},
                bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪឍ"): log[bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫណ")],
            }
            if bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫត") in log:
                bstack1ll11lllll1_opy_[bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬថ")] = log[bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ទ")]
            elif bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧធ") in log:
                bstack1ll11lllll1_opy_[bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨន")] = log[bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩប")]
            bstack1ll11l1l11l_opy_.append(bstack1ll11lllll1_opy_)
        cls.bstack11l1l11111_opy_({
            bstack111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧផ"): bstack111l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨព"),
            bstack111l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪភ"): bstack1ll11l1l11l_opy_
        })
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1ll11l11ll1_opy_(cls, steps):
        bstack1ll11l1l1ll_opy_ = []
        for step in steps:
            bstack1ll11l1l111_opy_ = {
                bstack111l_opy_ (u"࠭࡫ࡪࡰࡧࠫម"): bstack111l_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪយ"),
                bstack111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧរ"): step[bstack111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨល")],
                bstack111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭វ"): step[bstack111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧឝ")],
                bstack111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ឞ"): step[bstack111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧស")],
                bstack111l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩហ"): step[bstack111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪឡ")]
            }
            if bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩអ") in step:
                bstack1ll11l1l111_opy_[bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪឣ")] = step[bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫឤ")]
            elif bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬឥ") in step:
                bstack1ll11l1l111_opy_[bstack111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ឦ")] = step[bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧឧ")]
            bstack1ll11l1l1ll_opy_.append(bstack1ll11l1l111_opy_)
        cls.bstack11l1l11111_opy_({
            bstack111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬឨ"): bstack111l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ឩ"),
            bstack111l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨឪ"): bstack1ll11l1l1ll_opy_
        })
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1lll11ll_opy_(cls, screenshot):
        cls.bstack11l1l11111_opy_({
            bstack111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨឫ"): bstack111l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩឬ"),
            bstack111l_opy_ (u"࠭࡬ࡰࡩࡶࠫឭ"): [{
                bstack111l_opy_ (u"ࠧ࡬࡫ࡱࡨࠬឮ"): bstack111l_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪឯ"),
                bstack111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬឰ"): datetime.datetime.utcnow().isoformat() + bstack111l_opy_ (u"ࠪ࡞ࠬឱ"),
                bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬឲ"): screenshot[bstack111l_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫឳ")],
                bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭឴"): screenshot[bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ឵")]
            }]
        }, bstack1ll1l1111ll_opy_=bstack111l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ា"))
    @classmethod
    @bstack11l1lll111_opy_(class_method=True)
    def bstack1l111l1l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1l11111_opy_({
            bstack111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ិ"): bstack111l_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧី"),
            bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ឹ"): {
                bstack111l_opy_ (u"ࠧࡻࡵࡪࡦࠥឺ"): cls.current_test_uuid(),
                bstack111l_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧុ"): cls.bstack11ll111ll1_opy_(driver)
            }
        })
    @classmethod
    def bstack11ll111lll_opy_(cls, event: str, bstack11l1ll11l1_opy_: bstack11l1l1l1ll_opy_):
        bstack11l11lllll_opy_ = {
            bstack111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫូ"): event,
            bstack11l1ll11l1_opy_.bstack11l11l1111_opy_(): bstack11l1ll11l1_opy_.bstack11l1ll1lll_opy_(event)
        }
        cls.bstack11l1l11111_opy_(bstack11l11lllll_opy_)
        result = getattr(bstack11l1ll11l1_opy_, bstack111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨួ"), None)
        if event == bstack111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪើ"):
            threading.current_thread().bstackTestMeta = {bstack111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪឿ"): bstack111l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬៀ")}
        elif event == bstack111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧេ"):
            threading.current_thread().bstackTestMeta = {bstack111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ែ"): getattr(result, bstack111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧៃ"), bstack111l_opy_ (u"ࠨࠩោ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪៅ"), None) is None or os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫំ")] == bstack111l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤះ")) and (os.environ.get(bstack111l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪៈ"), None) is None or os.environ[bstack111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ៉")] == bstack111l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ៊")):
            return False
        return True
    @staticmethod
    def bstack1ll11l1l1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11ll111ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack111l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ់"): bstack111l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ៌"),
            bstack111l_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭៍"): bstack111l_opy_ (u"ࠫࡹࡸࡵࡦࠩ៎")
        }
        if os.environ.get(bstack111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭៏"), None):
            headers[bstack111l_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭័")] = bstack111l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ៑").format(os.environ[bstack111l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ្")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack111l_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ៓").format(bstack1ll1l11111l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ។"), None)
    @staticmethod
    def bstack11ll111ll1_opy_(driver):
        return {
            bstack1lllll1l1ll_opy_(): bstack1111l1llll_opy_(driver)
        }
    @staticmethod
    def bstack1ll11ll11l1_opy_(exception_info, report):
        return [{bstack111l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ៕"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111lllll11_opy_(typename):
        if bstack111l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ៖") in typename:
            return bstack111l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢៗ")
        return bstack111l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ៘")