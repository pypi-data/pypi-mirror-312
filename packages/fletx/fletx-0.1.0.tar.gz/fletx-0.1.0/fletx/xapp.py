from flet import Page
from .xstate import Xstate
from .xview import Xview
from .xparams import Xparams
from.view_not_found import NotFoundView
from repath import match

def route(route:str,view:Xview) -> dict:
    return {"route":route,"view":view}

class Xapp:
    def __init__(self,page:Page,state:Xstate,routes:list[route],init_route = "/"):
        
        self.__page = page
        self.__state = state(page)
        self.__routes = routes
        self.__params = Xparams()
        page.on_route_change = self.route_event_handler
        page.views.pop()
        page.go(init_route)

    def route_event_handler(self,route):
        route_match = None

        for r in self.__routes:
            route_match = match(r["route"], self.__page.route)
            if route_match:
                self.__params = Xparams(route_match.groupdict())
                view = r["view"](page=self.__page,state = self.__state,params=self.__params)
                self.__page.views.append(view.build())
                self.__page.update()
                break

        if route_match == None:
            self.__page.views.append(NotFoundView(page=self.__page,state = self.__state,params=Xparams()).build())
            self.__page.update()

