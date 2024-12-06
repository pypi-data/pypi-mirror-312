from flet import Page,View,Text
from .xstate import Xstate
from .xparams import Xparams


class Xview:
    def __init__(self,page:Page,state:Xstate,params:Xparams):
        self.page = page
        self.state = state
        self.params = params
        self.init()

    def init(self):
        pass

    def update(self):
        self.page.update()

    async def update_async(self):
        self.page.update_async()

    def back(self,*args, **kwargs):
        if self.page.views.__len__()>1:
            pre_r = self.page.views[-2].route
            self.page.views.pop()
            self.page.views.pop()
            self.page.go(pre_r)
            
    def build(self):
        return View(
            controls=[
                Text("Xview")
            ]
        )

    