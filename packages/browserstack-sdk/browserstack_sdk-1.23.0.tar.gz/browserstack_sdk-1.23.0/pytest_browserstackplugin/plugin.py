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
import datetime
import inspect
import logging
import os
import signal
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1lll11l1l1_opy_, bstack111l111l1_opy_, update, bstack11ll1lll1_opy_,
                                       bstack111ll1l1_opy_, bstack1ll1lll11_opy_, bstack1l11l111_opy_, bstack1lll1l1l11_opy_,
                                       bstack1111l1l1_opy_, bstack1lll111l_opy_, bstack1l1l1l1lll_opy_, bstack1l1l11l1_opy_,
                                       bstack1ll1111l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11111111l_opy_)
from browserstack_sdk.bstack11111lll1_opy_ import bstack1l1lllll11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11lll1lll1_opy_
from bstack_utils.capture import bstack11ll111l11_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1llll1111_opy_, bstack1111l111l_opy_, bstack1ll1l111ll_opy_, \
    bstack1ll1l1l11_opy_
from bstack_utils.helper import bstack1l1llll1l_opy_, bstack1llllllll11_opy_, bstack11l1lll1ll_opy_, bstack11lll11ll1_opy_, bstack1111ll111l_opy_, bstack1ll11l111l_opy_, \
    bstack11111lll1l_opy_, \
    bstack11111l1l1l_opy_, bstack11lll11111_opy_, bstack1l11l1ll1l_opy_, bstack1lllll1l111_opy_, bstack1111l1lll_opy_, Notset, \
    bstack1llll1lll1_opy_, bstack11111ll11l_opy_, bstack11111111l1_opy_, Result, bstack1111l111l1_opy_, bstack1llllll11l1_opy_, bstack11l1lll111_opy_, \
    bstack1ll1l111_opy_, bstack1l11llll1l_opy_, bstack111lll11l_opy_, bstack111111lll1_opy_
from bstack_utils.bstack1lllll11l1l_opy_ import bstack1lllll11lll_opy_
from bstack_utils.messages import bstack1llllll1ll_opy_, bstack1111l11l_opy_, bstack1ll1ll11_opy_, bstack1l1l1l11ll_opy_, bstack11llllll1_opy_, \
    bstack1llll1ll1l_opy_, bstack1l1ll11l_opy_, bstack1l1l1l1l1l_opy_, bstack1llll11ll_opy_, bstack1lll1ll11_opy_, \
    bstack11llll1lll_opy_, bstack111ll1lll_opy_
from bstack_utils.proxy import bstack1l1ll11l11_opy_, bstack11ll11l1_opy_
from bstack_utils.bstack1l11l1llll_opy_ import bstack1ll1lll11l1_opy_, bstack1ll1lll1l11_opy_, bstack1ll1ll1lll1_opy_, bstack1ll1llll111_opy_, \
    bstack1ll1ll1llll_opy_, bstack1ll1lll1lll_opy_, bstack1ll1llll11l_opy_, bstack1llll111l1_opy_, bstack1ll1lll111l_opy_
from bstack_utils.bstack1ll111l1_opy_ import bstack1ll1l1llll_opy_
from bstack_utils.bstack1ll11l11l1_opy_ import bstack1l11l1l1ll_opy_, bstack1l1111l1l1_opy_, bstack1l1ll11ll1_opy_, \
    bstack111111ll_opy_, bstack1l11lll1ll_opy_
from bstack_utils.bstack11ll111l1l_opy_ import bstack11ll1111l1_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack1lll1lllll_opy_
import bstack_utils.bstack1lll1ll111_opy_ as bstack1lll111ll_opy_
from bstack_utils.bstack1l11ll1l1l_opy_ import bstack11ll111ll_opy_
from bstack_utils.bstack111111l11_opy_ import bstack111111l11_opy_
from browserstack_sdk.__init__ import bstack11l111ll_opy_
bstack1l1111l1ll_opy_ = None
bstack1ll1ll1l1_opy_ = None
bstack1l11lllll1_opy_ = None
bstack1l11111l11_opy_ = None
bstack1l11llll11_opy_ = None
bstack1l1l111111_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack111l1111_opy_ = None
bstack1l1lllll1_opy_ = None
bstack1ll1l1l111_opy_ = None
bstack1l11llllll_opy_ = None
bstack1l1111l11l_opy_ = None
bstack1l1ll11111_opy_ = None
bstack11lll1111_opy_ = bstack111l_opy_ (u"࠭ࠧᠹ")
CONFIG = {}
bstack1ll1l1ll_opy_ = False
bstack1l111ll1l_opy_ = bstack111l_opy_ (u"ࠧࠨᠺ")
bstack1ll111l1l_opy_ = bstack111l_opy_ (u"ࠨࠩᠻ")
bstack1ll1l1l1_opy_ = False
bstack1l11l1l1_opy_ = []
bstack11l1llll_opy_ = bstack1llll1111_opy_
bstack1l1llllll1l_opy_ = bstack111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᠼ")
bstack1111llll1_opy_ = {}
bstack1ll1111ll1_opy_ = False
logger = bstack11lll1lll1_opy_.get_logger(__name__, bstack11l1llll_opy_)
store = {
    bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᠽ"): []
}
bstack1ll11111l1l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l1l1l11l_opy_ = {}
current_test_uuid = None
def bstack1l1lll111_opy_(page, bstack11llllllll_opy_):
    try:
        page.evaluate(bstack111l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᠾ"),
                      bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩᠿ") + json.dumps(
                          bstack11llllllll_opy_) + bstack111l_opy_ (u"ࠨࡽࡾࠤᡀ"))
    except Exception as e:
        print(bstack111l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧᡁ"), e)
def bstack1lll1l1l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᡂ"), bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧᡃ") + json.dumps(
            message) + bstack111l_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭ᡄ") + json.dumps(level) + bstack111l_opy_ (u"ࠫࢂࢃࠧᡅ"))
    except Exception as e:
        print(bstack111l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣᡆ"), e)
def pytest_configure(config):
    bstack1l1ll1l111_opy_ = Config.bstack11llll1111_opy_()
    config.args = bstack1lll1lllll_opy_.bstack1ll111l1l1l_opy_(config.args)
    bstack1l1ll1l111_opy_.bstack1l1ll1ll11_opy_(bstack111lll11l_opy_(config.getoption(bstack111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᡇ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll1111lll1_opy_ = item.config.getoption(bstack111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᡈ"))
    plugins = item.config.getoption(bstack111l_opy_ (u"ࠣࡲ࡯ࡹ࡬࡯࡮ࡴࠤᡉ"))
    report = outcome.get_result()
    bstack1ll111111l1_opy_(item, call, report)
    if bstack111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢᡊ") not in plugins or bstack1111l1lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack111l_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦᡋ"), None)
    page = getattr(item, bstack111l_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥᡌ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll1111ll11_opy_(item, report, summary, bstack1ll1111lll1_opy_)
    if (page is not None):
        bstack1l1llll1ll1_opy_(item, report, summary, bstack1ll1111lll1_opy_)
def bstack1ll1111ll11_opy_(item, report, summary, bstack1ll1111lll1_opy_):
    if report.when == bstack111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᡍ") and report.skipped:
        bstack1ll1lll111l_opy_(report)
    if report.when in [bstack111l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᡎ"), bstack111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᡏ")]:
        return
    if not bstack1111ll111l_opy_():
        return
    try:
        if (str(bstack1ll1111lll1_opy_).lower() != bstack111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᡐ")):
            item._driver.execute_script(
                bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧᡑ") + json.dumps(
                    report.nodeid) + bstack111l_opy_ (u"ࠪࢁࢂ࠭ᡒ"))
        os.environ[bstack111l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᡓ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack111l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧᡔ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᡕ")))
    bstack1l1l1llll_opy_ = bstack111l_opy_ (u"ࠢࠣᡖ")
    bstack1ll1lll111l_opy_(report)
    if not passed:
        try:
            bstack1l1l1llll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack111l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᡗ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l1llll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack111l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᡘ")))
        bstack1l1l1llll_opy_ = bstack111l_opy_ (u"ࠥࠦᡙ")
        if not passed:
            try:
                bstack1l1l1llll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᡚ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l1llll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᡛ")
                    + json.dumps(bstack111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢᡜ"))
                    + bstack111l_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥᡝ")
                )
            else:
                item._driver.execute_script(
                    bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᡞ")
                    + json.dumps(str(bstack1l1l1llll_opy_))
                    + bstack111l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᡟ")
                )
        except Exception as e:
            summary.append(bstack111l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣᡠ").format(e))
def bstack1l1lllll11l_opy_(test_name, error_message):
    try:
        bstack1ll1111111l_opy_ = []
        bstack1l11lll11l_opy_ = os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᡡ"), bstack111l_opy_ (u"ࠬ࠶ࠧᡢ"))
        bstack11111ll1_opy_ = {bstack111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᡣ"): test_name, bstack111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᡤ"): error_message, bstack111l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᡥ"): bstack1l11lll11l_opy_}
        bstack1l1lllll111_opy_ = os.path.join(tempfile.gettempdir(), bstack111l_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᡦ"))
        if os.path.exists(bstack1l1lllll111_opy_):
            with open(bstack1l1lllll111_opy_) as f:
                bstack1ll1111111l_opy_ = json.load(f)
        bstack1ll1111111l_opy_.append(bstack11111ll1_opy_)
        with open(bstack1l1lllll111_opy_, bstack111l_opy_ (u"ࠪࡻࠬᡧ")) as f:
            json.dump(bstack1ll1111111l_opy_, f)
    except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩᡨ") + str(e))
def bstack1l1llll1ll1_opy_(item, report, summary, bstack1ll1111lll1_opy_):
    if report.when in [bstack111l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᡩ"), bstack111l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᡪ")]:
        return
    if (str(bstack1ll1111lll1_opy_).lower() != bstack111l_opy_ (u"ࠧࡵࡴࡸࡩࠬᡫ")):
        bstack1l1lll111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᡬ")))
    bstack1l1l1llll_opy_ = bstack111l_opy_ (u"ࠤࠥᡭ")
    bstack1ll1lll111l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1l1llll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᡮ").format(e)
                )
        try:
            if passed:
                bstack1l11lll1ll_opy_(getattr(item, bstack111l_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᡯ"), None), bstack111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᡰ"))
            else:
                error_message = bstack111l_opy_ (u"࠭ࠧᡱ")
                if bstack1l1l1llll_opy_:
                    bstack1lll1l1l1l_opy_(item._page, str(bstack1l1l1llll_opy_), bstack111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᡲ"))
                    bstack1l11lll1ll_opy_(getattr(item, bstack111l_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᡳ"), None), bstack111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᡴ"), str(bstack1l1l1llll_opy_))
                    error_message = str(bstack1l1l1llll_opy_)
                else:
                    bstack1l11lll1ll_opy_(getattr(item, bstack111l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᡵ"), None), bstack111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᡶ"))
                bstack1l1lllll11l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack111l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤᡷ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack111l_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᡸ"), default=bstack111l_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ᡹"), help=bstack111l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ᡺"))
    parser.addoption(bstack111l_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ᡻"), default=bstack111l_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤ᡼"), help=bstack111l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥ᡽"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack111l_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢ᡾"), action=bstack111l_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧ᡿"), default=bstack111l_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢᢀ"),
                         help=bstack111l_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢᢁ"))
def bstack11ll1l11l1_opy_(log):
    if not (log[bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᢂ")] and log[bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᢃ")].strip()):
        return
    active = bstack11ll1l1111_opy_()
    log = {
        bstack111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᢄ"): log[bstack111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᢅ")],
        bstack111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᢆ"): bstack11l1lll1ll_opy_().isoformat() + bstack111l_opy_ (u"࡛ࠧࠩᢇ"),
        bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᢈ"): log[bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᢉ")],
    }
    if active:
        if active[bstack111l_opy_ (u"ࠪࡸࡾࡶࡥࠨᢊ")] == bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᢋ"):
            log[bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᢌ")] = active[bstack111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᢍ")]
        elif active[bstack111l_opy_ (u"ࠧࡵࡻࡳࡩࠬᢎ")] == bstack111l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᢏ"):
            log[bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᢐ")] = active[bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᢑ")]
    bstack11ll111ll_opy_.bstack11l11l1l1_opy_([log])
def bstack11ll1l1111_opy_():
    if len(store[bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᢒ")]) > 0 and store[bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᢓ")][-1]:
        return {
            bstack111l_opy_ (u"࠭ࡴࡺࡲࡨࠫᢔ"): bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᢕ"),
            bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᢖ"): store[bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᢗ")][-1]
        }
    if store.get(bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᢘ"), None):
        return {
            bstack111l_opy_ (u"ࠫࡹࡿࡰࡦࠩᢙ"): bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࠪᢚ"),
            bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᢛ"): store[bstack111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᢜ")]
        }
    return None
bstack11ll11l11l_opy_ = bstack11ll111l11_opy_(bstack11ll1l11l1_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        item._1ll11111ll1_opy_ = True
        bstack1l1l1111l1_opy_ = bstack1lll111ll_opy_.bstack1111lll11_opy_(bstack11111l1l1l_opy_(item.own_markers))
        item._a11y_test_case = bstack1l1l1111l1_opy_
        if bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᢝ"), None):
            driver = getattr(item, bstack111l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᢞ"), None)
            item._a11y_started = bstack1lll111ll_opy_.bstack1lll111111_opy_(driver, bstack1l1l1111l1_opy_)
        if not bstack11ll111ll_opy_.on() or bstack1l1llllll1l_opy_ != bstack111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᢟ"):
            return
        global current_test_uuid, bstack11ll11l11l_opy_
        bstack11ll11l11l_opy_.start()
        bstack11l1l1l111_opy_ = {
            bstack111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᢠ"): uuid4().__str__(),
            bstack111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᢡ"): bstack11l1lll1ll_opy_().isoformat() + bstack111l_opy_ (u"࡚࠭ࠨᢢ")
        }
        current_test_uuid = bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᢣ")]
        store[bstack111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᢤ")] = bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᢥ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l1l1l11l_opy_[item.nodeid] = {**_11l1l1l11l_opy_[item.nodeid], **bstack11l1l1l111_opy_}
        bstack1l1llllll11_opy_(item, _11l1l1l11l_opy_[item.nodeid], bstack111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᢦ"))
    except Exception as err:
        print(bstack111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭ᢧ"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll11111l1l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1lllll1l111_opy_():
        atexit.register(bstack111lllll_opy_)
        if not bstack1ll11111l1l_opy_:
            try:
                bstack1l1llll1lll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111111lll1_opy_():
                    bstack1l1llll1lll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1l1llll1lll_opy_:
                    signal.signal(s, bstack1ll11111111_opy_)
                bstack1ll11111l1l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨᢨ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll1lll11l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩᢩ࠭")
    try:
        if not bstack11ll111ll_opy_.on():
            return
        bstack11ll11l11l_opy_.start()
        uuid = uuid4().__str__()
        bstack11l1l1l111_opy_ = {
            bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᢪ"): uuid,
            bstack111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᢫"): bstack11l1lll1ll_opy_().isoformat() + bstack111l_opy_ (u"ࠩ࡝ࠫ᢬"),
            bstack111l_opy_ (u"ࠪࡸࡾࡶࡥࠨ᢭"): bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ᢮"),
            bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ᢯"): bstack111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᢰ"),
            bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᢱ"): bstack111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᢲ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᢳ")] = item
        store[bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᢴ")] = [uuid]
        if not _11l1l1l11l_opy_.get(item.nodeid, None):
            _11l1l1l11l_opy_[item.nodeid] = {bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᢵ"): [], bstack111l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᢶ"): []}
        _11l1l1l11l_opy_[item.nodeid][bstack111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᢷ")].append(bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᢸ")])
        _11l1l1l11l_opy_[item.nodeid + bstack111l_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨᢹ")] = bstack11l1l1l111_opy_
        bstack1ll1111l1l1_opy_(item, bstack11l1l1l111_opy_, bstack111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᢺ"))
    except Exception as err:
        print(bstack111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᢻ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1111llll1_opy_
        bstack1l11lll11l_opy_ = 0
        if bstack1ll1l1l1_opy_ is True:
            bstack1l11lll11l_opy_ = int(os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᢼ")))
        if bstack1l1ll111ll_opy_.bstack1ll11llll1_opy_() == bstack111l_opy_ (u"ࠧࡺࡲࡶࡧࠥᢽ"):
            if bstack1l1ll111ll_opy_.bstack1l1ll1ll_opy_() == bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᢾ"):
                bstack1ll111l1l11_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᢿ"), None)
                bstack111111ll1_opy_ = bstack1ll111l1l11_opy_ + bstack111l_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦᣀ")
                driver = getattr(item, bstack111l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᣁ"), None)
                bstack1ll11l1l1l_opy_ = getattr(item, bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨᣂ"), None)
                bstack1ll1111lll_opy_ = getattr(item, bstack111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᣃ"), None)
                PercySDK.screenshot(driver, bstack111111ll1_opy_, bstack1ll11l1l1l_opy_=bstack1ll11l1l1l_opy_, bstack1ll1111lll_opy_=bstack1ll1111lll_opy_, bstack1l1111ll11_opy_=bstack1l11lll11l_opy_)
        if getattr(item, bstack111l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬᣄ"), False):
            bstack1l1lllll11_opy_.bstack11l1111l_opy_(getattr(item, bstack111l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᣅ"), None), bstack1111llll1_opy_, logger, item)
        if not bstack11ll111ll_opy_.on():
            return
        bstack11l1l1l111_opy_ = {
            bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᣆ"): uuid4().__str__(),
            bstack111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᣇ"): bstack11l1lll1ll_opy_().isoformat() + bstack111l_opy_ (u"ࠩ࡝ࠫᣈ"),
            bstack111l_opy_ (u"ࠪࡸࡾࡶࡥࠨᣉ"): bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᣊ"),
            bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᣋ"): bstack111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᣌ"),
            bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᣍ"): bstack111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᣎ")
        }
        _11l1l1l11l_opy_[item.nodeid + bstack111l_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬᣏ")] = bstack11l1l1l111_opy_
        bstack1ll1111l1l1_opy_(item, bstack11l1l1l111_opy_, bstack111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᣐ"))
    except Exception as err:
        print(bstack111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪᣑ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack11ll111ll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1ll1llll111_opy_(fixturedef.argname):
        store[bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫᣒ")] = request.node
    elif bstack1ll1ll1llll_opy_(fixturedef.argname):
        store[bstack111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᣓ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᣔ"): fixturedef.argname,
            bstack111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᣕ"): bstack11111lll1l_opy_(outcome),
            bstack111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᣖ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᣗ")]
        if not _11l1l1l11l_opy_.get(current_test_item.nodeid, None):
            _11l1l1l11l_opy_[current_test_item.nodeid] = {bstack111l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᣘ"): []}
        _11l1l1l11l_opy_[current_test_item.nodeid][bstack111l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᣙ")].append(fixture)
    except Exception as err:
        logger.debug(bstack111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᣚ"), str(err))
if bstack1111l1lll_opy_() and bstack11ll111ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11l1l1l11l_opy_[request.node.nodeid][bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᣛ")].bstack1l1l1lll11_opy_(id(step))
        except Exception as err:
            print(bstack111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ᣜ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11l1l1l11l_opy_[request.node.nodeid][bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᣝ")].bstack11ll11ll11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᣞ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11ll111l1l_opy_: bstack11ll1111l1_opy_ = _11l1l1l11l_opy_[request.node.nodeid][bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᣟ")]
            bstack11ll111l1l_opy_.bstack11ll11ll11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᣠ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1l1llllll1l_opy_
        try:
            if not bstack11ll111ll_opy_.on() or bstack1l1llllll1l_opy_ != bstack111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᣡ"):
                return
            global bstack11ll11l11l_opy_
            bstack11ll11l11l_opy_.start()
            driver = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ᣢ"), None)
            if not _11l1l1l11l_opy_.get(request.node.nodeid, None):
                _11l1l1l11l_opy_[request.node.nodeid] = {}
            bstack11ll111l1l_opy_ = bstack11ll1111l1_opy_.bstack1ll1l1l11l1_opy_(
                scenario, feature, request.node,
                name=bstack1ll1lll1lll_opy_(request.node, scenario),
                bstack11ll11llll_opy_=bstack1ll11l111l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack111l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᣣ"),
                tags=bstack1ll1llll11l_opy_(feature, scenario),
                bstack11ll11l111_opy_=bstack11ll111ll_opy_.bstack11ll111ll1_opy_(driver) if driver and driver.session_id else {}
            )
            _11l1l1l11l_opy_[request.node.nodeid][bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᣤ")] = bstack11ll111l1l_opy_
            bstack1l1lllll1l1_opy_(bstack11ll111l1l_opy_.uuid)
            bstack11ll111ll_opy_.bstack11ll111lll_opy_(bstack111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᣥ"), bstack11ll111l1l_opy_)
        except Exception as err:
            print(bstack111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ᣦ"), str(err))
def bstack1ll111l11l1_opy_(bstack11ll1111ll_opy_):
    if bstack11ll1111ll_opy_ in store[bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᣧ")]:
        store[bstack111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᣨ")].remove(bstack11ll1111ll_opy_)
def bstack1l1lllll1l1_opy_(bstack11ll1ll1l1_opy_):
    store[bstack111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᣩ")] = bstack11ll1ll1l1_opy_
    threading.current_thread().current_test_uuid = bstack11ll1ll1l1_opy_
@bstack11ll111ll_opy_.bstack1ll11l1l1l1_opy_
def bstack1ll111111l1_opy_(item, call, report):
    global bstack1l1llllll1l_opy_
    bstack1llll11l1l_opy_ = bstack1ll11l111l_opy_()
    if hasattr(report, bstack111l_opy_ (u"ࠨࡵࡷࡳࡵ࠭ᣪ")):
        bstack1llll11l1l_opy_ = bstack1111l111l1_opy_(report.stop)
    elif hasattr(report, bstack111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨᣫ")):
        bstack1llll11l1l_opy_ = bstack1111l111l1_opy_(report.start)
    try:
        if getattr(report, bstack111l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᣬ"), bstack111l_opy_ (u"ࠫࠬᣭ")) == bstack111l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᣮ"):
            bstack11ll11l11l_opy_.reset()
        if getattr(report, bstack111l_opy_ (u"࠭ࡷࡩࡧࡱࠫᣯ"), bstack111l_opy_ (u"ࠧࠨᣰ")) == bstack111l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᣱ"):
            if bstack1l1llllll1l_opy_ == bstack111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᣲ"):
                _11l1l1l11l_opy_[item.nodeid][bstack111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣳ")] = bstack1llll11l1l_opy_
                bstack1l1llllll11_opy_(item, _11l1l1l11l_opy_[item.nodeid], bstack111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᣴ"), report, call)
                store[bstack111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᣵ")] = None
            elif bstack1l1llllll1l_opy_ == bstack111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ᣶"):
                bstack11ll111l1l_opy_ = _11l1l1l11l_opy_[item.nodeid][bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ᣷")]
                bstack11ll111l1l_opy_.set(hooks=_11l1l1l11l_opy_[item.nodeid].get(bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᣸"), []))
                exception, bstack11ll11111l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11ll11111l_opy_ = [call.excinfo.exconly(), getattr(report, bstack111l_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨ᣹"), bstack111l_opy_ (u"ࠪࠫ᣺"))]
                bstack11ll111l1l_opy_.stop(time=bstack1llll11l1l_opy_, result=Result(result=getattr(report, bstack111l_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ᣻"), bstack111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᣼")), exception=exception, bstack11ll11111l_opy_=bstack11ll11111l_opy_))
                bstack11ll111ll_opy_.bstack11ll111lll_opy_(bstack111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᣽"), _11l1l1l11l_opy_[item.nodeid][bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ᣾")])
        elif getattr(report, bstack111l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭᣿"), bstack111l_opy_ (u"ࠩࠪᤀ")) in [bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᤁ"), bstack111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᤂ")]:
            bstack11ll1l111l_opy_ = item.nodeid + bstack111l_opy_ (u"ࠬ࠳ࠧᤃ") + getattr(report, bstack111l_opy_ (u"࠭ࡷࡩࡧࡱࠫᤄ"), bstack111l_opy_ (u"ࠧࠨᤅ"))
            if getattr(report, bstack111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᤆ"), False):
                hook_type = bstack111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᤇ") if getattr(report, bstack111l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᤈ"), bstack111l_opy_ (u"ࠫࠬᤉ")) == bstack111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᤊ") else bstack111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᤋ")
                _11l1l1l11l_opy_[bstack11ll1l111l_opy_] = {
                    bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᤌ"): uuid4().__str__(),
                    bstack111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᤍ"): bstack1llll11l1l_opy_,
                    bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᤎ"): hook_type
                }
            _11l1l1l11l_opy_[bstack11ll1l111l_opy_][bstack111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᤏ")] = bstack1llll11l1l_opy_
            bstack1ll111l11l1_opy_(_11l1l1l11l_opy_[bstack11ll1l111l_opy_][bstack111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᤐ")])
            bstack1ll1111l1l1_opy_(item, _11l1l1l11l_opy_[bstack11ll1l111l_opy_], bstack111l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᤑ"), report, call)
            if getattr(report, bstack111l_opy_ (u"࠭ࡷࡩࡧࡱࠫᤒ"), bstack111l_opy_ (u"ࠧࠨᤓ")) == bstack111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᤔ"):
                if getattr(report, bstack111l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᤕ"), bstack111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᤖ")) == bstack111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᤗ"):
                    bstack11l1l1l111_opy_ = {
                        bstack111l_opy_ (u"ࠬࡻࡵࡪࡦࠪᤘ"): uuid4().__str__(),
                        bstack111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᤙ"): bstack1ll11l111l_opy_(),
                        bstack111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᤚ"): bstack1ll11l111l_opy_()
                    }
                    _11l1l1l11l_opy_[item.nodeid] = {**_11l1l1l11l_opy_[item.nodeid], **bstack11l1l1l111_opy_}
                    bstack1l1llllll11_opy_(item, _11l1l1l11l_opy_[item.nodeid], bstack111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᤛ"))
                    bstack1l1llllll11_opy_(item, _11l1l1l11l_opy_[item.nodeid], bstack111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᤜ"), report, call)
    except Exception as err:
        print(bstack111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨᤝ"), str(err))
def bstack1ll1111l11l_opy_(test, bstack11l1l1l111_opy_, result=None, call=None, bstack11l111111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11ll111l1l_opy_ = {
        bstack111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᤞ"): bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ᤟")],
        bstack111l_opy_ (u"࠭ࡴࡺࡲࡨࠫᤠ"): bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࠬᤡ"),
        bstack111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᤢ"): test.name,
        bstack111l_opy_ (u"ࠩࡥࡳࡩࡿࠧᤣ"): {
            bstack111l_opy_ (u"ࠪࡰࡦࡴࡧࠨᤤ"): bstack111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᤥ"),
            bstack111l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᤦ"): inspect.getsource(test.obj)
        },
        bstack111l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᤧ"): test.name,
        bstack111l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᤨ"): test.name,
        bstack111l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᤩ"): bstack1lll1lllll_opy_.bstack11l1l1lll1_opy_(test),
        bstack111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᤪ"): file_path,
        bstack111l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᤫ"): file_path,
        bstack111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᤬"): bstack111l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭᤭"),
        bstack111l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ᤮"): file_path,
        bstack111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᤯"): bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᤰ")],
        bstack111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᤱ"): bstack111l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᤲ"),
        bstack111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᤳ"): {
            bstack111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᤴ"): test.nodeid
        },
        bstack111l_opy_ (u"࠭ࡴࡢࡩࡶࠫᤵ"): bstack11111l1l1l_opy_(test.own_markers)
    }
    if bstack11l111111_opy_ in [bstack111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᤶ"), bstack111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᤷ")]:
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠩࡰࡩࡹࡧࠧᤸ")] = {
            bstack111l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷ᤹ࠬ"): bstack11l1l1l111_opy_.get(bstack111l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭᤺"), [])
        }
    if bstack11l111111_opy_ == bstack111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ᤻࠭"):
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᤼")] = bstack111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ᤽")
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᤾")] = bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᤿")]
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᥀")] = bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᥁")]
    if result:
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᥂")] = result.outcome
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ᥃")] = result.duration * 1000
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᥄")] = bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᥅")]
        if result.failed:
            bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ᥆")] = bstack11ll111ll_opy_.bstack111lllll11_opy_(call.excinfo.typename)
            bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ᥇")] = bstack11ll111ll_opy_.bstack1ll11ll11l1_opy_(call.excinfo, result)
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ᥈")] = bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ᥉")]
    if outcome:
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᥊")] = bstack11111lll1l_opy_(outcome)
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ᥋")] = 0
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᥌")] = bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᥍")]
        if bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᥎")] == bstack111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᥏"):
            bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᥐ")] = bstack111l_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᥑ")  # bstack1ll11111lll_opy_
            bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᥒ")] = [{bstack111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᥓ"): [bstack111l_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᥔ")]}]
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᥕ")] = bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᥖ")]
    return bstack11ll111l1l_opy_
def bstack1ll1111llll_opy_(test, bstack11l11ll11l_opy_, bstack11l111111_opy_, result, call, outcome, bstack1l1lllllll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11l11ll11l_opy_[bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᥗ")]
    hook_name = bstack11l11ll11l_opy_[bstack111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᥘ")]
    hook_data = {
        bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᥙ"): bstack11l11ll11l_opy_[bstack111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᥚ")],
        bstack111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᥛ"): bstack111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᥜ"),
        bstack111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᥝ"): bstack111l_opy_ (u"ࠬࢁࡽࠨᥞ").format(bstack1ll1lll1l11_opy_(hook_name)),
        bstack111l_opy_ (u"࠭ࡢࡰࡦࡼࠫᥟ"): {
            bstack111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᥠ"): bstack111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᥡ"),
            bstack111l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᥢ"): None
        },
        bstack111l_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᥣ"): test.name,
        bstack111l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᥤ"): bstack1lll1lllll_opy_.bstack11l1l1lll1_opy_(test, hook_name),
        bstack111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᥥ"): file_path,
        bstack111l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᥦ"): file_path,
        bstack111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᥧ"): bstack111l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᥨ"),
        bstack111l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᥩ"): file_path,
        bstack111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᥪ"): bstack11l11ll11l_opy_[bstack111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᥫ")],
        bstack111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᥬ"): bstack111l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨᥭ") if bstack1l1llllll1l_opy_ == bstack111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ᥮") else bstack111l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ᥯"),
        bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᥰ"): hook_type
    }
    bstack1ll1l1l1l11_opy_ = bstack11l1l1llll_opy_(_11l1l1l11l_opy_.get(test.nodeid, None))
    if bstack1ll1l1l1l11_opy_:
        hook_data[bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᥱ")] = bstack1ll1l1l1l11_opy_
    if result:
        hook_data[bstack111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᥲ")] = result.outcome
        hook_data[bstack111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᥳ")] = result.duration * 1000
        hook_data[bstack111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᥴ")] = bstack11l11ll11l_opy_[bstack111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᥵")]
        if result.failed:
            hook_data[bstack111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ᥶")] = bstack11ll111ll_opy_.bstack111lllll11_opy_(call.excinfo.typename)
            hook_data[bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᥷")] = bstack11ll111ll_opy_.bstack1ll11ll11l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᥸")] = bstack11111lll1l_opy_(outcome)
        hook_data[bstack111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ᥹")] = 100
        hook_data[bstack111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᥺")] = bstack11l11ll11l_opy_[bstack111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᥻")]
        if hook_data[bstack111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᥼")] == bstack111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᥽"):
            hook_data[bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ᥾")] = bstack111l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ᥿")  # bstack1ll11111lll_opy_
            hook_data[bstack111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᦀ")] = [{bstack111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᦁ"): [bstack111l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᦂ")]}]
    if bstack1l1lllllll1_opy_:
        hook_data[bstack111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᦃ")] = bstack1l1lllllll1_opy_.result
        hook_data[bstack111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᦄ")] = bstack11111ll11l_opy_(bstack11l11ll11l_opy_[bstack111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᦅ")], bstack11l11ll11l_opy_[bstack111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᦆ")])
        hook_data[bstack111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᦇ")] = bstack11l11ll11l_opy_[bstack111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᦈ")]
        if hook_data[bstack111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᦉ")] == bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᦊ"):
            hook_data[bstack111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᦋ")] = bstack11ll111ll_opy_.bstack111lllll11_opy_(bstack1l1lllllll1_opy_.exception_type)
            hook_data[bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᦌ")] = [{bstack111l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᦍ"): bstack11111111l1_opy_(bstack1l1lllllll1_opy_.exception)}]
    return hook_data
def bstack1l1llllll11_opy_(test, bstack11l1l1l111_opy_, bstack11l111111_opy_, result=None, call=None, outcome=None):
    bstack11ll111l1l_opy_ = bstack1ll1111l11l_opy_(test, bstack11l1l1l111_opy_, result, call, bstack11l111111_opy_, outcome)
    driver = getattr(test, bstack111l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᦎ"), None)
    if bstack11l111111_opy_ == bstack111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᦏ") and driver:
        bstack11ll111l1l_opy_[bstack111l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᦐ")] = bstack11ll111ll_opy_.bstack11ll111ll1_opy_(driver)
    if bstack11l111111_opy_ == bstack111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᦑ"):
        bstack11l111111_opy_ = bstack111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᦒ")
    bstack11l11lllll_opy_ = {
        bstack111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᦓ"): bstack11l111111_opy_,
        bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᦔ"): bstack11ll111l1l_opy_
    }
    bstack11ll111ll_opy_.bstack11l1l11111_opy_(bstack11l11lllll_opy_)
    if bstack11l111111_opy_ == bstack111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᦕ"):
        threading.current_thread().bstackTestMeta = {bstack111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᦖ"): bstack111l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᦗ")}
    elif bstack11l111111_opy_ == bstack111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᦘ"):
        threading.current_thread().bstackTestMeta = {bstack111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᦙ"): getattr(result, bstack111l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᦚ"), bstack111l_opy_ (u"ࠪࠫᦛ"))}
def bstack1ll1111l1l1_opy_(test, bstack11l1l1l111_opy_, bstack11l111111_opy_, result=None, call=None, outcome=None, bstack1l1lllllll1_opy_=None):
    hook_data = bstack1ll1111llll_opy_(test, bstack11l1l1l111_opy_, bstack11l111111_opy_, result, call, outcome, bstack1l1lllllll1_opy_)
    bstack11l11lllll_opy_ = {
        bstack111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᦜ"): bstack11l111111_opy_,
        bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᦝ"): hook_data
    }
    bstack11ll111ll_opy_.bstack11l1l11111_opy_(bstack11l11lllll_opy_)
def bstack11l1l1llll_opy_(bstack11l1l1l111_opy_):
    if not bstack11l1l1l111_opy_:
        return None
    if bstack11l1l1l111_opy_.get(bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᦞ"), None):
        return getattr(bstack11l1l1l111_opy_[bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᦟ")], bstack111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᦠ"), None)
    return bstack11l1l1l111_opy_.get(bstack111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᦡ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack11ll111ll_opy_.on():
            return
        places = [bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᦢ"), bstack111l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᦣ"), bstack111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᦤ")]
        bstack11l11llll1_opy_ = []
        for bstack1ll11111l11_opy_ in places:
            records = caplog.get_records(bstack1ll11111l11_opy_)
            bstack1ll1111l1ll_opy_ = bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᦥ") if bstack1ll11111l11_opy_ == bstack111l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᦦ") else bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᦧ")
            bstack1ll1111l111_opy_ = request.node.nodeid + (bstack111l_opy_ (u"ࠩࠪᦨ") if bstack1ll11111l11_opy_ == bstack111l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᦩ") else bstack111l_opy_ (u"ࠫ࠲࠭ᦪ") + bstack1ll11111l11_opy_)
            bstack11ll1ll1l1_opy_ = bstack11l1l1llll_opy_(_11l1l1l11l_opy_.get(bstack1ll1111l111_opy_, None))
            if not bstack11ll1ll1l1_opy_:
                continue
            for record in records:
                if bstack1llllll11l1_opy_(record.message):
                    continue
                bstack11l11llll1_opy_.append({
                    bstack111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᦫ"): bstack1llllllll11_opy_(record.created).isoformat() + bstack111l_opy_ (u"࡚࠭ࠨ᦬"),
                    bstack111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭᦭"): record.levelname,
                    bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᦮"): record.message,
                    bstack1ll1111l1ll_opy_: bstack11ll1ll1l1_opy_
                })
        if len(bstack11l11llll1_opy_) > 0:
            bstack11ll111ll_opy_.bstack11l11l1l1_opy_(bstack11l11llll1_opy_)
    except Exception as err:
        print(bstack111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭᦯"), str(err))
def bstack1l111l1l1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1ll1111ll1_opy_
    bstack1l1l111l11_opy_ = bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᦰ"), None) and bstack1l1llll1l_opy_(
            threading.current_thread(), bstack111l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᦱ"), None)
    bstack1l1111111l_opy_ = getattr(driver, bstack111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᦲ"), None) != None and getattr(driver, bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᦳ"), None) == True
    if sequence == bstack111l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᦴ") and driver != None:
      if not bstack1ll1111ll1_opy_ and bstack1111ll111l_opy_() and bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᦵ") in CONFIG and CONFIG[bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᦶ")] == True and bstack111111l11_opy_.bstack11l1l111_opy_(driver_command) and (bstack1l1111111l_opy_ or bstack1l1l111l11_opy_) and not bstack11111111l_opy_(args):
        try:
          bstack1ll1111ll1_opy_ = True
          logger.debug(bstack111l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬᦷ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack111l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩᦸ").format(str(err)))
        bstack1ll1111ll1_opy_ = False
    if sequence == bstack111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᦹ"):
        if driver_command == bstack111l_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᦺ"):
            bstack11ll111ll_opy_.bstack1lll11ll_opy_({
                bstack111l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᦻ"): response[bstack111l_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧᦼ")],
                bstack111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᦽ"): store[bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᦾ")]
            })
def bstack111lllll_opy_():
    global bstack1l11l1l1_opy_
    bstack11lll1lll1_opy_.bstack1l11lll1l_opy_()
    logging.shutdown()
    bstack11ll111ll_opy_.bstack11l1l1ll11_opy_()
    for driver in bstack1l11l1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11111111_opy_(*args):
    global bstack1l11l1l1_opy_
    bstack11ll111ll_opy_.bstack11l1l1ll11_opy_()
    for driver in bstack1l11l1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l11ll1ll_opy_(self, *args, **kwargs):
    bstack1l11l1111_opy_ = bstack1l1111l1ll_opy_(self, *args, **kwargs)
    bstack1l1l11111l_opy_ = getattr(threading.current_thread(), bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬᦿ"), None)
    if bstack1l1l11111l_opy_ and bstack1l1l11111l_opy_.get(bstack111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᧀ"), bstack111l_opy_ (u"࠭ࠧᧁ")) == bstack111l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᧂ"):
        bstack11ll111ll_opy_.bstack1l111l1l_opy_(self)
    return bstack1l11l1111_opy_
def bstack1ll1lll1ll_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1ll1l111_opy_ = Config.bstack11llll1111_opy_()
    if bstack1l1ll1l111_opy_.get_property(bstack111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬᧃ")):
        return
    bstack1l1ll1l111_opy_.bstack1ll11l11ll_opy_(bstack111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ᧄ"), True)
    global bstack11lll1111_opy_
    global bstack1ll1lll1l1_opy_
    bstack11lll1111_opy_ = framework_name
    logger.info(bstack111ll1lll_opy_.format(bstack11lll1111_opy_.split(bstack111l_opy_ (u"ࠪ࠱ࠬᧅ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1111ll111l_opy_():
            Service.start = bstack1l11l111_opy_
            Service.stop = bstack1lll1l1l11_opy_
            webdriver.Remote.__init__ = bstack1l1l1ll1ll_opy_
            webdriver.Remote.get = bstack1l11l111l1_opy_
            if not isinstance(os.getenv(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬᧆ")), str):
                return
            WebDriver.close = bstack1111l1l1_opy_
            WebDriver.quit = bstack1lllll111l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1111ll111l_opy_() and bstack11ll111ll_opy_.on():
            webdriver.Remote.__init__ = bstack1l11ll1ll_opy_
        bstack1ll1lll1l1_opy_ = True
    except Exception as e:
        pass
    bstack1ll1lll11l_opy_()
    if os.environ.get(bstack111l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᧇ")):
        bstack1ll1lll1l1_opy_ = eval(os.environ.get(bstack111l_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᧈ")))
    if not bstack1ll1lll1l1_opy_:
        bstack1l1l1l1lll_opy_(bstack111l_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤᧉ"), bstack11llll1lll_opy_)
    if bstack1ll111lll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._111l11l1_opy_ = bstack1l111l11_opy_
        except Exception as e:
            logger.error(bstack1llll1ll1l_opy_.format(str(e)))
    if bstack111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᧊") in str(framework_name).lower():
        if not bstack1111ll111l_opy_():
            return
        try:
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
def bstack1lllll111l_opy_(self):
    global bstack11lll1111_opy_
    global bstack1l1l11l1l1_opy_
    global bstack1ll1ll1l1_opy_
    try:
        if bstack111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᧋") in bstack11lll1111_opy_ and self.session_id != None and bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ᧌"), bstack111l_opy_ (u"ࠫࠬ᧍")) != bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᧎"):
            bstack1111l111_opy_ = bstack111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᧏") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᧐")
            bstack1l11llll1l_opy_(logger, True)
            if self != None:
                bstack111111ll_opy_(self, bstack1111l111_opy_, bstack111l_opy_ (u"ࠨ࠮ࠣࠫ᧑").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭᧒"), None)
        if item is not None and bstack1l1llll1l_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᧓"), None):
            bstack1l1lllll11_opy_.bstack11l1111l_opy_(self, bstack1111llll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack111l_opy_ (u"ࠫࠬ᧔")
    except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ᧕") + str(e))
    bstack1ll1ll1l1_opy_(self)
    self.session_id = None
def bstack1l1l1ll1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1l11l1l1_opy_
    global bstack1llllllll_opy_
    global bstack1ll1l1l1_opy_
    global bstack11lll1111_opy_
    global bstack1l1111l1ll_opy_
    global bstack1l11l1l1_opy_
    global bstack1l111ll1l_opy_
    global bstack1ll111l1l_opy_
    global bstack1111llll1_opy_
    CONFIG[bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᧖")] = str(bstack11lll1111_opy_) + str(__version__)
    command_executor = bstack1l11l1ll1l_opy_(bstack1l111ll1l_opy_, CONFIG)
    logger.debug(bstack1l1l1l11ll_opy_.format(command_executor))
    proxy = bstack1ll1111l1_opy_(CONFIG, proxy)
    bstack1l11lll11l_opy_ = 0
    try:
        if bstack1ll1l1l1_opy_ is True:
            bstack1l11lll11l_opy_ = int(os.environ.get(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ᧗")))
    except:
        bstack1l11lll11l_opy_ = 0
    bstack1l11ll111l_opy_ = bstack1lll11l1l1_opy_(CONFIG, bstack1l11lll11l_opy_)
    logger.debug(bstack1l1l1l1l1l_opy_.format(str(bstack1l11ll111l_opy_)))
    bstack1111llll1_opy_ = CONFIG.get(bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᧘"))[bstack1l11lll11l_opy_]
    if bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᧙") in CONFIG and CONFIG[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ᧚")]:
        bstack1l1ll11ll1_opy_(bstack1l11ll111l_opy_, bstack1ll111l1l_opy_)
    if bstack1lll111ll_opy_.bstack1l1111l1_opy_(CONFIG, bstack1l11lll11l_opy_) and bstack1lll111ll_opy_.bstack1lllll111_opy_(bstack1l11ll111l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        bstack1lll111ll_opy_.set_capabilities(bstack1l11ll111l_opy_, CONFIG)
    if desired_capabilities:
        bstack11ll1lll_opy_ = bstack111l111l1_opy_(desired_capabilities)
        bstack11ll1lll_opy_[bstack111l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ᧛")] = bstack1llll1lll1_opy_(CONFIG)
        bstack1llll111ll_opy_ = bstack1lll11l1l1_opy_(bstack11ll1lll_opy_)
        if bstack1llll111ll_opy_:
            bstack1l11ll111l_opy_ = update(bstack1llll111ll_opy_, bstack1l11ll111l_opy_)
        desired_capabilities = None
    if options:
        bstack1lll111l_opy_(options, bstack1l11ll111l_opy_)
    if not options:
        options = bstack11ll1lll1_opy_(bstack1l11ll111l_opy_)
    if proxy and bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ᧜")):
        options.proxy(proxy)
    if options and bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ᧝")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11lll11111_opy_() < version.parse(bstack111l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭᧞")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l11ll111l_opy_)
    logger.info(bstack1ll1ll11_opy_)
    if bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ᧟")):
        bstack1l1111l1ll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ᧠")):
        bstack1l1111l1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ᧡")):
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
        bstack11ll1ll1_opy_ = bstack111l_opy_ (u"ࠫࠬ᧢")
        if bstack11lll11111_opy_() >= version.parse(bstack111l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭᧣")):
            bstack11ll1ll1_opy_ = self.caps.get(bstack111l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ᧤"))
        else:
            bstack11ll1ll1_opy_ = self.capabilities.get(bstack111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ᧥"))
        if bstack11ll1ll1_opy_:
            bstack1ll1l111_opy_(bstack11ll1ll1_opy_)
            if bstack11lll11111_opy_() <= version.parse(bstack111l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ᧦")):
                self.command_executor._url = bstack111l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ᧧") + bstack1l111ll1l_opy_ + bstack111l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ᧨")
            else:
                self.command_executor._url = bstack111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ᧩") + bstack11ll1ll1_opy_ + bstack111l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ᧪")
            logger.debug(bstack1111l11l_opy_.format(bstack11ll1ll1_opy_))
        else:
            logger.debug(bstack1llllll1ll_opy_.format(bstack111l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ᧫")))
    except Exception as e:
        logger.debug(bstack1llllll1ll_opy_.format(e))
    bstack1l1l11l1l1_opy_ = self.session_id
    if bstack111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᧬") in bstack11lll1111_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ᧭"), None)
        if item:
            bstack1ll111l11ll_opy_ = getattr(item, bstack111l_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ᧮"), False)
            if not getattr(item, bstack111l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ᧯"), None) and bstack1ll111l11ll_opy_:
                setattr(store[bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ᧰")], bstack111l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭᧱"), self)
        bstack1l1l11111l_opy_ = getattr(threading.current_thread(), bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ᧲"), None)
        if bstack1l1l11111l_opy_ and bstack1l1l11111l_opy_.get(bstack111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ᧳"), bstack111l_opy_ (u"ࠨࠩ᧴")) == bstack111l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ᧵"):
            bstack11ll111ll_opy_.bstack1l111l1l_opy_(self)
    bstack1l11l1l1_opy_.append(self)
    if bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᧶") in CONFIG and bstack111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ᧷") in CONFIG[bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᧸")][bstack1l11lll11l_opy_]:
        bstack1llllllll_opy_ = CONFIG[bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᧹")][bstack1l11lll11l_opy_][bstack111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᧺")]
    logger.debug(bstack1lll1ll11_opy_.format(bstack1l1l11l1l1_opy_))
def bstack1l11l111l1_opy_(self, url):
    global bstack1l1lllll1_opy_
    global CONFIG
    try:
        bstack1l1111l1l1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1llll11ll_opy_.format(str(err)))
    try:
        bstack1l1lllll1_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1llllll1_opy_ = str(e)
            if any(err_msg in bstack1l1llllll1_opy_ for err_msg in bstack1ll1l111ll_opy_):
                bstack1l1111l1l1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1llll11ll_opy_.format(str(err)))
        raise e
def bstack11ll1lll1l_opy_(item, when):
    global bstack1l1111l11l_opy_
    try:
        bstack1l1111l11l_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1l1ll111_opy_(item, call, rep):
    global bstack1l1ll11111_opy_
    global bstack1l11l1l1_opy_
    name = bstack111l_opy_ (u"ࠨࠩ᧻")
    try:
        if rep.when == bstack111l_opy_ (u"ࠩࡦࡥࡱࡲࠧ᧼"):
            bstack1l1l11l1l1_opy_ = threading.current_thread().bstackSessionId
            bstack1ll1111lll1_opy_ = item.config.getoption(bstack111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᧽"))
            try:
                if (str(bstack1ll1111lll1_opy_).lower() != bstack111l_opy_ (u"ࠫࡹࡸࡵࡦࠩ᧾")):
                    name = str(rep.nodeid)
                    bstack111l1l111_opy_ = bstack1l11l1l1ll_opy_(bstack111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᧿"), name, bstack111l_opy_ (u"࠭ࠧᨀ"), bstack111l_opy_ (u"ࠧࠨᨁ"), bstack111l_opy_ (u"ࠨࠩᨂ"), bstack111l_opy_ (u"ࠩࠪᨃ"))
                    os.environ[bstack111l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ᨄ")] = name
                    for driver in bstack1l11l1l1_opy_:
                        if bstack1l1l11l1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack111l1l111_opy_)
            except Exception as e:
                logger.debug(bstack111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫᨅ").format(str(e)))
            try:
                bstack1llll111l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᨆ"):
                    status = bstack111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᨇ") if rep.outcome.lower() == bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᨈ") else bstack111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᨉ")
                    reason = bstack111l_opy_ (u"ࠩࠪᨊ")
                    if status == bstack111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᨋ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack111l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᨌ") if status == bstack111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᨍ") else bstack111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᨎ")
                    data = name + bstack111l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩᨏ") if status == bstack111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᨐ") else name + bstack111l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬᨑ") + reason
                    bstack1l111l111_opy_ = bstack1l11l1l1ll_opy_(bstack111l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᨒ"), bstack111l_opy_ (u"ࠫࠬᨓ"), bstack111l_opy_ (u"ࠬ࠭ᨔ"), bstack111l_opy_ (u"࠭ࠧᨕ"), level, data)
                    for driver in bstack1l11l1l1_opy_:
                        if bstack1l1l11l1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l111l111_opy_)
            except Exception as e:
                logger.debug(bstack111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫᨖ").format(str(e)))
    except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬᨗ").format(str(e)))
    bstack1l1ll11111_opy_(item, call, rep)
notset = Notset()
def bstack1ll11111ll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l11llllll_opy_
    if str(name).lower() == bstack111l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳᨘࠩ"):
        return bstack111l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᨙ")
    else:
        return bstack1l11llllll_opy_(self, name, default, skip)
def bstack1l111l11_opy_(self):
    global CONFIG
    global bstack1l1l1l1l_opy_
    try:
        proxy = bstack1l1ll11l11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack111l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᨚ")):
                proxies = bstack11ll11l1_opy_(proxy, bstack1l11l1ll1l_opy_())
                if len(proxies) > 0:
                    protocol, bstack11lllll1_opy_ = proxies.popitem()
                    if bstack111l_opy_ (u"ࠧࡀ࠯࠰ࠤᨛ") in bstack11lllll1_opy_:
                        return bstack11lllll1_opy_
                    else:
                        return bstack111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ᨜") + bstack11lllll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦ᨝").format(str(e)))
    return bstack1l1l1l1l_opy_(self)
def bstack1ll111lll1_opy_():
    return (bstack111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ᨞") in CONFIG or bstack111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭᨟") in CONFIG) and bstack11lll11ll1_opy_() and bstack11lll11111_opy_() >= version.parse(
        bstack1111l111l_opy_)
def bstack1ll11l1lll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1llllllll_opy_
    global bstack1ll1l1l1_opy_
    global bstack11lll1111_opy_
    CONFIG[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᨠ")] = str(bstack11lll1111_opy_) + str(__version__)
    bstack1l11lll11l_opy_ = 0
    try:
        if bstack1ll1l1l1_opy_ is True:
            bstack1l11lll11l_opy_ = int(os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᨡ")))
    except:
        bstack1l11lll11l_opy_ = 0
    CONFIG[bstack111l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᨢ")] = True
    bstack1l11ll111l_opy_ = bstack1lll11l1l1_opy_(CONFIG, bstack1l11lll11l_opy_)
    logger.debug(bstack1l1l1l1l1l_opy_.format(str(bstack1l11ll111l_opy_)))
    if CONFIG.get(bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᨣ")):
        bstack1l1ll11ll1_opy_(bstack1l11ll111l_opy_, bstack1ll111l1l_opy_)
    if bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᨤ") in CONFIG and bstack111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᨥ") in CONFIG[bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᨦ")][bstack1l11lll11l_opy_]:
        bstack1llllllll_opy_ = CONFIG[bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᨧ")][bstack1l11lll11l_opy_][bstack111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᨨ")]
    import urllib
    import json
    if bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᨩ") in CONFIG and str(CONFIG[bstack111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᨪ")]).lower() != bstack111l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᨫ"):
        bstack1l1llll11_opy_ = bstack11l111ll_opy_()
        bstack1l111lllll_opy_ = bstack1l1llll11_opy_ + urllib.parse.quote(json.dumps(bstack1l11ll111l_opy_))
    else:
        bstack1l111lllll_opy_ = bstack111l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪᨬ") + urllib.parse.quote(json.dumps(bstack1l11ll111l_opy_))
    browser = self.connect(bstack1l111lllll_opy_)
    return browser
def bstack1ll1lll11l_opy_():
    global bstack1ll1lll1l1_opy_
    global bstack11lll1111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11l11l1l_opy_
        if not bstack1111ll111l_opy_():
            global bstack1ll1lll1_opy_
            if not bstack1ll1lll1_opy_:
                from bstack_utils.helper import bstack11ll11ll1_opy_, bstack1ll1llll11_opy_
                bstack1ll1lll1_opy_ = bstack11ll11ll1_opy_()
                bstack1ll1llll11_opy_(bstack11lll1111_opy_)
            BrowserType.connect = bstack11l11l1l_opy_
            return
        BrowserType.launch = bstack1ll11l1lll_opy_
        bstack1ll1lll1l1_opy_ = True
    except Exception as e:
        pass
def bstack1ll1111ll1l_opy_():
    global CONFIG
    global bstack1ll1l1ll_opy_
    global bstack1l111ll1l_opy_
    global bstack1ll111l1l_opy_
    global bstack1ll1l1l1_opy_
    global bstack11l1llll_opy_
    CONFIG = json.loads(os.environ.get(bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨᨭ")))
    bstack1ll1l1ll_opy_ = eval(os.environ.get(bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫᨮ")))
    bstack1l111ll1l_opy_ = os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫᨯ"))
    bstack1l1l11l1_opy_(CONFIG, bstack1ll1l1ll_opy_)
    bstack11l1llll_opy_ = bstack11lll1lll1_opy_.bstack1lll11lll_opy_(CONFIG, bstack11l1llll_opy_)
    global bstack1l1111l1ll_opy_
    global bstack1ll1ll1l1_opy_
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
    except Exception as e:
        pass
    if (bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᨰ") in CONFIG or bstack111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᨱ") in CONFIG) and bstack11lll11ll1_opy_():
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
        logger.debug(bstack111l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨᨲ"))
    bstack1ll111l1l_opy_ = CONFIG.get(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᨳ"), {}).get(bstack111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᨴ"))
    bstack1ll1l1l1_opy_ = True
    bstack1ll1lll1ll_opy_(bstack1ll1l1l11_opy_)
if (bstack1lllll1l111_opy_()):
    bstack1ll1111ll1l_opy_()
@bstack11l1lll111_opy_(class_method=False)
def bstack1ll111l111l_opy_(hook_name, event, bstack1ll111l1111_opy_=None):
    if hook_name not in [bstack111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᨵ"), bstack111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᨶ"), bstack111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᨷ"), bstack111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᨸ"), bstack111l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᨹ"), bstack111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᨺ"), bstack111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᨻ"), bstack111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᨼ")]:
        return
    node = store[bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᨽ")]
    if hook_name in [bstack111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᨾ"), bstack111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᨿ")]:
        node = store[bstack111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ᩀ")]
    elif hook_name in [bstack111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᩁ"), bstack111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᩂ")]:
        node = store[bstack111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨᩃ")]
    if event == bstack111l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᩄ"):
        hook_type = bstack1ll1ll1lll1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11l11ll11l_opy_ = {
            bstack111l_opy_ (u"ࠬࡻࡵࡪࡦࠪᩅ"): uuid,
            bstack111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᩆ"): bstack1ll11l111l_opy_(),
            bstack111l_opy_ (u"ࠧࡵࡻࡳࡩࠬᩇ"): bstack111l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᩈ"),
            bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᩉ"): hook_type,
            bstack111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᩊ"): hook_name
        }
        store[bstack111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᩋ")].append(uuid)
        bstack1ll111111ll_opy_ = node.nodeid
        if hook_type == bstack111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᩌ"):
            if not _11l1l1l11l_opy_.get(bstack1ll111111ll_opy_, None):
                _11l1l1l11l_opy_[bstack1ll111111ll_opy_] = {bstack111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᩍ"): []}
            _11l1l1l11l_opy_[bstack1ll111111ll_opy_][bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᩎ")].append(bstack11l11ll11l_opy_[bstack111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᩏ")])
        _11l1l1l11l_opy_[bstack1ll111111ll_opy_ + bstack111l_opy_ (u"ࠩ࠰ࠫᩐ") + hook_name] = bstack11l11ll11l_opy_
        bstack1ll1111l1l1_opy_(node, bstack11l11ll11l_opy_, bstack111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᩑ"))
    elif event == bstack111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᩒ"):
        bstack11ll1l111l_opy_ = node.nodeid + bstack111l_opy_ (u"ࠬ࠳ࠧᩓ") + hook_name
        _11l1l1l11l_opy_[bstack11ll1l111l_opy_][bstack111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᩔ")] = bstack1ll11l111l_opy_()
        bstack1ll111l11l1_opy_(_11l1l1l11l_opy_[bstack11ll1l111l_opy_][bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᩕ")])
        bstack1ll1111l1l1_opy_(node, _11l1l1l11l_opy_[bstack11ll1l111l_opy_], bstack111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᩖ"), bstack1l1lllllll1_opy_=bstack1ll111l1111_opy_)
def bstack1l1llllllll_opy_():
    global bstack1l1llllll1l_opy_
    if bstack1111l1lll_opy_():
        bstack1l1llllll1l_opy_ = bstack111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᩗ")
    else:
        bstack1l1llllll1l_opy_ = bstack111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᩘ")
@bstack11ll111ll_opy_.bstack1ll11l1l1l1_opy_
def bstack1l1lllll1ll_opy_():
    bstack1l1llllllll_opy_()
    if bstack11lll11ll1_opy_():
        bstack1ll1l1llll_opy_(bstack1l111l1l1l_opy_)
    try:
        bstack1lllll11lll_opy_(bstack1ll111l111l_opy_)
    except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧᩙ").format(e))
bstack1l1lllll1ll_opy_()