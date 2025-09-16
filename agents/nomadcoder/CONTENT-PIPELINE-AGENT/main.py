from dotenv import load_dotenv

load_dotenv()

from crewai.flow.flow import Flow, listen, start, router, or_
from crewai import Agent, LLM
from pydantic import BaseModel
from tools import web_search_tool
from typing import List
from seo_crew import SeoCrew
from virality_crew import ViralityCrew

class BlogPost(BaseModel):
    title: str
    subtitle: str
    sections: List[str]

class Tweet(BaseModel):
    content: str
    hashtags: str

class LinkedInPost(BaseModel):
    hook: str
    content: str
    call_to_action: str

class Score(BaseModel):
    score: int = 0
    reason: str = ""
    
  
class ContentPipelineState(BaseModel):
    # inputs
    content_type: str = ""
    topic: str = ""

    # internal
    max_characters: int = 0
    score: Score | None = None
    research: str = ""

    # Content
    blog_post: BlogPost | None = None
    tweet: Tweet | None = None
    linkedin_post: LinkedInPost | None = None
    

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
        researcher = Agent(
            role="Head Researcher",
            backstory="You're like a digital detective who loves digging up fascinating facts and insights. You have a knack for finding the good stuff that others miss.",
            goal=f"Find the most interesting and useful info about {self.state.topic}",
            tools=[web_search_tool],
        )

        self.state.research = researcher.kickoff(
            f"Find the most interesting and useful info about {self.state.topic}"
        )

    @router(conduct_research)
    def conduct_research_router(self):
        content_type = self.state.content_type

        if content_type == "tweet":
            return "make_tweet"
        elif content_type == "blog":
            return "make_blog"
        else:
            return "make_linkedin"
        
    @listen(or_("make_blog", "remake_blog"))
    def handle_make_blog(self):
        blog_post = self.state.blog_post

        llm = LLM(model="openai/o4-mini", response_format=BlogPost)
        if blog_post is None:
            result = llm.call(f"""
            Make a blog post with SEO practices on the topic {self.state.topic} using the fllowing resarch: 
            
            <research>
            ===============
            {self.state.research}
            ===============
            </research>
            """)
        else:
            result = llm.call(f"""
            You wrote this blog post, but it does not have good SEO score because of {self.state.score.reason}. 
            
            Improve it.

            <blog post>
            {self.state.blog_post.model_dump_json()}
            </blog post>
            
            Use the following research.

            <research>
            ===============
            {self.state.research}
            ===============
            </research>
            """)

        self.state.blog_post = BlogPost.model_validate_json(result)
            
        
    @listen(or_("make_tweet", "remake_tweet"))
    def handle_make_tweet(self):
        tweet = self.state.tweet

        llm = LLM(model="openai/o4-mini", response_format=Tweet)
        if tweet is None:
            result = llm.call(f"""
            Make a tweet that can go viral on the topic {self.state.topic} using the fllowing resarch: 
            
            <research>
            ===============
            {self.state.research}
            ===============
            </research>
            """)
        else:
            result = llm.call(f"""
            You wrote this tweet, but it does not have good virality score because of {self.state.score.reason}. 
            
            Improve it.

            <tweet>
            {self.state.tweet.model_dump_json()}
            </tweet>
            
            Use the following research.

            <research>
            ===============
            {self.state.research}
            ===============
            </research>
            """)

        self.state.tweet = Tweet.model_validate_json(result)
            
        
    @listen(or_("make_linkedin", "remake_linkedin"))
    def handle_make_linkedin(self):
        linkedin_post = self.state.linkedin_post

        llm = LLM(model="openai/o4-mini", response_format=LinkedInPost)
        if linkedin_post is None:
            result = llm.call(f"""
            Make a linkedin post that can go viral on the topic {self.state.topic} using the fllowing resarch: 
            
            <research>
            ===============
            {self.state.research}
            ===============
            </research>
            """)
        else:
            result = llm.call(f"""
            You wrote this linkedin post, but it does not have good virality score because of {self.state.score.reason}. 
            
            Improve it.

            <linkedin post>
            {self.state.linkedin_post.model_dump_json()}
            </linkedin post>
            
            Use the following research.

            <research>
            ===============
            {self.state.research}
            ===============
            </research>
            """)
        
        self.state.linkedin_post = LinkedInPost.model_validate_json(result)            
    
    @listen(handle_make_blog)
    def check_seo(self):
        result = SeoCrew().crew().kickoff(
            inputs={"blog_post": self.state.blog_post.model_dump_json(), "topic": self.state.topic})
        self.state.score = result.pydantic

    @listen(or_(handle_make_tweet, handle_make_linkedin))
    def check_virality(self):
        result = ViralityCrew().crew().kickoff(
            inputs={
                "topic": self.state.topic, 
                "content_type": self.state.content_type, 
                "content": self.state.tweet.model_dump_json() 
                if self.state.content_type == "tweet" 
                else self.state.linkedin_post.model_dump_json()
            })
        self.state.score = result.pydantic

    @router(or_(check_seo, check_virality))
    def score_router(self):
        content_type = self.state.content_type
        
        if self.state.score.score >= 6:
            return "check_passed"
        else:
            if content_type == "blog":
                return "remake_blog"
            elif content_type == "linkedin":
                return "remake_linkedin"
            else:
                return "remake_tweet"

    @listen("check_passed")
    def finalize_content(self):
        print("Finalizing content")
        """Finalize the content"""
        print("🎉 Finalizing content...")

        if self.state.content_type == "blog":
            print(f"📝 Blog Post: {self.state.blog_post.title}")
            print(f"🔍 SEO Score: {self.state.score.score}/100")
        elif self.state.content_type == "tweet":
            print(f"🐦 Tweet: {self.state.tweet}")
            print(f"🚀 Virality Score: {self.state.score.score}/100")
        elif self.state.content_type == "linkedin":
            print(f"💼 LinkedIn: {self.state.linkedin_post.title}")
            print(f"🚀 Virality Score: {self.state.score.score}/100")

        print("✅ Content ready for publication!")
        return (
            self.state.linkedin_post
            if self.state.content_type == "linkedin"
            else (
                self.state.tweet
                if self.state.content_type == "tweet"
                else self.state.blog_post
            )
        )

flow = ContentPipelineFlow()
flow.plot()
flow.kickoff(inputs={"content_type": "blog", "topic": "AI dog training"})
