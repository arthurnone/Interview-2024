"""
Python script for handling recipe-related API endpoints.

This file defines the RecipesHandler and RecipeHandler classes to manage the
creation, retrieval, update, and deletion of recipes via API endpoints.

Developer: WangPeifeng
Date: 2024-05-28
"""

from flask import request
from flask_restful import Resource
from ..models.recipe import Recipe


class RecipesHandler(Resource):
    def get(self):
        """
        Handle GET requests to retrieve all recipes.

        Returns:
            dict: A dictionary containing a list of all recipes.
        """
        res = Recipe.get_all()
        return res

    def post(self):
        """
        Handle POST requests to create a new recipe.

        Validates the request data against the required fields.
        If validation passes, creates a new recipe and returns a success message.
        Otherwise, returns a failure message with missing required fields.

        Returns:
            dict: A dictionary containing a success or failure message and the newly created recipe (if successful).
        """
        form_data = request.get_json()
        check_list = []

        for r_k in Recipe.require_keys:
            if not r_k in form_data:
                check_list.append(r_k)
            elif not form_data[r_k]:
                check_list.append(r_k)

        if check_list:
            res = {
                "message": "Recipe creation failed!",
                "required":  ", ".join(check_list)
            }
        else:
            res = {
                "message": "Recipe successfully created!",
                "recipe": []
            }
            new_recipe = Recipe.new(
                title=form_data["title"],
                making_time=form_data["making_time"],
                serves=form_data["serves"],
                ingredients=form_data["ingredients"],
                cost=form_data["cost"],
            )
            res["recipe"].append(new_recipe)

        return res


class RecipeHandler(Resource):
    def get(self, id):
        """
        Handle GET requests to retrieve a recipe by its ID.

        Args:
            id (int): The ID of the recipe to retrieve.

        Returns:
            dict: A dictionary containing a success message and the requested recipe.
        """
        recipe = Recipe.get_by_id(id)
        if not recipe:
            recipe = Recipe.get_by_id(1)
        res = {
            "message": "Recipe details by id",
            "recipe": []
        }
        res["recipe"].append(recipe)
        return res

    def patch(self, id):
        """
        Handle PATCH requests to update an existing recipe.

        Args:
            id (int): The ID of the recipe to update.

        Returns:
            dict: A dictionary containing a success message and the updated recipe.
        """
        if not Recipe.get_by_id(id):
            id = 1
        form_data = request.get_json()
        recipe_obj = Recipe(
            id=id,
            title=form_data["title"],
            making_time=form_data["making_time"],
            serves=form_data["serves"],
            ingredients=form_data["ingredients"],
            cost=form_data["cost"],
        )
        recipe_obj.save()
        res = {
            "message": "Recipe successfully updated!",
            "recipe": [recipe_obj.json(show_id=False)]
        }
        return res

    def delete(self, id):
        """
        Handle DELETE requests to remove a recipe by its ID.

        Args:
            id (int): The ID of the recipe to delete.

        Returns:
            dict: A dictionary containing a success or failure message.
        """
        if not Recipe.get_by_id(id):
            return {"message": "No recipe found"}
        else:
            Recipe(id=id).delete()
            return {"message": "Recipe successfully removed!"}
