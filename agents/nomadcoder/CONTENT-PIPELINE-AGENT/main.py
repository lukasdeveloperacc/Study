from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel

class ContentPipelineState(BaseModel):
    # inputs
    content_type: str = ""
    topic: str = ""

    # internal
    max_characters: int = 0

class ContentPipelineFlow(Flow[ContentPipelineState]):
    @start()
    def init_content_pipeline(self):
        if self.state.content_type not in ["tweet", "blog", "linkedin"]:
            raise ValueError("Invalid content type")

        if self.state.topic == "":
            raise ValueError("Topic is required")
        
        if self.state.content_type == "tweet":
            self.state.max_characters = 150
        elif self.state.content_type == "blog":
            self.state.max_characters = 800
        elif self.state.content_type == "linkedin":
            self.state.max_characters = 500

    @listen("init_content_pipeline")
    def conduct_research(self):
        print("Researching...")
        return True

    @router(conduct_research)
    def router(self):
        content_type = self.state.content_type
        if content_type == "tweet":
            return "make_tweet"
        elif content_type == "blog":
            return "make_blog"
        else:
            return "make_linkedin"
        
    @listen("make_blog")
    def handle_make_blog(self):
        print("Making blog...")
        
    @listen("make_tweet")
    def handle_make_tweet(self):
        print("Making tweet...")
        
    @listen("make_linkedin")
    def handle_make_linkedin(self):
        print("Making linkedin...")
    
    @listen(handle_make_blog)
    def check_seo(self):
        print("Checking blog seo...")

    @listen(or_(handle_make_tweet, handle_make_linkedin))
    def check_virality(self):
        print("Checking virality...")

    @listen(or_(check_seo, check_virality))
    def finalize_content(self):
        print("Finalizing content...")

flow = ContentPipelineFlow()
flow.plot()
# flow.kickoff(inputs={"content_type": "tweet", "topic": "AI"})
