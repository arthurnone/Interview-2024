"""
Python script for managing recipe data.

This file defines the Recipe class with methods to interact with the recipe database,
including creating, reading, updating, and deleting recipes.

Developer: WangPeifeng
Date: 2024-05-29
"""

from ..db import db


class Recipe:
    keys = ["id", "title", "making_time", "serves",
            "ingredients", "cost", "created_at", "updated_at"]
    require_keys = ["title", "making_time", "serves", "ingredients", "cost"]

    def __init__(self, id=None, title=None, making_time=None, serves=None, ingredients=None, cost=None):
        """
        Initialize a new Recipe instance.

        Args:
            id (int, optional): The ID of the recipe.
            title (str, optional): The title of the recipe.
            making_time (str, optional): The making time of the recipe.
            serves (str, optional): The number of servings.
            ingredients (str, optional): The ingredients required for the recipe.
            cost (int, optional): The cost of the recipe.
        """
        self.id = id
        self.title = title
        self.making_time = making_time
        self.serves = serves
        self.ingredients = ingredients
        self.cost = cost

    def json(self, show_id=True):
        """
        Convert the Recipe instance to a JSON-serializable dictionary.

        Args:
            show_id (bool, optional): Whether to include the recipe ID in the JSON. Default is True.

        Returns:
            dict: JSON-serializable representation of the Recipe instance.
        """
        res = {
            "title": self.title,
            "making_time": self.making_time,
            "serves": self.serves,
            "ingredients": self.ingredients,
            "cost": self.cost,
        }
        if show_id:
            res["id"] = self.id
        return res

    @staticmethod
    def get_all():
        """
        Retrieve all recipes from the database.

        Returns:
            dict: A dictionary containing a list of all recipes.
        """
        key_sql = ",".join(Recipe.require_keys)
        cursor = db.get_cursor()
        cursor.execute(f"SELECT id,{key_sql} FROM recipes")
        results = cursor.fetchall()
        cursor.close()

        recipes = []
        for row in results:
            recipe = Recipe(
                id=row[0],
                title=row[1],
                making_time=row[2],
                serves=row[3],
                ingredients=row[4],
                cost=row[5],
            )
            recipes.append(recipe.json())
        return {
            "recipes": recipes
        }

    @classmethod
    def get_by_id(cls, recipe_id, is_new=False):
        """
        Retrieve a recipe by its ID.

        Args:
            recipe_id (int): The ID of the recipe to retrieve.
            is_new (bool, optional): Whether to include creation and update timestamps. Default is False.

        Returns:
            dict or None: A dictionary representing the recipe if found, otherwise None.
        """
        if is_new:
            keys = cls.keys
        else:
            keys = cls.require_keys
        cursor = db.get_cursor()
        cursor.execute(
            f"SELECT {','.join(keys)} FROM recipes WHERE id = {recipe_id}")
        result = cursor.fetchone()
        if not result:
            return None
        cursor.close()
        data = {}
        for k, v in enumerate(keys):
            data[v] = result[k]
        if is_new:
            data["created_at"] = data["created_at"].strftime(
                '%Y-%m-%d %H:%M:%S')
            data["updated_at"] = data["updated_at"].strftime(
                '%Y-%m-%d %H:%M:%S')
        else:
            data["id"] = recipe_id
        return data

    @classmethod
    def new(cls, title=None, making_time=None, serves=None, ingredients=None, cost=None):
        """
        Create a new recipe in the database.

        Args:
            title (str): The title of the recipe.
            making_time (str): The making time of the recipe.
            serves (str): The number of servings.
            ingredients (str): The ingredients required for the recipe.
            cost (int): The cost of the recipe.

        Returns:
            dict: A dictionary representing the newly created recipe.
        """
        sql = f"""
            INSERT INTO recipes ({','.join(cls.require_keys)})
            VALUES ('{title}', '{making_time}',
                    '{serves}', '{ingredients}', {cost})
        """
        cursor = db.get_cursor()
        cursor.execute(sql)
        new_id = cursor.connection.insert_id()
        cursor.connection.commit()
        cursor.close()
        return cls.get_by_id(new_id, True)

    def save(self):
        """
        Save updates to an existing recipe in the database.
        """
        sql = f"""
            UPDATE recipes SET title = '{self.title}', making_time = '{self.making_time}', serves = '{self.serves}',
            ingredients = '{self.ingredients}', cost = {self.cost} WHERE id = {self.id}
        """
        cursor = db.get_cursor()
        cursor.execute(sql)
        cursor.connection.commit()
        cursor.close()

    def delete(self):
        """
        Delete the recipe from the database if it has an ID.
        """
        if self.id:
            cursor = db.get_cursor()
            cursor.execute(f"DELETE FROM recipes WHERE id = {self.id}")
            cursor.connection.commit()
            cursor.close()
