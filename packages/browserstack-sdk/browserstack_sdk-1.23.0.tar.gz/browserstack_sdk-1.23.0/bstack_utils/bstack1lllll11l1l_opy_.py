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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111111l1ll_opy_
from browserstack_sdk.bstack11111lll1_opy_ import bstack1l1lllll11_opy_
def _1llll1ll111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lllll11lll_opy_:
    def __init__(self, handler):
        self._1lllll11111_opy_ = {}
        self._1llll1ll1l1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1lllll11_opy_.version()
        if bstack111111l1ll_opy_(pytest_version, bstack111l_opy_ (u"ࠧ࠾࠮࠲࠰࠴ࠦᔌ")) >= 0:
            self._1lllll11111_opy_[bstack111l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᔍ")] = Module._register_setup_function_fixture
            self._1lllll11111_opy_[bstack111l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᔎ")] = Module._register_setup_module_fixture
            self._1lllll11111_opy_[bstack111l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᔏ")] = Class._register_setup_class_fixture
            self._1lllll11111_opy_[bstack111l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᔐ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1llll1lll11_opy_(bstack111l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᔑ"))
            Module._register_setup_module_fixture = self.bstack1llll1lll11_opy_(bstack111l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᔒ"))
            Class._register_setup_class_fixture = self.bstack1llll1lll11_opy_(bstack111l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᔓ"))
            Class._register_setup_method_fixture = self.bstack1llll1lll11_opy_(bstack111l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᔔ"))
        else:
            self._1lllll11111_opy_[bstack111l_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᔕ")] = Module._inject_setup_function_fixture
            self._1lllll11111_opy_[bstack111l_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᔖ")] = Module._inject_setup_module_fixture
            self._1lllll11111_opy_[bstack111l_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᔗ")] = Class._inject_setup_class_fixture
            self._1lllll11111_opy_[bstack111l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᔘ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1llll1lll11_opy_(bstack111l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᔙ"))
            Module._inject_setup_module_fixture = self.bstack1llll1lll11_opy_(bstack111l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᔚ"))
            Class._inject_setup_class_fixture = self.bstack1llll1lll11_opy_(bstack111l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᔛ"))
            Class._inject_setup_method_fixture = self.bstack1llll1lll11_opy_(bstack111l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᔜ"))
    def bstack1llll1l1lll_opy_(self, bstack1llll1lllll_opy_, hook_type):
        bstack1llll1ll1ll_opy_ = id(bstack1llll1lllll_opy_.__class__)
        if (bstack1llll1ll1ll_opy_, hook_type) in self._1llll1ll1l1_opy_:
            return
        meth = getattr(bstack1llll1lllll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1llll1ll1l1_opy_[(bstack1llll1ll1ll_opy_, hook_type)] = meth
            setattr(bstack1llll1lllll_opy_, hook_type, self.bstack1lllll1111l_opy_(hook_type, bstack1llll1ll1ll_opy_))
    def bstack1llll1llll1_opy_(self, instance, bstack1lllll11l11_opy_):
        if bstack1lllll11l11_opy_ == bstack111l_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᔝ"):
            self.bstack1llll1l1lll_opy_(instance.obj, bstack111l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᔞ"))
            self.bstack1llll1l1lll_opy_(instance.obj, bstack111l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢᔟ"))
        if bstack1lllll11l11_opy_ == bstack111l_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᔠ"):
            self.bstack1llll1l1lll_opy_(instance.obj, bstack111l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦᔡ"))
            self.bstack1llll1l1lll_opy_(instance.obj, bstack111l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣᔢ"))
        if bstack1lllll11l11_opy_ == bstack111l_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᔣ"):
            self.bstack1llll1l1lll_opy_(instance.obj, bstack111l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨᔤ"))
            self.bstack1llll1l1lll_opy_(instance.obj, bstack111l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥᔥ"))
        if bstack1lllll11l11_opy_ == bstack111l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᔦ"):
            self.bstack1llll1l1lll_opy_(instance.obj, bstack111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥᔧ"))
            self.bstack1llll1l1lll_opy_(instance.obj, bstack111l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢᔨ"))
    @staticmethod
    def bstack1lllll111ll_opy_(hook_type, func, args):
        if hook_type in [bstack111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᔩ"), bstack111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᔪ")]:
            _1llll1ll111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1lllll1111l_opy_(self, hook_type, bstack1llll1ll1ll_opy_):
        def bstack1lllll11ll1_opy_(arg=None):
            self.handler(hook_type, bstack111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᔫ"))
            result = None
            try:
                bstack1llll1lll1l_opy_ = self._1llll1ll1l1_opy_[(bstack1llll1ll1ll_opy_, hook_type)]
                self.bstack1lllll111ll_opy_(hook_type, bstack1llll1lll1l_opy_, (arg,))
                result = Result(result=bstack111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᔬ"))
            except Exception as e:
                result = Result(result=bstack111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᔭ"), exception=e)
                self.handler(hook_type, bstack111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᔮ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᔯ"), result)
        def bstack1llll1ll11l_opy_(this, arg=None):
            self.handler(hook_type, bstack111l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᔰ"))
            result = None
            exception = None
            try:
                self.bstack1lllll111ll_opy_(hook_type, self._1llll1ll1l1_opy_[hook_type], (this, arg))
                result = Result(result=bstack111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᔱ"))
            except Exception as e:
                result = Result(result=bstack111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᔲ"), exception=e)
                self.handler(hook_type, bstack111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᔳ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᔴ"), result)
        if hook_type in [bstack111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᔵ"), bstack111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᔶ")]:
            return bstack1llll1ll11l_opy_
        return bstack1lllll11ll1_opy_
    def bstack1llll1lll11_opy_(self, bstack1lllll11l11_opy_):
        def bstack1lllll111l1_opy_(this, *args, **kwargs):
            self.bstack1llll1llll1_opy_(this, bstack1lllll11l11_opy_)
            self._1lllll11111_opy_[bstack1lllll11l11_opy_](this, *args, **kwargs)
        return bstack1lllll111l1_opy_