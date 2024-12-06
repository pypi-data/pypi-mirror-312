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
import datetime
import threading
from bstack_utils.helper import bstack111lll1l1l_opy_, bstack11l11ll1l_opy_, get_host_info, bstack1111111111_opy_, \
 bstack1l1ll111l1_opy_, bstack1l1llll1l_opy_, bstack11l1lll111_opy_, bstack11111l11ll_opy_, bstack1ll11l111l_opy_
import bstack_utils.bstack1lll1ll111_opy_ as bstack1lll111ll_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack1lll1lllll_opy_
from bstack_utils.percy import bstack1l1ll111ll_opy_
from bstack_utils.config import Config
bstack1l1ll1l111_opy_ = Config.bstack11llll1111_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1ll111ll_opy_()
@bstack11l1lll111_opy_(class_method=False)
def bstack1ll11ll1lll_opy_(bs_config, bstack1l1lll1l11_opy_):
  try:
    data = {
        bstack111l_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ៙"): bstack111l_opy_ (u"ࠩ࡭ࡷࡴࡴࠧ៚"),
        bstack111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩ៛"): bs_config.get(bstack111l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩៜ"), bstack111l_opy_ (u"ࠬ࠭៝")),
        bstack111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ៞"): bs_config.get(bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ៟"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ០"): bs_config.get(bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ១")),
        bstack111l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ២"): bs_config.get(bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ៣"), bstack111l_opy_ (u"ࠬ࠭៤")),
        bstack111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ៥"): bstack1ll11l111l_opy_(),
        bstack111l_opy_ (u"ࠧࡵࡣࡪࡷࠬ៦"): bstack1111111111_opy_(bs_config),
        bstack111l_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ៧"): get_host_info(),
        bstack111l_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ៨"): bstack11l11ll1l_opy_(),
        bstack111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ៩"): os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ៪")),
        bstack111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪ៫"): os.environ.get(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ៬"), False),
        bstack111l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ៭"): bstack111lll1l1l_opy_(),
        bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ៮"): bstack1ll11l11111_opy_(),
        bstack111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭៯"): bstack1ll111lll1l_opy_(bstack1l1lll1l11_opy_),
        bstack111l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ៰"): bstack1llll11l_opy_(bs_config, bstack1l1lll1l11_opy_.get(bstack111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ៱"), bstack111l_opy_ (u"ࠬ࠭៲"))),
        bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ៳"): bstack1l1ll111l1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ៴").format(str(error)))
    return None
def bstack1ll111lll1l_opy_(framework):
  return {
    bstack111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ៵"): framework.get(bstack111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ៶"), bstack111l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ៷")),
    bstack111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ៸"): framework.get(bstack111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ៹")),
    bstack111l_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ៺"): framework.get(bstack111l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ៻")),
    bstack111l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ៼"): bstack111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ៽"),
    bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ៾"): framework.get(bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ៿"))
  }
def bstack1llll11l_opy_(bs_config, framework):
  bstack11lll11l1l_opy_ = False
  bstack11111ll1l_opy_ = False
  bstack1ll11l1111l_opy_ = False
  if bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᠀") in bs_config:
    bstack1ll11l1111l_opy_ = True
  elif bstack111l_opy_ (u"࠭ࡡࡱࡲࠪ᠁") in bs_config:
    bstack11lll11l1l_opy_ = True
  else:
    bstack11111ll1l_opy_ = True
  bstack1ll11lll1_opy_ = {
    bstack111l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᠂"): bstack1lll1lllll_opy_.bstack1ll111llll1_opy_(bs_config, framework),
    bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᠃"): bstack1lll111ll_opy_.bstack111l1ll1ll_opy_(bs_config),
    bstack111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ᠄"): bs_config.get(bstack111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ᠅"), False),
    bstack111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᠆"): bstack11111ll1l_opy_,
    bstack111l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᠇"): bstack11lll11l1l_opy_,
    bstack111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ᠈"): bstack1ll11l1111l_opy_
  }
  return bstack1ll11lll1_opy_
@bstack11l1lll111_opy_(class_method=False)
def bstack1ll11l11111_opy_():
  try:
    bstack1ll11l11l1l_opy_ = json.loads(os.getenv(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ᠉"), bstack111l_opy_ (u"ࠨࡽࢀࠫ᠊")))
    return {
        bstack111l_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ᠋"): bstack1ll11l11l1l_opy_
    }
  except Exception as error:
    logger.error(bstack111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ᠌").format(str(error)))
    return {}
def bstack1ll11lll1l1_opy_(array, bstack1ll11l111ll_opy_, bstack1ll111ll1ll_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll11l111ll_opy_]
    result[key] = o[bstack1ll111ll1ll_opy_]
  return result
def bstack1ll11lll111_opy_(bstack11l111111_opy_=bstack111l_opy_ (u"ࠫࠬ᠍")):
  bstack1ll11l11l11_opy_ = bstack1lll111ll_opy_.on()
  bstack1ll111lllll_opy_ = bstack1lll1lllll_opy_.on()
  bstack1ll111lll11_opy_ = percy.bstack1ll11llll1_opy_()
  if bstack1ll111lll11_opy_ and not bstack1ll111lllll_opy_ and not bstack1ll11l11l11_opy_:
    return bstack11l111111_opy_ not in [bstack111l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩ᠎"), bstack111l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ᠏")]
  elif bstack1ll11l11l11_opy_ and not bstack1ll111lllll_opy_:
    return bstack11l111111_opy_ not in [bstack111l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᠐"), bstack111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᠑"), bstack111l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭᠒")]
  return bstack1ll11l11l11_opy_ or bstack1ll111lllll_opy_ or bstack1ll111lll11_opy_
@bstack11l1lll111_opy_(class_method=False)
def bstack1ll1l111111_opy_(bstack11l111111_opy_, test=None):
  bstack1ll11l111l1_opy_ = bstack1lll111ll_opy_.on()
  if not bstack1ll11l111l1_opy_ or bstack11l111111_opy_ not in [bstack111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ᠓")] or test == None:
    return None
  return {
    bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᠔"): bstack1ll11l111l1_opy_ and bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᠕"), None) == True and bstack1lll111ll_opy_.bstack1111lll11_opy_(test[bstack111l_opy_ (u"࠭ࡴࡢࡩࡶࠫ᠖")])
  }