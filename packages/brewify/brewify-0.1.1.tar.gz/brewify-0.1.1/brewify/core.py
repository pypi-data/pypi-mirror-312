import requests
from abc import ABC
from .models import *
from fastapi import status

class Brexception(Exception):
    """A brewify exception, hahaha! (I should raise my child)"""
    pass



class Brewify(ABC):
    """Baseclass for the `brewify` library"""
    def __init__(self: "Brewify", api_key: str = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.base = "https://brew-api.vercel.app"

    
    def request(self, endpoint: str, params: str):
        """base `requester` method for this class"""
        try:
            df = params if params else ""
            s = self.session.get(
                url=f"{self.base}/{endpoint}{df}".replace(" ", "%20"), 
                headers={'Authorization': self.api_key},
                timeout=120
                )
            
        
            if s.status_code == status.HTTP_401_UNAUTHORIZED:
               raise Brexception("No such API key found in PostgreSQL database. Head to https://discord.gg/brew to obtain one.")
            
            s.raise_for_status()


            return s

            
        except requests.HTTPError as e:
            raise Brexception(f"http error: {str(e.args[0])}")
        
    def get_google_image(self, query: str) -> ImageLinkResponse:
        """`smegsy`"""
        r = self.request(endpoint="google/search/images", params=f"?query={query}")
        return ImageLinkResponse(**r.json())
    
    def search_google(self, query: str) -> TextSearchResponse:
        """try to not do a different search frequently as it costs my `wallet` (please dont do it)"""
        r = self.request(endpoint="google/search/text", params=f"?query={query}")
        s: dict = r.json()
        return TextSearchResponse(**s)
    
    def imdb_search(self, query: str) -> ImdbSearchResponseModel:
        """idk for the `movieheads`"""
        r = self.request(endpoint="imdb/search", params=f"?query={query}")
        d: dict = r.json()
        return ImdbSearchResponseModel(**d)
    
    def discord_guild_search(self, invite_code: str = None) -> Model:
        """who the `freak` uses this (no diddy)"""
        r = self.request(endpoint="lookup/discord/guild", params=f"?invite_code={invite_code}")
        d: dict = r.json()
        return Model(**d)
    
    def discord_user_search(self, user_id: int = None) -> UserInfoResponse:
        """filthy discordians"""
        r = self.request(endpoint="lookup/discord/user", params=f"?user={user_id}")
        s: dict = r.json()
        return UserInfoResponse(**s)
    
    def sentiment_analysis(self, sentence: str = None) -> SentimentAnalysisResponses:
        """The model for this took atleast `two hours`"""
        r = self.request(endpoint="sentiment", params=f"?text={sentence}")
        s = r.json()
        if not s or not s[0]:  
           raise Brexception("No sentiment data returned")
        
        
        return SentimentAnalysisResponses(s[0])
    
    def chatbot(self, query: str = None) -> Ask:
        """THIS IS ONLY MADE FOR `CHATTING` PURPOSES DONT ASK IT FOR TUTORIALS"""
        r = self.request(endpoint="ask", params=f"?query={query}")
        s = r.json()
        return Ask(response=str(s[0]["generated_text"]))
    
    def joke(self) -> Joke:
        """tells a `joke` duh"""
        r = self.request(endpoint="joke", params=None)
        s: dict = r.json()
        return Joke(setup=s.get("setup"), punchline=s.get("punchline"))
    
    def uwuify(self, msg: str) -> Uwu:
        """Gimme nitro `d-d-daddy...`"""
        r = self.request(endpoint="uwuify", params=f"?msg={msg}")
        s: dict = r.json()
        return Uwu(text=s.get("text"))
    
    def github_profile(self, username: str) -> GitHubResponse:
        """really you need an `explanation`?"""
        r = self.request(endpoint="lookup/github/profile", params=f"?username={username}")
        return GitHubResponse(**r.json())
    
    def country(self, country_code: str) -> CountryInfoResponse:
        """
        :params:
        `country_code`: str = The ISO country code of the desired country you want to gain info for e.g, US
        """
        r = self.request(endpoint="country", params=f"?country_code={country_code}")
        return CountryInfoResponse(**r.json())
    
    def ipinfo(self, ip: str) -> IPGeolocationResponse:
        """im `tired` bruh"""
        r = self.request(endpoint="geo", params=f"?ip={ip}")
        return IPGeolocationResponse(**r.json())