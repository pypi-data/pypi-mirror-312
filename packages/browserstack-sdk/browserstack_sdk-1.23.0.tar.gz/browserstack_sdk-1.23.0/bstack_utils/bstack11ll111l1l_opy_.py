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
from uuid import uuid4
from bstack_utils.helper import bstack1ll11l111l_opy_, bstack11111ll11l_opy_
from bstack_utils.bstack1l11l1llll_opy_ import bstack1ll1lll11ll_opy_
class bstack11l1l1l1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11ll11llll_opy_=None, framework=None, tags=[], scope=[], bstack1ll1l11ll11_opy_=None, bstack1ll1l11l111_opy_=True, bstack1ll1l1l1l1l_opy_=None, bstack11l111111_opy_=None, result=None, duration=None, bstack11l1ll1l1l_opy_=None, meta={}):
        self.bstack11l1ll1l1l_opy_ = bstack11l1ll1l1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1l11l111_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11ll11llll_opy_ = bstack11ll11llll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1l11ll11_opy_ = bstack1ll1l11ll11_opy_
        self.bstack1ll1l1l1l1l_opy_ = bstack1ll1l1l1l1l_opy_
        self.bstack11l111111_opy_ = bstack11l111111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack11l11l111l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11ll1l1ll1_opy_(self, meta):
        self.meta = meta
    def bstack11ll1l1lll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll1l111lll_opy_(self):
        bstack1ll1l1l1111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᚩ"): bstack1ll1l1l1111_opy_,
            bstack111l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᚪ"): bstack1ll1l1l1111_opy_,
            bstack111l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᚫ"): bstack1ll1l1l1111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111l_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᚬ") + key)
            setattr(self, key, val)
    def bstack1ll1l11l1l1_opy_(self):
        return {
            bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᚭ"): self.name,
            bstack111l_opy_ (u"ࠪࡦࡴࡪࡹࠨᚮ"): {
                bstack111l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᚯ"): bstack111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᚰ"),
                bstack111l_opy_ (u"࠭ࡣࡰࡦࡨࠫᚱ"): self.code
            },
            bstack111l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᚲ"): self.scope,
            bstack111l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᚳ"): self.tags,
            bstack111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᚴ"): self.framework,
            bstack111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᚵ"): self.bstack11ll11llll_opy_
        }
    def bstack1ll1l1l1lll_opy_(self):
        return {
         bstack111l_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᚶ"): self.meta
        }
    def bstack1ll1l11llll_opy_(self):
        return {
            bstack111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᚷ"): {
                bstack111l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᚸ"): self.bstack1ll1l11ll11_opy_
            }
        }
    def bstack1ll1l11lll1_opy_(self, bstack1ll1l1l11ll_opy_, details):
        step = next(filter(lambda st: st[bstack111l_opy_ (u"ࠧࡪࡦࠪᚹ")] == bstack1ll1l1l11ll_opy_, self.meta[bstack111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᚺ")]), None)
        step.update(details)
    def bstack1l1l1lll11_opy_(self, bstack1ll1l1l11ll_opy_):
        step = next(filter(lambda st: st[bstack111l_opy_ (u"ࠩ࡬ࡨࠬᚻ")] == bstack1ll1l1l11ll_opy_, self.meta[bstack111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᚼ")]), None)
        step.update({
            bstack111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᚽ"): bstack1ll11l111l_opy_()
        })
    def bstack11ll11ll11_opy_(self, bstack1ll1l1l11ll_opy_, result, duration=None):
        bstack1ll1l1l1l1l_opy_ = bstack1ll11l111l_opy_()
        if bstack1ll1l1l11ll_opy_ is not None and self.meta.get(bstack111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᚾ")):
            step = next(filter(lambda st: st[bstack111l_opy_ (u"࠭ࡩࡥࠩᚿ")] == bstack1ll1l1l11ll_opy_, self.meta[bstack111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᛀ")]), None)
            step.update({
                bstack111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛁ"): bstack1ll1l1l1l1l_opy_,
                bstack111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᛂ"): duration if duration else bstack11111ll11l_opy_(step[bstack111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᛃ")], bstack1ll1l1l1l1l_opy_),
                bstack111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᛄ"): result.result,
                bstack111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᛅ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1l1l1ll1_opy_):
        if self.meta.get(bstack111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᛆ")):
            self.meta[bstack111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᛇ")].append(bstack1ll1l1l1ll1_opy_)
        else:
            self.meta[bstack111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᛈ")] = [ bstack1ll1l1l1ll1_opy_ ]
    def bstack1ll1l11l11l_opy_(self):
        return {
            bstack111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᛉ"): self.bstack11l11l111l_opy_(),
            **self.bstack1ll1l11l1l1_opy_(),
            **self.bstack1ll1l111lll_opy_(),
            **self.bstack1ll1l1l1lll_opy_()
        }
    def bstack1ll1l11ll1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᛊ"): self.bstack1ll1l1l1l1l_opy_,
            bstack111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᛋ"): self.duration,
            bstack111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᛌ"): self.result.result
        }
        if data[bstack111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᛍ")] == bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᛎ"):
            data[bstack111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᛏ")] = self.result.bstack111lllll11_opy_()
            data[bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᛐ")] = [{bstack111l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᛑ"): self.result.bstack11111ll1ll_opy_()}]
        return data
    def bstack1ll1l111ll1_opy_(self):
        return {
            bstack111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᛒ"): self.bstack11l11l111l_opy_(),
            **self.bstack1ll1l11l1l1_opy_(),
            **self.bstack1ll1l111lll_opy_(),
            **self.bstack1ll1l11ll1l_opy_(),
            **self.bstack1ll1l1l1lll_opy_()
        }
    def bstack11l1ll1lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111l_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᛓ") in event:
            return self.bstack1ll1l11l11l_opy_()
        elif bstack111l_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᛔ") in event:
            return self.bstack1ll1l111ll1_opy_()
    def bstack11l11l1111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1l1l1l1l_opy_ = time if time else bstack1ll11l111l_opy_()
        self.duration = duration if duration else bstack11111ll11l_opy_(self.bstack11ll11llll_opy_, self.bstack1ll1l1l1l1l_opy_)
        if result:
            self.result = result
class bstack11ll1111l1_opy_(bstack11l1l1l1ll_opy_):
    def __init__(self, hooks=[], bstack11ll11l111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11ll11l111_opy_ = bstack11ll11l111_opy_
        super().__init__(*args, **kwargs, bstack11l111111_opy_=bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࠬᛕ"))
    @classmethod
    def bstack1ll1l1l11l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111l_opy_ (u"ࠨ࡫ࡧࠫᛖ"): id(step),
                bstack111l_opy_ (u"ࠩࡷࡩࡽࡺࠧᛗ"): step.name,
                bstack111l_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᛘ"): step.keyword,
            })
        return bstack11ll1111l1_opy_(
            **kwargs,
            meta={
                bstack111l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᛙ"): {
                    bstack111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᛚ"): feature.name,
                    bstack111l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᛛ"): feature.filename,
                    bstack111l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᛜ"): feature.description
                },
                bstack111l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᛝ"): {
                    bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᛞ"): scenario.name
                },
                bstack111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᛟ"): steps,
                bstack111l_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᛠ"): bstack1ll1lll11ll_opy_(test)
            }
        )
    def bstack1ll1l111l1l_opy_(self):
        return {
            bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᛡ"): self.hooks
        }
    def bstack1ll1l1l111l_opy_(self):
        if self.bstack11ll11l111_opy_:
            return {
                bstack111l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᛢ"): self.bstack11ll11l111_opy_
            }
        return {}
    def bstack1ll1l111ll1_opy_(self):
        return {
            **super().bstack1ll1l111ll1_opy_(),
            **self.bstack1ll1l111l1l_opy_()
        }
    def bstack1ll1l11l11l_opy_(self):
        return {
            **super().bstack1ll1l11l11l_opy_(),
            **self.bstack1ll1l1l111l_opy_()
        }
    def bstack11l11l1111_opy_(self):
        return bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᛣ")
class bstack11ll1ll11l_opy_(bstack11l1l1l1ll_opy_):
    def __init__(self, hook_type, *args,bstack11ll11l111_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1l1l1l11_opy_ = None
        self.bstack11ll11l111_opy_ = bstack11ll11l111_opy_
        super().__init__(*args, **kwargs, bstack11l111111_opy_=bstack111l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᛤ"))
    def bstack11l1l111l1_opy_(self):
        return self.hook_type
    def bstack1ll1l11l1ll_opy_(self):
        return {
            bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᛥ"): self.hook_type
        }
    def bstack1ll1l111ll1_opy_(self):
        return {
            **super().bstack1ll1l111ll1_opy_(),
            **self.bstack1ll1l11l1ll_opy_()
        }
    def bstack1ll1l11l11l_opy_(self):
        return {
            **super().bstack1ll1l11l11l_opy_(),
            bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᛦ"): self.bstack1ll1l1l1l11_opy_,
            **self.bstack1ll1l11l1ll_opy_()
        }
    def bstack11l11l1111_opy_(self):
        return bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᛧ")
    def bstack11ll1ll111_opy_(self, bstack1ll1l1l1l11_opy_):
        self.bstack1ll1l1l1l11_opy_ = bstack1ll1l1l1l11_opy_