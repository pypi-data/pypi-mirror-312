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
bstack1ll1ll1l1ll_opy_ = 1000
bstack1ll1ll11lll_opy_ = 5
bstack1ll1ll11l1l_opy_ = 30
bstack1ll1ll1l11l_opy_ = 2
class bstack1ll1ll1111l_opy_:
    def __init__(self, handler, bstack1ll1ll111ll_opy_=bstack1ll1ll1l1ll_opy_, bstack1ll1ll11l11_opy_=bstack1ll1ll11lll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll1ll111ll_opy_ = bstack1ll1ll111ll_opy_
        self.bstack1ll1ll11l11_opy_ = bstack1ll1ll11l11_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1ll1ll1l111_opy_()
    def bstack1ll1ll1l111_opy_(self):
        self.timer = threading.Timer(self.bstack1ll1ll11l11_opy_, self.bstack1ll1ll11ll1_opy_)
        self.timer.start()
    def bstack1ll1ll111l1_opy_(self):
        self.timer.cancel()
    def bstack1ll1ll1l1l1_opy_(self):
        self.bstack1ll1ll111l1_opy_()
        self.bstack1ll1ll1l111_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll1ll111ll_opy_:
                t = threading.Thread(target=self.bstack1ll1ll11ll1_opy_)
                t.start()
                self.bstack1ll1ll1l1l1_opy_()
    def bstack1ll1ll11ll1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1ll1ll111ll_opy_]
        del self.queue[:self.bstack1ll1ll111ll_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1ll1ll111l1_opy_()
        while len(self.queue) > 0:
            self.bstack1ll1ll11ll1_opy_()