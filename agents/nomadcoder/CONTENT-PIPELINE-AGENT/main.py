from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel

class MyFirstFolowState(BaseModel):
    user_id: int = 1
    is_admin: bool = False

    
class MyFirstFlow(Flow[MyFirstFolowState]):
    @start()
    def first(self):
        print(self.state.user_id)
        print("Hello")

    @listen(first)
    def second(self):
        self.state.user_id = 2
        print("World")

    @listen(first)
    def third(self):
        print("CrewAI !")

    @listen(and_(second, third))
    def final(self):
        print(":)")

    @router(final)
    def route(self):
        if self.state.user_id == 2:
            return 'even' # emit event
        else:
            return 'odd'

    @listen("even")
    def handle_even(self):
        print("even")

    @listen("odd")
    def handle_odd(self):
        print("odd")
    
    
    
flow = MyFirstFlow()
# flow.plot()
flow.kickoff()
