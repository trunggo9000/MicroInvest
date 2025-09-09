"""
This module contains page components for the MicroInvest application.
Each page is a function that renders a specific view in the application.
"""

from .welcome import show_welcome_page
from .questionnaire import show_questionnaire_page
from .portfolio import show_portfolio_page
from .analysis import show_analysis_page
from .goals import show_goals_page

__all__ = [
    'show_welcome_page',
    'show_questionnaire_page', 
    'show_portfolio_page',
    'show_analysis_page',
    'show_goals_page'
]
