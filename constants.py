import os

from src.models.label import Label
from src.models.action import Action
from src.models.board import Board
from src.models.card import Card
from src.models.card_label import CardLabel
from src.models.card_membership import CardMembership
from src.models.list import List
from src.models.task import Task
from src.models.project_manager import ProjectManager
from src.models.project import Project
from src.models.user_account import UserAccount


LOG_FILE_NAME = 'transactions.json'  # service.undo transactions log

DATA_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)),
    'src',
    'data'
)

ATTACHMENT_URL = ''

ENTITY_TYPES = {
    'Label': Label,
    'Action': Action,
    'Board': Board,
    'Card': Card,
    'CardLabel': CardLabel,
    'CardMembership': CardMembership,
    'List': List,
    'Task': Task,
    'ProjectManager': ProjectManager,
    'Project': Project,
    'UserAccount': UserAccount
}
