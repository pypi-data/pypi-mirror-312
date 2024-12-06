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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111l111111_opy_, bstack1l1llll111_opy_, bstack11l1llll1_opy_, bstack1l1l11l1ll_opy_,
                                    bstack111l11111l_opy_, bstack1111llllll_opy_, bstack111l11l111_opy_, bstack111l111l11_opy_)
from bstack_utils.messages import bstack1lllll11l1_opy_, bstack1llll1ll1l_opy_
from bstack_utils.proxy import bstack1ll1ll1l11_opy_, bstack1l1ll11l11_opy_
bstack1l1ll1l111_opy_ = Config.bstack11llll1111_opy_()
logger = logging.getLogger(__name__)
def bstack111lll1111_opy_(config):
    return config[bstack111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫጴ")]
def bstack111lll111l_opy_(config):
    return config[bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ጵ")]
def bstack1l11lll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1lllll1l11l_opy_(obj):
    values = []
    bstack1111lll111_opy_ = re.compile(bstack111l_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣጶ"), re.I)
    for key in obj.keys():
        if bstack1111lll111_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1111111111_opy_(config):
    tags = []
    tags.extend(bstack1lllll1l11l_opy_(os.environ))
    tags.extend(bstack1lllll1l11l_opy_(config))
    return tags
def bstack11111l1l1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111ll1111_opy_(bstack1llllll1ll1_opy_):
    if not bstack1llllll1ll1_opy_:
        return bstack111l_opy_ (u"ࠬ࠭ጷ")
    return bstack111l_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢጸ").format(bstack1llllll1ll1_opy_.name, bstack1llllll1ll1_opy_.email)
def bstack111lll1l1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111l1l1ll_opy_ = repo.common_dir
        info = {
            bstack111l_opy_ (u"ࠢࡴࡪࡤࠦጹ"): repo.head.commit.hexsha,
            bstack111l_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦጺ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111l_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤጻ"): repo.active_branch.name,
            bstack111l_opy_ (u"ࠥࡸࡦ࡭ࠢጼ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢጽ"): bstack1111ll1111_opy_(repo.head.commit.committer),
            bstack111l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨጾ"): repo.head.commit.committed_datetime.isoformat(),
            bstack111l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨጿ"): bstack1111ll1111_opy_(repo.head.commit.author),
            bstack111l_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧፀ"): repo.head.commit.authored_datetime.isoformat(),
            bstack111l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤፁ"): repo.head.commit.message,
            bstack111l_opy_ (u"ࠤࡵࡳࡴࡺࠢፂ"): repo.git.rev_parse(bstack111l_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧፃ")),
            bstack111l_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧፄ"): bstack1111l1l1ll_opy_,
            bstack111l_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣፅ"): subprocess.check_output([bstack111l_opy_ (u"ࠨࡧࡪࡶࠥፆ"), bstack111l_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥፇ"), bstack111l_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦፈ")]).strip().decode(
                bstack111l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨፉ")),
            bstack111l_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧፊ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨፋ"): repo.git.rev_list(
                bstack111l_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧፌ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111l111ll_opy_ = []
        for remote in remotes:
            bstack1111ll1lll_opy_ = {
                bstack111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦፍ"): remote.name,
                bstack111l_opy_ (u"ࠢࡶࡴ࡯ࠦፎ"): remote.url,
            }
            bstack1111l111ll_opy_.append(bstack1111ll1lll_opy_)
        bstack1111l11l1l_opy_ = {
            bstack111l_opy_ (u"ࠣࡰࡤࡱࡪࠨፏ"): bstack111l_opy_ (u"ࠤࡪ࡭ࡹࠨፐ"),
            **info,
            bstack111l_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦፑ"): bstack1111l111ll_opy_
        }
        bstack1111l11l1l_opy_ = bstack1lllll1l1l1_opy_(bstack1111l11l1l_opy_)
        return bstack1111l11l1l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢፒ").format(err))
        return {}
def bstack1lllll1l1l1_opy_(bstack1111l11l1l_opy_):
    bstack1111l1ll1l_opy_ = bstack1llllll111l_opy_(bstack1111l11l1l_opy_)
    if bstack1111l1ll1l_opy_ and bstack1111l1ll1l_opy_ > bstack111l11111l_opy_:
        bstack1111l11111_opy_ = bstack1111l1ll1l_opy_ - bstack111l11111l_opy_
        bstack1111l11lll_opy_ = bstack11111ll111_opy_(bstack1111l11l1l_opy_[bstack111l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨፓ")], bstack1111l11111_opy_)
        bstack1111l11l1l_opy_[bstack111l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢፔ")] = bstack1111l11lll_opy_
        logger.info(bstack111l_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤፕ")
                    .format(bstack1llllll111l_opy_(bstack1111l11l1l_opy_) / 1024))
    return bstack1111l11l1l_opy_
def bstack1llllll111l_opy_(bstack111llll1l_opy_):
    try:
        if bstack111llll1l_opy_:
            bstack11111l1111_opy_ = json.dumps(bstack111llll1l_opy_)
            bstack1llllll1l1l_opy_ = sys.getsizeof(bstack11111l1111_opy_)
            return bstack1llllll1l1l_opy_
    except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣፖ").format(e))
    return -1
def bstack11111ll111_opy_(field, bstack1111l1l1l1_opy_):
    try:
        bstack1lllllll1l1_opy_ = len(bytes(bstack1111llllll_opy_, bstack111l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨፗ")))
        bstack1lllllll1ll_opy_ = bytes(field, bstack111l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩፘ"))
        bstack1llllllllll_opy_ = len(bstack1lllllll1ll_opy_)
        bstack1llllll11ll_opy_ = ceil(bstack1llllllllll_opy_ - bstack1111l1l1l1_opy_ - bstack1lllllll1l1_opy_)
        if bstack1llllll11ll_opy_ > 0:
            bstack1111111l11_opy_ = bstack1lllllll1ll_opy_[:bstack1llllll11ll_opy_].decode(bstack111l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪፙ"), errors=bstack111l_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬፚ")) + bstack1111llllll_opy_
            return bstack1111111l11_opy_
    except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦ፛").format(e))
    return field
def bstack11l11ll1l_opy_():
    env = os.environ
    if (bstack111l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ፜") in env and len(env[bstack111l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ፝")]) > 0) or (
            bstack111l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ፞") in env and len(env[bstack111l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ፟")]) > 0):
        return {
            bstack111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ፠"): bstack111l_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨ፡"),
            bstack111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ።"): env.get(bstack111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ፣")),
            bstack111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ፤"): env.get(bstack111l_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦ፥")),
            bstack111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ፦"): env.get(bstack111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ፧"))
        }
    if env.get(bstack111l_opy_ (u"ࠧࡉࡉࠣ፨")) == bstack111l_opy_ (u"ࠨࡴࡳࡷࡨࠦ፩") and bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤ፪"))):
        return {
            bstack111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ፫"): bstack111l_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦ፬"),
            bstack111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ፭"): env.get(bstack111l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ፮")),
            bstack111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ፯"): env.get(bstack111l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥ፰")),
            bstack111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፱"): env.get(bstack111l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦ፲"))
        }
    if env.get(bstack111l_opy_ (u"ࠤࡆࡍࠧ፳")) == bstack111l_opy_ (u"ࠥࡸࡷࡻࡥࠣ፴") and bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦ፵"))):
        return {
            bstack111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ፶"): bstack111l_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤ፷"),
            bstack111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ፸"): env.get(bstack111l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣ፹")),
            bstack111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ፺"): env.get(bstack111l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ፻")),
            bstack111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ፼"): env.get(bstack111l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ፽"))
        }
    if env.get(bstack111l_opy_ (u"ࠨࡃࡊࠤ፾")) == bstack111l_opy_ (u"ࠢࡵࡴࡸࡩࠧ፿") and env.get(bstack111l_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᎀ")) == bstack111l_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᎁ"):
        return {
            bstack111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᎂ"): bstack111l_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᎃ"),
            bstack111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎄ"): None,
            bstack111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᎅ"): None,
            bstack111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᎆ"): None
        }
    if env.get(bstack111l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᎇ")) and env.get(bstack111l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᎈ")):
        return {
            bstack111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᎉ"): bstack111l_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᎊ"),
            bstack111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎋ"): env.get(bstack111l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᎌ")),
            bstack111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎍ"): None,
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎎ"): env.get(bstack111l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᎏ"))
        }
    if env.get(bstack111l_opy_ (u"ࠥࡇࡎࠨ᎐")) == bstack111l_opy_ (u"ࠦࡹࡸࡵࡦࠤ᎑") and bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦ᎒"))):
        return {
            bstack111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᎓"): bstack111l_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ᎔"),
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᎕"): env.get(bstack111l_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧ᎖")),
            bstack111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᎗"): None,
            bstack111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᎘"): env.get(bstack111l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᎙"))
        }
    if env.get(bstack111l_opy_ (u"ࠨࡃࡊࠤ᎚")) == bstack111l_opy_ (u"ࠢࡵࡴࡸࡩࠧ᎛") and bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦ᎜"))):
        return {
            bstack111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᎝"): bstack111l_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨ᎞"),
            bstack111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᎟"): env.get(bstack111l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᎠ")),
            bstack111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᎡ"): env.get(bstack111l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᎢ")),
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎣ"): env.get(bstack111l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᎤ"))
        }
    if env.get(bstack111l_opy_ (u"ࠥࡇࡎࠨᎥ")) == bstack111l_opy_ (u"ࠦࡹࡸࡵࡦࠤᎦ") and bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᎧ"))):
        return {
            bstack111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎨ"): bstack111l_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᎩ"),
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎪ"): env.get(bstack111l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᎫ")),
            bstack111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᎬ"): env.get(bstack111l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᎭ")),
            bstack111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᎮ"): env.get(bstack111l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᎯ"))
        }
    if env.get(bstack111l_opy_ (u"ࠢࡄࡋࠥᎰ")) == bstack111l_opy_ (u"ࠣࡶࡵࡹࡪࠨᎱ") and bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᎲ"))):
        return {
            bstack111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᎳ"): bstack111l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᎴ"),
            bstack111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎵ"): env.get(bstack111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᎶ")),
            bstack111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎷ"): env.get(bstack111l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᎸ")) or env.get(bstack111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᎹ")),
            bstack111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᎺ"): env.get(bstack111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᎻ"))
        }
    if bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᎼ"))):
        return {
            bstack111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎽ"): bstack111l_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᎾ"),
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎿ"): bstack111l_opy_ (u"ࠤࡾࢁࢀࢃࠢᏀ").format(env.get(bstack111l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭Ꮑ")), env.get(bstack111l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᏂ"))),
            bstack111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᏃ"): env.get(bstack111l_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᏄ")),
            bstack111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᏅ"): env.get(bstack111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᏆ"))
        }
    if bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᏇ"))):
        return {
            bstack111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᏈ"): bstack111l_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᏉ"),
            bstack111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏊ"): bstack111l_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᏋ").format(env.get(bstack111l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭Ꮜ")), env.get(bstack111l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᏍ")), env.get(bstack111l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᏎ")), env.get(bstack111l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᏏ"))),
            bstack111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᏐ"): env.get(bstack111l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᏑ")),
            bstack111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᏒ"): env.get(bstack111l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᏓ"))
        }
    if env.get(bstack111l_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᏔ")) and env.get(bstack111l_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᏕ")):
        return {
            bstack111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᏖ"): bstack111l_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᏗ"),
            bstack111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏘ"): bstack111l_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᏙ").format(env.get(bstack111l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᏚ")), env.get(bstack111l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭Ꮫ")), env.get(bstack111l_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩᏜ"))),
            bstack111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏝ"): env.get(bstack111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᏞ")),
            bstack111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏟ"): env.get(bstack111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᏠ"))
        }
    if any([env.get(bstack111l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᏡ")), env.get(bstack111l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᏢ")), env.get(bstack111l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᏣ"))]):
        return {
            bstack111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᏤ"): bstack111l_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦᏥ"),
            bstack111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏦ"): env.get(bstack111l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᏧ")),
            bstack111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᏨ"): env.get(bstack111l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᏩ")),
            bstack111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᏪ"): env.get(bstack111l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᏫ"))
        }
    if env.get(bstack111l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᏬ")):
        return {
            bstack111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏭ"): bstack111l_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᏮ"),
            bstack111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏯ"): env.get(bstack111l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᏰ")),
            bstack111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏱ"): env.get(bstack111l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᏲ")),
            bstack111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏳ"): env.get(bstack111l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᏴ"))
        }
    if env.get(bstack111l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᏵ")) or env.get(bstack111l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤ᏶")):
        return {
            bstack111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᏷"): bstack111l_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᏸ"),
            bstack111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᏹ"): env.get(bstack111l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᏺ")),
            bstack111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᏻ"): bstack111l_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᏼ") if env.get(bstack111l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᏽ")) else None,
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᏾"): env.get(bstack111l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢ᏿"))
        }
    if any([env.get(bstack111l_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣ᐀")), env.get(bstack111l_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᐁ")), env.get(bstack111l_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᐂ"))]):
        return {
            bstack111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐃ"): bstack111l_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᐄ"),
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐅ"): None,
            bstack111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᐆ"): env.get(bstack111l_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᐇ")),
            bstack111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᐈ"): env.get(bstack111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᐉ"))
        }
    if env.get(bstack111l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᐊ")):
        return {
            bstack111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐋ"): bstack111l_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦᐌ"),
            bstack111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐍ"): env.get(bstack111l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᐎ")),
            bstack111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᐏ"): bstack111l_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᐐ").format(env.get(bstack111l_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᐑ"))) if env.get(bstack111l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᐒ")) else None,
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐓ"): env.get(bstack111l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᐔ"))
        }
    if bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦᐕ"))):
        return {
            bstack111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᐖ"): bstack111l_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨᐗ"),
            bstack111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᐘ"): env.get(bstack111l_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦᐙ")),
            bstack111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᐚ"): env.get(bstack111l_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧᐛ")),
            bstack111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᐜ"): env.get(bstack111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᐝ"))
        }
    if bstack111lll11l_opy_(env.get(bstack111l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᐞ"))):
        return {
            bstack111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐟ"): bstack111l_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᐠ"),
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᐡ"): bstack111l_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᐢ").format(env.get(bstack111l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᐣ")), env.get(bstack111l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᐤ")), env.get(bstack111l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᐥ"))),
            bstack111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᐦ"): env.get(bstack111l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᐧ")),
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐨ"): env.get(bstack111l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᐩ"))
        }
    if env.get(bstack111l_opy_ (u"ࠥࡇࡎࠨᐪ")) == bstack111l_opy_ (u"ࠦࡹࡸࡵࡦࠤᐫ") and env.get(bstack111l_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᐬ")) == bstack111l_opy_ (u"ࠨ࠱ࠣᐭ"):
        return {
            bstack111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᐮ"): bstack111l_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᐯ"),
            bstack111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᐰ"): bstack111l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᐱ").format(env.get(bstack111l_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᐲ"))),
            bstack111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᐳ"): None,
            bstack111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐴ"): None,
        }
    if env.get(bstack111l_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᐵ")):
        return {
            bstack111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᐶ"): bstack111l_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᐷ"),
            bstack111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᐸ"): None,
            bstack111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᐹ"): env.get(bstack111l_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᐺ")),
            bstack111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᐻ"): env.get(bstack111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᐼ"))
        }
    if any([env.get(bstack111l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᐽ")), env.get(bstack111l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᐾ")), env.get(bstack111l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᐿ")), env.get(bstack111l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᑀ"))]):
        return {
            bstack111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᑁ"): bstack111l_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᑂ"),
            bstack111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᑃ"): None,
            bstack111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᑄ"): env.get(bstack111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᑅ")) or None,
            bstack111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᑆ"): env.get(bstack111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᑇ"), 0)
        }
    if env.get(bstack111l_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᑈ")):
        return {
            bstack111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᑉ"): bstack111l_opy_ (u"ࠢࡈࡱࡆࡈࠧᑊ"),
            bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᑋ"): None,
            bstack111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᑌ"): env.get(bstack111l_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᑍ")),
            bstack111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᑎ"): env.get(bstack111l_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᑏ"))
        }
    if env.get(bstack111l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᑐ")):
        return {
            bstack111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᑑ"): bstack111l_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᑒ"),
            bstack111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᑓ"): env.get(bstack111l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᑔ")),
            bstack111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᑕ"): env.get(bstack111l_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᑖ")),
            bstack111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᑗ"): env.get(bstack111l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᑘ"))
        }
    return {bstack111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᑙ"): None}
def get_host_info():
    return {
        bstack111l_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᑚ"): platform.node(),
        bstack111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᑛ"): platform.system(),
        bstack111l_opy_ (u"ࠦࡹࡿࡰࡦࠤᑜ"): platform.machine(),
        bstack111l_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᑝ"): platform.version(),
        bstack111l_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᑞ"): platform.architecture()[0]
    }
def bstack11lll11ll1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1lllll1l1ll_opy_():
    if bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᑟ")):
        return bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᑠ")
    return bstack111l_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᑡ")
def bstack1111l1llll_opy_(driver):
    info = {
        bstack111l_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᑢ"): driver.capabilities,
        bstack111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᑣ"): driver.session_id,
        bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᑤ"): driver.capabilities.get(bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᑥ"), None),
        bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᑦ"): driver.capabilities.get(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᑧ"), None),
        bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᑨ"): driver.capabilities.get(bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᑩ"), None),
    }
    if bstack1lllll1l1ll_opy_() == bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᑪ"):
        if bstack1111l1l1l_opy_():
            info[bstack111l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᑫ")] = bstack111l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᑬ")
        elif driver.capabilities.get(bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑭ"), {}).get(bstack111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᑮ"), False):
            info[bstack111l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᑯ")] = bstack111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᑰ")
        else:
            info[bstack111l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᑱ")] = bstack111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᑲ")
    return info
def bstack1111l1l1l_opy_():
    if bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᑳ")):
        return True
    if bstack111lll11l_opy_(os.environ.get(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᑴ"), None)):
        return True
    return False
def bstack1111ll11l_opy_(bstack1lllll1lll1_opy_, url, data, config):
    headers = config.get(bstack111l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᑵ"), None)
    proxies = bstack1ll1ll1l11_opy_(config, url)
    auth = config.get(bstack111l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᑶ"), None)
    response = requests.request(
            bstack1lllll1lll1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack111ll1ll1_opy_(bstack1l1111llll_opy_, size):
    bstack1lll1l1lll_opy_ = []
    while len(bstack1l1111llll_opy_) > size:
        bstack1111111l1_opy_ = bstack1l1111llll_opy_[:size]
        bstack1lll1l1lll_opy_.append(bstack1111111l1_opy_)
        bstack1l1111llll_opy_ = bstack1l1111llll_opy_[size:]
    bstack1lll1l1lll_opy_.append(bstack1l1111llll_opy_)
    return bstack1lll1l1lll_opy_
def bstack11111l11ll_opy_(message, bstack11111lllll_opy_=False):
    os.write(1, bytes(message, bstack111l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᑷ")))
    os.write(1, bytes(bstack111l_opy_ (u"ࠫࡡࡴࠧᑸ"), bstack111l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᑹ")))
    if bstack11111lllll_opy_:
        with open(bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬᑺ") + os.environ[bstack111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᑻ")] + bstack111l_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ᑼ"), bstack111l_opy_ (u"ࠩࡤࠫᑽ")) as f:
            f.write(message + bstack111l_opy_ (u"ࠪࡠࡳ࠭ᑾ"))
def bstack1111ll111l_opy_():
    return os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᑿ")].lower() == bstack111l_opy_ (u"ࠬࡺࡲࡶࡧࠪᒀ")
def bstack1lll1lll11_opy_(bstack1111lll1ll_opy_):
    return bstack111l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᒁ").format(bstack111l111111_opy_, bstack1111lll1ll_opy_)
def bstack1ll11l111l_opy_():
    return bstack11l1lll1ll_opy_().replace(tzinfo=None).isoformat() + bstack111l_opy_ (u"࡛ࠧࠩᒂ")
def bstack11111ll11l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111l_opy_ (u"ࠨ࡜ࠪᒃ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111l_opy_ (u"ࠩ࡝ࠫᒄ")))).total_seconds() * 1000
def bstack1111l111l1_opy_(timestamp):
    return bstack1llllllll11_opy_(timestamp).isoformat() + bstack111l_opy_ (u"ࠪ࡞ࠬᒅ")
def bstack11111ll1l1_opy_(bstack1111ll11l1_opy_):
    date_format = bstack111l_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩᒆ")
    bstack1lllll1llll_opy_ = datetime.datetime.strptime(bstack1111ll11l1_opy_, date_format)
    return bstack1lllll1llll_opy_.isoformat() + bstack111l_opy_ (u"ࠬࡠࠧᒇ")
def bstack11111lll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒈ")
    else:
        return bstack111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᒉ")
def bstack111lll11l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᒊ")
def bstack1111llll11_opy_(val):
    return val.__str__().lower() == bstack111l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᒋ")
def bstack11l1lll111_opy_(bstack111111l11l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111111l11l_opy_ as e:
                print(bstack111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᒌ").format(func.__name__, bstack111111l11l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1llllllll1l_opy_(bstack11111l1l11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11111l1l11_opy_(cls, *args, **kwargs)
            except bstack111111l11l_opy_ as e:
                print(bstack111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᒍ").format(bstack11111l1l11_opy_.__name__, bstack111111l11l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1llllllll1l_opy_
    else:
        return decorator
def bstack1l1ll111l1_opy_(bstack11l11111l1_opy_):
    if bstack111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᒎ") in bstack11l11111l1_opy_ and bstack1111llll11_opy_(bstack11l11111l1_opy_[bstack111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᒏ")]):
        return False
    if bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᒐ") in bstack11l11111l1_opy_ and bstack1111llll11_opy_(bstack11l11111l1_opy_[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᒑ")]):
        return False
    return True
def bstack1111l1lll_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l11l1ll1l_opy_(hub_url, CONFIG):
    if bstack11lll11111_opy_() <= version.parse(bstack111l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᒒ")):
        if hub_url != bstack111l_opy_ (u"ࠪࠫᒓ"):
            return bstack111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᒔ") + hub_url + bstack111l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᒕ")
        return bstack11l1llll1_opy_
    if hub_url != bstack111l_opy_ (u"࠭ࠧᒖ"):
        return bstack111l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᒗ") + hub_url + bstack111l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᒘ")
    return bstack1l1l11l1ll_opy_
def bstack1lllll1l111_opy_():
    return isinstance(os.getenv(bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᒙ")), str)
def bstack11l1lllll_opy_(url):
    return urlparse(url).hostname
def bstack11llll1l1_opy_(hostname):
    for bstack1111lllll_opy_ in bstack1l1llll111_opy_:
        regex = re.compile(bstack1111lllll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1llllll1l11_opy_(bstack1111ll1l11_opy_, file_name, logger):
    bstack1l1lll1ll1_opy_ = os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠪࢂࠬᒚ")), bstack1111ll1l11_opy_)
    try:
        if not os.path.exists(bstack1l1lll1ll1_opy_):
            os.makedirs(bstack1l1lll1ll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠫࢃ࠭ᒛ")), bstack1111ll1l11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111l_opy_ (u"ࠬࡽࠧᒜ")):
                pass
            with open(file_path, bstack111l_opy_ (u"ࠨࡷࠬࠤᒝ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lllll11l1_opy_.format(str(e)))
def bstack1lllll1ll11_opy_(file_name, key, value, logger):
    file_path = bstack1llllll1l11_opy_(bstack111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᒞ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11lllllll1_opy_ = json.load(open(file_path, bstack111l_opy_ (u"ࠨࡴࡥࠫᒟ")))
        else:
            bstack11lllllll1_opy_ = {}
        bstack11lllllll1_opy_[key] = value
        with open(file_path, bstack111l_opy_ (u"ࠤࡺ࠯ࠧᒠ")) as outfile:
            json.dump(bstack11lllllll1_opy_, outfile)
def bstack11lll111l1_opy_(file_name, logger):
    file_path = bstack1llllll1l11_opy_(bstack111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᒡ"), file_name, logger)
    bstack11lllllll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111l_opy_ (u"ࠫࡷ࠭ᒢ")) as bstack11l1l11l_opy_:
            bstack11lllllll1_opy_ = json.load(bstack11l1l11l_opy_)
    return bstack11lllllll1_opy_
def bstack1l1ll1lll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᒣ") + file_path + bstack111l_opy_ (u"࠭ࠠࠨᒤ") + str(e))
def bstack11lll11111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111l_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᒥ")
def bstack1llll1lll1_opy_(config):
    if bstack111l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᒦ") in config:
        del (config[bstack111l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᒧ")])
        return False
    if bstack11lll11111_opy_() < version.parse(bstack111l_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᒨ")):
        return False
    if bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᒩ")):
        return True
    if bstack111l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᒪ") in config and config[bstack111l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᒫ")] is False:
        return False
    else:
        return True
def bstack11lll1l1l_opy_(args_list, bstack111111ll1l_opy_):
    index = -1
    for value in bstack111111ll1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11ll11111l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11ll11111l_opy_ = bstack11ll11111l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᒬ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒭ"), exception=exception)
    def bstack111lllll11_opy_(self):
        if self.result != bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᒮ"):
            return None
        if isinstance(self.exception_type, str) and bstack111l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᒯ") in self.exception_type:
            return bstack111l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᒰ")
        return bstack111l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᒱ")
    def bstack11111ll1ll_opy_(self):
        if self.result != bstack111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒲ"):
            return None
        if self.bstack11ll11111l_opy_:
            return self.bstack11ll11111l_opy_
        return bstack11111111l1_opy_(self.exception)
def bstack11111111l1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1llllll11l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1llll1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack111111l1_opy_(config, logger):
    try:
        import playwright
        bstack1lllllll111_opy_ = playwright.__file__
        bstack1111l11l11_opy_ = os.path.split(bstack1lllllll111_opy_)
        bstack1111l1111l_opy_ = bstack1111l11l11_opy_[0] + bstack111l_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᒳ")
        os.environ[bstack111l_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᒴ")] = bstack1l1ll11l11_opy_(config)
        with open(bstack1111l1111l_opy_, bstack111l_opy_ (u"ࠩࡵࠫᒵ")) as f:
            bstack1lll111l11_opy_ = f.read()
            bstack1111ll1l1l_opy_ = bstack111l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᒶ")
            bstack1111111lll_opy_ = bstack1lll111l11_opy_.find(bstack1111ll1l1l_opy_)
            if bstack1111111lll_opy_ == -1:
              process = subprocess.Popen(bstack111l_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᒷ"), shell=True, cwd=bstack1111l11l11_opy_[0])
              process.wait()
              bstack1111ll11ll_opy_ = bstack111l_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᒸ")
              bstack11111llll1_opy_ = bstack111l_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᒹ")
              bstack1111ll1ll1_opy_ = bstack1lll111l11_opy_.replace(bstack1111ll11ll_opy_, bstack11111llll1_opy_)
              with open(bstack1111l1111l_opy_, bstack111l_opy_ (u"ࠧࡸࠩᒺ")) as f:
                f.write(bstack1111ll1ll1_opy_)
    except Exception as e:
        logger.error(bstack1llll1ll1l_opy_.format(str(e)))
def bstack1l11111lll_opy_():
  try:
    bstack1llllll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᒻ"))
    bstack1111lll1l1_opy_ = []
    if os.path.exists(bstack1llllll1111_opy_):
      with open(bstack1llllll1111_opy_) as f:
        bstack1111lll1l1_opy_ = json.load(f)
      os.remove(bstack1llllll1111_opy_)
    return bstack1111lll1l1_opy_
  except:
    pass
  return []
def bstack1ll1l111_opy_(bstack11ll1ll1_opy_):
  try:
    bstack1111lll1l1_opy_ = []
    bstack1llllll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack111l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᒼ"))
    if os.path.exists(bstack1llllll1111_opy_):
      with open(bstack1llllll1111_opy_) as f:
        bstack1111lll1l1_opy_ = json.load(f)
    bstack1111lll1l1_opy_.append(bstack11ll1ll1_opy_)
    with open(bstack1llllll1111_opy_, bstack111l_opy_ (u"ࠪࡻࠬᒽ")) as f:
        json.dump(bstack1111lll1l1_opy_, f)
  except:
    pass
def bstack1l11llll1l_opy_(logger, bstack1llllll1lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack111l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᒾ"), bstack111l_opy_ (u"ࠬ࠭ᒿ"))
    if test_name == bstack111l_opy_ (u"࠭ࠧᓀ"):
        test_name = threading.current_thread().__dict__.get(bstack111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ᓁ"), bstack111l_opy_ (u"ࠨࠩᓂ"))
    bstack111111111l_opy_ = bstack111l_opy_ (u"ࠩ࠯ࠤࠬᓃ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1llllll1lll_opy_:
        bstack1l11lll11l_opy_ = os.environ.get(bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᓄ"), bstack111l_opy_ (u"ࠫ࠵࠭ᓅ"))
        bstack11111ll1_opy_ = {bstack111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓆ"): test_name, bstack111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᓇ"): bstack111111111l_opy_, bstack111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᓈ"): bstack1l11lll11l_opy_}
        bstack11111111ll_opy_ = []
        bstack1lllllll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᓉ"))
        if os.path.exists(bstack1lllllll11l_opy_):
            with open(bstack1lllllll11l_opy_) as f:
                bstack11111111ll_opy_ = json.load(f)
        bstack11111111ll_opy_.append(bstack11111ll1_opy_)
        with open(bstack1lllllll11l_opy_, bstack111l_opy_ (u"ࠩࡺࠫᓊ")) as f:
            json.dump(bstack11111111ll_opy_, f)
    else:
        bstack11111ll1_opy_ = {bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨᓋ"): test_name, bstack111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᓌ"): bstack111111111l_opy_, bstack111l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᓍ"): str(multiprocessing.current_process().name)}
        if bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪᓎ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11111ll1_opy_)
  except Exception as e:
      logger.warn(bstack111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᓏ").format(e))
def bstack1l111ll1_opy_(error_message, test_name, index, logger):
  try:
    bstack11111l1ll1_opy_ = []
    bstack11111ll1_opy_ = {bstack111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᓐ"): test_name, bstack111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᓑ"): error_message, bstack111l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᓒ"): index}
    bstack1111111ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᓓ"))
    if os.path.exists(bstack1111111ll1_opy_):
        with open(bstack1111111ll1_opy_) as f:
            bstack11111l1ll1_opy_ = json.load(f)
    bstack11111l1ll1_opy_.append(bstack11111ll1_opy_)
    with open(bstack1111111ll1_opy_, bstack111l_opy_ (u"ࠬࡽࠧᓔ")) as f:
        json.dump(bstack11111l1ll1_opy_, f)
  except Exception as e:
    logger.warn(bstack111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᓕ").format(e))
def bstack1l111ll11l_opy_(bstack1111111ll_opy_, name, logger):
  try:
    bstack11111ll1_opy_ = {bstack111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᓖ"): name, bstack111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᓗ"): bstack1111111ll_opy_, bstack111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᓘ"): str(threading.current_thread()._name)}
    return bstack11111ll1_opy_
  except Exception as e:
    logger.warn(bstack111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᓙ").format(e))
  return
def bstack111111lll1_opy_():
    return platform.system() == bstack111l_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬᓚ")
def bstack1l1l1l11_opy_(bstack1111l1l11l_opy_, config, logger):
    bstack1111l1ll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111l1l11l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᓛ").format(e))
    return bstack1111l1ll11_opy_
def bstack111111l1ll_opy_(bstack1111111l1l_opy_, bstack111111l1l1_opy_):
    bstack1lllll1ll1l_opy_ = version.parse(bstack1111111l1l_opy_)
    bstack11111lll11_opy_ = version.parse(bstack111111l1l1_opy_)
    if bstack1lllll1ll1l_opy_ > bstack11111lll11_opy_:
        return 1
    elif bstack1lllll1ll1l_opy_ < bstack11111lll11_opy_:
        return -1
    else:
        return 0
def bstack11l1lll1ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1llllllll11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1lllllllll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1ll1111111_opy_(options, framework, bstack1ll11lll1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack111l_opy_ (u"࠭ࡧࡦࡶࠪᓜ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11111lll_opy_ = caps.get(bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓝ"))
    bstack1111l1l111_opy_ = True
    bstack111ll1111_opy_ = os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᓞ")]
    if bstack1111llll11_opy_(caps.get(bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩ࡜࠹ࡃࠨᓟ"))) or bstack1111llll11_opy_(caps.get(bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪᓠ"))):
        bstack1111l1l111_opy_ = False
    if bstack1llll1lll1_opy_({bstack111l_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦᓡ"): bstack1111l1l111_opy_}):
        bstack11111lll_opy_ = bstack11111lll_opy_ or {}
        bstack11111lll_opy_[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᓢ")] = bstack1lllllllll1_opy_(framework)
        bstack11111lll_opy_[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᓣ")] = bstack1111ll111l_opy_()
        bstack11111lll_opy_[bstack111l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᓤ")] = bstack111ll1111_opy_
        bstack11111lll_opy_[bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᓥ")] = bstack1ll11lll1_opy_
        if getattr(options, bstack111l_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᓦ"), None):
            options.set_capability(bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᓧ"), bstack11111lll_opy_)
        else:
            options[bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᓨ")] = bstack11111lll_opy_
    else:
        if getattr(options, bstack111l_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ᓩ"), None):
            options.set_capability(bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᓪ"), bstack1lllllllll1_opy_(framework))
            options.set_capability(bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᓫ"), bstack1111ll111l_opy_())
            options.set_capability(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᓬ"), bstack111ll1111_opy_)
            options.set_capability(bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᓭ"), bstack1ll11lll1_opy_)
        else:
            options[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᓮ")] = bstack1lllllllll1_opy_(framework)
            options[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᓯ")] = bstack1111ll111l_opy_()
            options[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᓰ")] = bstack111ll1111_opy_
            options[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᓱ")] = bstack1ll11lll1_opy_
    return options
def bstack11111l11l1_opy_(bstack1111l11ll1_opy_, framework):
    bstack1ll11lll1_opy_ = bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤᓲ"))
    if bstack1111l11ll1_opy_ and len(bstack1111l11ll1_opy_.split(bstack111l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᓳ"))) > 1:
        ws_url = bstack1111l11ll1_opy_.split(bstack111l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᓴ"))[0]
        if bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᓵ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111l111l_opy_ = json.loads(urllib.parse.unquote(bstack1111l11ll1_opy_.split(bstack111l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᓶ"))[1]))
            bstack11111l111l_opy_ = bstack11111l111l_opy_ or {}
            bstack111ll1111_opy_ = os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᓷ")]
            bstack11111l111l_opy_[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᓸ")] = str(framework) + str(__version__)
            bstack11111l111l_opy_[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᓹ")] = bstack1111ll111l_opy_()
            bstack11111l111l_opy_[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᓺ")] = bstack111ll1111_opy_
            bstack11111l111l_opy_[bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᓻ")] = bstack1ll11lll1_opy_
            bstack1111l11ll1_opy_ = bstack1111l11ll1_opy_.split(bstack111l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᓼ"))[0] + bstack111l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᓽ") + urllib.parse.quote(json.dumps(bstack11111l111l_opy_))
    return bstack1111l11ll1_opy_
def bstack11ll11ll1_opy_():
    global bstack1ll1lll1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll1lll1_opy_ = BrowserType.connect
    return bstack1ll1lll1_opy_
def bstack1ll1llll11_opy_(framework_name):
    global bstack11lll1111_opy_
    bstack11lll1111_opy_ = framework_name
    return framework_name
def bstack11l11l1l_opy_(self, *args, **kwargs):
    global bstack1ll1lll1_opy_
    try:
        global bstack11lll1111_opy_
        if bstack111l_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᓾ") in kwargs:
            kwargs[bstack111l_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᓿ")] = bstack11111l11l1_opy_(
                kwargs.get(bstack111l_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᔀ"), None),
                bstack11lll1111_opy_
            )
    except Exception as e:
        logger.error(bstack111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣᔁ").format(str(e)))
    return bstack1ll1lll1_opy_(self, *args, **kwargs)
def bstack111111ll11_opy_(bstack111111l111_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll1ll1l11_opy_(bstack111111l111_opy_, bstack111l_opy_ (u"ࠤࠥᔂ"))
        if proxies and proxies.get(bstack111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᔃ")):
            parsed_url = urlparse(proxies.get(bstack111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᔄ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨᔅ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩᔆ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᔇ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫᔈ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l11lll111_opy_(bstack111111l111_opy_):
    bstack11111l1lll_opy_ = {
        bstack111l111l11_opy_[bstack1111l1lll1_opy_]: bstack111111l111_opy_[bstack1111l1lll1_opy_]
        for bstack1111l1lll1_opy_ in bstack111111l111_opy_
        if bstack1111l1lll1_opy_ in bstack111l111l11_opy_
    }
    bstack11111l1lll_opy_[bstack111l_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤᔉ")] = bstack111111ll11_opy_(bstack111111l111_opy_, bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᔊ")))
    bstack111111llll_opy_ = [element.lower() for element in bstack111l11l111_opy_]
    bstack1111lll11l_opy_(bstack11111l1lll_opy_, bstack111111llll_opy_)
    return bstack11111l1lll_opy_
def bstack1111lll11l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack111l_opy_ (u"ࠦ࠯࠰ࠪࠫࠤᔋ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111lll11l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111lll11l_opy_(item, keys)