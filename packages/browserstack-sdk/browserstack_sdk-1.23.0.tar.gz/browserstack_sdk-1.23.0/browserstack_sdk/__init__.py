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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1111l11l1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1ll1ll_opy_ import bstack1l11l11ll1_opy_
import time
import requests
def bstack1l11ll1lll_opy_():
  global CONFIG
  headers = {
        bstack111l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll1ll1l11_opy_(CONFIG, bstack111l11111_opy_)
  try:
    response = requests.get(bstack111l11111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1l11ll_opy_ = response.json()[bstack111l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l11l1lll1_opy_.format(response.json()))
      return bstack1l1l11ll_opy_
    else:
      logger.debug(bstack111lll1l1_opy_.format(bstack111l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111lll1l1_opy_.format(e))
def bstack1l1ll1111l_opy_(hub_url):
  global CONFIG
  url = bstack111l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll1ll1l11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l11111111_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1lll111l1_opy_.format(hub_url, e))
def bstack1llll1111l_opy_():
  try:
    global bstack1l111ll1l_opy_
    bstack1l1l11ll_opy_ = bstack1l11ll1lll_opy_()
    bstack11l1ll11l_opy_ = []
    results = []
    for bstack1lll1ll1l1_opy_ in bstack1l1l11ll_opy_:
      bstack11l1ll11l_opy_.append(bstack111ll11l1_opy_(target=bstack1l1ll1111l_opy_,args=(bstack1lll1ll1l1_opy_,)))
    for t in bstack11l1ll11l_opy_:
      t.start()
    for t in bstack11l1ll11l_opy_:
      results.append(t.join())
    bstack1l1l11l111_opy_ = {}
    for item in results:
      hub_url = item[bstack111l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack111l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1l11l111_opy_[hub_url] = latency
    bstack1l11ll11_opy_ = min(bstack1l1l11l111_opy_, key= lambda x: bstack1l1l11l111_opy_[x])
    bstack1l111ll1l_opy_ = bstack1l11ll11_opy_
    logger.debug(bstack1l1l1lll1l_opy_.format(bstack1l11ll11_opy_))
  except Exception as e:
    logger.debug(bstack11lll11l1_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack11lll1lll1_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1l1l11_opy_, bstack1111ll11l_opy_, bstack1lll1lll11_opy_, bstack1l1llll1l_opy_, bstack1l1ll111l1_opy_, \
  Notset, bstack1llll1lll1_opy_, \
  bstack11lll111l1_opy_, bstack1l1ll1lll1_opy_, bstack11lll1l1l_opy_, bstack11l11ll1l_opy_, bstack1111l1lll_opy_, bstack11lll11ll1_opy_, \
  bstack1l11lll1_opy_, \
  bstack111111l1_opy_, bstack1l11111lll_opy_, bstack1ll1l111_opy_, bstack1l111ll11l_opy_, \
  bstack1l11llll1l_opy_, bstack1l111ll1_opy_, bstack111lll11l_opy_, bstack1l11lll111_opy_
from bstack_utils.bstack1ll111lll_opy_ import bstack11l11ll1_opy_
from bstack_utils.bstack1ll111l1_opy_ import bstack1ll1l1llll_opy_
from bstack_utils.bstack1ll11l11l1_opy_ import bstack111111ll_opy_, bstack1l11lll1ll_opy_
from bstack_utils.bstack1l11ll1l1l_opy_ import bstack11ll111ll_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack1lll1lllll_opy_
from bstack_utils.bstack111111l11_opy_ import bstack111111l11_opy_
from bstack_utils.proxy import bstack11ll11l1_opy_, bstack1ll1ll1l11_opy_, bstack1l1ll11l11_opy_, bstack1l1ll1ll1_opy_
import bstack_utils.bstack1lll1ll111_opy_ as bstack1lll111ll_opy_
from browserstack_sdk.bstack11111lll1_opy_ import *
from browserstack_sdk.bstack1lll11ll1_opy_ import *
from bstack_utils.bstack1l11l1llll_opy_ import bstack1llll111l1_opy_
from browserstack_sdk.bstack11llll111l_opy_ import *
import requests
from bstack_utils.constants import *
def bstack1l1l11lll_opy_():
    global bstack1l111ll1l_opy_
    try:
        bstack1l1l1l11l1_opy_ = bstack1llll1llll_opy_()
        bstack11l11l11l_opy_(bstack1l1l1l11l1_opy_)
        hub_url = bstack1l1l1l11l1_opy_.get(bstack111l_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack111l_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack111l_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack111l_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1l111ll1l_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1llll1llll_opy_():
    global CONFIG
    bstack1l1l1lll1_opy_ = CONFIG.get(bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack111l_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack111l_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1l1l1lll1_opy_, str):
        raise ValueError(bstack111l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1l1l1l11l1_opy_ = bstack1ll1111l11_opy_(bstack1l1l1lll1_opy_)
        return bstack1l1l1l11l1_opy_
    except Exception as e:
        logger.error(bstack111l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1ll1111l11_opy_(bstack1l1l1lll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack111l_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack11lll1l1_opy_ + bstack1l1l1lll1_opy_
        auth = (CONFIG[bstack111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11111l11l_opy_ = json.loads(response.text)
            return bstack11111l11l_opy_
    except ValueError as ve:
        logger.error(bstack111l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack111l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11l11l11l_opy_(bstack1lll1l11l1_opy_):
    global CONFIG
    if bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack111l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack111l_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1lll1l11l1_opy_:
        bstack11111ll11_opy_ = CONFIG.get(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack111l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack11111ll11_opy_)
        bstack1lll1111l1_opy_ = bstack1lll1l11l1_opy_.get(bstack111l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1ll11lll11_opy_ = bstack111l_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1lll1111l1_opy_)
        logger.debug(bstack111l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1ll11lll11_opy_)
        bstack1ll1l1ll11_opy_ = {
            bstack111l_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack111l_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack111l_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack111l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack111l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1ll11lll11_opy_
        }
        bstack11111ll11_opy_.update(bstack1ll1l1ll11_opy_)
        logger.debug(bstack111l_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack11111ll11_opy_)
        CONFIG[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack11111ll11_opy_
        logger.debug(bstack111l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack11l111ll_opy_():
    bstack1l1l1l11l1_opy_ = bstack1llll1llll_opy_()
    if not bstack1l1l1l11l1_opy_[bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack111l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1l1l1l11l1_opy_[bstack111l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack111l_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
def bstack1l11l1l1l_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1l11l11111_opy_
        logger.debug(bstack111l_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack111l_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack111l_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack11lll111l_opy_ = json.loads(response.text)
                bstack1ll1l1l1l1_opy_ = bstack11lll111l_opy_.get(bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1ll1l1l1l1_opy_:
                    bstack11l1l1l1_opy_ = bstack1ll1l1l1l1_opy_[0]
                    bstack11111111_opy_ = bstack11l1l1l1_opy_.get(bstack111l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack11l1l1ll_opy_ = bstack1l11l11l1l_opy_ + bstack11111111_opy_
                    result.extend([bstack11111111_opy_, bstack11l1l1ll_opy_])
                    logger.info(bstack11lll1llll_opy_.format(bstack11l1l1ll_opy_))
                    bstack1lll1l1ll1_opy_ = CONFIG[bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1lll1l1ll1_opy_ += bstack111l_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1lll1l1ll1_opy_ != bstack11l1l1l1_opy_.get(bstack111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1ll11ll111_opy_.format(bstack11l1l1l1_opy_.get(bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1lll1l1ll1_opy_))
                    return result
                else:
                    logger.debug(bstack111l_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack111l_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack111l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack111l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
import bstack_utils.bstack1l1l111l_opy_ as bstack1l1l1l11l_opy_
import bstack_utils.bstack111ll111l_opy_ as bstack1l1l111l1_opy_
bstack11lll1ll1l_opy_ = bstack111l_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࢹ")
bstack1l1l11ll11_opy_ = bstack111l_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧࢺ")
from ._version import __version__
bstack11ll1l1l_opy_ = None
CONFIG = {}
bstack1lll111ll1_opy_ = {}
bstack1ll1ll111l_opy_ = {}
bstack1l1l11l1l1_opy_ = None
bstack11llll1l_opy_ = None
bstack1llllllll_opy_ = None
bstack1lll1llll1_opy_ = -1
bstack1111l1111_opy_ = 0
bstack11l1llll_opy_ = bstack1llll1111_opy_
bstack1l1l11111_opy_ = 1
bstack1ll1l1l1_opy_ = False
bstack1ll11l1l_opy_ = False
bstack11lll1111_opy_ = bstack111l_opy_ (u"ࠩࠪࢻ")
bstack1ll111l1l_opy_ = bstack111l_opy_ (u"ࠪࠫࢼ")
bstack1ll1l1ll_opy_ = False
bstack1l1lll11l1_opy_ = True
bstack1l1lll1l_opy_ = bstack111l_opy_ (u"ࠫࠬࢽ")
bstack1l11l1l1_opy_ = []
bstack1l111ll1l_opy_ = bstack111l_opy_ (u"ࠬ࠭ࢾ")
bstack1ll1lll1l1_opy_ = False
bstack1l11llll_opy_ = None
bstack11lll11l_opy_ = None
bstack1l111l11l1_opy_ = None
bstack1lllllllll_opy_ = -1
bstack1llll1l1l_opy_ = os.path.join(os.path.expanduser(bstack111l_opy_ (u"࠭ࡾࠨࢿ")), bstack111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣀ"), bstack111l_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣁ"))
bstack1ll1111l_opy_ = 0
bstack1ll11ll1l1_opy_ = 0
bstack1ll1l1lll_opy_ = []
bstack1llll1l1ll_opy_ = []
bstack1l1ll11l1_opy_ = []
bstack1ll111ll_opy_ = []
bstack111lll1l_opy_ = bstack111l_opy_ (u"ࠩࠪࣂ")
bstack1ll1ll1l_opy_ = bstack111l_opy_ (u"ࠪࠫࣃ")
bstack1l1l1lll_opy_ = False
bstack1l1l11l1l_opy_ = False
bstack1111llll1_opy_ = {}
bstack1l1111l1ll_opy_ = None
bstack1ll1ll1l1_opy_ = None
bstack1lll1lll1l_opy_ = None
bstack11111l1l_opy_ = None
bstack1111ll1l_opy_ = None
bstack1l11l11ll_opy_ = None
bstack1l11lllll1_opy_ = None
bstack1l11111l11_opy_ = None
bstack1l111lll1l_opy_ = None
bstack1l11llll11_opy_ = None
bstack1l1l111111_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack111l1111_opy_ = None
bstack1l1lllll1_opy_ = None
bstack1ll1l1l111_opy_ = None
bstack1l11llllll_opy_ = None
bstack1l1111l11l_opy_ = None
bstack11ll1l11l_opy_ = None
bstack1l1ll11111_opy_ = None
bstack1lll11l11l_opy_ = None
bstack1llll111l_opy_ = None
bstack1ll1lll1_opy_ = None
bstack1ll1111ll1_opy_ = False
bstack1ll11ll1ll_opy_ = bstack111l_opy_ (u"ࠦࠧࣄ")
logger = bstack11lll1lll1_opy_.get_logger(__name__, bstack11l1llll_opy_)
bstack1l1ll1l111_opy_ = Config.bstack11llll1111_opy_()
percy = bstack1l1ll111ll_opy_()
bstack11l11l111_opy_ = bstack1l11l11ll1_opy_()
bstack1111llll_opy_ = bstack11llll111l_opy_()
def bstack111l1lll1_opy_():
  global CONFIG
  global bstack1l1l1lll_opy_
  global bstack1l1ll1l111_opy_
  bstack1l1ll1llll_opy_ = bstack1lllll1ll_opy_(CONFIG)
  if bstack1l1ll111l1_opy_(CONFIG):
    if (bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࣅ") in bstack1l1ll1llll_opy_ and str(bstack1l1ll1llll_opy_[bstack111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࣆ")]).lower() == bstack111l_opy_ (u"ࠧࡵࡴࡸࡩࠬࣇ")):
      bstack1l1l1lll_opy_ = True
    bstack1l1ll1l111_opy_.bstack1l1ll1ll11_opy_(bstack1l1ll1llll_opy_.get(bstack111l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬࣈ"), False))
  else:
    bstack1l1l1lll_opy_ = True
    bstack1l1ll1l111_opy_.bstack1l1ll1ll11_opy_(True)
def bstack11l1l1ll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11lll11111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1111l1ll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111l_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨࣉ") == args[i].lower() or bstack111l_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪࠦ࣊") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1lll1l_opy_
      bstack1l1lll1l_opy_ += bstack111l_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠡࠩ࣋") + path
      return path
  return None
bstack11lll1ll_opy_ = re.compile(bstack111l_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿ࠣ࣌"))
def bstack11l1ll1l1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11lll1ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111l_opy_ (u"ࠨࠤࡼࠤ࣍") + group + bstack111l_opy_ (u"ࠢࡾࠤ࣎"), os.environ.get(group))
  return value
def bstack11l1lll1l_opy_():
  bstack1l1l1l111l_opy_ = bstack1111l1ll_opy_()
  if bstack1l1l1l111l_opy_ and os.path.exists(os.path.abspath(bstack1l1l1l111l_opy_)):
    fileName = bstack1l1l1l111l_opy_
  if bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉ࣏ࠬ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࣐࠭")])) and not bstack111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩ࣑ࠬ") in locals():
    fileName = os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")]
  if bstack111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫࣓ࠧ") in locals():
    bstack111lll1_opy_ = os.path.abspath(fileName)
  else:
    bstack111lll1_opy_ = bstack111l_opy_ (u"࠭ࠧࣔ")
  bstack11lllll1l_opy_ = os.getcwd()
  bstack1ll11lllll_opy_ = bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣕ")
  bstack1l11l1l11l_opy_ = bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣖ")
  while (not os.path.exists(bstack111lll1_opy_)) and bstack11lllll1l_opy_ != bstack111l_opy_ (u"ࠤࠥࣗ"):
    bstack111lll1_opy_ = os.path.join(bstack11lllll1l_opy_, bstack1ll11lllll_opy_)
    if not os.path.exists(bstack111lll1_opy_):
      bstack111lll1_opy_ = os.path.join(bstack11lllll1l_opy_, bstack1l11l1l11l_opy_)
    if bstack11lllll1l_opy_ != os.path.dirname(bstack11lllll1l_opy_):
      bstack11lllll1l_opy_ = os.path.dirname(bstack11lllll1l_opy_)
    else:
      bstack11lllll1l_opy_ = bstack111l_opy_ (u"ࠥࠦࣘ")
  if not os.path.exists(bstack111lll1_opy_):
    bstack1llll1l1_opy_(
      bstack1l1l11l11_opy_.format(os.getcwd()))
  try:
    with open(bstack111lll1_opy_, bstack111l_opy_ (u"ࠫࡷ࠭ࣙ")) as stream:
      yaml.add_implicit_resolver(bstack111l_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣚ"), bstack11lll1ll_opy_)
      yaml.add_constructor(bstack111l_opy_ (u"ࠨࠡࡱࡣࡷ࡬ࡪࡾࠢࣛ"), bstack11l1ll1l1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack111lll1_opy_, bstack111l_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1llll1l1_opy_(bstack111l111l_opy_.format(str(exc)))
def bstack1l11l1ll1_opy_(config):
  bstack1llll1ll_opy_ = bstack11ll1llll1_opy_(config)
  for option in list(bstack1llll1ll_opy_):
    if option.lower() in bstack11ll1111l_opy_ and option != bstack11ll1111l_opy_[option.lower()]:
      bstack1llll1ll_opy_[bstack11ll1111l_opy_[option.lower()]] = bstack1llll1ll_opy_[option]
      del bstack1llll1ll_opy_[option]
  return config
def bstack1l1ll111_opy_():
  global bstack1ll1ll111l_opy_
  for key, bstack1111l1l11_opy_ in bstack1l11ll1ll1_opy_.items():
    if isinstance(bstack1111l1l11_opy_, list):
      for var in bstack1111l1l11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll1ll111l_opy_[key] = os.environ[var]
          break
    elif bstack1111l1l11_opy_ in os.environ and os.environ[bstack1111l1l11_opy_] and str(os.environ[bstack1111l1l11_opy_]).strip():
      bstack1ll1ll111l_opy_[key] = os.environ[bstack1111l1l11_opy_]
  if bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣝ") in os.environ:
    bstack1ll1ll111l_opy_[bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣞ")] = {}
    bstack1ll1ll111l_opy_[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣟ")][bstack111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")] = os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ࣡")]
def bstack1l1l1ll1_opy_():
  global bstack1lll111ll1_opy_
  global bstack1l1lll1l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack111l_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣢").lower() == val.lower():
      bstack1lll111ll1_opy_[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣣࠫ")] = {}
      bstack1lll111ll1_opy_[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣤ")][bstack111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣥ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l111111l1_opy_ in bstack1lllll11ll_opy_.items():
    if isinstance(bstack1l111111l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l111111l1_opy_:
          if idx < len(sys.argv) and bstack111l_opy_ (u"ࠪ࠱࠲ࣦ࠭") + var.lower() == val.lower() and not key in bstack1lll111ll1_opy_:
            bstack1lll111ll1_opy_[key] = sys.argv[idx + 1]
            bstack1l1lll1l_opy_ += bstack111l_opy_ (u"ࠫࠥ࠳࠭ࠨࣧ") + var + bstack111l_opy_ (u"ࠬࠦࠧࣨ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack111l_opy_ (u"࠭࠭࠮ࣩࠩ") + bstack1l111111l1_opy_.lower() == val.lower() and not key in bstack1lll111ll1_opy_:
          bstack1lll111ll1_opy_[key] = sys.argv[idx + 1]
          bstack1l1lll1l_opy_ += bstack111l_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + bstack1l111111l1_opy_ + bstack111l_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack111l111l1_opy_(config):
  bstack1l111l1111_opy_ = config.keys()
  for bstack1ll11111l_opy_, bstack1ll11l1ll_opy_ in bstack1l111111_opy_.items():
    if bstack1ll11l1ll_opy_ in bstack1l111l1111_opy_:
      config[bstack1ll11111l_opy_] = config[bstack1ll11l1ll_opy_]
      del config[bstack1ll11l1ll_opy_]
  for bstack1ll11111l_opy_, bstack1ll11l1ll_opy_ in bstack11llllll11_opy_.items():
    if isinstance(bstack1ll11l1ll_opy_, list):
      for bstack1ll1l11l_opy_ in bstack1ll11l1ll_opy_:
        if bstack1ll1l11l_opy_ in bstack1l111l1111_opy_:
          config[bstack1ll11111l_opy_] = config[bstack1ll1l11l_opy_]
          del config[bstack1ll1l11l_opy_]
          break
    elif bstack1ll11l1ll_opy_ in bstack1l111l1111_opy_:
      config[bstack1ll11111l_opy_] = config[bstack1ll11l1ll_opy_]
      del config[bstack1ll11l1ll_opy_]
  for bstack1ll1l11l_opy_ in list(config):
    for bstack1l1l111l1l_opy_ in bstack1l1llll1_opy_:
      if bstack1ll1l11l_opy_.lower() == bstack1l1l111l1l_opy_.lower() and bstack1ll1l11l_opy_ != bstack1l1l111l1l_opy_:
        config[bstack1l1l111l1l_opy_] = config[bstack1ll1l11l_opy_]
        del config[bstack1ll1l11l_opy_]
  bstack1l1l111ll_opy_ = [{}]
  if not config.get(bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࣬")):
    config[bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࣭࠭")] = [{}]
  bstack1l1l111ll_opy_ = config[bstack111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ࣮ࠧ")]
  for platform in bstack1l1l111ll_opy_:
    for bstack1ll1l11l_opy_ in list(platform):
      for bstack1l1l111l1l_opy_ in bstack1l1llll1_opy_:
        if bstack1ll1l11l_opy_.lower() == bstack1l1l111l1l_opy_.lower() and bstack1ll1l11l_opy_ != bstack1l1l111l1l_opy_:
          platform[bstack1l1l111l1l_opy_] = platform[bstack1ll1l11l_opy_]
          del platform[bstack1ll1l11l_opy_]
  for bstack1ll11111l_opy_, bstack1ll11l1ll_opy_ in bstack11llllll11_opy_.items():
    for platform in bstack1l1l111ll_opy_:
      if isinstance(bstack1ll11l1ll_opy_, list):
        for bstack1ll1l11l_opy_ in bstack1ll11l1ll_opy_:
          if bstack1ll1l11l_opy_ in platform:
            platform[bstack1ll11111l_opy_] = platform[bstack1ll1l11l_opy_]
            del platform[bstack1ll1l11l_opy_]
            break
      elif bstack1ll11l1ll_opy_ in platform:
        platform[bstack1ll11111l_opy_] = platform[bstack1ll11l1ll_opy_]
        del platform[bstack1ll11l1ll_opy_]
  for bstack1111ll11_opy_ in bstack1l1ll1l11_opy_:
    if bstack1111ll11_opy_ in config:
      if not bstack1l1ll1l11_opy_[bstack1111ll11_opy_] in config:
        config[bstack1l1ll1l11_opy_[bstack1111ll11_opy_]] = {}
      config[bstack1l1ll1l11_opy_[bstack1111ll11_opy_]].update(config[bstack1111ll11_opy_])
      del config[bstack1111ll11_opy_]
  for platform in bstack1l1l111ll_opy_:
    for bstack1111ll11_opy_ in bstack1l1ll1l11_opy_:
      if bstack1111ll11_opy_ in list(platform):
        if not bstack1l1ll1l11_opy_[bstack1111ll11_opy_] in platform:
          platform[bstack1l1ll1l11_opy_[bstack1111ll11_opy_]] = {}
        platform[bstack1l1ll1l11_opy_[bstack1111ll11_opy_]].update(platform[bstack1111ll11_opy_])
        del platform[bstack1111ll11_opy_]
  config = bstack1l11l1ll1_opy_(config)
  return config
def bstack1l11ll111_opy_(config):
  global bstack1ll111l1l_opy_
  bstack111l1l11l_opy_ = False
  if bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦ࣯ࠩ") in config and str(config[bstack111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࣰࠪ")]).lower() != bstack111l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪࣱ࠭"):
    if bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࣲࠬ") not in config or str(config[bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ࣳ")]).lower() == bstack111l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
      config[bstack111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪࣵ")] = False
    else:
      bstack1l1l1l11l1_opy_ = bstack1llll1llll_opy_()
      if bstack111l_opy_ (u"ࠬ࡯ࡳࡕࡴ࡬ࡥࡱࡍࡲࡪࡦࣶࠪ") in bstack1l1l1l11l1_opy_:
        if not bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࣷ") in config:
          config[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣸ")] = {}
        config[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࣹࠬ")][bstack111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࣺࠫ")] = bstack111l_opy_ (u"ࠪࡥࡹࡹ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠩࣻ")
        bstack111l1l11l_opy_ = True
        bstack1ll111l1l_opy_ = config[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")].get(bstack111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ"))
  if bstack1l1ll111l1_opy_(config) and bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࣾ") in config and str(config[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ")]).lower() != bstack111l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ") and not bstack111l1l11l_opy_:
    if not bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ँ") in config:
      config[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧं")] = {}
    if not config[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨः")].get(bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠩऄ")) and not bstack111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨअ") in config[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")]:
      bstack1ll11l111l_opy_ = datetime.datetime.now()
      bstack11111l111_opy_ = bstack1ll11l111l_opy_.strftime(bstack111l_opy_ (u"ࠨࠧࡧࡣࠪࡨ࡟ࠦࡊࠨࡑࠬइ"))
      hostname = socket.gethostname()
      bstack1111ll1l1_opy_ = bstack111l_opy_ (u"ࠩࠪई").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111l_opy_ (u"ࠪࡿࢂࡥࡻࡾࡡࡾࢁࠬउ").format(bstack11111l111_opy_, hostname, bstack1111ll1l1_opy_)
      config[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऊ")][bstack111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऋ")] = identifier
    bstack1ll111l1l_opy_ = config[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪऌ")].get(bstack111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऍ"))
  return config
def bstack111l11ll1_opy_():
  bstack1ll1llll_opy_ =  bstack11l11ll1l_opy_()[bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠧऎ")]
  return bstack1ll1llll_opy_ if bstack1ll1llll_opy_ else -1
def bstack111llll1_opy_(bstack1ll1llll_opy_):
  global CONFIG
  if not bstack111l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫए") in CONFIG[bstack111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ")]:
    return
  CONFIG[bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ")] = CONFIG[bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ")].replace(
    bstack111l_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨओ"),
    str(bstack1ll1llll_opy_)
  )
def bstack1l11ll11l_opy_():
  global CONFIG
  if not bstack111l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭औ") in CONFIG[bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")]:
    return
  bstack1ll11l111l_opy_ = datetime.datetime.now()
  bstack11111l111_opy_ = bstack1ll11l111l_opy_.strftime(bstack111l_opy_ (u"ࠩࠨࡨ࠲ࠫࡢ࠮ࠧࡋ࠾ࠪࡓࠧख"))
  CONFIG[bstack111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬग")] = CONFIG[bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")].replace(
    bstack111l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫङ"),
    bstack11111l111_opy_
  )
def bstack111llll11_opy_():
  global CONFIG
  if bstack111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच") in CONFIG and not bool(CONFIG[bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")]):
    del CONFIG[bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪज")]
    return
  if not bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG:
    CONFIG[bstack111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = bstack111l_opy_ (u"ࠫࠨࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧट")
  if bstack111l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫठ") in CONFIG[bstack111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")]:
    bstack1l11ll11l_opy_()
    os.environ[bstack111l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫढ")] = CONFIG[bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪण")]
  if not bstack111l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫत") in CONFIG[bstack111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")]:
    return
  bstack1ll1llll_opy_ = bstack111l_opy_ (u"ࠫࠬद")
  bstack1l1l1l1111_opy_ = bstack111l11ll1_opy_()
  if bstack1l1l1l1111_opy_ != -1:
    bstack1ll1llll_opy_ = bstack111l_opy_ (u"ࠬࡉࡉࠡࠩध") + str(bstack1l1l1l1111_opy_)
  if bstack1ll1llll_opy_ == bstack111l_opy_ (u"࠭ࠧन"):
    bstack11ll11l11_opy_ = bstack1lll1l1ll_opy_(CONFIG[bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪऩ")])
    if bstack11ll11l11_opy_ != -1:
      bstack1ll1llll_opy_ = str(bstack11ll11l11_opy_)
  if bstack1ll1llll_opy_:
    bstack111llll1_opy_(bstack1ll1llll_opy_)
    os.environ[bstack111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬप")] = CONFIG[bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")]
def bstack1lll1l1l_opy_(bstack1ll11l1ll1_opy_, bstack11l111lll_opy_, path):
  bstack111llll1l_opy_ = {
    bstack111l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧब"): bstack11l111lll_opy_
  }
  if os.path.exists(path):
    bstack11lllllll1_opy_ = json.load(open(path, bstack111l_opy_ (u"ࠫࡷࡨࠧभ")))
  else:
    bstack11lllllll1_opy_ = {}
  bstack11lllllll1_opy_[bstack1ll11l1ll1_opy_] = bstack111llll1l_opy_
  with open(path, bstack111l_opy_ (u"ࠧࡽࠫࠣम")) as outfile:
    json.dump(bstack11lllllll1_opy_, outfile)
def bstack1lll1l1ll_opy_(bstack1ll11l1ll1_opy_):
  bstack1ll11l1ll1_opy_ = str(bstack1ll11l1ll1_opy_)
  bstack1l1lll1ll1_opy_ = os.path.join(os.path.expanduser(bstack111l_opy_ (u"࠭ࡾࠨय")), bstack111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧर"))
  try:
    if not os.path.exists(bstack1l1lll1ll1_opy_):
      os.makedirs(bstack1l1lll1ll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠨࢀࠪऱ")), bstack111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩल"), bstack111l_opy_ (u"ࠪ࠲ࡧࡻࡩ࡭ࡦ࠰ࡲࡦࡳࡥ࠮ࡥࡤࡧ࡭࡫࠮࡫ࡵࡲࡲࠬळ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111l_opy_ (u"ࠫࡼ࠭ऴ")):
        pass
      with open(file_path, bstack111l_opy_ (u"ࠧࡽࠫࠣव")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111l_opy_ (u"࠭ࡲࠨश")) as bstack11l1l11l_opy_:
      bstack11llll11l_opy_ = json.load(bstack11l1l11l_opy_)
    if bstack1ll11l1ll1_opy_ in bstack11llll11l_opy_:
      bstack11llll1l1l_opy_ = bstack11llll11l_opy_[bstack1ll11l1ll1_opy_][bstack111l_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫष")]
      bstack1l1l11llll_opy_ = int(bstack11llll1l1l_opy_) + 1
      bstack1lll1l1l_opy_(bstack1ll11l1ll1_opy_, bstack1l1l11llll_opy_, file_path)
      return bstack1l1l11llll_opy_
    else:
      bstack1lll1l1l_opy_(bstack1ll11l1ll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lllll11l1_opy_.format(str(e)))
    return -1
def bstack1l11l111l_opy_(config):
  if not config[bstack111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪस")] or not config[bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬह")]:
    return True
  else:
    return False
def bstack11lllllll_opy_(config, index=0):
  global bstack1ll1l1ll_opy_
  bstack11111lll_opy_ = {}
  caps = bstack1ll11ll11l_opy_ + bstack1ll1llllll_opy_
  if config.get(bstack111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧऺ"), False):
    bstack11111lll_opy_[bstack111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨऻ")] = True
    bstack11111lll_opy_[bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")] = config.get(bstack111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪऽ"), {})
  if bstack1ll1l1ll_opy_:
    caps += bstack11lll111_opy_
  for key in config:
    if key in caps + [bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪा")]:
      continue
    bstack11111lll_opy_[key] = config[key]
  if bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫि") in config:
    for bstack1l11ll11ll_opy_ in config[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬी")][index]:
      if bstack1l11ll11ll_opy_ in caps:
        continue
      bstack11111lll_opy_[bstack1l11ll11ll_opy_] = config[bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")][index][bstack1l11ll11ll_opy_]
  bstack11111lll_opy_[bstack111l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ू")] = socket.gethostname()
  if bstack111l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ृ") in bstack11111lll_opy_:
    del (bstack11111lll_opy_[bstack111l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧॄ")])
  return bstack11111lll_opy_
def bstack11ll1llll_opy_(config):
  global bstack1ll1l1ll_opy_
  bstack11l11111_opy_ = {}
  caps = bstack1ll1llllll_opy_
  if bstack1ll1l1ll_opy_:
    caps += bstack11lll111_opy_
  for key in caps:
    if key in config:
      bstack11l11111_opy_[key] = config[key]
  return bstack11l11111_opy_
def bstack1l1ll1l1l_opy_(bstack11111lll_opy_, bstack11l11111_opy_):
  bstack1ll1111ll_opy_ = {}
  for key in bstack11111lll_opy_.keys():
    if key in bstack1l111111_opy_:
      bstack1ll1111ll_opy_[bstack1l111111_opy_[key]] = bstack11111lll_opy_[key]
    else:
      bstack1ll1111ll_opy_[key] = bstack11111lll_opy_[key]
  for key in bstack11l11111_opy_:
    if key in bstack1l111111_opy_:
      bstack1ll1111ll_opy_[bstack1l111111_opy_[key]] = bstack11l11111_opy_[key]
    else:
      bstack1ll1111ll_opy_[key] = bstack11l11111_opy_[key]
  return bstack1ll1111ll_opy_
def bstack1lll11l1l1_opy_(config, index=0):
  global bstack1ll1l1ll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l1l1l1ll_opy_ = bstack1l1l1l11_opy_(bstack1ll1ll1lll_opy_, config, logger)
  bstack11l11111_opy_ = bstack11ll1llll_opy_(config)
  bstack1l111ll1ll_opy_ = bstack1ll1llllll_opy_
  bstack1l111ll1ll_opy_ += bstack1111ll111_opy_
  bstack11l11111_opy_ = update(bstack11l11111_opy_, bstack1l1l1l1ll_opy_)
  if bstack1ll1l1ll_opy_:
    bstack1l111ll1ll_opy_ += bstack11lll111_opy_
  if bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॅ") in config:
    if bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ॆ") in config[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬे")][index]:
      caps[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨै")] = config[bstack111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॉ")][index][bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ")]
    if bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧो") in config[bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index]:
      caps[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯्ࠩ")] = str(config[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫॏ")])
    bstack1llll11lll_opy_ = bstack1l1l1l11_opy_(bstack1ll1ll1lll_opy_, config[bstack111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॐ")][index], logger)
    bstack1l111ll1ll_opy_ += list(bstack1llll11lll_opy_.keys())
    for bstack1l1ll1l1ll_opy_ in bstack1l111ll1ll_opy_:
      if bstack1l1ll1l1ll_opy_ in config[bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index]:
        if bstack1l1ll1l1ll_opy_ == bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ॒"):
          try:
            bstack1llll11lll_opy_[bstack1l1ll1l1ll_opy_] = str(config[bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index][bstack1l1ll1l1ll_opy_] * 1.0)
          except:
            bstack1llll11lll_opy_[bstack1l1ll1l1ll_opy_] = str(config[bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index][bstack1l1ll1l1ll_opy_])
        else:
          bstack1llll11lll_opy_[bstack1l1ll1l1ll_opy_] = config[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॕ")][index][bstack1l1ll1l1ll_opy_]
        del (config[bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1l1ll1l1ll_opy_])
    bstack11l11111_opy_ = update(bstack11l11111_opy_, bstack1llll11lll_opy_)
  bstack11111lll_opy_ = bstack11lllllll_opy_(config, index)
  for bstack1ll1l11l_opy_ in bstack1ll1llllll_opy_ + list(bstack1l1l1l1ll_opy_.keys()):
    if bstack1ll1l11l_opy_ in bstack11111lll_opy_:
      bstack11l11111_opy_[bstack1ll1l11l_opy_] = bstack11111lll_opy_[bstack1ll1l11l_opy_]
      del (bstack11111lll_opy_[bstack1ll1l11l_opy_])
  if bstack1llll1lll1_opy_(config):
    bstack11111lll_opy_[bstack111l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫॗ")] = True
    caps.update(bstack11l11111_opy_)
    caps[bstack111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭क़")] = bstack11111lll_opy_
  else:
    bstack11111lll_opy_[bstack111l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ख़")] = False
    caps.update(bstack1l1ll1l1l_opy_(bstack11111lll_opy_, bstack11l11111_opy_))
    if bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬग़") in caps:
      caps[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩज़")] = caps[bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")]
      del (caps[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")])
    if bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬफ़") in caps:
      caps[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧय़")] = caps[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧॠ")]
      del (caps[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ")])
  return caps
def bstack1l11l1ll1l_opy_():
  global bstack1l111ll1l_opy_
  global CONFIG
  if bstack11lll11111_opy_() <= version.parse(bstack111l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨॢ")):
    if bstack1l111ll1l_opy_ != bstack111l_opy_ (u"ࠩࠪॣ"):
      return bstack111l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ।") + bstack1l111ll1l_opy_ + bstack111l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ॥")
    return bstack11l1llll1_opy_
  if bstack1l111ll1l_opy_ != bstack111l_opy_ (u"ࠬ࠭०"):
    return bstack111l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ१") + bstack1l111ll1l_opy_ + bstack111l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ२")
  return bstack1l1l11l1ll_opy_
def bstack1ll11l1111_opy_(options):
  return hasattr(options, bstack111l_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ३"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l111l1ll_opy_(options, bstack1l1111l1l_opy_):
  for bstack1ll111l11l_opy_ in bstack1l1111l1l_opy_:
    if bstack1ll111l11l_opy_ in [bstack111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ४"), bstack111l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ५")]:
      continue
    if bstack1ll111l11l_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll111l11l_opy_] = update(options._experimental_options[bstack1ll111l11l_opy_],
                                                         bstack1l1111l1l_opy_[bstack1ll111l11l_opy_])
    else:
      options.add_experimental_option(bstack1ll111l11l_opy_, bstack1l1111l1l_opy_[bstack1ll111l11l_opy_])
  if bstack111l_opy_ (u"ࠫࡦࡸࡧࡴࠩ६") in bstack1l1111l1l_opy_:
    for arg in bstack1l1111l1l_opy_[bstack111l_opy_ (u"ࠬࡧࡲࡨࡵࠪ७")]:
      options.add_argument(arg)
    del (bstack1l1111l1l_opy_[bstack111l_opy_ (u"࠭ࡡࡳࡩࡶࠫ८")])
  if bstack111l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ९") in bstack1l1111l1l_opy_:
    for ext in bstack1l1111l1l_opy_[bstack111l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ॰")]:
      options.add_extension(ext)
    del (bstack1l1111l1l_opy_[bstack111l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॱ")])
def bstack1ll111llll_opy_(options, bstack1ll1l1ll1l_opy_):
  if bstack111l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩॲ") in bstack1ll1l1ll1l_opy_:
    for bstack1ll11lll1l_opy_ in bstack1ll1l1ll1l_opy_[bstack111l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪॳ")]:
      if bstack1ll11lll1l_opy_ in options._preferences:
        options._preferences[bstack1ll11lll1l_opy_] = update(options._preferences[bstack1ll11lll1l_opy_], bstack1ll1l1ll1l_opy_[bstack111l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫॴ")][bstack1ll11lll1l_opy_])
      else:
        options.set_preference(bstack1ll11lll1l_opy_, bstack1ll1l1ll1l_opy_[bstack111l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ")][bstack1ll11lll1l_opy_])
  if bstack111l_opy_ (u"ࠧࡢࡴࡪࡷࠬॶ") in bstack1ll1l1ll1l_opy_:
    for arg in bstack1ll1l1ll1l_opy_[bstack111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ")]:
      options.add_argument(arg)
def bstack1ll1l1l11l_opy_(options, bstack1lll1l111l_opy_):
  if bstack111l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪॸ") in bstack1lll1l111l_opy_:
    options.use_webview(bool(bstack1lll1l111l_opy_[bstack111l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫॹ")]))
  bstack1l111l1ll_opy_(options, bstack1lll1l111l_opy_)
def bstack1l1l1llll1_opy_(options, bstack1ll1lllll_opy_):
  for bstack1lll1llll_opy_ in bstack1ll1lllll_opy_:
    if bstack1lll1llll_opy_ in [bstack111l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨॺ"), bstack111l_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")]:
      continue
    options.set_capability(bstack1lll1llll_opy_, bstack1ll1lllll_opy_[bstack1lll1llll_opy_])
  if bstack111l_opy_ (u"࠭ࡡࡳࡩࡶࠫॼ") in bstack1ll1lllll_opy_:
    for arg in bstack1ll1lllll_opy_[bstack111l_opy_ (u"ࠧࡢࡴࡪࡷࠬॽ")]:
      options.add_argument(arg)
  if bstack111l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬॾ") in bstack1ll1lllll_opy_:
    options.bstack1l111111l_opy_(bool(bstack1ll1lllll_opy_[bstack111l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ॿ")]))
def bstack1l1111lll1_opy_(options, bstack111l1l11_opy_):
  for bstack1ll1llll1_opy_ in bstack111l1l11_opy_:
    if bstack1ll1llll1_opy_ in [bstack111l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧঀ"), bstack111l_opy_ (u"ࠫࡦࡸࡧࡴࠩঁ")]:
      continue
    options._options[bstack1ll1llll1_opy_] = bstack111l1l11_opy_[bstack1ll1llll1_opy_]
  if bstack111l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩং") in bstack111l1l11_opy_:
    for bstack111ll1l11_opy_ in bstack111l1l11_opy_[bstack111l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ")]:
      options.bstack1lllll1l1l_opy_(
        bstack111ll1l11_opy_, bstack111l1l11_opy_[bstack111l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঄")][bstack111ll1l11_opy_])
  if bstack111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭অ") in bstack111l1l11_opy_:
    for arg in bstack111l1l11_opy_[bstack111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧআ")]:
      options.add_argument(arg)
def bstack1l11l1ll11_opy_(options, caps):
  if not hasattr(options, bstack111l_opy_ (u"ࠪࡏࡊ࡟ࠧই")):
    return
  if options.KEY == bstack111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩঈ") and options.KEY in caps:
    bstack1l111l1ll_opy_(options, caps[bstack111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪউ")])
  elif options.KEY == bstack111l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫঊ") and options.KEY in caps:
    bstack1ll111llll_opy_(options, caps[bstack111l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঋ")])
  elif options.KEY == bstack111l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঌ") and options.KEY in caps:
    bstack1l1l1llll1_opy_(options, caps[bstack111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ঍")])
  elif options.KEY == bstack111l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ঎") and options.KEY in caps:
    bstack1ll1l1l11l_opy_(options, caps[bstack111l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬএ")])
  elif options.KEY == bstack111l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫঐ") and options.KEY in caps:
    bstack1l1111lll1_opy_(options, caps[bstack111l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ঑")])
def bstack11ll1lll1_opy_(caps):
  global bstack1ll1l1ll_opy_
  if isinstance(os.environ.get(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ঒")), str):
    bstack1ll1l1ll_opy_ = eval(os.getenv(bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩও")))
  if bstack1ll1l1ll_opy_:
    if bstack11l1l1ll1_opy_() < version.parse(bstack111l_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨঔ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪক")
    if bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩখ") in caps:
      browser = caps[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ")]
    elif bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧঘ") in caps:
      browser = caps[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨঙ")]
    browser = str(browser).lower()
    if browser == bstack111l_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨচ") or browser == bstack111l_opy_ (u"ࠩ࡬ࡴࡦࡪࠧছ"):
      browser = bstack111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪজ")
    if browser == bstack111l_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬঝ"):
      browser = bstack111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬঞ")
    if browser not in [bstack111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ট"), bstack111l_opy_ (u"ࠧࡦࡦࡪࡩࠬঠ"), bstack111l_opy_ (u"ࠨ࡫ࡨࠫড"), bstack111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩঢ"), bstack111l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫণ")]:
      return None
    try:
      package = bstack111l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ত").format(browser)
      name = bstack111l_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭থ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1ll11l1111_opy_(options):
        return None
      for bstack1ll1l11l_opy_ in caps.keys():
        options.set_capability(bstack1ll1l11l_opy_, caps[bstack1ll1l11l_opy_])
      bstack1l11l1ll11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lll111l_opy_(options, bstack1l11ll111l_opy_):
  if not bstack1ll11l1111_opy_(options):
    return
  for bstack1ll1l11l_opy_ in bstack1l11ll111l_opy_.keys():
    if bstack1ll1l11l_opy_ in bstack1111ll111_opy_:
      continue
    if bstack1ll1l11l_opy_ in options._caps and type(options._caps[bstack1ll1l11l_opy_]) in [dict, list]:
      options._caps[bstack1ll1l11l_opy_] = update(options._caps[bstack1ll1l11l_opy_], bstack1l11ll111l_opy_[bstack1ll1l11l_opy_])
    else:
      options.set_capability(bstack1ll1l11l_opy_, bstack1l11ll111l_opy_[bstack1ll1l11l_opy_])
  bstack1l11l1ll11_opy_(options, bstack1l11ll111l_opy_)
  if bstack111l_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬদ") in options._caps:
    if options._caps[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬধ")] and options._caps[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ন")].lower() != bstack111l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ঩"):
      del options._caps[bstack111l_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩপ")]
def bstack11llll1l11_opy_(proxy_config):
  if bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨফ") in proxy_config:
    proxy_config[bstack111l_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧব")] = proxy_config[bstack111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪভ")]
    del (proxy_config[bstack111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম")])
  if bstack111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫয") in proxy_config and proxy_config[bstack111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬর")].lower() != bstack111l_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪ঱"):
    proxy_config[bstack111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল")] = bstack111l_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬ঳")
  if bstack111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫ঴") in proxy_config:
    proxy_config[bstack111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack111l_opy_ (u"ࠨࡲࡤࡧࠬশ")
  return proxy_config
def bstack1ll1111l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨষ") in config:
    return proxy
  config[bstack111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩস")] = bstack11llll1l11_opy_(config[bstack111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪহ")])
  if proxy == None:
    proxy = Proxy(config[bstack111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺")])
  return proxy
def bstack1l111l11_opy_(self):
  global CONFIG
  global bstack1l1l1l1l_opy_
  try:
    proxy = bstack1l1ll11l11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111l_opy_ (u"࠭࠮ࡱࡣࡦࠫ঻")):
        proxies = bstack11ll11l1_opy_(proxy, bstack1l11l1ll1l_opy_())
        if len(proxies) > 0:
          protocol, bstack11lllll1_opy_ = proxies.popitem()
          if bstack111l_opy_ (u"ࠢ࠻࠱࠲়ࠦ") in bstack11lllll1_opy_:
            return bstack11lllll1_opy_
          else:
            return bstack111l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤঽ") + bstack11lllll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨা").format(str(e)))
  return bstack1l1l1l1l_opy_(self)
def bstack1ll111lll1_opy_():
  global CONFIG
  return bstack1l1ll1ll1_opy_(CONFIG) and bstack11lll11ll1_opy_() and bstack11lll11111_opy_() >= version.parse(bstack1111l111l_opy_)
def bstack1111l11ll_opy_():
  global CONFIG
  return (bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ি") in CONFIG or bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨী") in CONFIG) and bstack1l11lll1_opy_()
def bstack11ll1llll1_opy_(config):
  bstack1llll1ll_opy_ = {}
  if bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩু") in config:
    bstack1llll1ll_opy_ = config[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪূ")]
  if bstack111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ৃ") in config:
    bstack1llll1ll_opy_ = config[bstack111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧৄ")]
  proxy = bstack1l1ll11l11_opy_(config)
  if proxy:
    if proxy.endswith(bstack111l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৅")) and os.path.isfile(proxy):
      bstack1llll1ll_opy_[bstack111l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৆")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩে")):
        proxies = bstack1ll1ll1l11_opy_(config, bstack1l11l1ll1l_opy_())
        if len(proxies) > 0:
          protocol, bstack11lllll1_opy_ = proxies.popitem()
          if bstack111l_opy_ (u"ࠧࡀ࠯࠰ࠤৈ") in bstack11lllll1_opy_:
            parsed_url = urlparse(bstack11lllll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111l_opy_ (u"ࠨ࠺࠰࠱ࠥ৉") + bstack11lllll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1llll1ll_opy_[bstack111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ৊")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1llll1ll_opy_[bstack111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫো")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1llll1ll_opy_[bstack111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬৌ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1llll1ll_opy_[bstack111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ্࠭")] = str(parsed_url.password)
  return bstack1llll1ll_opy_
def bstack1lllll1ll_opy_(config):
  if bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩৎ") in config:
    return config[bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪ৏")]
  return {}
def bstack1l1ll11ll1_opy_(caps):
  global bstack1ll111l1l_opy_
  if bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৐") in caps:
    caps[bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ৑")][bstack111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ৒")] = True
    if bstack1ll111l1l_opy_:
      caps[bstack111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓")][bstack111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৔")] = bstack1ll111l1l_opy_
  else:
    caps[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ৕")] = True
    if bstack1ll111l1l_opy_:
      caps[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৖")] = bstack1ll111l1l_opy_
def bstack1ll1l11111_opy_():
  global CONFIG
  if not bstack1l1ll111l1_opy_(CONFIG):
    return
  if bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪৗ") in CONFIG and bstack111lll11l_opy_(CONFIG[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ৘")]):
    if (
      bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ৙") in CONFIG
      and bstack111lll11l_opy_(CONFIG[bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৚")].get(bstack111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ৛")))
    ):
      logger.debug(bstack111l_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧড়"))
      return
    bstack1llll1ll_opy_ = bstack11ll1llll1_opy_(CONFIG)
    bstack11111l1ll_opy_(CONFIG[bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨঢ়")], bstack1llll1ll_opy_)
def bstack11111l1ll_opy_(key, bstack1llll1ll_opy_):
  global bstack11ll1l1l_opy_
  logger.info(bstack1l1lll1ll_opy_)
  try:
    bstack11ll1l1l_opy_ = Local()
    bstack1lll1l1111_opy_ = {bstack111l_opy_ (u"࠭࡫ࡦࡻࠪ৞"): key}
    bstack1lll1l1111_opy_.update(bstack1llll1ll_opy_)
    logger.debug(bstack1111ll1ll_opy_.format(str(bstack1lll1l1111_opy_)))
    bstack11ll1l1l_opy_.start(**bstack1lll1l1111_opy_)
    if bstack11ll1l1l_opy_.isRunning():
      logger.info(bstack11lll1l11_opy_)
  except Exception as e:
    bstack1llll1l1_opy_(bstack1l11ll1111_opy_.format(str(e)))
def bstack1ll1ll11l_opy_():
  global bstack11ll1l1l_opy_
  if bstack11ll1l1l_opy_.isRunning():
    logger.info(bstack1l1ll1111_opy_)
    bstack11ll1l1l_opy_.stop()
  bstack11ll1l1l_opy_ = None
def bstack1llll111_opy_(bstack11lll1ll11_opy_=[]):
  global CONFIG
  bstack11l1111l1_opy_ = []
  bstack1l1lll1l1_opy_ = [bstack111l_opy_ (u"ࠧࡰࡵࠪয়"), bstack111l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫৠ"), bstack111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ৡ"), bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬৢ"), bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩৣ"), bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৤")]
  try:
    for err in bstack11lll1ll11_opy_:
      bstack111l1l1ll_opy_ = {}
      for k in bstack1l1lll1l1_opy_:
        val = CONFIG[bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৥")][int(err[bstack111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭০")])].get(k)
        if val:
          bstack111l1l1ll_opy_[k] = val
      if(err[bstack111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ১")] != bstack111l_opy_ (u"ࠩࠪ২")):
        bstack111l1l1ll_opy_[bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩ৩")] = {
          err[bstack111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ৪")]: err[bstack111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")]
        }
        bstack11l1111l1_opy_.append(bstack111l1l1ll_opy_)
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ৬") + str(e))
  finally:
    return bstack11l1111l1_opy_
def bstack1lll11ll11_opy_(file_name):
  bstack11lllll11l_opy_ = []
  try:
    bstack1ll1l11ll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1ll1l11ll_opy_):
      with open(bstack1ll1l11ll_opy_) as f:
        bstack111l11ll_opy_ = json.load(f)
        bstack11lllll11l_opy_ = bstack111l11ll_opy_
      os.remove(bstack1ll1l11ll_opy_)
    return bstack11lllll11l_opy_
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩ࡭ࡳࡪࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡯࡭ࡸࡺ࠺ࠡࠩ৭") + str(e))
    return bstack11lllll11l_opy_
def bstack111lllll_opy_():
  global bstack1ll11ll1ll_opy_
  global bstack1l11l1l1_opy_
  global bstack1ll1l1lll_opy_
  global bstack1llll1l1ll_opy_
  global bstack1l1ll11l1_opy_
  global bstack1ll1ll1l_opy_
  global CONFIG
  bstack1l11l1l1l1_opy_ = os.environ.get(bstack111l_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ৮"))
  if bstack1l11l1l1l1_opy_ in [bstack111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ৯"), bstack111l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩৰ")]:
    bstack111ll111_opy_()
  percy.shutdown()
  if bstack1ll11ll1ll_opy_:
    logger.warning(bstack11lllll1l1_opy_.format(str(bstack1ll11ll1ll_opy_)))
  else:
    try:
      bstack11lllllll1_opy_ = bstack11lll111l1_opy_(bstack111l_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪৱ"), logger)
      if bstack11lllllll1_opy_.get(bstack111l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ৲")) and bstack11lllllll1_opy_.get(bstack111l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ৳")).get(bstack111l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ৴")):
        logger.warning(bstack11lllll1l1_opy_.format(str(bstack11lllllll1_opy_[bstack111l_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭৵")][bstack111l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ৶")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1lllllll1_opy_)
  global bstack11ll1l1l_opy_
  if bstack11ll1l1l_opy_:
    bstack1ll1ll11l_opy_()
  try:
    for driver in bstack1l11l1l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1lll1111ll_opy_)
  if bstack1ll1ll1l_opy_ == bstack111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ৷"):
    bstack1l1ll11l1_opy_ = bstack1lll11ll11_opy_(bstack111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ৸"))
  if bstack1ll1ll1l_opy_ == bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ৹") and len(bstack1llll1l1ll_opy_) == 0:
    bstack1llll1l1ll_opy_ = bstack1lll11ll11_opy_(bstack111l_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ৺"))
    if len(bstack1llll1l1ll_opy_) == 0:
      bstack1llll1l1ll_opy_ = bstack1lll11ll11_opy_(bstack111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭৻"))
  bstack1llll1l111_opy_ = bstack111l_opy_ (u"ࠨࠩৼ")
  if len(bstack1ll1l1lll_opy_) > 0:
    bstack1llll1l111_opy_ = bstack1llll111_opy_(bstack1ll1l1lll_opy_)
  elif len(bstack1llll1l1ll_opy_) > 0:
    bstack1llll1l111_opy_ = bstack1llll111_opy_(bstack1llll1l1ll_opy_)
  elif len(bstack1l1ll11l1_opy_) > 0:
    bstack1llll1l111_opy_ = bstack1llll111_opy_(bstack1l1ll11l1_opy_)
  elif len(bstack1ll111ll_opy_) > 0:
    bstack1llll1l111_opy_ = bstack1llll111_opy_(bstack1ll111ll_opy_)
  if bool(bstack1llll1l111_opy_):
    bstack1ll11l11l_opy_(bstack1llll1l111_opy_)
  else:
    bstack1ll11l11l_opy_()
  bstack1l1ll1lll1_opy_(bstack1l111lll_opy_, logger)
  bstack11lll1lll1_opy_.bstack11l11l1l1_opy_(CONFIG)
  if len(bstack1l1ll11l1_opy_) > 0:
    sys.exit(len(bstack1l1ll11l1_opy_))
def bstack11ll11ll_opy_(bstack1lll11llll_opy_, frame):
  global bstack1l1ll1l111_opy_
  logger.error(bstack1lllll11_opy_)
  bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬ৽"), bstack1lll11llll_opy_)
  if hasattr(signal, bstack111l_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫ৾")):
    bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫ৿"), signal.Signals(bstack1lll11llll_opy_).name)
  else:
    bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ਀"), bstack111l_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਁ"))
  bstack1l11l1l1l1_opy_ = os.environ.get(bstack111l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਂ"))
  if bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਃ"):
    bstack11ll111ll_opy_.stop(bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ਄")))
  bstack111lllll_opy_()
  sys.exit(1)
def bstack1llll1l1_opy_(err):
  logger.critical(bstack1l1lll1111_opy_.format(str(err)))
  bstack1ll11l11l_opy_(bstack1l1lll1111_opy_.format(str(err)), True)
  atexit.unregister(bstack111lllll_opy_)
  bstack111ll111_opy_()
  sys.exit(1)
def bstack1l1l1l1lll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll11l11l_opy_(message, True)
  atexit.unregister(bstack111lllll_opy_)
  bstack111ll111_opy_()
  sys.exit(1)
def bstack11lll1l111_opy_():
  global CONFIG
  global bstack1lll111ll1_opy_
  global bstack1ll1ll111l_opy_
  global bstack1l1lll11l1_opy_
  CONFIG = bstack11l1lll1l_opy_()
  load_dotenv(CONFIG.get(bstack111l_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਅ")))
  bstack1l1ll111_opy_()
  bstack1l1l1ll1_opy_()
  CONFIG = bstack111l111l1_opy_(CONFIG)
  update(CONFIG, bstack1ll1ll111l_opy_)
  update(CONFIG, bstack1lll111ll1_opy_)
  CONFIG = bstack1l11ll111_opy_(CONFIG)
  bstack1l1lll11l1_opy_ = bstack1l1ll111l1_opy_(CONFIG)
  os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧਆ")] = bstack1l1lll11l1_opy_.__str__()
  bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਇ"), bstack1l1lll11l1_opy_)
  if (bstack111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਈ") in CONFIG and bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਉ") in bstack1lll111ll1_opy_) or (
          bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਊ") in CONFIG and bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ਋") not in bstack1ll1ll111l_opy_):
    if os.getenv(bstack111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ਌")):
      CONFIG[bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭਍")] = os.getenv(bstack111l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ਎"))
    else:
      bstack111llll11_opy_()
  elif (bstack111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਏ") not in CONFIG and bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਐ") in CONFIG) or (
          bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਑") in bstack1ll1ll111l_opy_ and bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ਒") not in bstack1lll111ll1_opy_):
    del (CONFIG[bstack111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬਓ")])
  if bstack1l11l111l_opy_(CONFIG):
    bstack1llll1l1_opy_(bstack1ll1l1l1l_opy_)
  bstack1l1llllll_opy_()
  bstack1ll111ll1l_opy_()
  if bstack1ll1l1ll_opy_:
    CONFIG[bstack111l_opy_ (u"ࠫࡦࡶࡰࠨਔ")] = bstack1l111lll1_opy_(CONFIG)
    logger.info(bstack1l1l1lllll_opy_.format(CONFIG[bstack111l_opy_ (u"ࠬࡧࡰࡱࠩਕ")]))
  if not bstack1l1lll11l1_opy_:
    CONFIG[bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਖ")] = [{}]
def bstack1l1l11l1_opy_(config, bstack1111l1l1l_opy_):
  global CONFIG
  global bstack1ll1l1ll_opy_
  CONFIG = config
  bstack1ll1l1ll_opy_ = bstack1111l1l1l_opy_
def bstack1ll111ll1l_opy_():
  global CONFIG
  global bstack1ll1l1ll_opy_
  if bstack111l_opy_ (u"ࠧࡢࡲࡳࠫਗ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1l1l1lll_opy_(e, bstack1l111llll1_opy_)
    bstack1ll1l1ll_opy_ = True
    bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧਘ"), True)
def bstack1l111lll1_opy_(config):
  bstack1lll1l11_opy_ = bstack111l_opy_ (u"ࠩࠪਙ")
  app = config[bstack111l_opy_ (u"ࠪࡥࡵࡶࠧਚ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lllll1ll1_opy_:
      if os.path.exists(app):
        bstack1lll1l11_opy_ = bstack1llllll11l_opy_(config, app)
      elif bstack1l1111l11_opy_(app):
        bstack1lll1l11_opy_ = app
      else:
        bstack1llll1l1_opy_(bstack1l111111ll_opy_.format(app))
    else:
      if bstack1l1111l11_opy_(app):
        bstack1lll1l11_opy_ = app
      elif os.path.exists(app):
        bstack1lll1l11_opy_ = bstack1llllll11l_opy_(app)
      else:
        bstack1llll1l1_opy_(bstack1l1111ll1_opy_)
  else:
    if len(app) > 2:
      bstack1llll1l1_opy_(bstack111l1ll1l_opy_)
    elif len(app) == 2:
      if bstack111l_opy_ (u"ࠫࡵࡧࡴࡩࠩਛ") in app and bstack111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨਜ") in app:
        if os.path.exists(app[bstack111l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫਝ")]):
          bstack1lll1l11_opy_ = bstack1llllll11l_opy_(config, app[bstack111l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬਞ")], app[bstack111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫਟ")])
        else:
          bstack1llll1l1_opy_(bstack1l111111ll_opy_.format(app))
      else:
        bstack1llll1l1_opy_(bstack111l1ll1l_opy_)
    else:
      for key in app:
        if key in bstack1llllll11_opy_:
          if key == bstack111l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧਠ"):
            if os.path.exists(app[key]):
              bstack1lll1l11_opy_ = bstack1llllll11l_opy_(config, app[key])
            else:
              bstack1llll1l1_opy_(bstack1l111111ll_opy_.format(app))
          else:
            bstack1lll1l11_opy_ = app[key]
        else:
          bstack1llll1l1_opy_(bstack11llll11_opy_)
  return bstack1lll1l11_opy_
def bstack1l1111l11_opy_(bstack1lll1l11_opy_):
  import re
  bstack1ll1llll1l_opy_ = re.compile(bstack111l_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥਡ"))
  bstack1llllll111_opy_ = re.compile(bstack111l_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣਢ"))
  if bstack111l_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫਣ") in bstack1lll1l11_opy_ or re.fullmatch(bstack1ll1llll1l_opy_, bstack1lll1l11_opy_) or re.fullmatch(bstack1llllll111_opy_, bstack1lll1l11_opy_):
    return True
  else:
    return False
def bstack1llllll11l_opy_(config, path, bstack1ll111ll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111l_opy_ (u"࠭ࡲࡣࠩਤ")).read()).hexdigest()
  bstack1lll11l11_opy_ = bstack1l11l1l111_opy_(md5_hash)
  bstack1lll1l11_opy_ = None
  if bstack1lll11l11_opy_:
    logger.info(bstack11lll111ll_opy_.format(bstack1lll11l11_opy_, md5_hash))
    return bstack1lll11l11_opy_
  bstack11lllll11_opy_ = MultipartEncoder(
    fields={
      bstack111l_opy_ (u"ࠧࡧ࡫࡯ࡩࠬਥ"): (os.path.basename(path), open(os.path.abspath(path), bstack111l_opy_ (u"ࠨࡴࡥࠫਦ")), bstack111l_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭ਧ")),
      bstack111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ਨ"): bstack1ll111ll1_opy_
    }
  )
  response = requests.post(bstack11l111ll1_opy_, data=bstack11lllll11_opy_,
                           headers={bstack111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ਩"): bstack11lllll11_opy_.content_type},
                           auth=(config[bstack111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧਪ")], config[bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩਫ")]))
  try:
    res = json.loads(response.text)
    bstack1lll1l11_opy_ = res[bstack111l_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨਬ")]
    logger.info(bstack11lll1l1l1_opy_.format(bstack1lll1l11_opy_))
    bstack11llll1ll1_opy_(md5_hash, bstack1lll1l11_opy_)
  except ValueError as err:
    bstack1llll1l1_opy_(bstack1l1llll1l1_opy_.format(str(err)))
  return bstack1lll1l11_opy_
def bstack1l1llllll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l1l11111_opy_
  bstack1ll1l11l11_opy_ = 1
  bstack1l1l1111ll_opy_ = 1
  if bstack111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨਭ") in CONFIG:
    bstack1l1l1111ll_opy_ = CONFIG[bstack111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩਮ")]
  else:
    bstack1l1l1111ll_opy_ = bstack1lll1111l_opy_(framework_name, args) or 1
  if bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ") in CONFIG:
    bstack1ll1l11l11_opy_ = len(CONFIG[bstack111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਰ")])
  bstack1l1l11111_opy_ = int(bstack1l1l1111ll_opy_) * int(bstack1ll1l11l11_opy_)
def bstack1lll1111l_opy_(framework_name, args):
  if framework_name == bstack1l11l1lll_opy_ and args and bstack111l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ਱") in args:
      bstack1lll11l1ll_opy_ = args.index(bstack111l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫਲ"))
      return int(args[bstack1lll11l1ll_opy_ + 1]) or 1
  return 1
def bstack1l11l1l111_opy_(md5_hash):
  bstack11l1l1l1l_opy_ = os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠧࡿࠩਲ਼")), bstack111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ਴"), bstack111l_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪਵ"))
  if os.path.exists(bstack11l1l1l1l_opy_):
    bstack111l11l11_opy_ = json.load(open(bstack11l1l1l1l_opy_, bstack111l_opy_ (u"ࠪࡶࡧ࠭ਸ਼")))
    if md5_hash in bstack111l11l11_opy_:
      bstack1l111l1l1_opy_ = bstack111l11l11_opy_[md5_hash]
      bstack1llll11l1l_opy_ = datetime.datetime.now()
      bstack1ll1l1111_opy_ = datetime.datetime.strptime(bstack1l111l1l1_opy_[bstack111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ਷")], bstack111l_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩਸ"))
      if (bstack1llll11l1l_opy_ - bstack1ll1l1111_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l111l1l1_opy_[bstack111l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫਹ")]):
        return None
      return bstack1l111l1l1_opy_[bstack111l_opy_ (u"ࠧࡪࡦࠪ਺")]
  else:
    return None
def bstack11llll1ll1_opy_(md5_hash, bstack1lll1l11_opy_):
  bstack1l1lll1ll1_opy_ = os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠨࢀࠪ਻")), bstack111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬਼ࠩ"))
  if not os.path.exists(bstack1l1lll1ll1_opy_):
    os.makedirs(bstack1l1lll1ll1_opy_)
  bstack11l1l1l1l_opy_ = os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠪࢂࠬ਽")), bstack111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਾ"), bstack111l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ਿ"))
  bstack1lllll1l11_opy_ = {
    bstack111l_opy_ (u"࠭ࡩࡥࠩੀ"): bstack1lll1l11_opy_,
    bstack111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪੁ"): datetime.datetime.strftime(datetime.datetime.now(), bstack111l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬੂ")),
    bstack111l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ੃"): str(__version__)
  }
  if os.path.exists(bstack11l1l1l1l_opy_):
    bstack111l11l11_opy_ = json.load(open(bstack11l1l1l1l_opy_, bstack111l_opy_ (u"ࠪࡶࡧ࠭੄")))
  else:
    bstack111l11l11_opy_ = {}
  bstack111l11l11_opy_[md5_hash] = bstack1lllll1l11_opy_
  with open(bstack11l1l1l1l_opy_, bstack111l_opy_ (u"ࠦࡼ࠱ࠢ੅")) as outfile:
    json.dump(bstack111l11l11_opy_, outfile)
def bstack1l11l111_opy_(self):
  return
def bstack1lll1l1l11_opy_(self):
  return
def bstack1111l1l1_opy_(self):
  global bstack111l1111_opy_
  bstack111l1111_opy_(self)
def bstack1l111l111l_opy_():
  global bstack1l111l11l1_opy_
  bstack1l111l11l1_opy_ = True
def bstack1lllll111l_opy_(self):
  global bstack11lll1111_opy_
  global bstack1l1l11l1l1_opy_
  global bstack1ll1ll1l1_opy_
  try:
    if bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ੆") in bstack11lll1111_opy_ and self.session_id != None and bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪੇ"), bstack111l_opy_ (u"ࠧࠨੈ")) != bstack111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ੉"):
      bstack1111l111_opy_ = bstack111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੊") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪੋ")
      if bstack1111l111_opy_ == bstack111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫੌ"):
        bstack1l11llll1l_opy_(logger)
      if self != None:
        bstack111111ll_opy_(self, bstack1111l111_opy_, bstack111l_opy_ (u"ࠬ࠲ࠠࠨ੍").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111l_opy_ (u"࠭ࠧ੎")
    if bstack111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੏") in bstack11lll1111_opy_ and getattr(threading.current_thread(), bstack111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੐"), None):
      bstack1l1lllll11_opy_.bstack11l1111l_opy_(self, bstack1111llll1_opy_, logger, wait=True)
    if bstack111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩੑ") in bstack11lll1111_opy_:
      if not threading.currentThread().behave_test_status:
        bstack111111ll_opy_(self, bstack111l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ੒"))
      bstack1l1l111l1_opy_.bstack1111lll1l_opy_(self)
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ੓") + str(e))
  bstack1ll1ll1l1_opy_(self)
  self.session_id = None
def bstack1l11111l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1ll1111111_opy_
    global bstack11lll1111_opy_
    command_executor = kwargs.get(bstack111l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ੔"), bstack111l_opy_ (u"࠭ࠧ੕"))
    bstack1ll11l111_opy_ = False
    if type(command_executor) == str and bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ੖") in command_executor:
      bstack1ll11l111_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ੗") in str(getattr(command_executor, bstack111l_opy_ (u"ࠩࡢࡹࡷࡲࠧ੘"), bstack111l_opy_ (u"ࠪࠫਖ਼"))):
      bstack1ll11l111_opy_ = True
    else:
      return bstack1l1111l1ll_opy_(self, *args, **kwargs)
    if bstack1ll11l111_opy_:
      bstack1ll11lll1_opy_ = bstack1l1l1l11l_opy_.bstack1llll11l_opy_(CONFIG, bstack11lll1111_opy_)
      if kwargs.get(bstack111l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬਗ਼")):
        kwargs[bstack111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ਜ਼")] = bstack1ll1111111_opy_(kwargs[bstack111l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧੜ")], bstack11lll1111_opy_, bstack1ll11lll1_opy_)
      elif kwargs.get(bstack111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ੝")):
        kwargs[bstack111l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨਫ਼")] = bstack1ll1111111_opy_(kwargs[bstack111l_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ੟")], bstack11lll1111_opy_, bstack1ll11lll1_opy_)
  except Exception as e:
    logger.error(bstack111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ੠").format(str(e)))
  return bstack1l1111l1ll_opy_(self, *args, **kwargs)
def bstack1l11ll1ll_opy_(self, command_executor=bstack111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ੡"), *args, **kwargs):
  bstack1l11l1111_opy_ = bstack1l11111l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1lll1lllll_opy_.on():
    return bstack1l11l1111_opy_
  try:
    logger.debug(bstack111l_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩ੢").format(str(command_executor)))
    logger.debug(bstack111l_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨ੣").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ੤") in command_executor._url:
      bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ੥"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ੦") in command_executor):
    bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ੧"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1l11111l_opy_ = getattr(threading.current_thread(), bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ੨"), None)
  if bstack111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ੩") in bstack11lll1111_opy_ or bstack111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ੪") in bstack11lll1111_opy_:
    bstack11ll111ll_opy_.bstack1l111l1l_opy_(self)
  if bstack111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੫") in bstack11lll1111_opy_ and bstack1l1l11111l_opy_ and bstack1l1l11111l_opy_.get(bstack111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੬"), bstack111l_opy_ (u"ࠩࠪ੭")) == bstack111l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ੮"):
    bstack11ll111ll_opy_.bstack1l111l1l_opy_(self)
  return bstack1l11l1111_opy_
def bstack11111111l_opy_(args):
  return bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬ੯") in str(args)
def bstack111lll1ll_opy_(self, driver_command, *args, **kwargs):
  global bstack1lll11l11l_opy_
  global bstack1ll1111ll1_opy_
  bstack1l1l111l11_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩੰ"), None) and bstack1l1llll1l_opy_(
          threading.current_thread(), bstack111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬੱ"), None)
  bstack1l1111111l_opy_ = getattr(self, bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧੲ"), None) != None and getattr(self, bstack111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨੳ"), None) == True
  if not bstack1ll1111ll1_opy_ and bstack1l1lll11l1_opy_ and bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩੴ") in CONFIG and CONFIG[bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪੵ")] == True and bstack111111l11_opy_.bstack11l1l111_opy_(driver_command) and (bstack1l1111111l_opy_ or bstack1l1l111l11_opy_) and not bstack11111111l_opy_(args):
    try:
      bstack1ll1111ll1_opy_ = True
      logger.debug(bstack111l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭੶").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack111l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪ੷").format(str(err)))
    bstack1ll1111ll1_opy_ = False
  response = bstack1lll11l11l_opy_(self, driver_command, *args, **kwargs)
  if (bstack111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ੸") in str(bstack11lll1111_opy_).lower() or bstack111l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ੹") in str(bstack11lll1111_opy_).lower()) and bstack1lll1lllll_opy_.on():
    try:
      if driver_command == bstack111l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ੺"):
        bstack11ll111ll_opy_.bstack1lll11ll_opy_({
            bstack111l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ੻"): response[bstack111l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ੼")],
            bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ੽"): bstack11ll111ll_opy_.current_test_uuid() if bstack11ll111ll_opy_.current_test_uuid() else bstack1lll1lllll_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1l1l1ll1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1l1l11l1l1_opy_
  global bstack1lll1llll1_opy_
  global bstack1llllllll_opy_
  global bstack1ll1l1l1_opy_
  global bstack1ll11l1l_opy_
  global bstack11lll1111_opy_
  global bstack1l1111l1ll_opy_
  global bstack1l11l1l1_opy_
  global bstack1lllllllll_opy_
  global bstack1111llll1_opy_
  CONFIG[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ੾")] = str(bstack11lll1111_opy_) + str(__version__)
  bstack111ll1111_opy_ = os.environ[bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ੿")]
  bstack1ll11lll1_opy_ = bstack1l1l1l11l_opy_.bstack1llll11l_opy_(CONFIG, bstack11lll1111_opy_)
  CONFIG[bstack111l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ઀")] = bstack111ll1111_opy_
  CONFIG[bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪઁ")] = bstack1ll11lll1_opy_
  command_executor = bstack1l11l1ll1l_opy_()
  logger.debug(bstack1l1l1l11ll_opy_.format(command_executor))
  proxy = bstack1ll1111l1_opy_(CONFIG, proxy)
  bstack1l11lll11l_opy_ = 0 if bstack1lll1llll1_opy_ < 0 else bstack1lll1llll1_opy_
  try:
    if bstack1ll1l1l1_opy_ is True:
      bstack1l11lll11l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1ll11l1l_opy_ is True:
      bstack1l11lll11l_opy_ = int(threading.current_thread().name)
  except:
    bstack1l11lll11l_opy_ = 0
  bstack1l11ll111l_opy_ = bstack1lll11l1l1_opy_(CONFIG, bstack1l11lll11l_opy_)
  logger.debug(bstack1l1l1l1l1l_opy_.format(str(bstack1l11ll111l_opy_)))
  if bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ં") in CONFIG and bstack111lll11l_opy_(CONFIG[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧઃ")]):
    bstack1l1ll11ll1_opy_(bstack1l11ll111l_opy_)
  if bstack1lll111ll_opy_.bstack1l1111l1_opy_(CONFIG, bstack1l11lll11l_opy_) and bstack1lll111ll_opy_.bstack1lllll111_opy_(bstack1l11ll111l_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1lll111ll_opy_.set_capabilities(bstack1l11ll111l_opy_, CONFIG)
  if desired_capabilities:
    bstack11ll1lll_opy_ = bstack111l111l1_opy_(desired_capabilities)
    bstack11ll1lll_opy_[bstack111l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ઄")] = bstack1llll1lll1_opy_(CONFIG)
    bstack1llll111ll_opy_ = bstack1lll11l1l1_opy_(bstack11ll1lll_opy_)
    if bstack1llll111ll_opy_:
      bstack1l11ll111l_opy_ = update(bstack1llll111ll_opy_, bstack1l11ll111l_opy_)
    desired_capabilities = None
  if options:
    bstack1lll111l_opy_(options, bstack1l11ll111l_opy_)
  if not options:
    options = bstack11ll1lll1_opy_(bstack1l11ll111l_opy_)
  bstack1111llll1_opy_ = CONFIG.get(bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨઅ"))[bstack1l11lll11l_opy_]
  if proxy and bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭આ")):
    options.proxy(proxy)
  if options and bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ઇ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11lll11111_opy_() < version.parse(bstack111l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧઈ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l11ll111l_opy_)
  logger.info(bstack1ll1ll11_opy_)
  if bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩઉ")):
    bstack1l1111l1ll_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩઊ")):
    bstack1l1111l1ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫઋ")):
    bstack1l1111l1ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1111l1ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack11ll1ll1_opy_ = bstack111l_opy_ (u"ࠬ࠭ઌ")
    if bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧઍ")):
      bstack11ll1ll1_opy_ = self.caps.get(bstack111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ઎"))
    else:
      bstack11ll1ll1_opy_ = self.capabilities.get(bstack111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣએ"))
    if bstack11ll1ll1_opy_:
      bstack1ll1l111_opy_(bstack11ll1ll1_opy_)
      if bstack11lll11111_opy_() <= version.parse(bstack111l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩઐ")):
        self.command_executor._url = bstack111l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦઑ") + bstack1l111ll1l_opy_ + bstack111l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ઒")
      else:
        self.command_executor._url = bstack111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢઓ") + bstack11ll1ll1_opy_ + bstack111l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢઔ")
      logger.debug(bstack1111l11l_opy_.format(bstack11ll1ll1_opy_))
    else:
      logger.debug(bstack1llllll1ll_opy_.format(bstack111l_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣક")))
  except Exception as e:
    logger.debug(bstack1llllll1ll_opy_.format(e))
  if bstack111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧખ") in bstack11lll1111_opy_:
    bstack1l1llll11l_opy_(bstack1lll1llll1_opy_, bstack1lllllllll_opy_)
  bstack1l1l11l1l1_opy_ = self.session_id
  if bstack111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩગ") in bstack11lll1111_opy_ or bstack111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪઘ") in bstack11lll1111_opy_ or bstack111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪઙ") in bstack11lll1111_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1l11111l_opy_ = getattr(threading.current_thread(), bstack111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭ચ"), None)
  if bstack111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭છ") in bstack11lll1111_opy_ or bstack111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭જ") in bstack11lll1111_opy_:
    bstack11ll111ll_opy_.bstack1l111l1l_opy_(self)
  if bstack111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨઝ") in bstack11lll1111_opy_ and bstack1l1l11111l_opy_ and bstack1l1l11111l_opy_.get(bstack111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩઞ"), bstack111l_opy_ (u"ࠪࠫટ")) == bstack111l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬઠ"):
    bstack11ll111ll_opy_.bstack1l111l1l_opy_(self)
  bstack1l11l1l1_opy_.append(self)
  if bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨડ") in CONFIG and bstack111l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫઢ") in CONFIG[bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪણ")][bstack1l11lll11l_opy_]:
    bstack1llllllll_opy_ = CONFIG[bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫત")][bstack1l11lll11l_opy_][bstack111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧથ")]
  logger.debug(bstack1lll1ll11_opy_.format(bstack1l1l11l1l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11l111ll_opy_
    def bstack11l1lll11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll1lll1l1_opy_
      if(bstack111l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧદ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠫࢃ࠭ધ")), bstack111l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬન"), bstack111l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ઩")), bstack111l_opy_ (u"ࠧࡸࠩપ")) as fp:
          fp.write(bstack111l_opy_ (u"ࠣࠤફ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦબ")))):
          with open(args[1], bstack111l_opy_ (u"ࠪࡶࠬભ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111l_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪમ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11lll1ll1l_opy_)
            if bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩય") in CONFIG and str(CONFIG[bstack111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪર")]).lower() != bstack111l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭઱"):
                bstack1l111lllll_opy_ = bstack11l111ll_opy_()
                bstack1l1l11ll11_opy_ = bstack111l_opy_ (u"ࠨࠩࠪࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡀࠐࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠ࠿ࠏࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬ࠿ࠏࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࠐࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁࡻࠋࠢࠣࡰࡪࡺࠠࡤࡣࡳࡷࡀࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠎࠥࠦࡴࡳࡻࠣࡿࢀࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠏࠦࠠࠡࠢࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡀࠐࠠࠡࡿࢀࠤࡨࡧࡴࡤࡪࠣࠬࡪࡾࠩࠡࡽࡾࠎࠥࠦࠠࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࡨࡶࡷࡵࡲࠩࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠽ࠦ࠱ࠦࡥࡹࠫ࠾ࠎࠥࠦࡽࡾࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶࠫࡿࢀࠐࠠࠡࠢࠣࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺ࠺ࠡࠩࡾࡧࡩࡶࡕࡳ࡮ࢀࠫࠥ࠱ࠠࡦࡰࡦࡳࡩ࡫ࡕࡓࡋࡆࡳࡲࡶ࡯࡯ࡧࡱࡸ࠭ࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡣࡢࡲࡶ࠭࠮࠲ࠊࠡࠢࠣࠤ࠳࠴࠮࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠊࠡࠢࢀࢁ࠮ࡁࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠎࢂࢃ࠻ࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠎ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠊࠨࠩࠪલ").format(bstack1l111lllll_opy_=bstack1l111lllll_opy_)
            lines.insert(1, bstack1l1l11ll11_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦળ")), bstack111l_opy_ (u"ࠪࡻࠬ઴")) as bstack1lll1111_opy_:
              bstack1lll1111_opy_.writelines(lines)
        CONFIG[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭વ")] = str(bstack11lll1111_opy_) + str(__version__)
        bstack111ll1111_opy_ = os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪશ")]
        bstack1ll11lll1_opy_ = bstack1l1l1l11l_opy_.bstack1llll11l_opy_(CONFIG, bstack11lll1111_opy_)
        CONFIG[bstack111l_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩષ")] = bstack111ll1111_opy_
        CONFIG[bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩસ")] = bstack1ll11lll1_opy_
        bstack1l11lll11l_opy_ = 0 if bstack1lll1llll1_opy_ < 0 else bstack1lll1llll1_opy_
        try:
          if bstack1ll1l1l1_opy_ is True:
            bstack1l11lll11l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1ll11l1l_opy_ is True:
            bstack1l11lll11l_opy_ = int(threading.current_thread().name)
        except:
          bstack1l11lll11l_opy_ = 0
        CONFIG[bstack111l_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣહ")] = False
        CONFIG[bstack111l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ઺")] = True
        bstack1l11ll111l_opy_ = bstack1lll11l1l1_opy_(CONFIG, bstack1l11lll11l_opy_)
        logger.debug(bstack1l1l1l1l1l_opy_.format(str(bstack1l11ll111l_opy_)))
        if CONFIG.get(bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ઻")):
          bstack1l1ll11ll1_opy_(bstack1l11ll111l_opy_)
        if bstack111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ઼ࠧ") in CONFIG and bstack111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪઽ") in CONFIG[bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩા")][bstack1l11lll11l_opy_]:
          bstack1llllllll_opy_ = CONFIG[bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪિ")][bstack1l11lll11l_opy_][bstack111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ી")]
        args.append(os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠩࢁࠫુ")), bstack111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪૂ"), bstack111l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ૃ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l11ll111l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢૄ"))
      bstack1ll1lll1l1_opy_ = True
      return bstack1ll1l1l111_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll11l1lll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1lll1llll1_opy_
    global bstack1llllllll_opy_
    global bstack1ll1l1l1_opy_
    global bstack1ll11l1l_opy_
    global bstack11lll1111_opy_
    CONFIG[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨૅ")] = str(bstack11lll1111_opy_) + str(__version__)
    bstack111ll1111_opy_ = os.environ[bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ૆")]
    bstack1ll11lll1_opy_ = bstack1l1l1l11l_opy_.bstack1llll11l_opy_(CONFIG, bstack11lll1111_opy_)
    CONFIG[bstack111l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫે")] = bstack111ll1111_opy_
    CONFIG[bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫૈ")] = bstack1ll11lll1_opy_
    bstack1l11lll11l_opy_ = 0 if bstack1lll1llll1_opy_ < 0 else bstack1lll1llll1_opy_
    try:
      if bstack1ll1l1l1_opy_ is True:
        bstack1l11lll11l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1ll11l1l_opy_ is True:
        bstack1l11lll11l_opy_ = int(threading.current_thread().name)
    except:
      bstack1l11lll11l_opy_ = 0
    CONFIG[bstack111l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤૉ")] = True
    bstack1l11ll111l_opy_ = bstack1lll11l1l1_opy_(CONFIG, bstack1l11lll11l_opy_)
    logger.debug(bstack1l1l1l1l1l_opy_.format(str(bstack1l11ll111l_opy_)))
    if CONFIG.get(bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ૊")):
      bstack1l1ll11ll1_opy_(bstack1l11ll111l_opy_)
    if bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨો") in CONFIG and bstack111l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫૌ") in CONFIG[bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ્ࠪ")][bstack1l11lll11l_opy_]:
      bstack1llllllll_opy_ = CONFIG[bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૎")][bstack1l11lll11l_opy_][bstack111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ૏")]
    import urllib
    import json
    if bstack111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧૐ") in CONFIG and str(CONFIG[bstack111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ૑")]).lower() != bstack111l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ૒"):
        bstack1l1llll11_opy_ = bstack11l111ll_opy_()
        bstack1l111lllll_opy_ = bstack1l1llll11_opy_ + urllib.parse.quote(json.dumps(bstack1l11ll111l_opy_))
    else:
        bstack1l111lllll_opy_ = bstack111l_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ૓") + urllib.parse.quote(json.dumps(bstack1l11ll111l_opy_))
    browser = self.connect(bstack1l111lllll_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll1lll11l_opy_():
    global bstack1ll1lll1l1_opy_
    global bstack11lll1111_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11l11l1l_opy_
        global bstack1l1ll1l111_opy_
        if not bstack1l1lll11l1_opy_:
          global bstack1ll1lll1_opy_
          if not bstack1ll1lll1_opy_:
            from bstack_utils.helper import bstack11ll11ll1_opy_, bstack1ll1llll11_opy_, bstack1ll1ll1ll1_opy_
            bstack1ll1lll1_opy_ = bstack11ll11ll1_opy_()
            bstack1ll1llll11_opy_(bstack11lll1111_opy_)
            bstack1ll11lll1_opy_ = bstack1l1l1l11l_opy_.bstack1llll11l_opy_(CONFIG, bstack11lll1111_opy_)
            bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ૔"), bstack1ll11lll1_opy_)
          BrowserType.connect = bstack11l11l1l_opy_
          return
        BrowserType.launch = bstack1ll11l1lll_opy_
        bstack1ll1lll1l1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l1lll11_opy_
      bstack1ll1lll1l1_opy_ = True
    except Exception as e:
      pass
def bstack1l1lll111_opy_(context, bstack11llllllll_opy_):
  try:
    context.page.evaluate(bstack111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ૕"), bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭૖")+ json.dumps(bstack11llllllll_opy_) + bstack111l_opy_ (u"ࠥࢁࢂࠨ૗"))
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤ૘"), e)
def bstack1lll1l1l1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ૙"), bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૚") + json.dumps(message) + bstack111l_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪ૛") + json.dumps(level) + bstack111l_opy_ (u"ࠨࡿࢀࠫ૜"))
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧ૝"), e)
def bstack1l11l111l1_opy_(self, url):
  global bstack1l1lllll1_opy_
  try:
    bstack1l1111l1l1_opy_(url)
  except Exception as err:
    logger.debug(bstack1llll11ll_opy_.format(str(err)))
  try:
    bstack1l1lllll1_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1llllll1_opy_ = str(e)
      if any(err_msg in bstack1l1llllll1_opy_ for err_msg in bstack1ll1l111ll_opy_):
        bstack1l1111l1l1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1llll11ll_opy_.format(str(err)))
    raise e
def bstack1l1lllll1l_opy_(self):
  global bstack11lll11l_opy_
  bstack11lll11l_opy_ = self
  return
def bstack11111llll_opy_(self):
  global bstack1l11llll_opy_
  bstack1l11llll_opy_ = self
  return
def bstack11ll11lll_opy_(test_name, bstack1lllll1l1_opy_):
  global CONFIG
  if percy.bstack1ll11llll1_opy_() == bstack111l_opy_ (u"ࠥࡸࡷࡻࡥࠣ૞"):
    bstack1l11111ll1_opy_ = os.path.relpath(bstack1lllll1l1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l11111ll1_opy_)
    bstack1l111ll11_opy_ = suite_name + bstack111l_opy_ (u"ࠦ࠲ࠨ૟") + test_name
    threading.current_thread().percySessionName = bstack1l111ll11_opy_
def bstack1l1ll1l1l1_opy_(self, test, *args, **kwargs):
  global bstack1lll1lll1l_opy_
  test_name = None
  bstack1lllll1l1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1lllll1l1_opy_ = str(test.source)
  bstack11ll11lll_opy_(test_name, bstack1lllll1l1_opy_)
  bstack1lll1lll1l_opy_(self, test, *args, **kwargs)
def bstack111llllll_opy_(driver, bstack1l111ll11_opy_):
  if not bstack1l1l1lll_opy_ and bstack1l111ll11_opy_:
      bstack11l11l1ll_opy_ = {
          bstack111l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬૠ"): bstack111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧૡ"),
          bstack111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪૢ"): {
              bstack111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ૣ"): bstack1l111ll11_opy_
          }
      }
      bstack1l1lll111l_opy_ = bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ૤").format(json.dumps(bstack11l11l1ll_opy_))
      driver.execute_script(bstack1l1lll111l_opy_)
  if bstack11llll1l_opy_:
      bstack11llll11l1_opy_ = {
          bstack111l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ૥"): bstack111l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭૦"),
          bstack111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ૧"): {
              bstack111l_opy_ (u"࠭ࡤࡢࡶࡤࠫ૨"): bstack1l111ll11_opy_ + bstack111l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ૩"),
              bstack111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ૪"): bstack111l_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ૫")
          }
      }
      if bstack11llll1l_opy_.status == bstack111l_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ૬"):
          bstack11ll1l11_opy_ = bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ૭").format(json.dumps(bstack11llll11l1_opy_))
          driver.execute_script(bstack11ll1l11_opy_)
          bstack111111ll_opy_(driver, bstack111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ૮"))
      elif bstack11llll1l_opy_.status == bstack111l_opy_ (u"࠭ࡆࡂࡋࡏࠫ૯"):
          reason = bstack111l_opy_ (u"ࠢࠣ૰")
          bstack1lll11l1l_opy_ = bstack1l111ll11_opy_ + bstack111l_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩ૱")
          if bstack11llll1l_opy_.message:
              reason = str(bstack11llll1l_opy_.message)
              bstack1lll11l1l_opy_ = bstack1lll11l1l_opy_ + bstack111l_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩ૲") + reason
          bstack11llll11l1_opy_[bstack111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭૳")] = {
              bstack111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ૴"): bstack111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ૵"),
              bstack111l_opy_ (u"࠭ࡤࡢࡶࡤࠫ૶"): bstack1lll11l1l_opy_
          }
          bstack11ll1l11_opy_ = bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ૷").format(json.dumps(bstack11llll11l1_opy_))
          driver.execute_script(bstack11ll1l11_opy_)
          bstack111111ll_opy_(driver, bstack111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ૸"), reason)
          bstack1l111ll1_opy_(reason, str(bstack11llll1l_opy_), str(bstack1lll1llll1_opy_), logger)
def bstack11lll1l11l_opy_(driver, test):
  if percy.bstack1ll11llll1_opy_() == bstack111l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢૹ") and percy.bstack1l1ll1ll_opy_() == bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧૺ"):
      bstack111111ll1_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧૻ"), None)
      bstack1llll1ll1_opy_(driver, bstack111111ll1_opy_, test)
  if bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩૼ"), None) and bstack1l1llll1l_opy_(
          threading.current_thread(), bstack111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ૽"), None):
      logger.info(bstack111l_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠦࠢ૾"))
      bstack1lll111ll_opy_.bstack1l11lllll_opy_(driver, name=test.name, path=test.source)
def bstack11111l11_opy_(test, bstack1l111ll11_opy_):
    try:
      data = {}
      if test:
        data[bstack111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭૿")] = bstack1l111ll11_opy_
      if bstack11llll1l_opy_:
        if bstack11llll1l_opy_.status == bstack111l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ଀"):
          data[bstack111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪଁ")] = bstack111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଂ")
        elif bstack11llll1l_opy_.status == bstack111l_opy_ (u"ࠬࡌࡁࡊࡎࠪଃ"):
          data[bstack111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭଄")] = bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧଅ")
          if bstack11llll1l_opy_.message:
            data[bstack111l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨଆ")] = str(bstack11llll1l_opy_.message)
      user = CONFIG[bstack111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫଇ")]
      key = CONFIG[bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ଈ")]
      url = bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩଉ").format(user, key, bstack1l1l11l1l1_opy_)
      headers = {
        bstack111l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫଊ"): bstack111l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩଋ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll111l11_opy_.format(str(e)))
def bstack1l1l1ll1l1_opy_(test, bstack1l111ll11_opy_):
  global CONFIG
  global bstack1l11llll_opy_
  global bstack11lll11l_opy_
  global bstack1l1l11l1l1_opy_
  global bstack11llll1l_opy_
  global bstack1llllllll_opy_
  global bstack11111l1l_opy_
  global bstack1111ll1l_opy_
  global bstack1l11l11ll_opy_
  global bstack1llll111l_opy_
  global bstack1l11l1l1_opy_
  global bstack1111llll1_opy_
  try:
    if not bstack1l1l11l1l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠧࡿࠩଌ")), bstack111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ଍"), bstack111l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ଎"))) as f:
        bstack1ll1l111l1_opy_ = json.loads(bstack111l_opy_ (u"ࠥࡿࠧଏ") + f.read().strip() + bstack111l_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ଐ") + bstack111l_opy_ (u"ࠧࢃࠢ଑"))
        bstack1l1l11l1l1_opy_ = bstack1ll1l111l1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l11l1l1_opy_:
    for driver in bstack1l11l1l1_opy_:
      if bstack1l1l11l1l1_opy_ == driver.session_id:
        if test:
          bstack11lll1l11l_opy_(driver, test)
        bstack111llllll_opy_(driver, bstack1l111ll11_opy_)
  elif bstack1l1l11l1l1_opy_:
    bstack11111l11_opy_(test, bstack1l111ll11_opy_)
  if bstack1l11llll_opy_:
    bstack1111ll1l_opy_(bstack1l11llll_opy_)
  if bstack11lll11l_opy_:
    bstack1l11l11ll_opy_(bstack11lll11l_opy_)
  if bstack1l111l11l1_opy_:
    bstack1llll111l_opy_()
def bstack1ll111l111_opy_(self, test, *args, **kwargs):
  bstack1l111ll11_opy_ = None
  if test:
    bstack1l111ll11_opy_ = str(test.name)
  bstack1l1l1ll1l1_opy_(test, bstack1l111ll11_opy_)
  bstack11111l1l_opy_(self, test, *args, **kwargs)
def bstack1111l1ll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l11lllll1_opy_
  global CONFIG
  global bstack1l11l1l1_opy_
  global bstack1l1l11l1l1_opy_
  bstack11ll1lllll_opy_ = None
  try:
    if bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ଒"), None):
      try:
        if not bstack1l1l11l1l1_opy_:
          with open(os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠧࡿࠩଓ")), bstack111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨଔ"), bstack111l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫକ"))) as f:
            bstack1ll1l111l1_opy_ = json.loads(bstack111l_opy_ (u"ࠥࡿࠧଖ") + f.read().strip() + bstack111l_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ଗ") + bstack111l_opy_ (u"ࠧࢃࠢଘ"))
            bstack1l1l11l1l1_opy_ = bstack1ll1l111l1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l11l1l1_opy_:
        for driver in bstack1l11l1l1_opy_:
          if bstack1l1l11l1l1_opy_ == driver.session_id:
            bstack11ll1lllll_opy_ = driver
    bstack1l1l1111l1_opy_ = bstack1lll111ll_opy_.bstack1111lll11_opy_(test.tags)
    if bstack11ll1lllll_opy_:
      threading.current_thread().isA11yTest = bstack1lll111ll_opy_.bstack1lll111111_opy_(bstack11ll1lllll_opy_, bstack1l1l1111l1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l1l1111l1_opy_
  except:
    pass
  bstack1l11lllll1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11llll1l_opy_
  bstack11llll1l_opy_ = self._test
def bstack11lll1111l_opy_():
  global bstack1llll1l1l_opy_
  try:
    if os.path.exists(bstack1llll1l1l_opy_):
      os.remove(bstack1llll1l1l_opy_)
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩଙ") + str(e))
def bstack1lll11ll1l_opy_():
  global bstack1llll1l1l_opy_
  bstack11lllllll1_opy_ = {}
  try:
    if not os.path.isfile(bstack1llll1l1l_opy_):
      with open(bstack1llll1l1l_opy_, bstack111l_opy_ (u"ࠧࡸࠩଚ")):
        pass
      with open(bstack1llll1l1l_opy_, bstack111l_opy_ (u"ࠣࡹ࠮ࠦଛ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1llll1l1l_opy_):
      bstack11lllllll1_opy_ = json.load(open(bstack1llll1l1l_opy_, bstack111l_opy_ (u"ࠩࡵࡦࠬଜ")))
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬଝ") + str(e))
  finally:
    return bstack11lllllll1_opy_
def bstack1l1llll11l_opy_(platform_index, item_index):
  global bstack1llll1l1l_opy_
  try:
    bstack11lllllll1_opy_ = bstack1lll11ll1l_opy_()
    bstack11lllllll1_opy_[item_index] = platform_index
    with open(bstack1llll1l1l_opy_, bstack111l_opy_ (u"ࠦࡼ࠱ࠢଞ")) as outfile:
      json.dump(bstack11lllllll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪଟ") + str(e))
def bstack1llllllll1_opy_(bstack1ll1l11ll1_opy_):
  global CONFIG
  bstack1l1l1l1l1_opy_ = bstack111l_opy_ (u"࠭ࠧଠ")
  if not bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଡ") in CONFIG:
    logger.info(bstack111l_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬଢ"))
  try:
    platform = CONFIG[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଣ")][bstack1ll1l11ll1_opy_]
    if bstack111l_opy_ (u"ࠪࡳࡸ࠭ତ") in platform:
      bstack1l1l1l1l1_opy_ += str(platform[bstack111l_opy_ (u"ࠫࡴࡹࠧଥ")]) + bstack111l_opy_ (u"ࠬ࠲ࠠࠨଦ")
    if bstack111l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩଧ") in platform:
      bstack1l1l1l1l1_opy_ += str(platform[bstack111l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪନ")]) + bstack111l_opy_ (u"ࠨ࠮ࠣࠫ଩")
    if bstack111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ପ") in platform:
      bstack1l1l1l1l1_opy_ += str(platform[bstack111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧଫ")]) + bstack111l_opy_ (u"ࠫ࠱ࠦࠧବ")
    if bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧଭ") in platform:
      bstack1l1l1l1l1_opy_ += str(platform[bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨମ")]) + bstack111l_opy_ (u"ࠧ࠭ࠢࠪଯ")
    if bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ର") in platform:
      bstack1l1l1l1l1_opy_ += str(platform[bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ଱")]) + bstack111l_opy_ (u"ࠪ࠰ࠥ࠭ଲ")
    if bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଳ") in platform:
      bstack1l1l1l1l1_opy_ += str(platform[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭଴")]) + bstack111l_opy_ (u"࠭ࠬࠡࠩଵ")
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧଶ") + str(e))
  finally:
    if bstack1l1l1l1l1_opy_[len(bstack1l1l1l1l1_opy_) - 2:] == bstack111l_opy_ (u"ࠨ࠮ࠣࠫଷ"):
      bstack1l1l1l1l1_opy_ = bstack1l1l1l1l1_opy_[:-2]
    return bstack1l1l1l1l1_opy_
def bstack1lll1l111_opy_(path, bstack1l1l1l1l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l111ll1l1_opy_ = ET.parse(path)
    bstack1l1l11l11l_opy_ = bstack1l111ll1l1_opy_.getroot()
    bstack1l11111ll_opy_ = None
    for suite in bstack1l1l11l11l_opy_.iter(bstack111l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨସ")):
      if bstack111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪହ") in suite.attrib:
        suite.attrib[bstack111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ଺")] += bstack111l_opy_ (u"ࠬࠦࠧ଻") + bstack1l1l1l1l1_opy_
        bstack1l11111ll_opy_ = suite
    bstack1111111l_opy_ = None
    for robot in bstack1l1l11l11l_opy_.iter(bstack111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ଼ࠬ")):
      bstack1111111l_opy_ = robot
    bstack11ll1111_opy_ = len(bstack1111111l_opy_.findall(bstack111l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ଽ")))
    if bstack11ll1111_opy_ == 1:
      bstack1111111l_opy_.remove(bstack1111111l_opy_.findall(bstack111l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧା"))[0])
      bstack1l1ll11ll_opy_ = ET.Element(bstack111l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨି"), attrib={bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨୀ"): bstack111l_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫୁ"), bstack111l_opy_ (u"ࠬ࡯ࡤࠨୂ"): bstack111l_opy_ (u"࠭ࡳ࠱ࠩୃ")})
      bstack1111111l_opy_.insert(1, bstack1l1ll11ll_opy_)
      bstack1l111llll_opy_ = None
      for suite in bstack1111111l_opy_.iter(bstack111l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ୄ")):
        bstack1l111llll_opy_ = suite
      bstack1l111llll_opy_.append(bstack1l11111ll_opy_)
      bstack1llll11l11_opy_ = None
      for status in bstack1l11111ll_opy_.iter(bstack111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ୅")):
        bstack1llll11l11_opy_ = status
      bstack1l111llll_opy_.append(bstack1llll11l11_opy_)
    bstack1l111ll1l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧ୆") + str(e))
def bstack1ll1l111l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11ll1l11l_opy_
  global CONFIG
  if bstack111l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢେ") in options:
    del options[bstack111l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣୈ")]
  bstack111llll1l_opy_ = bstack1lll11ll1l_opy_()
  for bstack1l1lll11_opy_ in bstack111llll1l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack111l_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬ୉"), str(bstack1l1lll11_opy_), bstack111l_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪ୊"))
    bstack1lll1l111_opy_(path, bstack1llllllll1_opy_(bstack111llll1l_opy_[bstack1l1lll11_opy_]))
  bstack11lll1111l_opy_()
  return bstack11ll1l11l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll11ll1_opy_(self, ff_profile_dir):
  global bstack1l11111l11_opy_
  if not ff_profile_dir:
    return None
  return bstack1l11111l11_opy_(self, ff_profile_dir)
def bstack11lll1ll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll111l1l_opy_
  bstack11llll1ll_opy_ = []
  if bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪୋ") in CONFIG:
    bstack11llll1ll_opy_ = CONFIG[bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫୌ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦ୍ࠥ")],
      pabot_args[bstack111l_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦ୎")],
      argfile,
      pabot_args.get(bstack111l_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ୏")),
      pabot_args[bstack111l_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ୐")],
      platform[0],
      bstack1ll111l1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111l_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ୑")] or [(bstack111l_opy_ (u"ࠢࠣ୒"), None)]
    for platform in enumerate(bstack11llll1ll_opy_)
  ]
def bstack11l1l1l11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1l11lll_opy_=bstack111l_opy_ (u"ࠨࠩ୓")):
  global bstack1l11llll11_opy_
  self.platform_index = platform_index
  self.bstack1l11lll1l1_opy_ = bstack1ll1l11lll_opy_
  bstack1l11llll11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l11111l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l111111_opy_
  global bstack1l1lll1l_opy_
  bstack1ll1l11l1l_opy_ = copy.deepcopy(item)
  if not bstack111l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ୔") in item.options:
    bstack1ll1l11l1l_opy_.options[bstack111l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ୕")] = []
  bstack1lll1lll_opy_ = bstack1ll1l11l1l_opy_.options[bstack111l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ୖ")].copy()
  for v in bstack1ll1l11l1l_opy_.options[bstack111l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧୗ")]:
    if bstack111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ୘") in v:
      bstack1lll1lll_opy_.remove(v)
    if bstack111l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ୙") in v:
      bstack1lll1lll_opy_.remove(v)
    if bstack111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ୚") in v:
      bstack1lll1lll_opy_.remove(v)
  bstack1lll1lll_opy_.insert(0, bstack111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ୛").format(bstack1ll1l11l1l_opy_.platform_index))
  bstack1lll1lll_opy_.insert(0, bstack111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪଡ଼").format(bstack1ll1l11l1l_opy_.bstack1l11lll1l1_opy_))
  bstack1ll1l11l1l_opy_.options[bstack111l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ଢ଼")] = bstack1lll1lll_opy_
  if bstack1l1lll1l_opy_:
    bstack1ll1l11l1l_opy_.options[bstack111l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ୞")].insert(0, bstack111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩୟ").format(bstack1l1lll1l_opy_))
  return bstack1l1l111111_opy_(caller_id, datasources, is_last, bstack1ll1l11l1l_opy_, outs_dir)
def bstack1ll1lll1l_opy_(command, item_index):
  if bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨୠ")):
    os.environ[bstack111l_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩୡ")] = json.dumps(CONFIG[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬୢ")][item_index % bstack1111l1111_opy_])
  global bstack1l1lll1l_opy_
  if bstack1l1lll1l_opy_:
    command[0] = command[0].replace(bstack111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩୣ"), bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ୤") + str(
      item_index) + bstack111l_opy_ (u"ࠬࠦࠧ୥") + bstack1l1lll1l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ୦"),
                                    bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫ୧") + str(item_index), 1)
def bstack1l11l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l111lll1l_opy_
  bstack1ll1lll1l_opy_(command, item_index)
  return bstack1l111lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1lll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l111lll1l_opy_
  bstack1ll1lll1l_opy_(command, item_index)
  return bstack1l111lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llll11ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l111lll1l_opy_
  bstack1ll1lll1l_opy_(command, item_index)
  return bstack1l111lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l11ll1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l11111l1l_opy_
  bstack111l1ll11_opy_ = bstack1l11111l1l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack111l_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨ୨")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111l_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭୩")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111l1ll11_opy_
def bstack1lll1l11l_opy_(runner, hook_name, context, element, bstack1ll11111_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1111llll_opy_.bstack111111l1l_opy_(hook_name, element)
    bstack1ll11111_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1111llll_opy_.bstack111111111_opy_(element)
      if hook_name not in [bstack111l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧ୪"), bstack111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧ୫")] and args and hasattr(args[0], bstack111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬ୬")):
        args[0].error_message = bstack111l_opy_ (u"࠭ࠧ୭")
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡬ࡦࡴࡤ࡭ࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩ୮").format(str(e)))
def bstack1lll111l1l_opy_(runner, name, context, bstack1ll11111_opy_, *args):
    if runner.hooks.get(bstack111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ୯")).__name__ != bstack111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧ୰"):
      bstack1lll1l11l_opy_(runner, name, context, runner, bstack1ll11111_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack111l1llll_opy_(bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩୱ")) else context.browser
      runner.driver_initialised = bstack111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ୲")
    except Exception as e:
      logger.debug(bstack111l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩ୳").format(str(e)))
def bstack1lllll11l_opy_(runner, name, context, bstack1ll11111_opy_, *args):
    bstack1lll1l11l_opy_(runner, name, context, context.feature, bstack1ll11111_opy_, *args)
    try:
      if not bstack1l1l1lll_opy_:
        bstack11ll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1llll_opy_(bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ୴")) else context.browser
        if is_driver_active(bstack11ll1lllll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ୵")
          bstack11llllllll_opy_ = str(runner.feature.name)
          bstack1l1lll111_opy_(context, bstack11llllllll_opy_)
          bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭୶") + json.dumps(bstack11llllllll_opy_) + bstack111l_opy_ (u"ࠩࢀࢁࠬ୷"))
    except Exception as e:
      logger.debug(bstack111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ୸").format(str(e)))
def bstack111ll1l1l_opy_(runner, name, context, bstack1ll11111_opy_, *args):
    if hasattr(context, bstack111l_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭୹")):
        bstack1111llll_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack111l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ୺")) else context.feature
    bstack1lll1l11l_opy_(runner, name, context, target, bstack1ll11111_opy_, *args)
def bstack111lllll1_opy_(runner, name, context, bstack1ll11111_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1111llll_opy_.start_test(context)
    bstack1lll1l11l_opy_(runner, name, context, context.scenario, bstack1ll11111_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l1l111l1_opy_.bstack1l1l1ll11_opy_(context, *args)
    try:
      bstack11ll1lllll_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ୻"), context.browser)
      if is_driver_active(bstack11ll1lllll_opy_):
        bstack11ll111ll_opy_.bstack1l111l1l_opy_(bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭୼"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ୽")
        if (not bstack1l1l1lll_opy_):
          scenario_name = args[0].name
          feature_name = bstack11llllllll_opy_ = str(runner.feature.name)
          bstack11llllllll_opy_ = feature_name + bstack111l_opy_ (u"ࠩࠣ࠱ࠥ࠭୾") + scenario_name
          if runner.driver_initialised == bstack111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ୿"):
            bstack1l1lll111_opy_(context, bstack11llllllll_opy_)
            bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ஀") + json.dumps(bstack11llllllll_opy_) + bstack111l_opy_ (u"ࠬࢃࡽࠨ஁"))
    except Exception as e:
      logger.debug(bstack111l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧஂ").format(str(e)))
def bstack1l1l111ll1_opy_(runner, name, context, bstack1ll11111_opy_, *args):
    bstack1lll1l11l_opy_(runner, name, context, args[0], bstack1ll11111_opy_, *args)
    try:
      bstack11ll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1llll_opy_(bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ஃ")) else context.browser
      if is_driver_active(bstack11ll1lllll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ஄")
        bstack1111llll_opy_.bstack1l1l1lll11_opy_(args[0])
        if runner.driver_initialised == bstack111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢஅ"):
          feature_name = bstack11llllllll_opy_ = str(runner.feature.name)
          bstack11llllllll_opy_ = feature_name + bstack111l_opy_ (u"ࠪࠤ࠲ࠦࠧஆ") + context.scenario.name
          bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩஇ") + json.dumps(bstack11llllllll_opy_) + bstack111l_opy_ (u"ࠬࢃࡽࠨஈ"))
    except Exception as e:
      logger.debug(bstack111l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪஉ").format(str(e)))
def bstack1ll11l1l11_opy_(runner, name, context, bstack1ll11111_opy_, *args):
  bstack1111llll_opy_.bstack11l11lll_opy_(args[0])
  try:
    bstack1l1ll1ll1l_opy_ = args[0].status.name
    bstack11ll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ஊ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11ll1lllll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack111l_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ஋")
        feature_name = bstack11llllllll_opy_ = str(runner.feature.name)
        bstack11llllllll_opy_ = feature_name + bstack111l_opy_ (u"ࠩࠣ࠱ࠥ࠭஌") + context.scenario.name
        bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ஍") + json.dumps(bstack11llllllll_opy_) + bstack111l_opy_ (u"ࠫࢂࢃࠧஎ"))
    if str(bstack1l1ll1ll1l_opy_).lower() == bstack111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬஏ"):
      bstack1l1l1llll_opy_ = bstack111l_opy_ (u"࠭ࠧஐ")
      bstack1ll1ll11ll_opy_ = bstack111l_opy_ (u"ࠧࠨ஑")
      bstack1l1111ll_opy_ = bstack111l_opy_ (u"ࠨࠩஒ")
      try:
        import traceback
        bstack1l1l1llll_opy_ = runner.exception.__class__.__name__
        bstack1llllll1l1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll1ll11ll_opy_ = bstack111l_opy_ (u"ࠩࠣࠫஓ").join(bstack1llllll1l1_opy_)
        bstack1l1111ll_opy_ = bstack1llllll1l1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1111111_opy_.format(str(e)))
      bstack1l1l1llll_opy_ += bstack1l1111ll_opy_
      bstack1lll1l1l1l_opy_(context, json.dumps(str(args[0].name) + bstack111l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤஔ") + str(bstack1ll1ll11ll_opy_)),
                          bstack111l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥக"))
      if runner.driver_initialised == bstack111l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ஖"):
        bstack1l11lll1ll_opy_(getattr(context, bstack111l_opy_ (u"࠭ࡰࡢࡩࡨࠫ஗"), None), bstack111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ஘"), bstack1l1l1llll_opy_)
        bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ங") + json.dumps(str(args[0].name) + bstack111l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣச") + str(bstack1ll1ll11ll_opy_)) + bstack111l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ஛"))
      if runner.driver_initialised == bstack111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤஜ"):
        bstack111111ll_opy_(bstack11ll1lllll_opy_, bstack111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ஝"), bstack111l_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥஞ") + str(bstack1l1l1llll_opy_))
    else:
      bstack1lll1l1l1l_opy_(context, bstack111l_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣட"), bstack111l_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ஠"))
      if runner.driver_initialised == bstack111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ஡"):
        bstack1l11lll1ll_opy_(getattr(context, bstack111l_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ஢"), None), bstack111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦண"))
      bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪத") + json.dumps(str(args[0].name) + bstack111l_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥ஥")) + bstack111l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭஦"))
      if runner.driver_initialised == bstack111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ஧"):
        bstack111111ll_opy_(bstack11ll1lllll_opy_, bstack111l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤந"))
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡴࡶࡨࡴ࠿ࠦࡻࡾࠩன").format(str(e)))
  bstack1lll1l11l_opy_(runner, name, context, args[0], bstack1ll11111_opy_, *args)
def bstack1llll11111_opy_(runner, name, context, bstack1ll11111_opy_, *args):
  bstack1111llll_opy_.end_test(args[0])
  try:
    bstack1l1l1l111_opy_ = args[0].status.name
    bstack11ll1lllll_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪப"), context.browser)
    bstack1l1l111l1_opy_.bstack1111lll1l_opy_(bstack11ll1lllll_opy_)
    if str(bstack1l1l1l111_opy_).lower() == bstack111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ஫"):
      bstack1l1l1llll_opy_ = bstack111l_opy_ (u"࠭ࠧ஬")
      bstack1ll1ll11ll_opy_ = bstack111l_opy_ (u"ࠧࠨ஭")
      bstack1l1111ll_opy_ = bstack111l_opy_ (u"ࠨࠩம")
      try:
        import traceback
        bstack1l1l1llll_opy_ = runner.exception.__class__.__name__
        bstack1llllll1l1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll1ll11ll_opy_ = bstack111l_opy_ (u"ࠩࠣࠫய").join(bstack1llllll1l1_opy_)
        bstack1l1111ll_opy_ = bstack1llllll1l1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1111111_opy_.format(str(e)))
      bstack1l1l1llll_opy_ += bstack1l1111ll_opy_
      bstack1lll1l1l1l_opy_(context, json.dumps(str(args[0].name) + bstack111l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤர") + str(bstack1ll1ll11ll_opy_)),
                          bstack111l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥற"))
      if runner.driver_initialised == bstack111l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢல") or runner.driver_initialised == bstack111l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ள"):
        bstack1l11lll1ll_opy_(getattr(context, bstack111l_opy_ (u"ࠧࡱࡣࡪࡩࠬழ"), None), bstack111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣவ"), bstack1l1l1llll_opy_)
        bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧஶ") + json.dumps(str(args[0].name) + bstack111l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤஷ") + str(bstack1ll1ll11ll_opy_)) + bstack111l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫஸ"))
      if runner.driver_initialised == bstack111l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢஹ") or runner.driver_initialised == bstack111l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭஺"):
        bstack111111ll_opy_(bstack11ll1lllll_opy_, bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ஻"), bstack111l_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ஼") + str(bstack1l1l1llll_opy_))
    else:
      bstack1lll1l1l1l_opy_(context, bstack111l_opy_ (u"ࠤࡓࡥࡸࡹࡥࡥࠣࠥ஽"), bstack111l_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣா"))
      if runner.driver_initialised == bstack111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨி") or runner.driver_initialised == bstack111l_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬீ"):
        bstack1l11lll1ll_opy_(getattr(context, bstack111l_opy_ (u"࠭ࡰࡢࡩࡨࠫு"), None), bstack111l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢூ"))
      bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭௃") + json.dumps(str(args[0].name) + bstack111l_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ௄")) + bstack111l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ௅"))
      if runner.driver_initialised == bstack111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨெ") or runner.driver_initialised == bstack111l_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬே"):
        bstack111111ll_opy_(bstack11ll1lllll_opy_, bstack111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨை"))
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ௉").format(str(e)))
  bstack1lll1l11l_opy_(runner, name, context, context.scenario, bstack1ll11111_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l11l11l_opy_(runner, name, context, bstack1ll11111_opy_, *args):
    target = context.scenario if hasattr(context, bstack111l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪொ")) else context.feature
    bstack1lll1l11l_opy_(runner, name, context, target, bstack1ll11111_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11lllll111_opy_(runner, name, context, bstack1ll11111_opy_, *args):
    try:
      bstack11ll1lllll_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨோ"), context.browser)
      if context.failed is True:
        bstack1ll1ll1l1l_opy_ = []
        bstack1ll11lll_opy_ = []
        bstack111ll11ll_opy_ = []
        bstack1111111ll_opy_ = bstack111l_opy_ (u"ࠪࠫௌ")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1ll1ll1l1l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1llllll1l1_opy_ = traceback.format_tb(exc_tb)
            bstack1l1lll1l1l_opy_ = bstack111l_opy_ (u"்ࠫࠥ࠭").join(bstack1llllll1l1_opy_)
            bstack1ll11lll_opy_.append(bstack1l1lll1l1l_opy_)
            bstack111ll11ll_opy_.append(bstack1llllll1l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1111111_opy_.format(str(e)))
        bstack1l1l1llll_opy_ = bstack111l_opy_ (u"ࠬ࠭௎")
        for i in range(len(bstack1ll1ll1l1l_opy_)):
          bstack1l1l1llll_opy_ += bstack1ll1ll1l1l_opy_[i] + bstack111ll11ll_opy_[i] + bstack111l_opy_ (u"࠭࡜࡯ࠩ௏")
        bstack1111111ll_opy_ = bstack111l_opy_ (u"ࠧࠡࠩௐ").join(bstack1ll11lll_opy_)
        if runner.driver_initialised in [bstack111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ௑"), bstack111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ௒")]:
          bstack1lll1l1l1l_opy_(context, bstack1111111ll_opy_, bstack111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ௓"))
          bstack1l11lll1ll_opy_(getattr(context, bstack111l_opy_ (u"ࠫࡵࡧࡧࡦࠩ௔"), None), bstack111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ௕"), bstack1l1l1llll_opy_)
          bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ௖") + json.dumps(bstack1111111ll_opy_) + bstack111l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧௗ"))
          bstack111111ll_opy_(bstack11ll1lllll_opy_, bstack111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ௘"), bstack111l_opy_ (u"ࠤࡖࡳࡲ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡡࡴࠢ௙") + str(bstack1l1l1llll_opy_))
          bstack11111ll1_opy_ = bstack1l111ll11l_opy_(bstack1111111ll_opy_, runner.feature.name, logger)
          if (bstack11111ll1_opy_ != None):
            bstack1ll111ll_opy_.append(bstack11111ll1_opy_)
      else:
        if runner.driver_initialised in [bstack111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ௚"), bstack111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ௛")]:
          bstack1lll1l1l1l_opy_(context, bstack111l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ௜") + str(runner.feature.name) + bstack111l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ௝"), bstack111l_opy_ (u"ࠢࡪࡰࡩࡳࠧ௞"))
          bstack1l11lll1ll_opy_(getattr(context, bstack111l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭௟"), None), bstack111l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ௠"))
          bstack11ll1lllll_opy_.execute_script(bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ௡") + json.dumps(bstack111l_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢ௢") + str(runner.feature.name) + bstack111l_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ௣")) + bstack111l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ௤"))
          bstack111111ll_opy_(bstack11ll1lllll_opy_, bstack111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ௥"))
          bstack11111ll1_opy_ = bstack1l111ll11l_opy_(bstack1111111ll_opy_, runner.feature.name, logger)
          if (bstack11111ll1_opy_ != None):
            bstack1ll111ll_opy_.append(bstack11111ll1_opy_)
    except Exception as e:
      logger.debug(bstack111l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ௦").format(str(e)))
    bstack1lll1l11l_opy_(runner, name, context, context.feature, bstack1ll11111_opy_, *args)
def bstack1lllll1111_opy_(runner, name, context, bstack1ll11111_opy_, *args):
    bstack1lll1l11l_opy_(runner, name, context, runner, bstack1ll11111_opy_, *args)
def bstack11l1ll11_opy_(self, name, context, *args):
  if bstack1l1lll11l1_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1111l1111_opy_
    bstack111ll1ll_opy_ = CONFIG[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௧")][platform_index]
    os.environ[bstack111l_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ௨")] = json.dumps(bstack111ll1ll_opy_)
  global bstack1ll11111_opy_
  if not hasattr(self, bstack111l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩ௩")):
    self.driver_initialised = None
  bstack1l1l1l1ll1_opy_ = {
      bstack111l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ௪"): bstack1lll111l1l_opy_,
      bstack111l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ௫"): bstack1lllll11l_opy_,
      bstack111l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫ௬"): bstack111ll1l1l_opy_,
      bstack111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ௭"): bstack111lllll1_opy_,
      bstack111l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧ௮"): bstack1l1l111ll1_opy_,
      bstack111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧ௯"): bstack1ll11l1l11_opy_,
      bstack111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ௰"): bstack1llll11111_opy_,
      bstack111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨ௱"): bstack1l11l11l_opy_,
      bstack111l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭௲"): bstack11lllll111_opy_,
      bstack111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ௳"): bstack1lllll1111_opy_
  }
  handler = bstack1l1l1l1ll1_opy_.get(name, bstack1ll11111_opy_)
  handler(self, name, context, bstack1ll11111_opy_, *args)
  if name in [bstack111l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ௴"), bstack111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ௵"), bstack111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭௶")]:
    try:
      bstack11ll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1llll_opy_(bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ௷")) else context.browser
      bstack11l111l1_opy_ = (
        (name == bstack111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ௸") and self.driver_initialised == bstack111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ௹")) or
        (name == bstack111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ௺") and self.driver_initialised == bstack111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ௻")) or
        (name == bstack111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ௼") and self.driver_initialised in [bstack111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௽"), bstack111l_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦ௾")]) or
        (name == bstack111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩ௿") and self.driver_initialised == bstack111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦఀ"))
      )
      if bstack11l111l1_opy_:
        self.driver_initialised = None
        bstack11ll1lllll_opy_.quit()
    except Exception:
      pass
def bstack111ll1l1_opy_(config, startdir):
  return bstack111l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧఁ").format(bstack111l_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢం"))
notset = Notset()
def bstack1ll11111ll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l11llllll_opy_
  if str(name).lower() == bstack111l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩః"):
    return bstack111l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤఄ")
  else:
    return bstack1l11llllll_opy_(self, name, default, skip)
def bstack11ll1lll1l_opy_(item, when):
  global bstack1l1111l11l_opy_
  try:
    bstack1l1111l11l_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll1lll11_opy_():
  return
def bstack1l11l1l1ll_opy_(type, name, status, reason, bstack1l1l11lll1_opy_, bstack11l11ll11_opy_):
  bstack11l11l1ll_opy_ = {
    bstack111l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫఅ"): type,
    bstack111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨఆ"): {}
  }
  if type == bstack111l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨఇ"):
    bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪఈ")][bstack111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧఉ")] = bstack1l1l11lll1_opy_
    bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬఊ")][bstack111l_opy_ (u"ࠪࡨࡦࡺࡡࠨఋ")] = json.dumps(str(bstack11l11ll11_opy_))
  if type == bstack111l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఌ"):
    bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ఍")][bstack111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫఎ")] = name
  if type == bstack111l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪఏ"):
    bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫఐ")][bstack111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ఑")] = status
    if status == bstack111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪఒ"):
      bstack11l11l1ll_opy_[bstack111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧఓ")][bstack111l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬఔ")] = json.dumps(str(reason))
  bstack1l1lll111l_opy_ = bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫక").format(json.dumps(bstack11l11l1ll_opy_))
  return bstack1l1lll111l_opy_
def bstack1l111l1l1l_opy_(driver_command, response):
    if driver_command == bstack111l_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫఖ"):
        bstack11ll111ll_opy_.bstack1lll11ll_opy_({
            bstack111l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧగ"): response[bstack111l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨఘ")],
            bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪఙ"): bstack11ll111ll_opy_.current_test_uuid()
        })
def bstack1l1l1ll111_opy_(item, call, rep):
  global bstack1l1ll11111_opy_
  global bstack1l11l1l1_opy_
  global bstack1l1l1lll_opy_
  name = bstack111l_opy_ (u"ࠫࠬచ")
  try:
    if rep.when == bstack111l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪఛ"):
      bstack1l1l11l1l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1l1lll_opy_:
          name = str(rep.nodeid)
          bstack111l1l111_opy_ = bstack1l11l1l1ll_opy_(bstack111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧజ"), name, bstack111l_opy_ (u"ࠧࠨఝ"), bstack111l_opy_ (u"ࠨࠩఞ"), bstack111l_opy_ (u"ࠩࠪట"), bstack111l_opy_ (u"ࠪࠫఠ"))
          threading.current_thread().bstack11llllll1l_opy_ = name
          for driver in bstack1l11l1l1_opy_:
            if bstack1l1l11l1l1_opy_ == driver.session_id:
              driver.execute_script(bstack111l1l111_opy_)
      except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫడ").format(str(e)))
      try:
        bstack1llll111l1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ఢ"):
          status = bstack111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ణ") if rep.outcome.lower() == bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧత") else bstack111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨథ")
          reason = bstack111l_opy_ (u"ࠩࠪద")
          if status == bstack111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪధ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩన") if status == bstack111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ఩") else bstack111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬప")
          data = name + bstack111l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩఫ") if status == bstack111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨబ") else name + bstack111l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬభ") + reason
          bstack1l111l111_opy_ = bstack1l11l1l1ll_opy_(bstack111l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬమ"), bstack111l_opy_ (u"ࠫࠬయ"), bstack111l_opy_ (u"ࠬ࠭ర"), bstack111l_opy_ (u"࠭ࠧఱ"), level, data)
          for driver in bstack1l11l1l1_opy_:
            if bstack1l1l11l1l1_opy_ == driver.session_id:
              driver.execute_script(bstack1l111l111_opy_)
      except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫల").format(str(e)))
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬళ").format(str(e)))
  bstack1l1ll11111_opy_(item, call, rep)
def bstack1llll1ll1_opy_(driver, bstack1lll11111l_opy_, test=None):
  global bstack1lll1llll1_opy_
  if test != None:
    bstack1ll11l1l1l_opy_ = getattr(test, bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧఴ"), None)
    bstack1ll1111lll_opy_ = getattr(test, bstack111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨవ"), None)
    PercySDK.screenshot(driver, bstack1lll11111l_opy_, bstack1ll11l1l1l_opy_=bstack1ll11l1l1l_opy_, bstack1ll1111lll_opy_=bstack1ll1111lll_opy_, bstack1l1111ll11_opy_=bstack1lll1llll1_opy_)
  else:
    PercySDK.screenshot(driver, bstack1lll11111l_opy_)
def bstack1l111l1l11_opy_(driver):
  if bstack11l11l111_opy_.bstack1l11l111ll_opy_() is True or bstack11l11l111_opy_.capturing() is True:
    return
  bstack11l11l111_opy_.bstack1ll111111_opy_()
  while not bstack11l11l111_opy_.bstack1l11l111ll_opy_():
    bstack1ll111ll11_opy_ = bstack11l11l111_opy_.bstack1ll11ll11_opy_()
    bstack1llll1ll1_opy_(driver, bstack1ll111ll11_opy_)
  bstack11l11l111_opy_.bstack111l11l1l_opy_()
def bstack11lll11ll_opy_(sequence, driver_command, response = None, bstack1lll11111_opy_ = None, args = None):
    try:
      if sequence != bstack111l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫశ"):
        return
      if percy.bstack1ll11llll1_opy_() == bstack111l_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦష"):
        return
      bstack1ll111ll11_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩస"), None)
      for command in bstack11l11llll_opy_:
        if command == driver_command:
          for driver in bstack1l11l1l1_opy_:
            bstack1l111l1l11_opy_(driver)
      bstack1lll1l11ll_opy_ = percy.bstack1l1ll1ll_opy_()
      if driver_command in bstack1ll11ll1l_opy_[bstack1lll1l11ll_opy_]:
        bstack11l11l111_opy_.bstack11l1ll1l_opy_(bstack1ll111ll11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll1lll1ll_opy_(framework_name):
  if bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫహ")):
      return
  bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ఺"), True)
  global bstack11lll1111_opy_
  global bstack1ll1lll1l1_opy_
  global bstack1l1l11l1l_opy_
  bstack11lll1111_opy_ = framework_name
  logger.info(bstack111ll1lll_opy_.format(bstack11lll1111_opy_.split(bstack111l_opy_ (u"ࠩ࠰ࠫ఻"))[0]))
  bstack111l1lll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1lll11l1_opy_:
      Service.start = bstack1l11l111_opy_
      Service.stop = bstack1lll1l1l11_opy_
      webdriver.Remote.get = bstack1l11l111l1_opy_
      WebDriver.close = bstack1111l1l1_opy_
      WebDriver.quit = bstack1lllll111l_opy_
      webdriver.Remote.__init__ = bstack1l1l1ll1ll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1l1lll11l1_opy_:
        webdriver.Remote.__init__ = bstack1l11ll1ll_opy_
    WebDriver.execute = bstack111lll1ll_opy_
    bstack1ll1lll1l1_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1lll11l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l111l111l_opy_
  except Exception as e:
    pass
  bstack1ll1lll11l_opy_()
  if not bstack1ll1lll1l1_opy_:
    bstack1l1l1l1lll_opy_(bstack111l_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨ఼ࠧ"), bstack11llll1lll_opy_)
  if bstack1ll111lll1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._111l11l1_opy_ = bstack1l111l11_opy_
    except Exception as e:
      logger.error(bstack1llll1ll1l_opy_.format(str(e)))
  if bstack1111l11ll_opy_():
    bstack111111l1_opy_(CONFIG, logger)
  if (bstack111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఽ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1ll11llll1_opy_() == bstack111l_opy_ (u"ࠧࡺࡲࡶࡧࠥా"):
          bstack1ll1l1llll_opy_(bstack11lll11ll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll11ll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11111llll_opy_
      except Exception as e:
        logger.warn(bstack11l11l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1lllll1l_opy_
      except Exception as e:
        logger.debug(bstack111111lll_opy_ + str(e))
    except Exception as e:
      bstack1l1l1l1lll_opy_(e, bstack11l11l11_opy_)
    Output.start_test = bstack1l1ll1l1l1_opy_
    Output.end_test = bstack1ll111l111_opy_
    TestStatus.__init__ = bstack1111l1ll1_opy_
    QueueItem.__init__ = bstack11l1l1l11_opy_
    pabot._create_items = bstack11lll1ll1_opy_
    try:
      from pabot import __version__ as bstack11lll1l1ll_opy_
      if version.parse(bstack11lll1l1ll_opy_) >= version.parse(bstack111l_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭ి")):
        pabot._run = bstack1llll11ll1_opy_
      elif version.parse(bstack11lll1l1ll_opy_) >= version.parse(bstack111l_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧీ")):
        pabot._run = bstack1l1lll11ll_opy_
      else:
        pabot._run = bstack1l11l11l11_opy_
    except Exception as e:
      pabot._run = bstack1l11l11l11_opy_
    pabot._create_command_for_execution = bstack1l11111l1_opy_
    pabot._report_results = bstack1ll1l111l_opy_
  if bstack111l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨు") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1l1lll_opy_(e, bstack1l1l1l1l11_opy_)
    Runner.run_hook = bstack11l1ll11_opy_
    Step.run = bstack1l11ll1l_opy_
  if bstack111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩూ") in str(framework_name).lower():
    if not bstack1l1lll11l1_opy_:
      return
    try:
      if percy.bstack1ll11llll1_opy_() == bstack111l_opy_ (u"ࠥࡸࡷࡻࡥࠣృ"):
          bstack1ll1l1llll_opy_(bstack11lll11ll_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111ll1l1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll1lll11_opy_
      Config.getoption = bstack1ll11111ll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1l1ll111_opy_
    except Exception as e:
      pass
def bstack1ll11llll_opy_():
  global CONFIG
  if bstack111l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫౄ") in CONFIG and int(CONFIG[bstack111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ౅")]) > 1:
    logger.warn(bstack1l1l1ll1l_opy_)
def bstack11l1l1111_opy_(arg, bstack1l1l1ll11l_opy_, bstack11lllll11l_opy_=None):
  global CONFIG
  global bstack1l111ll1l_opy_
  global bstack1ll1l1ll_opy_
  global bstack1l1lll11l1_opy_
  global bstack1l1ll1l111_opy_
  bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ె")
  if bstack1l1l1ll11l_opy_ and isinstance(bstack1l1l1ll11l_opy_, str):
    bstack1l1l1ll11l_opy_ = eval(bstack1l1l1ll11l_opy_)
  CONFIG = bstack1l1l1ll11l_opy_[bstack111l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧే")]
  bstack1l111ll1l_opy_ = bstack1l1l1ll11l_opy_[bstack111l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩై")]
  bstack1ll1l1ll_opy_ = bstack1l1l1ll11l_opy_[bstack111l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ౉")]
  bstack1l1lll11l1_opy_ = bstack1l1l1ll11l_opy_[bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ొ")]
  bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬో"), bstack1l1lll11l1_opy_)
  os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧౌ")] = bstack1l11l1l1l1_opy_
  os.environ[bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋ్ࠬ")] = json.dumps(CONFIG)
  os.environ[bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ౎")] = bstack1l111ll1l_opy_
  os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ౏")] = str(bstack1ll1l1ll_opy_)
  os.environ[bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨ౐")] = str(True)
  if bstack11lll1l1l_opy_(arg, [bstack111l_opy_ (u"ࠪ࠱ࡳ࠭౑"), bstack111l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ౒")]) != -1:
    os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭౓")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll11l11_opy_)
    return
  bstack11l1l1lll_opy_()
  global bstack1l1l11111_opy_
  global bstack1lll1llll1_opy_
  global bstack1ll111l1l_opy_
  global bstack1l1lll1l_opy_
  global bstack1llll1l1ll_opy_
  global bstack1l1l11l1l_opy_
  global bstack1ll1l1l1_opy_
  arg.append(bstack111l_opy_ (u"ࠨ࠭ࡘࠤ౔"))
  arg.append(bstack111l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩౕࠥ"))
  arg.append(bstack111l_opy_ (u"ࠣ࠯ౖ࡚ࠦ"))
  arg.append(bstack111l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣ౗"))
  global bstack1l1111l1ll_opy_
  global bstack1ll1ll1l1_opy_
  global bstack1lll11l11l_opy_
  global bstack1l11lllll1_opy_
  global bstack1l11111l11_opy_
  global bstack1l11llll11_opy_
  global bstack1l1l111111_opy_
  global bstack111l1111_opy_
  global bstack1l1lllll1_opy_
  global bstack1l1l1l1l_opy_
  global bstack1l11llllll_opy_
  global bstack1l1111l11l_opy_
  global bstack1l1ll11111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1111l1ll_opy_ = webdriver.Remote.__init__
    bstack1ll1ll1l1_opy_ = WebDriver.quit
    bstack111l1111_opy_ = WebDriver.close
    bstack1l1lllll1_opy_ = WebDriver.get
    bstack1lll11l11l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1ll1ll1_opy_(CONFIG) and bstack11lll11ll1_opy_():
    if bstack11lll11111_opy_() < version.parse(bstack1111l111l_opy_):
      logger.error(bstack1l1ll11l_opy_.format(bstack11lll11111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l1l1l_opy_ = RemoteConnection._111l11l1_opy_
      except Exception as e:
        logger.error(bstack1llll1ll1l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l11llllll_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1111l11l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11llllll1_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l1ll11111_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫౘ"))
  bstack1ll111l1l_opy_ = CONFIG.get(bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨౙ"), {}).get(bstack111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧౚ"))
  bstack1ll1l1l1_opy_ = True
  bstack1ll1lll1ll_opy_(bstack1ll1l1l11_opy_)
  os.environ[bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ౛")] = CONFIG[bstack111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ౜")]
  os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫౝ")] = CONFIG[bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ౞")]
  os.environ[bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭౟")] = bstack1l1lll11l1_opy_.__str__()
  from _pytest.config import main as bstack11lll1lll_opy_
  bstack1l11ll1l1_opy_ = []
  try:
    bstack1ll11111l1_opy_ = bstack11lll1lll_opy_(arg)
    if bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨౠ") in multiprocessing.current_process().__dict__.keys():
      for bstack111l1l1l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11ll1l1_opy_.append(bstack111l1l1l1_opy_)
    try:
      bstack1l1ll111l_opy_ = (bstack1l11ll1l1_opy_, int(bstack1ll11111l1_opy_))
      bstack11lllll11l_opy_.append(bstack1l1ll111l_opy_)
    except:
      bstack11lllll11l_opy_.append((bstack1l11ll1l1_opy_, bstack1ll11111l1_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l11ll1l1_opy_.append({bstack111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪౡ"): bstack111l_opy_ (u"࠭ࡐࡳࡱࡦࡩࡸࡹࠠࠨౢ") + os.environ.get(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧౣ")), bstack111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ౤"): traceback.format_exc(), bstack111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ౥"): int(os.environ.get(bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ౦")))})
    bstack11lllll11l_opy_.append((bstack1l11ll1l1_opy_, 1))
def bstack1l1111lll_opy_(arg):
  global bstack1ll11ll1l1_opy_
  bstack1ll1lll1ll_opy_(bstack1ll1ll111_opy_)
  os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ౧")] = str(bstack1ll1l1ll_opy_)
  from behave.__main__ import main as bstack111l1ll1_opy_
  status_code = bstack111l1ll1_opy_(arg)
  if status_code != 0:
    bstack1ll11ll1l1_opy_ = status_code
def bstack11lll11l11_opy_():
  logger.info(bstack1l111l1lll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ౨"), help=bstack111l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧ౩"))
  parser.add_argument(bstack111l_opy_ (u"ࠧ࠮ࡷࠪ౪"), bstack111l_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ౫"), help=bstack111l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨ౬"))
  parser.add_argument(bstack111l_opy_ (u"ࠪ࠱ࡰ࠭౭"), bstack111l_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪ౮"), help=bstack111l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭౯"))
  parser.add_argument(bstack111l_opy_ (u"࠭࠭ࡧࠩ౰"), bstack111l_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ౱"), help=bstack111l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ౲"))
  bstack11l1l111l_opy_ = parser.parse_args()
  try:
    bstack11l1111ll_opy_ = bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭౳")
    if bstack11l1l111l_opy_.framework and bstack11l1l111l_opy_.framework not in (bstack111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ౴"), bstack111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ౵")):
      bstack11l1111ll_opy_ = bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫ౶")
    bstack11llllll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1111ll_opy_)
    bstack111l1lll_opy_ = open(bstack11llllll_opy_, bstack111l_opy_ (u"࠭ࡲࠨ౷"))
    bstack1ll1l1111l_opy_ = bstack111l1lll_opy_.read()
    bstack111l1lll_opy_.close()
    if bstack11l1l111l_opy_.username:
      bstack1ll1l1111l_opy_ = bstack1ll1l1111l_opy_.replace(bstack111l_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ౸"), bstack11l1l111l_opy_.username)
    if bstack11l1l111l_opy_.key:
      bstack1ll1l1111l_opy_ = bstack1ll1l1111l_opy_.replace(bstack111l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ౹"), bstack11l1l111l_opy_.key)
    if bstack11l1l111l_opy_.framework:
      bstack1ll1l1111l_opy_ = bstack1ll1l1111l_opy_.replace(bstack111l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ౺"), bstack11l1l111l_opy_.framework)
    file_name = bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭౻")
    file_path = os.path.abspath(file_name)
    bstack1l1l11ll1l_opy_ = open(file_path, bstack111l_opy_ (u"ࠫࡼ࠭౼"))
    bstack1l1l11ll1l_opy_.write(bstack1ll1l1111l_opy_)
    bstack1l1l11ll1l_opy_.close()
    logger.info(bstack11ll1ll11_opy_)
    try:
      os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ౽")] = bstack11l1l111l_opy_.framework if bstack11l1l111l_opy_.framework != None else bstack111l_opy_ (u"ࠨࠢ౾")
      config = yaml.safe_load(bstack1ll1l1111l_opy_)
      config[bstack111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ౿")] = bstack111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧಀ")
      bstack1lll11l1_opy_(bstack1lll11l111_opy_, config)
    except Exception as e:
      logger.debug(bstack1l111l11ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l11l11lll_opy_.format(str(e)))
def bstack1lll11l1_opy_(bstack11l111111_opy_, config, bstack11111l1l1_opy_={}):
  global bstack1l1lll11l1_opy_
  global bstack1ll1ll1l_opy_
  global bstack1l1ll1l111_opy_
  if not config:
    return
  bstack11ll11l1l_opy_ = bstack1l11lll11_opy_ if not bstack1l1lll11l1_opy_ else (
    bstack111l1111l_opy_ if bstack111l_opy_ (u"ࠩࡤࡴࡵ࠭ಁ") in config else (
        bstack11l111l1l_opy_ if config.get(bstack111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧಂ")) else bstack1l11llll1_opy_
    )
)
  bstack11lll11l1l_opy_ = False
  bstack11111ll1l_opy_ = False
  if bstack1l1lll11l1_opy_ is True:
      if bstack111l_opy_ (u"ࠫࡦࡶࡰࠨಃ") in config:
          bstack11lll11l1l_opy_ = True
      else:
          bstack11111ll1l_opy_ = True
  bstack1ll11lll1_opy_ = bstack1l1l1l11l_opy_.bstack1llll11l_opy_(config, bstack1ll1ll1l_opy_)
  data = {
    bstack111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ಄"): config[bstack111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨಅ")],
    bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪಆ"): config[bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫಇ")],
    bstack111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ಈ"): bstack11l111111_opy_,
    bstack111l_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧಉ"): os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ಊ"), bstack1ll1ll1l_opy_),
    bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧಋ"): bstack111lll1l_opy_,
    bstack111l_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨಌ"): bstack1l11111lll_opy_(),
    bstack111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ಍"): {
      bstack111l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಎ"): str(config[bstack111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩಏ")]) if bstack111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪಐ") in config else bstack111l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ಑"),
      bstack111l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࡖࡦࡴࡶ࡭ࡴࡴࠧಒ"): sys.version,
      bstack111l_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨಓ"): bstack11llll111_opy_(os.getenv(bstack111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤಔ"), bstack111l_opy_ (u"ࠣࠤಕ"))),
      bstack111l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫಖ"): bstack111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪಗ"),
      bstack111l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬಘ"): bstack11ll11l1l_opy_,
      bstack111l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪಙ"): bstack1ll11lll1_opy_,
      bstack111l_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠬಚ"): os.environ[bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬಛ")],
      bstack111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫಜ"): bstack11l11ll1_opy_(os.environ.get(bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫಝ"), bstack1ll1ll1l_opy_)),
      bstack111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ಞ"): config[bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧಟ")] if config[bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨಠ")] else bstack111l_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢಡ"),
      bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩಢ"): str(config[bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪಣ")]) if bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫತ") in config else bstack111l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦಥ"),
      bstack111l_opy_ (u"ࠫࡴࡹࠧದ"): sys.platform,
      bstack111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧಧ"): socket.gethostname(),
      bstack111l_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨನ"): bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ಩"))
    }
  }
  if not bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨಪ")) is None:
    data[bstack111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬಫ")][bstack111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡒ࡫ࡴࡢࡦࡤࡸࡦ࠭ಬ")] = {
      bstack111l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫಭ"): bstack111l_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪಮ"),
      bstack111l_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭ಯ"): bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧರ")),
      bstack111l_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࡏࡷࡰࡦࡪࡸࠧಱ"): bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬಲ"))
    }
  if bstack11l111111_opy_ == bstack1ll1l11l1_opy_:
    data[bstack111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ಳ")][bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡆࡳࡳ࡬ࡩࡨࠩ಴")] = bstack1l11lll111_opy_(config)
    data[bstack111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨವ")][bstack111l_opy_ (u"࠭ࡩࡴࡒࡨࡶࡨࡿࡁࡶࡶࡲࡉࡳࡧࡢ࡭ࡧࡧࠫಶ")] = percy.bstack1l1ll11lll_opy_
    data[bstack111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪಷ")][bstack111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡂࡶ࡫࡯ࡨࡎࡪࠧಸ")] = percy.bstack11ll1l111_opy_
  update(data[bstack111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬಹ")], bstack11111l1l1_opy_)
  try:
    response = bstack1111ll11l_opy_(bstack111l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ಺"), bstack1lll1lll11_opy_(bstack11ll111l_opy_), data, {
      bstack111l_opy_ (u"ࠫࡦࡻࡴࡩࠩ಻"): (config[bstack111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫಼ࠧ")], config[bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩಽ")])
    })
    if response:
      logger.debug(bstack11l111l11_opy_.format(bstack11l111111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111lll111_opy_.format(str(e)))
def bstack11llll111_opy_(framework):
  return bstack111l_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦಾ").format(str(framework), __version__) if framework else bstack111l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤಿ").format(
    __version__)
def bstack11l1l1lll_opy_():
  global CONFIG
  global bstack11l1llll_opy_
  if bool(CONFIG):
    return
  try:
    bstack11lll1l111_opy_()
    logger.debug(bstack1lll11lll1_opy_.format(str(CONFIG)))
    bstack11l1llll_opy_ = bstack11lll1lll1_opy_.bstack1lll11lll_opy_(CONFIG, bstack11l1llll_opy_)
    bstack111l1lll1_opy_()
  except Exception as e:
    logger.error(bstack111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨೀ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11l1ll1ll_opy_
  atexit.register(bstack111lllll_opy_)
  signal.signal(signal.SIGINT, bstack11ll11ll_opy_)
  signal.signal(signal.SIGTERM, bstack11ll11ll_opy_)
def bstack11l1ll1ll_opy_(exctype, value, traceback):
  global bstack1l11l1l1_opy_
  try:
    for driver in bstack1l11l1l1_opy_:
      bstack111111ll_opy_(driver, bstack111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪು"), bstack111l_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢೂ") + str(value))
  except Exception:
    pass
  bstack1ll11l11l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll11l11l_opy_(message=bstack111l_opy_ (u"ࠬ࠭ೃ"), bstack1l1llll1ll_opy_ = False):
  global CONFIG
  bstack1l1ll1l1_opy_ = bstack111l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨೄ") if bstack1l1llll1ll_opy_ else bstack111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭೅")
  try:
    if message:
      bstack11111l1l1_opy_ = {
        bstack1l1ll1l1_opy_ : str(message)
      }
      bstack1lll11l1_opy_(bstack1ll1l11l1_opy_, CONFIG, bstack11111l1l1_opy_)
    else:
      bstack1lll11l1_opy_(bstack1ll1l11l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l1l11ll_opy_.format(str(e)))
def bstack111ll1ll1_opy_(bstack1l1111llll_opy_, size):
  bstack1lll1l1lll_opy_ = []
  while len(bstack1l1111llll_opy_) > size:
    bstack1111111l1_opy_ = bstack1l1111llll_opy_[:size]
    bstack1lll1l1lll_opy_.append(bstack1111111l1_opy_)
    bstack1l1111llll_opy_ = bstack1l1111llll_opy_[size:]
  bstack1lll1l1lll_opy_.append(bstack1l1111llll_opy_)
  return bstack1lll1l1lll_opy_
def bstack1l1l111lll_opy_(args):
  if bstack111l_opy_ (u"ࠨ࠯ࡰࠫೆ") in args and bstack111l_opy_ (u"ࠩࡳࡨࡧ࠭ೇ") in args:
    return True
  return False
def run_on_browserstack(bstack1l1111ll1l_opy_=None, bstack11lllll11l_opy_=None, bstack1llll1ll11_opy_=False):
  global CONFIG
  global bstack1l111ll1l_opy_
  global bstack1ll1l1ll_opy_
  global bstack1ll1ll1l_opy_
  global bstack1l1ll1l111_opy_
  bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠪࠫೈ")
  bstack1l1ll1lll1_opy_(bstack1l111lll_opy_, logger)
  if bstack1l1111ll1l_opy_ and isinstance(bstack1l1111ll1l_opy_, str):
    bstack1l1111ll1l_opy_ = eval(bstack1l1111ll1l_opy_)
  if bstack1l1111ll1l_opy_:
    CONFIG = bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ೉")]
    bstack1l111ll1l_opy_ = bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ೊ")]
    bstack1ll1l1ll_opy_ = bstack1l1111ll1l_opy_[bstack111l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨೋ")]
    bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩೌ"), bstack1ll1l1ll_opy_)
    bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ್")
  bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ೎"), uuid4().__str__())
  logger.debug(bstack111l_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࡂ࠭೏") + bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭೐")))
  if not bstack1llll1ll11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll11l11_opy_)
      return
    if sys.argv[1] == bstack111l_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ೑") or sys.argv[1] == bstack111l_opy_ (u"࠭࠭ࡷࠩ೒"):
      logger.info(bstack111l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧ೓").format(__version__))
      return
    if sys.argv[1] == bstack111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ೔"):
      bstack11lll11l11_opy_()
      return
  args = sys.argv
  bstack11l1l1lll_opy_()
  global bstack1l1l11111_opy_
  global bstack1111l1111_opy_
  global bstack1ll1l1l1_opy_
  global bstack1ll11l1l_opy_
  global bstack1lll1llll1_opy_
  global bstack1ll111l1l_opy_
  global bstack1l1lll1l_opy_
  global bstack1ll1l1lll_opy_
  global bstack1llll1l1ll_opy_
  global bstack1l1l11l1l_opy_
  global bstack1ll1111l_opy_
  bstack1111l1111_opy_ = len(CONFIG.get(bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬೕ"), []))
  if not bstack1l11l1l1l1_opy_:
    if args[1] == bstack111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪೖ") or args[1] == bstack111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ೗"):
      bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ೘")
      args = args[2:]
    elif args[1] == bstack111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೙"):
      bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭೚")
      args = args[2:]
    elif args[1] == bstack111l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ೛"):
      bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ೜")
      args = args[2:]
    elif args[1] == bstack111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫೝ"):
      bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬೞ")
      args = args[2:]
    elif args[1] == bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ೟"):
      bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ೠ")
      args = args[2:]
    elif args[1] == bstack111l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧೡ"):
      bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨೢ")
      args = args[2:]
    else:
      if not bstack111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬೣ") in CONFIG or str(CONFIG[bstack111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭೤")]).lower() in [bstack111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ೥"), bstack111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭೦")]:
        bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭೧")
        args = args[1:]
      elif str(CONFIG[bstack111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೨")]).lower() == bstack111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ೩"):
        bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ೪")
        args = args[1:]
      elif str(CONFIG[bstack111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭೫")]).lower() == bstack111l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ೬"):
        bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ೭")
        args = args[1:]
      elif str(CONFIG[bstack111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ೮")]).lower() == bstack111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ೯"):
        bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ೰")
        args = args[1:]
      elif str(CONFIG[bstack111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬೱ")]).lower() == bstack111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪೲ"):
        bstack1l11l1l1l1_opy_ = bstack111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫೳ")
        args = args[1:]
      else:
        os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೴")] = bstack1l11l1l1l1_opy_
        bstack1llll1l1_opy_(bstack1llll1l1l1_opy_)
  os.environ[bstack111l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧ೵")] = bstack1l11l1l1l1_opy_
  bstack1ll1ll1l_opy_ = bstack1l11l1l1l1_opy_
  global bstack1ll1l1l111_opy_
  global bstack1ll1lll1_opy_
  if bstack1l1111ll1l_opy_:
    try:
      os.environ[bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ೶")] = bstack1l11l1l1l1_opy_
      bstack1lll11l1_opy_(bstack1l1lll1lll_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11l1l11l1_opy_.format(str(e)))
  global bstack1l1111l1ll_opy_
  global bstack1ll1ll1l1_opy_
  global bstack1lll1lll1l_opy_
  global bstack11111l1l_opy_
  global bstack1l11l11ll_opy_
  global bstack1111ll1l_opy_
  global bstack1l11lllll1_opy_
  global bstack1l11111l11_opy_
  global bstack1l111lll1l_opy_
  global bstack1l11llll11_opy_
  global bstack1l1l111111_opy_
  global bstack111l1111_opy_
  global bstack1ll11111_opy_
  global bstack1l11111l1l_opy_
  global bstack1l1lllll1_opy_
  global bstack1l1l1l1l_opy_
  global bstack1l11llllll_opy_
  global bstack1l1111l11l_opy_
  global bstack11ll1l11l_opy_
  global bstack1l1ll11111_opy_
  global bstack1lll11l11l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1111l1ll_opy_ = webdriver.Remote.__init__
    bstack1ll1ll1l1_opy_ = WebDriver.quit
    bstack111l1111_opy_ = WebDriver.close
    bstack1l1lllll1_opy_ = WebDriver.get
    bstack1lll11l11l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll1l1l111_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11ll11ll1_opy_
    bstack1ll1lll1_opy_ = bstack11ll11ll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1llll111l_opy_
    from QWeb.keywords import browser
    bstack1llll111l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1ll1ll1_opy_(CONFIG) and bstack11lll11ll1_opy_():
    if bstack11lll11111_opy_() < version.parse(bstack1111l111l_opy_):
      logger.error(bstack1l1ll11l_opy_.format(bstack11lll11111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l1l1l_opy_ = RemoteConnection._111l11l1_opy_
      except Exception as e:
        logger.error(bstack1llll1ll1l_opy_.format(str(e)))
  if not CONFIG.get(bstack111l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ೷"), False) and not bstack1l1111ll1l_opy_:
    logger.info(bstack1ll1111l1l_opy_)
  if bstack111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭೸") in CONFIG and str(CONFIG[bstack111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ೹")]).lower() != bstack111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ೺"):
    bstack1l1l11lll_opy_()
  elif bstack1l11l1l1l1_opy_ != bstack111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ೻") or (bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭೼") and not bstack1l1111ll1l_opy_):
    bstack1llll1111l_opy_()
  if (bstack1l11l1l1l1_opy_ in [bstack111l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭೽"), bstack111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ೾"), bstack111l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ೿")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll11ll1_opy_
        bstack1111ll1l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l11l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l11l11ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack111111lll_opy_ + str(e))
    except Exception as e:
      bstack1l1l1l1lll_opy_(e, bstack11l11l11_opy_)
    if bstack1l11l1l1l1_opy_ != bstack111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫഀ"):
      bstack11lll1111l_opy_()
    bstack1lll1lll1l_opy_ = Output.start_test
    bstack11111l1l_opy_ = Output.end_test
    bstack1l11lllll1_opy_ = TestStatus.__init__
    bstack1l111lll1l_opy_ = pabot._run
    bstack1l11llll11_opy_ = QueueItem.__init__
    bstack1l1l111111_opy_ = pabot._create_command_for_execution
    bstack11ll1l11l_opy_ = pabot._report_results
  if bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഁ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1l1lll_opy_(e, bstack1l1l1l1l11_opy_)
    bstack1ll11111_opy_ = Runner.run_hook
    bstack1l11111l1l_opy_ = Step.run
  if bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬം"):
    try:
      from _pytest.config import Config
      bstack1l11llllll_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1111l11l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11llllll1_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l1ll11111_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧഃ"))
  try:
    framework_name = bstack111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ഄ") if bstack1l11l1l1l1_opy_ in [bstack111l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧഅ"), bstack111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨആ"), bstack111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫഇ")] else bstack1l111lll11_opy_(bstack1l11l1l1l1_opy_)
    bstack1l1lll1l11_opy_ = {
      bstack111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬഈ"): bstack111l_opy_ (u"ࠬࢁ࠰ࡾ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫഉ").format(framework_name) if bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ഊ") and bstack1111l1lll_opy_() else framework_name,
      bstack111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫഋ"): bstack11l11ll1_opy_(framework_name),
      bstack111l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ഌ"): __version__,
      bstack111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ഍"): bstack1l11l1l1l1_opy_
    }
    if bstack1l11l1l1l1_opy_ in bstack1ll1lllll1_opy_:
      if bstack1l1lll11l1_opy_ and bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪഎ") in CONFIG and CONFIG[bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫഏ")] == True:
        if bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬഐ") in CONFIG:
          os.environ[bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ഑")] = os.getenv(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨഒ"), json.dumps(CONFIG[bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨഓ")]))
          CONFIG[bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩഔ")].pop(bstack111l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨക"), None)
          CONFIG[bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫഖ")].pop(bstack111l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪഗ"), None)
        bstack1l1lll1l11_opy_[bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ഘ")] = {
          bstack111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬങ"): bstack111l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪച"),
          bstack111l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪഛ"): str(bstack11lll11111_opy_())
        }
    if bstack1l11l1l1l1_opy_ not in [bstack111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫജ")]:
      bstack1l11l1l11_opy_ = bstack11ll111ll_opy_.launch(CONFIG, bstack1l1lll1l11_opy_)
  except Exception as e:
    logger.debug(bstack11l11111l_opy_.format(bstack111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡊࡸࡦࠬഝ"), str(e)))
  if bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬഞ"):
    bstack1ll1l1l1_opy_ = True
    if bstack1l1111ll1l_opy_ and bstack1llll1ll11_opy_:
      bstack1ll111l1l_opy_ = CONFIG.get(bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪട"), {}).get(bstack111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩഠ"))
      bstack1ll1lll1ll_opy_(bstack1l1111l111_opy_)
    elif bstack1l1111ll1l_opy_:
      bstack1ll111l1l_opy_ = CONFIG.get(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬഡ"), {}).get(bstack111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫഢ"))
      global bstack1l11l1l1_opy_
      try:
        if bstack1l1l111lll_opy_(bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ണ")]) and multiprocessing.current_process().name == bstack111l_opy_ (u"ࠫ࠵࠭ത"):
          bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨഥ")].remove(bstack111l_opy_ (u"࠭࠭࡮ࠩദ"))
          bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪധ")].remove(bstack111l_opy_ (u"ࠨࡲࡧࡦࠬന"))
          bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬഩ")] = bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭പ")][0]
          with open(bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧഫ")], bstack111l_opy_ (u"ࠬࡸࠧബ")) as f:
            bstack1lll111l11_opy_ = f.read()
          bstack1ll1l1ll1_opy_ = bstack111l_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࠣࡁࠥࡹࡴࡳࠪ࡬ࡲࡹ࠮ࡡࡳࡩࠬ࠯࠶࠶ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡴ࡭࡟ࡥࡤࠫࡷࡪࡲࡦ࠭ࡣࡵ࡫࠱ࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠭࠯࠮ࡴࡧࡷࡣࡹࡸࡡࡤࡧࠫ࠭ࡡࡴࠢࠣࠤഭ").format(str(bstack1l1111ll1l_opy_))
          bstack1lll1ll11l_opy_ = bstack1ll1l1ll1_opy_ + bstack1lll111l11_opy_
          bstack1l111l1ll1_opy_ = bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪമ")] + bstack111l_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪയ")
          with open(bstack1l111l1ll1_opy_, bstack111l_opy_ (u"ࠩࡺࠫര")):
            pass
          with open(bstack1l111l1ll1_opy_, bstack111l_opy_ (u"ࠥࡻ࠰ࠨറ")) as f:
            f.write(bstack1lll1ll11l_opy_)
          import subprocess
          bstack11l1ll111_opy_ = subprocess.run([bstack111l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦല"), bstack1l111l1ll1_opy_])
          if os.path.exists(bstack1l111l1ll1_opy_):
            os.unlink(bstack1l111l1ll1_opy_)
          os._exit(bstack11l1ll111_opy_.returncode)
        else:
          if bstack1l1l111lll_opy_(bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨള")]):
            bstack1l1111ll1l_opy_[bstack111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩഴ")].remove(bstack111l_opy_ (u"ࠧ࠮࡯ࠪവ"))
            bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫശ")].remove(bstack111l_opy_ (u"ࠩࡳࡨࡧ࠭ഷ"))
            bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭സ")] = bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧഹ")][0]
          bstack1ll1lll1ll_opy_(bstack1l1111l111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨഺ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111l_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨ഻")] = bstack111l_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠ഼ࠩ")
          mod_globals[bstack111l_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪഽ")] = os.path.abspath(bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬാ")])
          exec(open(bstack1l1111ll1l_opy_[bstack111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ി")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111l_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫീ").format(str(e)))
          for driver in bstack1l11l1l1_opy_:
            bstack11lllll11l_opy_.append({
              bstack111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪു"): bstack1l1111ll1l_opy_[bstack111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩൂ")],
              bstack111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ൃ"): str(e),
              bstack111l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧൄ"): multiprocessing.current_process().name
            })
            bstack111111ll_opy_(driver, bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ൅"), bstack111l_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨെ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l11l1l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1ll1l1ll_opy_, CONFIG, logger)
      bstack1ll1l11111_opy_()
      bstack1ll11llll_opy_()
      bstack1l1l1ll11l_opy_ = {
        bstack111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧേ"): args[0],
        bstack111l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬൈ"): CONFIG,
        bstack111l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ൉"): bstack1l111ll1l_opy_,
        bstack111l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩൊ"): bstack1ll1l1ll_opy_
      }
      percy.bstack1ll11l1l1_opy_()
      if bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫോ") in CONFIG:
        bstack1lll1l1l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lllllll1l_opy_ = manager.list()
        if bstack1l1l111lll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬൌ")]):
            if index == 0:
              bstack1l1l1ll11l_opy_[bstack111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ്࠭")] = args
            bstack1lll1l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1l1ll11l_opy_, bstack1lllllll1l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧൎ")]):
            bstack1lll1l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1l1ll11l_opy_, bstack1lllllll1l_opy_)))
        for t in bstack1lll1l1l1_opy_:
          t.start()
        for t in bstack1lll1l1l1_opy_:
          t.join()
        bstack1ll1l1lll_opy_ = list(bstack1lllllll1l_opy_)
      else:
        if bstack1l1l111lll_opy_(args):
          bstack1l1l1ll11l_opy_[bstack111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൏")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1l1ll11l_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1lll1ll_opy_(bstack1l1111l111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111l_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨ൐")] = bstack111l_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩ൑")
          mod_globals[bstack111l_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪ൒")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൓") or bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩൔ"):
    percy.init(bstack1ll1l1ll_opy_, CONFIG, logger)
    percy.bstack1ll11l1l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1l1l1lll_opy_(e, bstack11l11l11_opy_)
    bstack1ll1l11111_opy_()
    bstack1ll1lll1ll_opy_(bstack1l11l1lll_opy_)
    if bstack1l1lll11l1_opy_:
      bstack1l1llllll_opy_(bstack1l11l1lll_opy_, args)
      if bstack111l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩൕ") in args:
        i = args.index(bstack111l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪൖ"))
        args.pop(i)
        args.pop(i)
      if bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩൗ") not in CONFIG:
        CONFIG[bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ൘")] = [{}]
        bstack1111l1111_opy_ = 1
      if bstack1l1l11111_opy_ == 0:
        bstack1l1l11111_opy_ = 1
      args.insert(0, str(bstack1l1l11111_opy_))
      args.insert(0, str(bstack111l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭൙")))
    if bstack11ll111ll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll1l1l1ll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l11l11l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111l_opy_ (u"ࠤࡕࡓࡇࡕࡔࡠࡑࡓࡘࡎࡕࡎࡔࠤ൚"),
        ).parse_args(bstack1ll1l1l1ll_opy_)
        bstack1ll111111l_opy_ = args.index(bstack1ll1l1l1ll_opy_[0]) if len(bstack1ll1l1l1ll_opy_) > 0 else len(args)
        args.insert(bstack1ll111111l_opy_, str(bstack111l_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧ൛")))
        args.insert(bstack1ll111111l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶ࠳ࡶࡹࠨ൜"))))
        if bstack111lll11l_opy_(os.environ.get(bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪ൝"))) and str(os.environ.get(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ൞"), bstack111l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬൟ"))) != bstack111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ൠ"):
          for bstack1lllll1lll_opy_ in bstack1l11l11l1_opy_:
            args.remove(bstack1lllll1lll_opy_)
          bstack111l1l1l_opy_ = os.environ.get(bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ൡ")).split(bstack111l_opy_ (u"ࠪ࠰ࠬൢ"))
          for bstack1l1l1111_opy_ in bstack111l1l1l_opy_:
            args.append(bstack1l1l1111_opy_)
      except Exception as e:
        logger.error(bstack111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡸࡹࡧࡣࡩ࡫ࡱ࡫ࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࠢൣ").format(e))
    pabot.main(args)
  elif bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭൤"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1l1l1lll_opy_(e, bstack11l11l11_opy_)
    for a in args:
      if bstack111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ൥") in a:
        bstack1lll1llll1_opy_ = int(a.split(bstack111l_opy_ (u"ࠧ࠻ࠩ൦"))[1])
      if bstack111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ൧") in a:
        bstack1ll111l1l_opy_ = str(a.split(bstack111l_opy_ (u"ࠩ࠽ࠫ൨"))[1])
      if bstack111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪ൩") in a:
        bstack1l1lll1l_opy_ = str(a.split(bstack111l_opy_ (u"ࠫ࠿࠭൪"))[1])
    bstack1ll1l1lll1_opy_ = None
    if bstack111l_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫ൫") in args:
      i = args.index(bstack111l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬ൬"))
      args.pop(i)
      bstack1ll1l1lll1_opy_ = args.pop(i)
    if bstack1ll1l1lll1_opy_ is not None:
      global bstack1lllllllll_opy_
      bstack1lllllllll_opy_ = bstack1ll1l1lll1_opy_
    bstack1ll1lll1ll_opy_(bstack1l11l1lll_opy_)
    run_cli(args)
    if bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ൭") in multiprocessing.current_process().__dict__.keys():
      for bstack111l1l1l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11lllll11l_opy_.append(bstack111l1l1l1_opy_)
  elif bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ൮"):
    percy.init(bstack1ll1l1ll_opy_, CONFIG, logger)
    percy.bstack1ll11l1l1_opy_()
    bstack1l11ll1l11_opy_ = bstack1l1lllll11_opy_(args, logger, CONFIG, bstack1l1lll11l1_opy_)
    bstack1l11ll1l11_opy_.bstack1lll1ll1l_opy_()
    bstack1ll1l11111_opy_()
    bstack1ll11l1l_opy_ = True
    bstack1l1l11l1l_opy_ = bstack1l11ll1l11_opy_.bstack1lll1ll1_opy_()
    bstack1l11ll1l11_opy_.bstack1l1l1ll11l_opy_(bstack1l1l1lll_opy_)
    bstack1llll1l11_opy_ = bstack1l11ll1l11_opy_.bstack11lll11lll_opy_(bstack11l1l1111_opy_, {
      bstack111l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ൯"): bstack1l111ll1l_opy_,
      bstack111l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ൰"): bstack1ll1l1ll_opy_,
      bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ൱"): bstack1l1lll11l1_opy_
    })
    try:
      bstack1l11ll1l1_opy_, bstack1l11ll11l1_opy_ = map(list, zip(*bstack1llll1l11_opy_))
      bstack1llll1l1ll_opy_ = bstack1l11ll1l1_opy_[0]
      for status_code in bstack1l11ll11l1_opy_:
        if status_code != 0:
          bstack1ll1111l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡥࡳࡴࡲࡶࡸࠦࡡ࡯ࡦࠣࡷࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠯ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡀࠠࡼࡿࠥ൲").format(str(e)))
  elif bstack1l11l1l1l1_opy_ == bstack111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭൳"):
    try:
      from behave.__main__ import main as bstack111l1ll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1l1l1lll_opy_(e, bstack1l1l1l1l11_opy_)
    bstack1ll1l11111_opy_()
    bstack1ll11l1l_opy_ = True
    bstack1l1lll11l_opy_ = 1
    if bstack111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ൴") in CONFIG:
      bstack1l1lll11l_opy_ = CONFIG[bstack111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ൵")]
    if bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ൶") in CONFIG:
      bstack1lll111lll_opy_ = int(bstack1l1lll11l_opy_) * int(len(CONFIG[bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭൷")]))
    else:
      bstack1lll111lll_opy_ = int(bstack1l1lll11l_opy_)
    config = Configuration(args)
    bstack1111lll1_opy_ = config.paths
    if len(bstack1111lll1_opy_) == 0:
      import glob
      pattern = bstack111l_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪ൸")
      bstack1ll111l1l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll111l1l1_opy_)
      config = Configuration(args)
      bstack1111lll1_opy_ = config.paths
    bstack1l11l1111l_opy_ = [os.path.normpath(item) for item in bstack1111lll1_opy_]
    bstack1ll1ll1111_opy_ = [os.path.normpath(item) for item in args]
    bstack11l11lll1_opy_ = [item for item in bstack1ll1ll1111_opy_ if item not in bstack1l11l1111l_opy_]
    import platform as pf
    if pf.system().lower() == bstack111l_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭൹"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11l1111l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1ll11l1l_opy_)))
                    for bstack1l1ll11l1l_opy_ in bstack1l11l1111l_opy_]
    bstack11ll1l1l1_opy_ = []
    for spec in bstack1l11l1111l_opy_:
      bstack111l11lll_opy_ = []
      bstack111l11lll_opy_ += bstack11l11lll1_opy_
      bstack111l11lll_opy_.append(spec)
      bstack11ll1l1l1_opy_.append(bstack111l11lll_opy_)
    execution_items = []
    for bstack111l11lll_opy_ in bstack11ll1l1l1_opy_:
      if bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩൺ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪൻ")]):
          item = {}
          item[bstack111l_opy_ (u"ࠨࡣࡵ࡫ࠬർ")] = bstack111l_opy_ (u"ࠩࠣࠫൽ").join(bstack111l11lll_opy_)
          item[bstack111l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩൾ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack111l_opy_ (u"ࠫࡦࡸࡧࠨൿ")] = bstack111l_opy_ (u"ࠬࠦࠧ඀").join(bstack111l11lll_opy_)
        item[bstack111l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬඁ")] = 0
        execution_items.append(item)
    bstack1l111l11l_opy_ = bstack111ll1ll1_opy_(execution_items, bstack1lll111lll_opy_)
    for execution_item in bstack1l111l11l_opy_:
      bstack1lll1l1l1_opy_ = []
      for item in execution_item:
        bstack1lll1l1l1_opy_.append(bstack111ll11l1_opy_(name=str(item[bstack111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ං")]),
                                             target=bstack1l1111lll_opy_,
                                             args=(item[bstack111l_opy_ (u"ࠨࡣࡵ࡫ࠬඃ")],)))
      for t in bstack1lll1l1l1_opy_:
        t.start()
      for t in bstack1lll1l1l1_opy_:
        t.join()
  else:
    bstack1llll1l1_opy_(bstack1llll1l1l1_opy_)
  if not bstack1l1111ll1l_opy_:
    bstack111ll111_opy_()
  bstack11lll1lll1_opy_.bstack1l11lll1l_opy_()
def browserstack_initialize(bstack1l1ll1lll_opy_=None):
  run_on_browserstack(bstack1l1ll1lll_opy_, None, True)
def bstack111ll111_opy_():
  global CONFIG
  global bstack1ll1ll1l_opy_
  global bstack1ll1111l_opy_
  global bstack1ll11ll1l1_opy_
  global bstack1l1ll1l111_opy_
  bstack11ll111ll_opy_.stop()
  bstack1lll1lllll_opy_.bstack1lll1ll1ll_opy_()
  if bstack111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭඄") in CONFIG and str(CONFIG[bstack111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧඅ")]).lower() != bstack111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪආ"):
    bstack111ll11l_opy_, bstack11l1l1ll_opy_ = bstack1l11l1l1l_opy_()
  else:
    bstack111ll11l_opy_, bstack11l1l1ll_opy_ = get_build_link()
  bstack11ll11111_opy_(bstack111ll11l_opy_)
  if bstack111ll11l_opy_ is not None and bstack111l11ll1_opy_() != -1:
    sessions = bstack1llll1l11l_opy_(bstack111ll11l_opy_)
    bstack1l1l11ll1_opy_(sessions, bstack11l1l1ll_opy_)
  if bstack1ll1ll1l_opy_ == bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬඇ") and bstack1ll1111l_opy_ != 0:
    sys.exit(bstack1ll1111l_opy_)
  if bstack1ll1ll1l_opy_ == bstack111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඈ") and bstack1ll11ll1l1_opy_ != 0:
    sys.exit(bstack1ll11ll1l1_opy_)
def bstack11ll11111_opy_(new_id):
    global bstack111lll1l_opy_
    bstack111lll1l_opy_ = new_id
def bstack1l111lll11_opy_(bstack1llll11l1_opy_):
  if bstack1llll11l1_opy_:
    return bstack1llll11l1_opy_.capitalize()
  else:
    return bstack111l_opy_ (u"ࠧࠨඉ")
def bstack11ll111l1_opy_(bstack1llllll1l_opy_):
  if bstack111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ඊ") in bstack1llllll1l_opy_ and bstack1llllll1l_opy_[bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧඋ")] != bstack111l_opy_ (u"ࠪࠫඌ"):
    return bstack1llllll1l_opy_[bstack111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩඍ")]
  else:
    bstack1l111ll11_opy_ = bstack111l_opy_ (u"ࠧࠨඎ")
    if bstack111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ඏ") in bstack1llllll1l_opy_ and bstack1llllll1l_opy_[bstack111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧඐ")] != None:
      bstack1l111ll11_opy_ += bstack1llllll1l_opy_[bstack111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨඑ")] + bstack111l_opy_ (u"ࠤ࠯ࠤࠧඒ")
      if bstack1llllll1l_opy_[bstack111l_opy_ (u"ࠪࡳࡸ࠭ඓ")] == bstack111l_opy_ (u"ࠦ࡮ࡵࡳࠣඔ"):
        bstack1l111ll11_opy_ += bstack111l_opy_ (u"ࠧ࡯ࡏࡔࠢࠥඕ")
      bstack1l111ll11_opy_ += (bstack1llllll1l_opy_[bstack111l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪඖ")] or bstack111l_opy_ (u"ࠧࠨ඗"))
      return bstack1l111ll11_opy_
    else:
      bstack1l111ll11_opy_ += bstack1l111lll11_opy_(bstack1llllll1l_opy_[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ඘")]) + bstack111l_opy_ (u"ࠤࠣࠦ඙") + (
              bstack1llllll1l_opy_[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬක")] or bstack111l_opy_ (u"ࠫࠬඛ")) + bstack111l_opy_ (u"ࠧ࠲ࠠࠣග")
      if bstack1llllll1l_opy_[bstack111l_opy_ (u"࠭࡯ࡴࠩඝ")] == bstack111l_opy_ (u"ࠢࡘ࡫ࡱࡨࡴࡽࡳࠣඞ"):
        bstack1l111ll11_opy_ += bstack111l_opy_ (u"࡙ࠣ࡬ࡲࠥࠨඟ")
      bstack1l111ll11_opy_ += bstack1llllll1l_opy_[bstack111l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ච")] or bstack111l_opy_ (u"ࠪࠫඡ")
      return bstack1l111ll11_opy_
def bstack11ll1l1ll_opy_(bstack1ll111l1ll_opy_):
  if bstack1ll111l1ll_opy_ == bstack111l_opy_ (u"ࠦࡩࡵ࡮ࡦࠤජ"):
    return bstack111l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡄࡱࡰࡴࡱ࡫ࡴࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨඣ")
  elif bstack1ll111l1ll_opy_ == bstack111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨඤ"):
    return bstack111l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡌࡡࡪ࡮ࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪඥ")
  elif bstack1ll111l1ll_opy_ == bstack111l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣඦ"):
    return bstack111l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡕࡧࡳࡴࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩට")
  elif bstack1ll111l1ll_opy_ == bstack111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤඨ"):
    return bstack111l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡈࡶࡷࡵࡲ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ඩ")
  elif bstack1ll111l1ll_opy_ == bstack111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨඪ"):
    return bstack111l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࠥࡨࡩࡦ࠹࠲࠷࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࠧࡪ࡫ࡡ࠴࠴࠹ࠦࡃ࡚ࡩ࡮ࡧࡲࡹࡹࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫණ")
  elif bstack1ll111l1ll_opy_ == bstack111l_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠣඬ"):
    return bstack111l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࡖࡺࡴ࡮ࡪࡰࡪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩත")
  else:
    return bstack111l_opy_ (u"ࠩ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃ࠭ථ") + bstack1l111lll11_opy_(
      bstack1ll111l1ll_opy_) + bstack111l_opy_ (u"ࠪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩද")
def bstack1l1ll1l11l_opy_(session):
  return bstack111l_opy_ (u"ࠫࡁࡺࡲࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡴࡲࡻࠧࡄ࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠡࡵࡨࡷࡸ࡯࡯࡯࠯ࡱࡥࡲ࡫ࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࡿࢂࠨࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣࡡࡥࡰࡦࡴ࡫ࠣࡀࡾࢁࡁ࠵ࡡ࠿࠾࠲ࡸࡩࡄࡻࡾࡽࢀࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂ࠯ࡵࡴࡁࠫධ").format(
    session[bstack111l_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩන")], bstack11ll111l1_opy_(session), bstack11ll1l1ll_opy_(session[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠬ඲")]),
    bstack11ll1l1ll_opy_(session[bstack111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧඳ")]),
    bstack1l111lll11_opy_(session[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩප")] or session[bstack111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩඵ")] or bstack111l_opy_ (u"ࠪࠫබ")) + bstack111l_opy_ (u"ࠦࠥࠨභ") + (session[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧම")] or bstack111l_opy_ (u"࠭ࠧඹ")),
    session[bstack111l_opy_ (u"ࠧࡰࡵࠪය")] + bstack111l_opy_ (u"ࠣࠢࠥර") + session[bstack111l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭඼")], session[bstack111l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬල")] or bstack111l_opy_ (u"ࠫࠬ඾"),
    session[bstack111l_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩ඿")] if session[bstack111l_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪව")] else bstack111l_opy_ (u"ࠧࠨශ"))
def bstack1l1l11ll1_opy_(sessions, bstack11l1l1ll_opy_):
  try:
    bstack11llll11ll_opy_ = bstack111l_opy_ (u"ࠣࠤෂ")
    if not os.path.exists(bstack111lll11_opy_):
      os.mkdir(bstack111lll11_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l_opy_ (u"ࠩࡤࡷࡸ࡫ࡴࡴ࠱ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧස")), bstack111l_opy_ (u"ࠪࡶࠬහ")) as f:
      bstack11llll11ll_opy_ = f.read()
    bstack11llll11ll_opy_ = bstack11llll11ll_opy_.replace(bstack111l_opy_ (u"ࠫࢀࠫࡒࡆࡕࡘࡐ࡙࡙࡟ࡄࡑࡘࡒ࡙ࠫࡽࠨළ"), str(len(sessions)))
    bstack11llll11ll_opy_ = bstack11llll11ll_opy_.replace(bstack111l_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡕࡓࡎࠨࢁࠬෆ"), bstack11l1l1ll_opy_)
    bstack11llll11ll_opy_ = bstack11llll11ll_opy_.replace(bstack111l_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠪࢃࠧ෇"),
                                              sessions[0].get(bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡢ࡯ࡨࠫ෈")) if sessions[0] else bstack111l_opy_ (u"ࠨࠩ෉"))
    with open(os.path.join(bstack111lll11_opy_, bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ්࠭")), bstack111l_opy_ (u"ࠪࡻࠬ෋")) as stream:
      stream.write(bstack11llll11ll_opy_.split(bstack111l_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ෌"))[0])
      for session in sessions:
        stream.write(bstack1l1ll1l11l_opy_(session))
      stream.write(bstack11llll11ll_opy_.split(bstack111l_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩ෍"))[1])
    logger.info(bstack111l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡤࡸ࡭ࡱࡪࠠࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠣࡥࡹࠦࡻࡾࠩ෎").format(bstack111lll11_opy_));
  except Exception as e:
    logger.debug(bstack1l1l1111l_opy_.format(str(e)))
def bstack1llll1l11l_opy_(bstack111ll11l_opy_):
  global CONFIG
  try:
    host = bstack111l_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪා") if bstack111l_opy_ (u"ࠨࡣࡳࡴࠬැ") in CONFIG else bstack111l_opy_ (u"ࠩࡤࡴ࡮࠭ෑ")
    user = CONFIG[bstack111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬි")]
    key = CONFIG[bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧී")]
    bstack1l1lllllll_opy_ = bstack111l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫු") if bstack111l_opy_ (u"࠭ࡡࡱࡲࠪ෕") in CONFIG else (bstack111l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫූ") if CONFIG.get(bstack111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ෗")) else bstack111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫෘ"))
    url = bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨෙ").format(user, key, host, bstack1l1lllllll_opy_,
                                                                                bstack111ll11l_opy_)
    headers = {
      bstack111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪේ"): bstack111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨෛ"),
    }
    proxies = bstack1ll1ll1l11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫො")], response.json()))
  except Exception as e:
    logger.debug(bstack1l111ll111_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack111lll1l_opy_
  try:
    if bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪෝ") in CONFIG:
      host = bstack111l_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫෞ") if bstack111l_opy_ (u"ࠩࡤࡴࡵ࠭ෟ") in CONFIG else bstack111l_opy_ (u"ࠪࡥࡵ࡯ࠧ෠")
      user = CONFIG[bstack111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭෡")]
      key = CONFIG[bstack111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ෢")]
      bstack1l1lllllll_opy_ = bstack111l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ෣") if bstack111l_opy_ (u"ࠧࡢࡲࡳࠫ෤") in CONFIG else bstack111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ෥")
      url = bstack111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩ෦").format(user, key, host, bstack1l1lllllll_opy_)
      headers = {
        bstack111l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ෧"): bstack111l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ෨"),
      }
      if bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ෩") in CONFIG:
        params = {bstack111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෪"): CONFIG[bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ෫")], bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ෬"): CONFIG[bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ෭")]}
      else:
        params = {bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ෮"): CONFIG[bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ෯")]}
      proxies = bstack1ll1ll1l11_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1lllllll11_opy_ = response.json()[0][bstack111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ෰")]
        if bstack1lllllll11_opy_:
          bstack11l1l1ll_opy_ = bstack1lllllll11_opy_[bstack111l_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ෱")].split(bstack111l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭ෲ"))[0] + bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩෳ") + bstack1lllllll11_opy_[
            bstack111l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ෴")]
          logger.info(bstack11lll1llll_opy_.format(bstack11l1l1ll_opy_))
          bstack111lll1l_opy_ = bstack1lllllll11_opy_[bstack111l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭෵")]
          bstack1lll1l1ll1_opy_ = CONFIG[bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ෶")]
          if bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ෷") in CONFIG:
            bstack1lll1l1ll1_opy_ += bstack111l_opy_ (u"࠭ࠠࠨ෸") + CONFIG[bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ෹")]
          if bstack1lll1l1ll1_opy_ != bstack1lllllll11_opy_[bstack111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭෺")]:
            logger.debug(bstack1ll11ll111_opy_.format(bstack1lllllll11_opy_[bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ෻")], bstack1lll1l1ll1_opy_))
          return [bstack1lllllll11_opy_[bstack111l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭෼")], bstack11l1l1ll_opy_]
    else:
      logger.warn(bstack1ll1lll111_opy_)
  except Exception as e:
    logger.debug(bstack1l1lllll_opy_.format(str(e)))
  return [None, None]
def bstack1l1111l1l1_opy_(url, bstack1l11l1ll_opy_=False):
  global CONFIG
  global bstack1ll11ll1ll_opy_
  if not bstack1ll11ll1ll_opy_:
    hostname = bstack11l1lllll_opy_(url)
    is_private = bstack11llll1l1_opy_(hostname)
    if (bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ෽") in CONFIG and not bstack111lll11l_opy_(CONFIG[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ෾")])) and (is_private or bstack1l11l1ll_opy_):
      bstack1ll11ll1ll_opy_ = hostname
def bstack11l1lllll_opy_(url):
  return urlparse(url).hostname
def bstack11llll1l1_opy_(hostname):
  for bstack1111lllll_opy_ in bstack1l1llll111_opy_:
    regex = re.compile(bstack1111lllll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111l1llll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1lll1llll1_opy_
  bstack1lll1lll1_opy_ = not (bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ෿"), None) and bstack1l1llll1l_opy_(
          threading.current_thread(), bstack111l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭฀"), None))
  bstack1llll1lll_opy_ = getattr(driver, bstack111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨก"), None) != True
  if not bstack1lll111ll_opy_.bstack1l1111l1_opy_(CONFIG, bstack1lll1llll1_opy_) or (bstack1llll1lll_opy_ and bstack1lll1lll1_opy_):
    logger.warning(bstack111l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧข"))
    return {}
  try:
    logger.debug(bstack111l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧฃ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack111111l11_opy_.bstack1ll1ll11l1_opy_)
    return results
  except Exception:
    logger.error(bstack111l_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨค"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1lll1llll1_opy_
  bstack1lll1lll1_opy_ = not (bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩฅ"), None) and bstack1l1llll1l_opy_(
          threading.current_thread(), bstack111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬฆ"), None))
  bstack1llll1lll_opy_ = getattr(driver, bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧง"), None) != True
  if not bstack1lll111ll_opy_.bstack1l1111l1_opy_(CONFIG, bstack1lll1llll1_opy_) or (bstack1llll1lll_opy_ and bstack1lll1lll1_opy_):
    logger.warning(bstack111l_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧจ"))
    return {}
  try:
    logger.debug(bstack111l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧฉ"))
    logger.debug(perform_scan(driver))
    bstack11lllll1ll_opy_ = driver.execute_async_script(bstack111111l11_opy_.bstack11l1lll1_opy_)
    return bstack11lllll1ll_opy_
  except Exception:
    logger.error(bstack111l_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦช"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1lll1llll1_opy_
  bstack1lll1lll1_opy_ = not (bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨซ"), None) and bstack1l1llll1l_opy_(
          threading.current_thread(), bstack111l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫฌ"), None))
  bstack1llll1lll_opy_ = getattr(driver, bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ญ"), None) != True
  if not bstack1lll111ll_opy_.bstack1l1111l1_opy_(CONFIG, bstack1lll1llll1_opy_) or (bstack1llll1lll_opy_ and bstack1lll1lll1_opy_):
    logger.warning(bstack111l_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤฎ"))
    return {}
  try:
    bstack111l111ll_opy_ = driver.execute_async_script(bstack111111l11_opy_.perform_scan, {bstack111l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨฏ"): kwargs.get(bstack111l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪฐ"), None) or bstack111l_opy_ (u"ࠪࠫฑ")})
    return bstack111l111ll_opy_
  except Exception:
    logger.error(bstack111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯࠰ࠥฒ"))
    return {}