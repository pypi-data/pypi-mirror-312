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
import re
from bstack_utils.bstack1ll11l11l1_opy_ import bstack1ll1ll1ll1l_opy_
def bstack1ll1lll1111_opy_(fixture_name):
    if fixture_name.startswith(bstack111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᙀ")):
        return bstack111l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᙁ")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᙂ")):
        return bstack111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᙃ")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᙄ")):
        return bstack111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᙅ")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᙆ")):
        return bstack111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᙇ")
def bstack1ll1lll1l1l_opy_(fixture_name):
    return bool(re.match(bstack111l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᙈ"), fixture_name))
def bstack1ll1llll111_opy_(fixture_name):
    return bool(re.match(bstack111l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᙉ"), fixture_name))
def bstack1ll1ll1llll_opy_(fixture_name):
    return bool(re.match(bstack111l_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᙊ"), fixture_name))
def bstack1ll1ll1ll11_opy_(fixture_name):
    if fixture_name.startswith(bstack111l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᙋ")):
        return bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᙌ"), bstack111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᙍ")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᙎ")):
        return bstack111l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᙏ"), bstack111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᙐ")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᙑ")):
        return bstack111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᙒ"), bstack111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᙓ")
    elif fixture_name.startswith(bstack111l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᙔ")):
        return bstack111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᙕ"), bstack111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᙖ")
    return None, None
def bstack1ll1lll1l11_opy_(hook_name):
    if hook_name in [bstack111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᙗ"), bstack111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᙘ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1ll1ll1lll1_opy_(hook_name):
    if hook_name in [bstack111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᙙ"), bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᙚ")]:
        return bstack111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᙛ")
    elif hook_name in [bstack111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᙜ"), bstack111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᙝ")]:
        return bstack111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᙞ")
    elif hook_name in [bstack111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᙟ"), bstack111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᙠ")]:
        return bstack111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᙡ")
    elif hook_name in [bstack111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᙢ"), bstack111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᙣ")]:
        return bstack111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᙤ")
    return hook_name
def bstack1ll1lll1lll_opy_(node, scenario):
    if hasattr(node, bstack111l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᙥ")):
        parts = node.nodeid.rsplit(bstack111l_opy_ (u"ࠣ࡝ࠥᙦ"))
        params = parts[-1]
        return bstack111l_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᙧ").format(scenario.name, params)
    return scenario.name
def bstack1ll1lll11ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᙨ")):
            examples = list(node.callspec.params[bstack111l_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᙩ")].values())
        return examples
    except:
        return []
def bstack1ll1llll11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1ll1lll111l_opy_(report):
    try:
        status = bstack111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᙪ")
        if report.passed or (report.failed and hasattr(report, bstack111l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᙫ"))):
            status = bstack111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᙬ")
        elif report.skipped:
            status = bstack111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᙭")
        bstack1ll1ll1ll1l_opy_(status)
    except:
        pass
def bstack1llll111l1_opy_(status):
    try:
        bstack1ll1lll1ll1_opy_ = bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᙮")
        if status == bstack111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᙯ"):
            bstack1ll1lll1ll1_opy_ = bstack111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᙰ")
        elif status == bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᙱ"):
            bstack1ll1lll1ll1_opy_ = bstack111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᙲ")
        bstack1ll1ll1ll1l_opy_(bstack1ll1lll1ll1_opy_)
    except:
        pass
def bstack1ll1lll11l1_opy_(item=None, report=None, summary=None, extra=None):
    return