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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll1l11l11_opy_ = {}
        bstack11ll1lll11_opy_ = os.environ.get(bstack111l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ณ"), bstack111l_opy_ (u"࠭ࠧด"))
        if not bstack11ll1lll11_opy_:
            return bstack1ll1l11l11_opy_
        try:
            bstack11ll1ll1ll_opy_ = json.loads(bstack11ll1lll11_opy_)
            if bstack111l_opy_ (u"ࠢࡰࡵࠥต") in bstack11ll1ll1ll_opy_:
                bstack1ll1l11l11_opy_[bstack111l_opy_ (u"ࠣࡱࡶࠦถ")] = bstack11ll1ll1ll_opy_[bstack111l_opy_ (u"ࠤࡲࡷࠧท")]
            if bstack111l_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢธ") in bstack11ll1ll1ll_opy_ or bstack111l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢน") in bstack11ll1ll1ll_opy_:
                bstack1ll1l11l11_opy_[bstack111l_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣบ")] = bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥป"), bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥผ")))
            if bstack111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤฝ") in bstack11ll1ll1ll_opy_ or bstack111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢพ") in bstack11ll1ll1ll_opy_:
                bstack1ll1l11l11_opy_[bstack111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣฟ")] = bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧภ"), bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥม")))
            if bstack111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣย") in bstack11ll1ll1ll_opy_ or bstack111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣร") in bstack11ll1ll1ll_opy_:
                bstack1ll1l11l11_opy_[bstack111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤฤ")] = bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦล"), bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦฦ")))
            if bstack111l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦว") in bstack11ll1ll1ll_opy_ or bstack111l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤศ") in bstack11ll1ll1ll_opy_:
                bstack1ll1l11l11_opy_[bstack111l_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥษ")] = bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢส"), bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧห")))
            if bstack111l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦฬ") in bstack11ll1ll1ll_opy_ or bstack111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤอ") in bstack11ll1ll1ll_opy_:
                bstack1ll1l11l11_opy_[bstack111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥฮ")] = bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢฯ"), bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧะ")))
            if bstack111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥั") in bstack11ll1ll1ll_opy_ or bstack111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥา") in bstack11ll1ll1ll_opy_:
                bstack1ll1l11l11_opy_[bstack111l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦำ")] = bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨิ"), bstack11ll1ll1ll_opy_.get(bstack111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨี")))
            if bstack111l_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢึ") in bstack11ll1ll1ll_opy_:
                bstack1ll1l11l11_opy_[bstack111l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣื")] = bstack11ll1ll1ll_opy_[bstack111l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤุ")]
        except Exception as error:
            logger.error(bstack111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ูࠦࠢ") +  str(error))
        return bstack1ll1l11l11_opy_