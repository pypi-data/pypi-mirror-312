from pydantic import BaseModel

from ..enterprise import Enterprise
from ..installation import Installation
from ..organization import Organization
from ..repository import Repository
from ..user import User
from .answer import Answer
from .discussion_action_enum import DiscussionActionEnum


class DiscussionEvent(BaseModel):
    action: DiscussionActionEnum
    answer: Answer
    enterprise: Enterprise | None = None
    installation: Installation | None = None
    organization: Organization | None = None
    repository: Repository
    sender: User
