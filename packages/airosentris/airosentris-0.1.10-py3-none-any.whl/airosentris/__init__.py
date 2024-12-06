
class Config:
    API_URL = None
    API_TOKEN = None
    AGENT_DETAILS = None


def get_config():
    return Config


def get_agent():
    return Config.AGENT_DETAILS

from .auth.Auth import login
from .projects.Project import init

import airosentris.dataset.social_comment