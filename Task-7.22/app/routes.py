"""
Python script for configuring API routes.

This file sets up the API routes for the application, mapping URL endpoints
to their corresponding request handlers.

Developer: WangPeifeng
Date: 2024-05-29
"""

from flask_restful import Api
from .api.recipes import RecipesHandler, RecipeHandler


def create_routes(app):
    api = Api(app)
    api.add_resource(RecipesHandler, '/recipes')
    api.add_resource(RecipeHandler, '/recipes/<int:id>')
