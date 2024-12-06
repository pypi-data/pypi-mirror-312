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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1lll1lll11_opy_, bstack1111ll11l_opy_
class bstack1l1ll111ll_opy_:
  working_dir = os.getcwd()
  bstack1111l1l1l_opy_ = False
  config = {}
  binary_path = bstack111l_opy_ (u"ࠬ࠭ᖦ")
  bstack1lll11l111l_opy_ = bstack111l_opy_ (u"࠭ࠧᖧ")
  bstack11l11l111_opy_ = False
  bstack1lll1l1llll_opy_ = None
  bstack1llll11111l_opy_ = {}
  bstack1lll11ll1ll_opy_ = 300
  bstack1lll1ll1l1l_opy_ = False
  logger = None
  bstack1lll1l1l111_opy_ = False
  bstack1l1ll11lll_opy_ = False
  bstack11ll1l111_opy_ = None
  bstack1lll1ll1111_opy_ = bstack111l_opy_ (u"ࠧࠨᖨ")
  bstack1lll11l1lll_opy_ = {
    bstack111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᖩ") : 1,
    bstack111l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᖪ") : 2,
    bstack111l_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᖫ") : 3,
    bstack111l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᖬ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lll11l1l11_opy_(self):
    bstack1lll1l11lll_opy_ = bstack111l_opy_ (u"ࠬ࠭ᖭ")
    bstack1lll1ll1lll_opy_ = sys.platform
    bstack1lll1l1ll1l_opy_ = bstack111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᖮ")
    if re.match(bstack111l_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢᖯ"), bstack1lll1ll1lll_opy_) != None:
      bstack1lll1l11lll_opy_ = bstack111l1111l1_opy_ + bstack111l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤᖰ")
      self.bstack1lll1ll1111_opy_ = bstack111l_opy_ (u"ࠩࡰࡥࡨ࠭ᖱ")
    elif re.match(bstack111l_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣᖲ"), bstack1lll1ll1lll_opy_) != None:
      bstack1lll1l11lll_opy_ = bstack111l1111l1_opy_ + bstack111l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧᖳ")
      bstack1lll1l1ll1l_opy_ = bstack111l_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣᖴ")
      self.bstack1lll1ll1111_opy_ = bstack111l_opy_ (u"࠭ࡷࡪࡰࠪᖵ")
    else:
      bstack1lll1l11lll_opy_ = bstack111l1111l1_opy_ + bstack111l_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥᖶ")
      self.bstack1lll1ll1111_opy_ = bstack111l_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᖷ")
    return bstack1lll1l11lll_opy_, bstack1lll1l1ll1l_opy_
  def bstack1lll1lll1ll_opy_(self):
    try:
      bstack1lll11ll1l1_opy_ = [os.path.join(expanduser(bstack111l_opy_ (u"ࠤࢁࠦᖸ")), bstack111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᖹ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lll11ll1l1_opy_:
        if(self.bstack1lll1lll111_opy_(path)):
          return path
      raise bstack111l_opy_ (u"࡚ࠦࡴࡡ࡭ࡤࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᖺ")
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢᖻ").format(e))
  def bstack1lll1lll111_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lll1ll111l_opy_(self, bstack1lll1l11lll_opy_, bstack1lll1l1ll1l_opy_):
    try:
      bstack1lll11l1111_opy_ = self.bstack1lll1lll1ll_opy_()
      bstack1lll1l11l11_opy_ = os.path.join(bstack1lll11l1111_opy_, bstack111l_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩᖼ"))
      bstack1lll1l11l1l_opy_ = os.path.join(bstack1lll11l1111_opy_, bstack1lll1l1ll1l_opy_)
      if os.path.exists(bstack1lll1l11l1l_opy_):
        self.logger.info(bstack111l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᖽ").format(bstack1lll1l11l1l_opy_))
        return bstack1lll1l11l1l_opy_
      if os.path.exists(bstack1lll1l11l11_opy_):
        self.logger.info(bstack111l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨᖾ").format(bstack1lll1l11l11_opy_))
        return self.bstack1lll11l11l1_opy_(bstack1lll1l11l11_opy_, bstack1lll1l1ll1l_opy_)
      self.logger.info(bstack111l_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢᖿ").format(bstack1lll1l11lll_opy_))
      response = bstack1111ll11l_opy_(bstack111l_opy_ (u"ࠪࡋࡊ࡚ࠧᗀ"), bstack1lll1l11lll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1lll1l11l11_opy_, bstack111l_opy_ (u"ࠫࡼࡨࠧᗁ")) as file:
          file.write(response.content)
        self.logger.info(bstack111l_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥᗂ").format(bstack1lll1l11l11_opy_))
        return self.bstack1lll11l11l1_opy_(bstack1lll1l11l11_opy_, bstack1lll1l1ll1l_opy_)
      else:
        raise(bstack111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤᗃ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᗄ").format(e))
  def bstack1lll1ll11l1_opy_(self, bstack1lll1l11lll_opy_, bstack1lll1l1ll1l_opy_):
    try:
      retry = 2
      bstack1lll1l11l1l_opy_ = None
      bstack1lll1l1l1l1_opy_ = False
      while retry > 0:
        bstack1lll1l11l1l_opy_ = self.bstack1lll1ll111l_opy_(bstack1lll1l11lll_opy_, bstack1lll1l1ll1l_opy_)
        bstack1lll1l1l1l1_opy_ = self.bstack1lll1llll1l_opy_(bstack1lll1l11lll_opy_, bstack1lll1l1ll1l_opy_, bstack1lll1l11l1l_opy_)
        if bstack1lll1l1l1l1_opy_:
          break
        retry -= 1
      return bstack1lll1l11l1l_opy_, bstack1lll1l1l1l1_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧᗅ").format(e))
    return bstack1lll1l11l1l_opy_, False
  def bstack1lll1llll1l_opy_(self, bstack1lll1l11lll_opy_, bstack1lll1l1ll1l_opy_, bstack1lll1l11l1l_opy_, bstack1lll1l111ll_opy_ = 0):
    if bstack1lll1l111ll_opy_ > 1:
      return False
    if bstack1lll1l11l1l_opy_ == None or os.path.exists(bstack1lll1l11l1l_opy_) == False:
      self.logger.warn(bstack111l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᗆ"))
      return False
    bstack1lll1ll11ll_opy_ = bstack111l_opy_ (u"ࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾࡢ࠯ࡤ࡮࡬ࠤࡡࡪ࠮࡝ࡦ࠮࠲ࡡࡪࠫࠣᗇ")
    command = bstack111l_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪᗈ").format(bstack1lll1l11l1l_opy_)
    bstack1llll1111l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1lll1ll11ll_opy_, bstack1llll1111l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack111l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦᗉ"))
      return False
  def bstack1lll11l11l1_opy_(self, bstack1lll1l11l11_opy_, bstack1lll1l1ll1l_opy_):
    try:
      working_dir = os.path.dirname(bstack1lll1l11l11_opy_)
      shutil.unpack_archive(bstack1lll1l11l11_opy_, working_dir)
      bstack1lll1l11l1l_opy_ = os.path.join(working_dir, bstack1lll1l1ll1l_opy_)
      os.chmod(bstack1lll1l11l1l_opy_, 0o755)
      return bstack1lll1l11l1l_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᗊ"))
  def bstack1lll11llll1_opy_(self):
    try:
      bstack1lll1l11111_opy_ = self.config.get(bstack111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᗋ"))
      bstack1lll11llll1_opy_ = bstack1lll1l11111_opy_ or (bstack1lll1l11111_opy_ is None and self.bstack1111l1l1l_opy_)
      if not bstack1lll11llll1_opy_ or self.config.get(bstack111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᗌ"), None) not in bstack111l111l1l_opy_:
        return False
      self.bstack11l11l111_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᗍ").format(e))
  def bstack1lll11l11ll_opy_(self):
    try:
      bstack1lll11l11ll_opy_ = self.bstack1lll111llll_opy_
      return bstack1lll11l11ll_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᗎ").format(e))
  def init(self, bstack1111l1l1l_opy_, config, logger):
    self.bstack1111l1l1l_opy_ = bstack1111l1l1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lll11llll1_opy_():
      return
    self.bstack1llll11111l_opy_ = config.get(bstack111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᗏ"), {})
    self.bstack1lll111llll_opy_ = config.get(bstack111l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᗐ"))
    try:
      bstack1lll1l11lll_opy_, bstack1lll1l1ll1l_opy_ = self.bstack1lll11l1l11_opy_()
      bstack1lll1l11l1l_opy_, bstack1lll1l1l1l1_opy_ = self.bstack1lll1ll11l1_opy_(bstack1lll1l11lll_opy_, bstack1lll1l1ll1l_opy_)
      if bstack1lll1l1l1l1_opy_:
        self.binary_path = bstack1lll1l11l1l_opy_
        thread = Thread(target=self.bstack1lll1l111l1_opy_)
        thread.start()
      else:
        self.bstack1lll1l1l111_opy_ = True
        self.logger.error(bstack111l_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥᗑ").format(bstack1lll1l11l1l_opy_))
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᗒ").format(e))
  def bstack1lll11l1l1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111l_opy_ (u"ࠨ࡮ࡲ࡫ࠬᗓ"), bstack111l_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬᗔ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111l_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢᗕ").format(logfile))
      self.bstack1lll11l111l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᗖ").format(e))
  def bstack1lll1l111l1_opy_(self):
    bstack1lll1lll1l1_opy_ = self.bstack1lll11ll11l_opy_()
    if bstack1lll1lll1l1_opy_ == None:
      self.bstack1lll1l1l111_opy_ = True
      self.logger.error(bstack111l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣᗗ"))
      return False
    command_args = [bstack111l_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢᗘ") if self.bstack1111l1l1l_opy_ else bstack111l_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫᗙ")]
    bstack1lll1llllll_opy_ = self.bstack1lll1ll1l11_opy_()
    if bstack1lll1llllll_opy_ != None:
      command_args.append(bstack111l_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢᗚ").format(bstack1lll1llllll_opy_))
    env = os.environ.copy()
    env[bstack111l_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢᗛ")] = bstack1lll1lll1l1_opy_
    env[bstack111l_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥᗜ")] = os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᗝ"), bstack111l_opy_ (u"ࠬ࠭ᗞ"))
    bstack1lll1l1l11l_opy_ = [self.binary_path]
    self.bstack1lll11l1l1l_opy_()
    self.bstack1lll1l1llll_opy_ = self.bstack1llll1111ll_opy_(bstack1lll1l1l11l_opy_ + command_args, env)
    self.logger.debug(bstack111l_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᗟ"))
    bstack1lll1l111ll_opy_ = 0
    while self.bstack1lll1l1llll_opy_.poll() == None:
      bstack1lll11lll11_opy_ = self.bstack1lll1l11ll1_opy_()
      if bstack1lll11lll11_opy_:
        self.logger.debug(bstack111l_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᗠ"))
        self.bstack1lll1ll1l1l_opy_ = True
        return True
      bstack1lll1l111ll_opy_ += 1
      self.logger.debug(bstack111l_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᗡ").format(bstack1lll1l111ll_opy_))
      time.sleep(2)
    self.logger.error(bstack111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᗢ").format(bstack1lll1l111ll_opy_))
    self.bstack1lll1l1l111_opy_ = True
    return False
  def bstack1lll1l11ll1_opy_(self, bstack1lll1l111ll_opy_ = 0):
    if bstack1lll1l111ll_opy_ > 10:
      return False
    try:
      bstack1lll1lllll1_opy_ = os.environ.get(bstack111l_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᗣ"), bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᗤ"))
      bstack1lll1l1ll11_opy_ = bstack1lll1lllll1_opy_ + bstack111l11l1ll_opy_
      response = requests.get(bstack1lll1l1ll11_opy_)
      data = response.json()
      self.bstack11ll1l111_opy_ = data.get(bstack111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫᗥ"), {}).get(bstack111l_opy_ (u"࠭ࡩࡥࠩᗦ"), None)
      return True
    except:
      self.logger.debug(bstack111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧᗧ"))
      return False
  def bstack1lll11ll11l_opy_(self):
    bstack1lll1ll1ll1_opy_ = bstack111l_opy_ (u"ࠨࡣࡳࡴࠬᗨ") if self.bstack1111l1l1l_opy_ else bstack111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᗩ")
    bstack1lll1l1l1ll_opy_ = bstack111l_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᗪ") if self.config.get(bstack111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᗫ")) is None else True
    bstack1111lll1ll_opy_ = bstack111l_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨᗬ").format(self.config[bstack111l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᗭ")], bstack1lll1ll1ll1_opy_, bstack1lll1l1l1ll_opy_)
    if self.bstack1lll111llll_opy_:
      bstack1111lll1ll_opy_ += bstack111l_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤᗮ").format(self.bstack1lll111llll_opy_)
    uri = bstack1lll1lll11_opy_(bstack1111lll1ll_opy_)
    try:
      response = bstack1111ll11l_opy_(bstack111l_opy_ (u"ࠨࡉࡈࡘࠬᗯ"), uri, {}, {bstack111l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᗰ"): (self.config[bstack111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᗱ")], self.config[bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᗲ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l11l111_opy_ = data.get(bstack111l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᗳ"))
        self.bstack1lll111llll_opy_ = data.get(bstack111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࠫᗴ"))
        os.environ[bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᗵ")] = str(self.bstack11l11l111_opy_)
        os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᗶ")] = str(self.bstack1lll111llll_opy_)
        if bstack1lll1l1l1ll_opy_ == bstack111l_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧᗷ") and str(self.bstack11l11l111_opy_).lower() == bstack111l_opy_ (u"ࠥࡸࡷࡻࡥࠣᗸ"):
          self.bstack1l1ll11lll_opy_ = True
        if bstack111l_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥᗹ") in data:
          return data[bstack111l_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᗺ")]
        else:
          raise bstack111l_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭ᗻ").format(data)
      else:
        raise bstack111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢᗼ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤᗽ").format(e))
  def bstack1lll1ll1l11_opy_(self):
    bstack1lll11lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack111l_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧᗾ"))
    try:
      if bstack111l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᗿ") not in self.bstack1llll11111l_opy_:
        self.bstack1llll11111l_opy_[bstack111l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᘀ")] = 2
      with open(bstack1lll11lllll_opy_, bstack111l_opy_ (u"ࠬࡽࠧᘁ")) as fp:
        json.dump(self.bstack1llll11111l_opy_, fp)
      return bstack1lll11lllll_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᘂ").format(e))
  def bstack1llll1111ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1lll1ll1111_opy_ == bstack111l_opy_ (u"ࠧࡸ࡫ࡱࠫᘃ"):
        bstack1lll1l1lll1_opy_ = [bstack111l_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩᘄ"), bstack111l_opy_ (u"ࠩ࠲ࡧࠬᘅ")]
        cmd = bstack1lll1l1lll1_opy_ + cmd
      cmd = bstack111l_opy_ (u"ࠪࠤࠬᘆ").join(cmd)
      self.logger.debug(bstack111l_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣᘇ").format(cmd))
      with open(self.bstack1lll11l111l_opy_, bstack111l_opy_ (u"ࠧࡧࠢᘈ")) as bstack1llll111111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llll111111_opy_, text=True, stderr=bstack1llll111111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lll1l1l111_opy_ = True
      self.logger.error(bstack111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᘉ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lll1ll1l1l_opy_:
        self.logger.info(bstack111l_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣᘊ"))
        cmd = [self.binary_path, bstack111l_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦᘋ")]
        self.bstack1llll1111ll_opy_(cmd)
        self.bstack1lll1ll1l1l_opy_ = False
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᘌ").format(cmd, e))
  def bstack1ll11l1l1_opy_(self):
    if not self.bstack11l11l111_opy_:
      return
    try:
      bstack1lll1lll11l_opy_ = 0
      while not self.bstack1lll1ll1l1l_opy_ and bstack1lll1lll11l_opy_ < self.bstack1lll11ll1ll_opy_:
        if self.bstack1lll1l1l111_opy_:
          self.logger.info(bstack111l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣᘍ"))
          return
        time.sleep(1)
        bstack1lll1lll11l_opy_ += 1
      os.environ[bstack111l_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪᘎ")] = str(self.bstack1lll11lll1l_opy_())
      self.logger.info(bstack111l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨᘏ"))
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᘐ").format(e))
  def bstack1lll11lll1l_opy_(self):
    if self.bstack1111l1l1l_opy_:
      return
    try:
      bstack1lll11ll111_opy_ = [platform[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᘑ")].lower() for platform in self.config.get(bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᘒ"), [])]
      bstack1lll1l1111l_opy_ = sys.maxsize
      bstack1lll11l1ll1_opy_ = bstack111l_opy_ (u"ࠩࠪᘓ")
      for browser in bstack1lll11ll111_opy_:
        if browser in self.bstack1lll11l1lll_opy_:
          bstack1lll1llll11_opy_ = self.bstack1lll11l1lll_opy_[browser]
        if bstack1lll1llll11_opy_ < bstack1lll1l1111l_opy_:
          bstack1lll1l1111l_opy_ = bstack1lll1llll11_opy_
          bstack1lll11l1ll1_opy_ = browser
      return bstack1lll11l1ll1_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᘔ").format(e))
  @classmethod
  def bstack1ll11llll1_opy_(self):
    return os.getenv(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᘕ"), bstack111l_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫᘖ")).lower()
  @classmethod
  def bstack1l1ll1ll_opy_(self):
    return os.getenv(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪᘗ"), bstack111l_opy_ (u"ࠧࠨᘘ"))