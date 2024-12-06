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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll11l111_opy_
bstack1l1ll1l111_opy_ = Config.bstack11llll1111_opy_()
def bstack1ll1lllll11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1111111_opy_(bstack1ll1llllll1_opy_, bstack1ll1llll1ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1llllll1_opy_):
        with open(bstack1ll1llllll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll1lllll11_opy_(bstack1ll1llllll1_opy_):
        pac = get_pac(url=bstack1ll1llllll1_opy_)
    else:
        raise Exception(bstack111l_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩᘚ").format(bstack1ll1llllll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111l_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦᘛ"), 80))
        bstack1ll1lllllll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1lllllll_opy_ = bstack111l_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬᘜ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1llll1ll_opy_, bstack1ll1lllllll_opy_)
    return proxy_url
def bstack1l1ll1ll1_opy_(config):
    return bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᘝ") in config or bstack111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᘞ") in config
def bstack1l1ll11l11_opy_(config):
    if not bstack1l1ll1ll1_opy_(config):
        return
    if config.get(bstack111l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᘟ")):
        return config.get(bstack111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᘠ"))
    if config.get(bstack111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᘡ")):
        return config.get(bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᘢ"))
def bstack1ll1ll1l11_opy_(config, bstack1ll1llll1ll_opy_):
    proxy = bstack1l1ll11l11_opy_(config)
    proxies = {}
    if config.get(bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᘣ")) or config.get(bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᘤ")):
        if proxy.endswith(bstack111l_opy_ (u"࠭࠮ࡱࡣࡦࠫᘥ")):
            proxies = bstack11ll11l1_opy_(proxy, bstack1ll1llll1ll_opy_)
        else:
            proxies = {
                bstack111l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᘦ"): proxy
            }
    bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᘧ"), proxies)
    return proxies
def bstack11ll11l1_opy_(bstack1ll1llllll1_opy_, bstack1ll1llll1ll_opy_):
    proxies = {}
    global bstack1ll1llll1l1_opy_
    if bstack111l_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᘨ") in globals():
        return bstack1ll1llll1l1_opy_
    try:
        proxy = bstack1lll1111111_opy_(bstack1ll1llllll1_opy_, bstack1ll1llll1ll_opy_)
        if bstack111l_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᘩ") in proxy:
            proxies = {}
        elif bstack111l_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᘪ") in proxy or bstack111l_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᘫ") in proxy or bstack111l_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᘬ") in proxy:
            bstack1ll1lllll1l_opy_ = proxy.split(bstack111l_opy_ (u"ࠢࠡࠤᘭ"))
            if bstack111l_opy_ (u"ࠣ࠼࠲࠳ࠧᘮ") in bstack111l_opy_ (u"ࠤࠥᘯ").join(bstack1ll1lllll1l_opy_[1:]):
                proxies = {
                    bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᘰ"): bstack111l_opy_ (u"ࠦࠧᘱ").join(bstack1ll1lllll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᘲ"): str(bstack1ll1lllll1l_opy_[0]).lower() + bstack111l_opy_ (u"ࠨ࠺࠰࠱ࠥᘳ") + bstack111l_opy_ (u"ࠢࠣᘴ").join(bstack1ll1lllll1l_opy_[1:])
                }
        elif bstack111l_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᘵ") in proxy:
            bstack1ll1lllll1l_opy_ = proxy.split(bstack111l_opy_ (u"ࠤࠣࠦᘶ"))
            if bstack111l_opy_ (u"ࠥ࠾࠴࠵ࠢᘷ") in bstack111l_opy_ (u"ࠦࠧᘸ").join(bstack1ll1lllll1l_opy_[1:]):
                proxies = {
                    bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᘹ"): bstack111l_opy_ (u"ࠨࠢᘺ").join(bstack1ll1lllll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᘻ"): bstack111l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᘼ") + bstack111l_opy_ (u"ࠤࠥᘽ").join(bstack1ll1lllll1l_opy_[1:])
                }
        else:
            proxies = {
                bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᘾ"): proxy
            }
    except Exception as e:
        print(bstack111l_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᘿ"), bstack1llll11l111_opy_.format(bstack1ll1llllll1_opy_, str(e)))
    bstack1ll1llll1l1_opy_ = proxies
    return proxies