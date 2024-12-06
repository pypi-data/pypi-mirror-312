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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack1llllll1l11_opy_, bstack11l1lllll_opy_, bstack1l1llll1l_opy_, bstack11llll1l1_opy_, \
    bstack1lllll1ll11_opy_
def bstack111lllll_opy_(bstack1ll1l1ll11l_opy_):
    for driver in bstack1ll1l1ll11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111111ll_opy_(driver, status, reason=bstack111l_opy_ (u"ࠩࠪᙵ")):
    bstack1l1ll1l111_opy_ = Config.bstack11llll1111_opy_()
    if bstack1l1ll1l111_opy_.bstack11l111111l_opy_():
        return
    bstack111l1l111_opy_ = bstack1l11l1l1ll_opy_(bstack111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᙶ"), bstack111l_opy_ (u"ࠫࠬᙷ"), status, reason, bstack111l_opy_ (u"ࠬ࠭ᙸ"), bstack111l_opy_ (u"࠭ࠧᙹ"))
    driver.execute_script(bstack111l1l111_opy_)
def bstack1l11lll1ll_opy_(page, status, reason=bstack111l_opy_ (u"ࠧࠨᙺ")):
    try:
        if page is None:
            return
        bstack1l1ll1l111_opy_ = Config.bstack11llll1111_opy_()
        if bstack1l1ll1l111_opy_.bstack11l111111l_opy_():
            return
        bstack111l1l111_opy_ = bstack1l11l1l1ll_opy_(bstack111l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᙻ"), bstack111l_opy_ (u"ࠩࠪᙼ"), status, reason, bstack111l_opy_ (u"ࠪࠫᙽ"), bstack111l_opy_ (u"ࠫࠬᙾ"))
        page.evaluate(bstack111l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᙿ"), bstack111l1l111_opy_)
    except Exception as e:
        print(bstack111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦ "), e)
def bstack1l11l1l1ll_opy_(type, name, status, reason, bstack1l1l11lll1_opy_, bstack11l11ll11_opy_):
    bstack11l11l1ll_opy_ = {
        bstack111l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᚁ"): type,
        bstack111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᚂ"): {}
    }
    if type == bstack111l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᚃ"):
        bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᚄ")][bstack111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᚅ")] = bstack1l1l11lll1_opy_
        bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᚆ")][bstack111l_opy_ (u"࠭ࡤࡢࡶࡤࠫᚇ")] = json.dumps(str(bstack11l11ll11_opy_))
    if type == bstack111l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᚈ"):
        bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᚉ")][bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᚊ")] = name
    if type == bstack111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᚋ"):
        bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᚌ")][bstack111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᚍ")] = status
        if status == bstack111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᚎ") and str(reason) != bstack111l_opy_ (u"ࠢࠣᚏ"):
            bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᚐ")][bstack111l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᚑ")] = json.dumps(str(reason))
    bstack1l1lll111l_opy_ = bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᚒ").format(json.dumps(bstack11l11l1ll_opy_))
    return bstack1l1lll111l_opy_
def bstack1l1111l1l1_opy_(url, config, logger, bstack1l11l1ll_opy_=False):
    hostname = bstack11l1lllll_opy_(url)
    is_private = bstack11llll1l1_opy_(hostname)
    try:
        if is_private or bstack1l11l1ll_opy_:
            file_path = bstack1llllll1l11_opy_(bstack111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᚓ"), bstack111l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᚔ"), logger)
            if os.environ.get(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᚕ")) and eval(
                    os.environ.get(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᚖ"))):
                return
            if (bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᚗ") in config and not config[bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᚘ")]):
                os.environ[bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᚙ")] = str(True)
                bstack1ll1l1ll111_opy_ = {bstack111l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᚚ"): hostname}
                bstack1lllll1ll11_opy_(bstack111l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ᚛"), bstack111l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ᚜"), bstack1ll1l1ll111_opy_, logger)
    except Exception as e:
        pass
def bstack1l1ll11ll1_opy_(caps, bstack1ll1l1ll1l1_opy_):
    if bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᚝") in caps:
        caps[bstack111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᚞")][bstack111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ᚟")] = True
        if bstack1ll1l1ll1l1_opy_:
            caps[bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᚠ")][bstack111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᚡ")] = bstack1ll1l1ll1l1_opy_
    else:
        caps[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᚢ")] = True
        if bstack1ll1l1ll1l1_opy_:
            caps[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᚣ")] = bstack1ll1l1ll1l1_opy_
def bstack1ll1ll1ll1l_opy_(bstack11l1lll11l_opy_):
    bstack1ll1l1ll1ll_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᚤ"), bstack111l_opy_ (u"ࠨࠩᚥ"))
    if bstack1ll1l1ll1ll_opy_ == bstack111l_opy_ (u"ࠩࠪᚦ") or bstack1ll1l1ll1ll_opy_ == bstack111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᚧ"):
        threading.current_thread().testStatus = bstack11l1lll11l_opy_
    else:
        if bstack11l1lll11l_opy_ == bstack111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᚨ"):
            threading.current_thread().testStatus = bstack11l1lll11l_opy_