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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111l111lll_opy_, bstack111l11l111_opy_
import tempfile
import json
bstack1llll1l11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨᔷ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack111l_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬᔸ"),
      datefmt=bstack111l_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪᔹ"),
      stream=sys.stdout
    )
  return logger
def bstack1llll11lll1_opy_():
  global bstack1llll1l11l1_opy_
  if os.path.exists(bstack1llll1l11l1_opy_):
    os.remove(bstack1llll1l11l1_opy_)
def bstack1l11lll1l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1lll11lll_opy_(config, log_level):
  bstack1llll1l1ll1_opy_ = log_level
  if bstack111l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᔺ") in config and config[bstack111l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᔻ")] in bstack111l111lll_opy_:
    bstack1llll1l1ll1_opy_ = bstack111l111lll_opy_[config[bstack111l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᔼ")]]
  if config.get(bstack111l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᔽ"), False):
    logging.getLogger().setLevel(bstack1llll1l1ll1_opy_)
    return bstack1llll1l1ll1_opy_
  global bstack1llll1l11l1_opy_
  bstack1l11lll1l_opy_()
  bstack1llll11ll11_opy_ = logging.Formatter(
    fmt=bstack111l_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᔾ"),
    datefmt=bstack111l_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩᔿ")
  )
  bstack1llll11llll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1llll1l11l1_opy_)
  file_handler.setFormatter(bstack1llll11ll11_opy_)
  bstack1llll11llll_opy_.setFormatter(bstack1llll11ll11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1llll11llll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack111l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪᕀ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1llll11llll_opy_.setLevel(bstack1llll1l1ll1_opy_)
  logging.getLogger().addHandler(bstack1llll11llll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1llll1l1ll1_opy_
def bstack1llll11ll1l_opy_(config):
  try:
    bstack1llll1l1l1l_opy_ = set(bstack111l11l111_opy_)
    bstack1llll1l1111_opy_ = bstack111l_opy_ (u"ࠩࠪᕁ")
    with open(bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ᕂ")) as bstack1llll1l11ll_opy_:
      bstack1llll1l1l11_opy_ = bstack1llll1l11ll_opy_.read()
      bstack1llll1l1111_opy_ = re.sub(bstack111l_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄࠩ࠮ࠫࠦ࡟ࡲࠬᕃ"), bstack111l_opy_ (u"ࠬ࠭ᕄ"), bstack1llll1l1l11_opy_, flags=re.M)
      bstack1llll1l1111_opy_ = re.sub(
        bstack111l_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠩࠩᕅ") + bstack111l_opy_ (u"ࠧࡽࠩᕆ").join(bstack1llll1l1l1l_opy_) + bstack111l_opy_ (u"ࠨࠫ࠱࠮ࠩ࠭ᕇ"),
        bstack111l_opy_ (u"ࡴࠪࡠ࠷ࡀࠠ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᕈ"),
        bstack1llll1l1111_opy_, flags=re.M | re.I
      )
    def bstack1llll1l111l_opy_(dic):
      bstack1llll11l1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llll1l1l1l_opy_:
          bstack1llll11l1l1_opy_[key] = bstack111l_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᕉ")
        else:
          if isinstance(value, dict):
            bstack1llll11l1l1_opy_[key] = bstack1llll1l111l_opy_(value)
          else:
            bstack1llll11l1l1_opy_[key] = value
      return bstack1llll11l1l1_opy_
    bstack1llll11l1l1_opy_ = bstack1llll1l111l_opy_(config)
    return {
      bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᕊ"): bstack1llll1l1111_opy_,
      bstack111l_opy_ (u"ࠬ࡬ࡩ࡯ࡣ࡯ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᕋ"): json.dumps(bstack1llll11l1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack11l11l1l1_opy_(config):
  global bstack1llll1l11l1_opy_
  try:
    if config.get(bstack111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᕌ"), False):
      return
    uuid = os.getenv(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᕍ"))
    if not uuid or uuid == bstack111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᕎ"):
      return
    bstack1llll11l1ll_opy_ = [bstack111l_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬᕏ"), bstack111l_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫᕐ"), bstack111l_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬᕑ"), bstack1llll1l11l1_opy_]
    bstack1l11lll1l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡲ࡯ࡨࡵ࠰ࠫᕒ") + uuid + bstack111l_opy_ (u"࠭࠮ࡵࡣࡵ࠲࡬ࢀࠧᕓ"))
    with tarfile.open(output_file, bstack111l_opy_ (u"ࠢࡸ࠼ࡪࡾࠧᕔ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1llll11l1ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1llll11ll1l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llll11l11l_opy_ = data.encode()
        tarinfo.size = len(bstack1llll11l11l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llll11l11l_opy_))
    bstack11lllll11_opy_ = MultipartEncoder(
      fields= {
        bstack111l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᕕ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack111l_opy_ (u"ࠩࡵࡦࠬᕖ")), bstack111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࠰࡫ࡿ࡯ࡰࠨᕗ")),
        bstack111l_opy_ (u"ࠫࡨࡲࡩࡦࡰࡷࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᕘ"): uuid
      }
    )
    response = requests.post(
      bstack111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡵࡱ࡮ࡲࡥࡩ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢᕙ"),
      data=bstack11lllll11_opy_,
      headers={bstack111l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᕚ"): bstack11lllll11_opy_.content_type},
      auth=(config[bstack111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᕛ")], config[bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᕜ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡰࡴࡧࡤࠡ࡮ࡲ࡫ࡸࡀࠠࠨᕝ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠩᕞ") + str(e))
  finally:
    try:
      bstack1llll11lll1_opy_()
    except:
      pass