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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11ll111l1l_opy_ import bstack11ll1ll11l_opy_, bstack11ll1111l1_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack1lll1lllll_opy_
from bstack_utils.helper import bstack1l1llll1l_opy_, bstack1ll11l111l_opy_, Result
from bstack_utils.bstack1l11ll1l1l_opy_ import bstack11ll111ll_opy_
from bstack_utils.capture import bstack11ll111l11_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11llll111l_opy_:
    def __init__(self):
        self.bstack11ll11l11l_opy_ = bstack11ll111l11_opy_(self.bstack11ll1l11l1_opy_)
        self.tests = {}
    @staticmethod
    def bstack11ll1l11l1_opy_(log):
        if not (log[bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧฺࠪ")] and log[bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ฻")].strip()):
            return
        active = bstack1lll1lllll_opy_.bstack11ll1l1111_opy_()
        log = {
            bstack111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ฼"): log[bstack111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ฽")],
            bstack111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ฾"): bstack1ll11l111l_opy_(),
            bstack111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ฿"): log[bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩเ")],
        }
        if active:
            if active[bstack111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧแ")] == bstack111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨโ"):
                log[bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫใ")] = active[bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬไ")]
            elif active[bstack111l_opy_ (u"࠭ࡴࡺࡲࡨࠫๅ")] == bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࠬๆ"):
                log[bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ็")] = active[bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥ่ࠩ")]
        bstack11ll111ll_opy_.bstack11l11l1l1_opy_([log])
    def start_test(self, attrs):
        bstack11ll1ll1l1_opy_ = uuid4().__str__()
        self.tests[bstack11ll1ll1l1_opy_] = {}
        self.bstack11ll11l11l_opy_.start()
        driver = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳ้ࠩ"), None)
        bstack11ll111l1l_opy_ = bstack11ll1111l1_opy_(
            name=attrs.scenario.name,
            uuid=bstack11ll1ll1l1_opy_,
            bstack11ll11llll_opy_=bstack1ll11l111l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack111l_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫๊ࠧ"),
            framework=bstack111l_opy_ (u"ࠬࡈࡥࡩࡣࡹࡩ๋ࠬ"),
            scope=[attrs.feature.name],
            bstack11ll11l111_opy_=bstack11ll111ll_opy_.bstack11ll111ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11ll1ll1l1_opy_][bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ์")] = bstack11ll111l1l_opy_
        threading.current_thread().current_test_uuid = bstack11ll1ll1l1_opy_
        bstack11ll111ll_opy_.bstack11ll111lll_opy_(bstack111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨํ"), bstack11ll111l1l_opy_)
    def end_test(self, attrs):
        bstack11ll1l1l1l_opy_ = {
            bstack111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ๎"): attrs.feature.name,
            bstack111l_opy_ (u"ࠤࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢ๏"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11ll111l1l_opy_ = self.tests[current_test_uuid][bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭๐")]
        meta = {
            bstack111l_opy_ (u"ࠦ࡫࡫ࡡࡵࡷࡵࡩࠧ๑"): bstack11ll1l1l1l_opy_,
            bstack111l_opy_ (u"ࠧࡹࡴࡦࡲࡶࠦ๒"): bstack11ll111l1l_opy_.meta.get(bstack111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ๓"), []),
            bstack111l_opy_ (u"ࠢࡴࡥࡨࡲࡦࡸࡩࡰࠤ๔"): {
                bstack111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ๕"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11ll111l1l_opy_.bstack11ll1l1ll1_opy_(meta)
        bstack11ll111l1l_opy_.bstack11ll1l1lll_opy_(bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ๖"), []))
        bstack11ll11lll1_opy_, exception = self._11ll1l1l11_opy_(attrs)
        bstack11ll1l11ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11ll11111l_opy_=[bstack11ll11lll1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭๗")].stop(time=bstack1ll11l111l_opy_(), duration=int(attrs.duration)*1000, result=bstack11ll1l11ll_opy_)
        bstack11ll111ll_opy_.bstack11ll111lll_opy_(bstack111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭๘"), self.tests[threading.current_thread().current_test_uuid][bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ๙")])
    def bstack1l1l1lll11_opy_(self, attrs):
        bstack11ll11l1ll_opy_ = {
            bstack111l_opy_ (u"࠭ࡩࡥࠩ๚"): uuid4().__str__(),
            bstack111l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ๛"): attrs.keyword,
            bstack111l_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨ๜"): [],
            bstack111l_opy_ (u"ࠩࡷࡩࡽࡺࠧ๝"): attrs.name,
            bstack111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ๞"): bstack1ll11l111l_opy_(),
            bstack111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ๟"): bstack111l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭๠"),
            bstack111l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ๡"): bstack111l_opy_ (u"ࠧࠨ๢")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ๣")].add_step(bstack11ll11l1ll_opy_)
        threading.current_thread().current_step_uuid = bstack11ll11l1ll_opy_[bstack111l_opy_ (u"ࠩ࡬ࡨࠬ๤")]
    def bstack11l11lll_opy_(self, attrs):
        current_test_id = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ๥"), None)
        current_step_uuid = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨ๦"), None)
        bstack11ll11lll1_opy_, exception = self._11ll1l1l11_opy_(attrs)
        bstack11ll1l11ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11ll11111l_opy_=[bstack11ll11lll1_opy_])
        self.tests[current_test_id][bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ๧")].bstack11ll11ll11_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11ll1l11ll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack111111l1l_opy_(self, name, attrs):
        try:
            bstack11ll1111ll_opy_ = uuid4().__str__()
            self.tests[bstack11ll1111ll_opy_] = {}
            self.bstack11ll11l11l_opy_.start()
            scopes = []
            driver = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ๨"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ๩")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11ll1111ll_opy_)
            if name in [bstack111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ๪"), bstack111l_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧ๫")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ๬"), bstack111l_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠦ๭")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack111l_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭๮")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11ll1ll11l_opy_(
                name=name,
                uuid=bstack11ll1111ll_opy_,
                bstack11ll11llll_opy_=bstack1ll11l111l_opy_(),
                file_path=file_path,
                framework=bstack111l_opy_ (u"ࠨࡂࡦࡪࡤࡺࡪࠨ๯"),
                bstack11ll11l111_opy_=bstack11ll111ll_opy_.bstack11ll111ll1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack111l_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣ๰"),
                hook_type=name
            )
            self.tests[bstack11ll1111ll_opy_][bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡢࡶࡤࠦ๱")] = hook_data
            current_test_id = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠤࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨ๲"), None)
            if current_test_id:
                hook_data.bstack11ll1ll111_opy_(current_test_id)
            if name == bstack111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ๳"):
                threading.current_thread().before_all_hook_uuid = bstack11ll1111ll_opy_
            threading.current_thread().current_hook_uuid = bstack11ll1111ll_opy_
            bstack11ll111ll_opy_.bstack11ll111lll_opy_(bstack111l_opy_ (u"ࠦࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠧ๴"), hook_data)
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡࡪࡲࡳࡰࠦࡥࡷࡧࡱࡸࡸ࠲ࠠࡩࡱࡲ࡯ࠥࡴࡡ࡮ࡧ࠽ࠤࠪࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠧࡶࠦ๵"), name, e)
    def bstack111111111_opy_(self, attrs):
        bstack11ll1l111l_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ๶"), None)
        hook_data = self.tests[bstack11ll1l111l_opy_][bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ๷")]
        status = bstack111l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ๸")
        exception = None
        bstack11ll11lll1_opy_ = None
        if hook_data.name == bstack111l_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧ๹"):
            self.bstack11ll11l11l_opy_.reset()
            bstack11ll11l1l1_opy_ = self.tests[bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ๺"), None)][bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ๻")].result.result
            if bstack11ll11l1l1_opy_ == bstack111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ๼"):
                if attrs.hook_failures == 1:
                    status = bstack111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ๽")
                elif attrs.hook_failures == 2:
                    status = bstack111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ๾")
            elif attrs.bstack11ll11ll1l_opy_:
                status = bstack111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ๿")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack111l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭຀") and attrs.hook_failures == 1:
                status = bstack111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥກ")
            elif hasattr(attrs, bstack111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫຂ")) and attrs.error_message:
                status = bstack111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ຃")
            bstack11ll11lll1_opy_, exception = self._11ll1l1l11_opy_(attrs)
        bstack11ll1l11ll_opy_ = Result(result=status, exception=exception, bstack11ll11111l_opy_=[bstack11ll11lll1_opy_])
        hook_data.stop(time=bstack1ll11l111l_opy_(), duration=0, result=bstack11ll1l11ll_opy_)
        bstack11ll111ll_opy_.bstack11ll111lll_opy_(bstack111l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨຄ"), self.tests[bstack11ll1l111l_opy_][bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ຅")])
        threading.current_thread().current_hook_uuid = None
    def _11ll1l1l11_opy_(self, attrs):
        try:
            import traceback
            bstack1llllll1l1_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11ll11lll1_opy_ = bstack1llllll1l1_opy_[-1] if bstack1llllll1l1_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࠧຆ"))
            bstack11ll11lll1_opy_ = None
            exception = None
        return bstack11ll11lll1_opy_, exception