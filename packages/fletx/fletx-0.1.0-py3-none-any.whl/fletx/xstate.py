from flet import Page

class Xstate:
    def __init__(self,page:Page):
        self.page = page

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