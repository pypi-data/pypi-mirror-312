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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11l11l1l11_opy_ import RobotHandler
from bstack_utils.capture import bstack11ll111l11_opy_
from bstack_utils.bstack11ll111l1l_opy_ import bstack11l1l1l1ll_opy_, bstack11ll1ll11l_opy_, bstack11ll1111l1_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack1lll1lllll_opy_
from bstack_utils.bstack1l11ll1l1l_opy_ import bstack11ll111ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1llll1l_opy_, bstack1ll11l111l_opy_, Result, \
    bstack11l1lll111_opy_, bstack11l1lll1ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ງ"): [],
        bstack111l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩຈ"): [],
        bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨຉ"): []
    }
    bstack11l1llllll_opy_ = []
    bstack11l11ll1l1_opy_ = []
    @staticmethod
    def bstack11ll1l11l1_opy_(log):
        if not (log[bstack111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຊ")] and log[bstack111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ຋")].strip()):
            return
        active = bstack1lll1lllll_opy_.bstack11ll1l1111_opy_()
        log = {
            bstack111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ຌ"): log[bstack111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧຍ")],
            bstack111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬຎ"): bstack11l1lll1ll_opy_().isoformat() + bstack111l_opy_ (u"ࠪ࡞ࠬຏ"),
            bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬຐ"): log[bstack111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຑ")],
        }
        if active:
            if active[bstack111l_opy_ (u"࠭ࡴࡺࡲࡨࠫຒ")] == bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬຓ"):
                log[bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨດ")] = active[bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩຕ")]
            elif active[bstack111l_opy_ (u"ࠪࡸࡾࡶࡥࠨຖ")] == bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩທ"):
                log[bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬຘ")] = active[bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ນ")]
        bstack11ll111ll_opy_.bstack11l11l1l1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11l1llll1l_opy_ = None
        self._11l11l1lll_opy_ = None
        self._11l1l1l11l_opy_ = OrderedDict()
        self.bstack11ll11l11l_opy_ = bstack11ll111l11_opy_(self.bstack11ll1l11l1_opy_)
    @bstack11l1lll111_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11l1ll11ll_opy_()
        if not self._11l1l1l11l_opy_.get(attrs.get(bstack111l_opy_ (u"ࠧࡪࡦࠪບ")), None):
            self._11l1l1l11l_opy_[attrs.get(bstack111l_opy_ (u"ࠨ࡫ࡧࠫປ"))] = {}
        bstack11l11ll111_opy_ = bstack11ll1111l1_opy_(
                bstack11l1ll1l1l_opy_=attrs.get(bstack111l_opy_ (u"ࠩ࡬ࡨࠬຜ")),
                name=name,
                bstack11ll11llll_opy_=bstack1ll11l111l_opy_(),
                file_path=os.path.relpath(attrs[bstack111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪຝ")], start=os.getcwd()) if attrs.get(bstack111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫພ")) != bstack111l_opy_ (u"ࠬ࠭ຟ") else bstack111l_opy_ (u"࠭ࠧຠ"),
                framework=bstack111l_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ມ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111l_opy_ (u"ࠨ࡫ࡧࠫຢ"), None)
        self._11l1l1l11l_opy_[attrs.get(bstack111l_opy_ (u"ࠩ࡬ࡨࠬຣ"))][bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭຤")] = bstack11l11ll111_opy_
    @bstack11l1lll111_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11l1l1l1l1_opy_()
        self._11l11ll1ll_opy_(messages)
        for bstack11l1l11ll1_opy_ in self.bstack11l1llllll_opy_:
            bstack11l1l11ll1_opy_[bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ລ")][bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ຦")].extend(self.store[bstack111l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬວ")])
            bstack11ll111ll_opy_.bstack11l1l11111_opy_(bstack11l1l11ll1_opy_)
        self.bstack11l1llllll_opy_ = []
        self.store[bstack111l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ຨ")] = []
    @bstack11l1lll111_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11ll11l11l_opy_.start()
        if not self._11l1l1l11l_opy_.get(attrs.get(bstack111l_opy_ (u"ࠨ࡫ࡧࠫຩ")), None):
            self._11l1l1l11l_opy_[attrs.get(bstack111l_opy_ (u"ࠩ࡬ࡨࠬສ"))] = {}
        driver = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩຫ"), None)
        bstack11ll111l1l_opy_ = bstack11ll1111l1_opy_(
            bstack11l1ll1l1l_opy_=attrs.get(bstack111l_opy_ (u"ࠫ࡮ࡪࠧຬ")),
            name=name,
            bstack11ll11llll_opy_=bstack1ll11l111l_opy_(),
            file_path=os.path.relpath(attrs[bstack111l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬອ")], start=os.getcwd()),
            scope=RobotHandler.bstack11l1l1lll1_opy_(attrs.get(bstack111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ຮ"), None)),
            framework=bstack111l_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ຯ"),
            tags=attrs[bstack111l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ະ")],
            hooks=self.store[bstack111l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨັ")],
            bstack11ll11l111_opy_=bstack11ll111ll_opy_.bstack11ll111ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111l_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧາ").format(bstack111l_opy_ (u"ࠦࠥࠨຳ").join(attrs[bstack111l_opy_ (u"ࠬࡺࡡࡨࡵࠪິ")]), name) if attrs[bstack111l_opy_ (u"࠭ࡴࡢࡩࡶࠫີ")] else name
        )
        self._11l1l1l11l_opy_[attrs.get(bstack111l_opy_ (u"ࠧࡪࡦࠪຶ"))][bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫື")] = bstack11ll111l1l_opy_
        threading.current_thread().current_test_uuid = bstack11ll111l1l_opy_.bstack11l11l111l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111l_opy_ (u"ࠩ࡬ࡨຸࠬ"), None)
        self.bstack11ll111lll_opy_(bstack111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧູࠫ"), bstack11ll111l1l_opy_)
    @bstack11l1lll111_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11ll11l11l_opy_.reset()
        bstack11l1lll11l_opy_ = bstack11l1l11l11_opy_.get(attrs.get(bstack111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶ຺ࠫ")), bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ົ"))
        self._11l1l1l11l_opy_[attrs.get(bstack111l_opy_ (u"࠭ࡩࡥࠩຼ"))][bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪຽ")].stop(time=bstack1ll11l111l_opy_(), duration=int(attrs.get(bstack111l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭຾"), bstack111l_opy_ (u"ࠩ࠳ࠫ຿"))), result=Result(result=bstack11l1lll11l_opy_, exception=attrs.get(bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫເ")), bstack11ll11111l_opy_=[attrs.get(bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬແ"))]))
        self.bstack11ll111lll_opy_(bstack111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧໂ"), self._11l1l1l11l_opy_[attrs.get(bstack111l_opy_ (u"࠭ࡩࡥࠩໃ"))][bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪໄ")], True)
        self.store[bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ໅")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11l1lll111_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11l1ll11ll_opy_()
        current_test_id = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫໆ"), None)
        bstack11ll111111_opy_ = current_test_id if bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬ໇"), None) else bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪ່ࠧ"), None)
        if attrs.get(bstack111l_opy_ (u"ࠬࡺࡹࡱࡧ້ࠪ"), bstack111l_opy_ (u"໊࠭ࠧ")).lower() in [bstack111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ໋࠭"), bstack111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ໌")]:
            hook_type = bstack11l1l11l1l_opy_(attrs.get(bstack111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧໍ")), bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ໎"), None))
            hook_name = bstack111l_opy_ (u"ࠫࢀࢃࠧ໏").format(attrs.get(bstack111l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ໐"), bstack111l_opy_ (u"࠭ࠧ໑")))
            if hook_type in [bstack111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ໒"), bstack111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ໓")]:
                hook_name = bstack111l_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿࠪ໔").format(bstack11l11l11l1_opy_.get(hook_type), attrs.get(bstack111l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ໕"), bstack111l_opy_ (u"ࠫࠬ໖")))
            bstack11l11ll11l_opy_ = bstack11ll1ll11l_opy_(
                bstack11l1ll1l1l_opy_=bstack11ll111111_opy_ + bstack111l_opy_ (u"ࠬ࠳ࠧ໗") + attrs.get(bstack111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ໘"), bstack111l_opy_ (u"ࠧࠨ໙")).lower(),
                name=hook_name,
                bstack11ll11llll_opy_=bstack1ll11l111l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ໚")), start=os.getcwd()),
                framework=bstack111l_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ໛"),
                tags=attrs[bstack111l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨໜ")],
                scope=RobotHandler.bstack11l1l1lll1_opy_(attrs.get(bstack111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫໝ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11l11ll11l_opy_.bstack11l11l111l_opy_()
            threading.current_thread().current_hook_id = bstack11ll111111_opy_ + bstack111l_opy_ (u"ࠬ࠳ࠧໞ") + attrs.get(bstack111l_opy_ (u"࠭ࡴࡺࡲࡨࠫໟ"), bstack111l_opy_ (u"ࠧࠨ໠")).lower()
            self.store[bstack111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ໡")] = [bstack11l11ll11l_opy_.bstack11l11l111l_opy_()]
            if bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭໢"), None):
                self.store[bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ໣")].append(bstack11l11ll11l_opy_.bstack11l11l111l_opy_())
            else:
                self.store[bstack111l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ໤")].append(bstack11l11ll11l_opy_.bstack11l11l111l_opy_())
            if bstack11ll111111_opy_:
                self._11l1l1l11l_opy_[bstack11ll111111_opy_ + bstack111l_opy_ (u"ࠬ࠳ࠧ໥") + attrs.get(bstack111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ໦"), bstack111l_opy_ (u"ࠧࠨ໧")).lower()] = { bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ໨"): bstack11l11ll11l_opy_ }
            bstack11ll111ll_opy_.bstack11ll111lll_opy_(bstack111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ໩"), bstack11l11ll11l_opy_)
        else:
            bstack11ll11l1ll_opy_ = {
                bstack111l_opy_ (u"ࠪ࡭ࡩ࠭໪"): uuid4().__str__(),
                bstack111l_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ໫"): bstack111l_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫ໬").format(attrs.get(bstack111l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭໭")), attrs.get(bstack111l_opy_ (u"ࠧࡢࡴࡪࡷࠬ໮"), bstack111l_opy_ (u"ࠨࠩ໯"))) if attrs.get(bstack111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ໰"), []) else attrs.get(bstack111l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ໱")),
                bstack111l_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ໲"): attrs.get(bstack111l_opy_ (u"ࠬࡧࡲࡨࡵࠪ໳"), []),
                bstack111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ໴"): bstack1ll11l111l_opy_(),
                bstack111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ໵"): bstack111l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ໶"),
                bstack111l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ໷"): attrs.get(bstack111l_opy_ (u"ࠪࡨࡴࡩࠧ໸"), bstack111l_opy_ (u"ࠫࠬ໹"))
            }
            if attrs.get(bstack111l_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭໺"), bstack111l_opy_ (u"࠭ࠧ໻")) != bstack111l_opy_ (u"ࠧࠨ໼"):
                bstack11ll11l1ll_opy_[bstack111l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ໽")] = attrs.get(bstack111l_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪ໾"))
            if not self.bstack11l11ll1l1_opy_:
                self._11l1l1l11l_opy_[self._11l1lll1l1_opy_()][bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໿")].add_step(bstack11ll11l1ll_opy_)
                threading.current_thread().current_step_uuid = bstack11ll11l1ll_opy_[bstack111l_opy_ (u"ࠫ࡮ࡪࠧༀ")]
            self.bstack11l11ll1l1_opy_.append(bstack11ll11l1ll_opy_)
    @bstack11l1lll111_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11l1l1l1l1_opy_()
        self._11l11ll1ll_opy_(messages)
        current_test_id = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ༁"), None)
        bstack11ll111111_opy_ = current_test_id if current_test_id else bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ༂"), None)
        bstack11l1ll1ll1_opy_ = bstack11l1l11l11_opy_.get(attrs.get(bstack111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ༃")), bstack111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ༄"))
        bstack11l1ll1l11_opy_ = attrs.get(bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༅"))
        if bstack11l1ll1ll1_opy_ != bstack111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ༆") and not attrs.get(bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༇")) and self._11l1llll1l_opy_:
            bstack11l1ll1l11_opy_ = self._11l1llll1l_opy_
        bstack11ll1l11ll_opy_ = Result(result=bstack11l1ll1ll1_opy_, exception=bstack11l1ll1l11_opy_, bstack11ll11111l_opy_=[bstack11l1ll1l11_opy_])
        if attrs.get(bstack111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ༈"), bstack111l_opy_ (u"࠭ࠧ༉")).lower() in [bstack111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭༊"), bstack111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ་")]:
            bstack11ll111111_opy_ = current_test_id if current_test_id else bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬ༌"), None)
            if bstack11ll111111_opy_:
                bstack11ll1l111l_opy_ = bstack11ll111111_opy_ + bstack111l_opy_ (u"ࠥ࠱ࠧ།") + attrs.get(bstack111l_opy_ (u"ࠫࡹࡿࡰࡦࠩ༎"), bstack111l_opy_ (u"ࠬ࠭༏")).lower()
                self._11l1l1l11l_opy_[bstack11ll1l111l_opy_][bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༐")].stop(time=bstack1ll11l111l_opy_(), duration=int(attrs.get(bstack111l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬ༑"), bstack111l_opy_ (u"ࠨ࠲ࠪ༒"))), result=bstack11ll1l11ll_opy_)
                bstack11ll111ll_opy_.bstack11ll111lll_opy_(bstack111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ༓"), self._11l1l1l11l_opy_[bstack11ll1l111l_opy_][bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༔")])
        else:
            bstack11ll111111_opy_ = current_test_id if current_test_id else bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭༕"), None)
            if bstack11ll111111_opy_ and len(self.bstack11l11ll1l1_opy_) == 1:
                current_step_uuid = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩ༖"), None)
                self._11l1l1l11l_opy_[bstack11ll111111_opy_][bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༗")].bstack11ll11ll11_opy_(current_step_uuid, duration=int(attrs.get(bstack111l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩ༘ࠬ"), bstack111l_opy_ (u"ࠨ࠲༙ࠪ"))), result=bstack11ll1l11ll_opy_)
            else:
                self.bstack11l1l1111l_opy_(attrs)
            self.bstack11l11ll1l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111l_opy_ (u"ࠩ࡫ࡸࡲࡲࠧ༚"), bstack111l_opy_ (u"ࠪࡲࡴ࠭༛")) == bstack111l_opy_ (u"ࠫࡾ࡫ࡳࠨ༜"):
                return
            self.messages.push(message)
            bstack11l11llll1_opy_ = []
            if bstack1lll1lllll_opy_.bstack11ll1l1111_opy_():
                bstack11l11llll1_opy_.append({
                    bstack111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ༝"): bstack1ll11l111l_opy_(),
                    bstack111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༞"): message.get(bstack111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༟")),
                    bstack111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ༠"): message.get(bstack111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ༡")),
                    **bstack1lll1lllll_opy_.bstack11ll1l1111_opy_()
                })
                if len(bstack11l11llll1_opy_) > 0:
                    bstack11ll111ll_opy_.bstack11l11l1l1_opy_(bstack11l11llll1_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack11ll111ll_opy_.bstack11l1l1ll11_opy_()
    def bstack11l1l1111l_opy_(self, bstack11l11l11ll_opy_):
        if not bstack1lll1lllll_opy_.bstack11ll1l1111_opy_():
            return
        kwname = bstack111l_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩ༢").format(bstack11l11l11ll_opy_.get(bstack111l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ༣")), bstack11l11l11ll_opy_.get(bstack111l_opy_ (u"ࠬࡧࡲࡨࡵࠪ༤"), bstack111l_opy_ (u"࠭ࠧ༥"))) if bstack11l11l11ll_opy_.get(bstack111l_opy_ (u"ࠧࡢࡴࡪࡷࠬ༦"), []) else bstack11l11l11ll_opy_.get(bstack111l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ༧"))
        error_message = bstack111l_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣ༨").format(kwname, bstack11l11l11ll_opy_.get(bstack111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ༩")), str(bstack11l11l11ll_opy_.get(bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༪"))))
        bstack11l11l1l1l_opy_ = bstack111l_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦ༫").format(kwname, bstack11l11l11ll_opy_.get(bstack111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭༬")))
        bstack11l1llll11_opy_ = error_message if bstack11l11l11ll_opy_.get(bstack111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༭")) else bstack11l11l1l1l_opy_
        bstack11l1l1ll1l_opy_ = {
            bstack111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ༮"): self.bstack11l11ll1l1_opy_[-1].get(bstack111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭༯"), bstack1ll11l111l_opy_()),
            bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༰"): bstack11l1llll11_opy_,
            bstack111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ༱"): bstack111l_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ༲") if bstack11l11l11ll_opy_.get(bstack111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭༳")) == bstack111l_opy_ (u"ࠧࡇࡃࡌࡐࠬ༴") else bstack111l_opy_ (u"ࠨࡋࡑࡊࡔ༵࠭"),
            **bstack1lll1lllll_opy_.bstack11ll1l1111_opy_()
        }
        bstack11ll111ll_opy_.bstack11l11l1l1_opy_([bstack11l1l1ll1l_opy_])
    def _11l1lll1l1_opy_(self):
        for bstack11l1ll1l1l_opy_ in reversed(self._11l1l1l11l_opy_):
            bstack11l11l1ll1_opy_ = bstack11l1ll1l1l_opy_
            data = self._11l1l1l11l_opy_[bstack11l1ll1l1l_opy_][bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༶")]
            if isinstance(data, bstack11ll1ll11l_opy_):
                if not bstack111l_opy_ (u"ࠪࡉࡆࡉࡈࠨ༷") in data.bstack11l1l111l1_opy_():
                    return bstack11l11l1ll1_opy_
            else:
                return bstack11l11l1ll1_opy_
    def _11l11ll1ll_opy_(self, messages):
        try:
            bstack11l1lllll1_opy_ = BuiltIn().get_variable_value(bstack111l_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥ༸")) in (bstack11l11lll11_opy_.DEBUG, bstack11l11lll11_opy_.TRACE)
            for message, bstack11l1ll111l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ༹࠭"))
                level = message.get(bstack111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ༺"))
                if level == bstack11l11lll11_opy_.FAIL:
                    self._11l1llll1l_opy_ = name or self._11l1llll1l_opy_
                    self._11l11l1lll_opy_ = bstack11l1ll111l_opy_.get(bstack111l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ༻")) if bstack11l1lllll1_opy_ and bstack11l1ll111l_opy_ else self._11l11l1lll_opy_
        except:
            pass
    @classmethod
    def bstack11ll111lll_opy_(self, event: str, bstack11l1ll11l1_opy_: bstack11l1l1l1ll_opy_, bstack11l1l111ll_opy_=False):
        if event == bstack111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ༼"):
            bstack11l1ll11l1_opy_.set(hooks=self.store[bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭༽")])
        if event == bstack111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ༾"):
            event = bstack111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭༿")
        if bstack11l1l111ll_opy_:
            bstack11l11lllll_opy_ = {
                bstack111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩཀ"): event,
                bstack11l1ll11l1_opy_.bstack11l11l1111_opy_(): bstack11l1ll11l1_opy_.bstack11l1ll1lll_opy_(event)
            }
            self.bstack11l1llllll_opy_.append(bstack11l11lllll_opy_)
        else:
            bstack11ll111ll_opy_.bstack11ll111lll_opy_(event, bstack11l1ll11l1_opy_)
class Messages:
    def __init__(self):
        self._11l1l11lll_opy_ = []
    def bstack11l1ll11ll_opy_(self):
        self._11l1l11lll_opy_.append([])
    def bstack11l1l1l1l1_opy_(self):
        return self._11l1l11lll_opy_.pop() if self._11l1l11lll_opy_ else list()
    def push(self, message):
        self._11l1l11lll_opy_[-1].append(message) if self._11l1l11lll_opy_ else self._11l1l11lll_opy_.append([message])
class bstack11l11lll11_opy_:
    FAIL = bstack111l_opy_ (u"࠭ࡆࡂࡋࡏࠫཁ")
    ERROR = bstack111l_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ག")
    WARNING = bstack111l_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭གྷ")
    bstack11l11lll1l_opy_ = bstack111l_opy_ (u"ࠩࡌࡒࡋࡕࠧང")
    DEBUG = bstack111l_opy_ (u"ࠪࡈࡊࡈࡕࡈࠩཅ")
    TRACE = bstack111l_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪཆ")
    bstack11l1ll1111_opy_ = [FAIL, ERROR]
def bstack11l1l1llll_opy_(bstack11l1l1l111_opy_):
    if not bstack11l1l1l111_opy_:
        return None
    if bstack11l1l1l111_opy_.get(bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཇ"), None):
        return getattr(bstack11l1l1l111_opy_[bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ཈")], bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬཉ"), None)
    return bstack11l1l1l111_opy_.get(bstack111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ཊ"), None)
def bstack11l1l11l1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨཋ"), bstack111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬཌ")]:
        return
    if hook_type.lower() == bstack111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪཌྷ"):
        if current_test_uuid is None:
            return bstack111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩཎ")
        else:
            return bstack111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫཏ")
    elif hook_type.lower() == bstack111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩཐ"):
        if current_test_uuid is None:
            return bstack111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫད")
        else:
            return bstack111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭དྷ")