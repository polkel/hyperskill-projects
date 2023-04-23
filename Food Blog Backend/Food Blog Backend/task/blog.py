import sqlite3
import os
import argparse


class RecipeDB:  # Can convert all SQL query += to io.StringIO later if necessary
    def __init__(self, db_name):
        self.db_name = db_name
        self.tables = dict()
        self.setup_tables()
        self.db_conn = None
        self.db_cursor = None
        if self.db_name not in os.listdir():
            self.update_db(True)
        else:
            self.update_db()

    def update_db(self, init_data=False):
        self.db_conn = sqlite3.connect(self.db_name)
        self.db_cursor = self.db_conn.cursor()
        self.sql_execute("PRAGMA foreign_keys = ON;")
        all_tables = self.get_all_tables()
        for table_name, table_cols in self.tables.items():
            if table_name not in all_tables:
                self.create_table(table_name, *table_cols)
                print(f"{table_name} table successfully created!\n")
        if init_data:
            data = {"meals": ["breakfast", "brunch", "lunch", "supper"],
                    "ingredients": ["milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"],
                    "measures": ["ml", "g", "l", "cup", "tbsp", "tsp", "dsp", ""]}
            for table_name, table_items in data.items():
                table_entries = [(item,) for item in table_items]
                self.insert_entries(table_name, (table_name[:-1] + "_name", ), table_entries)
        self.db_conn.commit()

    def get_all_tables(self):
        sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
        result = self.sql_execute(sql_query)
        table_list = result.fetchall()
        table_list = tuple(table_tuple[0] for table_tuple in table_list)
        return table_list

    def create_table(self, table_name, col_declaration, *args):
        sql_query = f"CREATE TABLE {table_name} (\n\t"
        sql_query += f"{col_declaration}"
        for arg in args:
            sql_query += f",\n\t{arg}"
        sql_query += "\n);"
        self.sql_execute(sql_query)

    def insert_entries(self, table_name, col_names_tuple, entries):
        col_names = ", ".join(col_names_tuple)
        question_marks = ", ".join(["?" for _ in col_names_tuple])
        sql_query = f"INSERT INTO {table_name} ({col_names})\n"
        sql_query += f"VALUES ({question_marks});"
        return self.sql_execute_many(sql_query, entries)

    def insert_entry(self, table_name, col_names_tuple, entry_tuple):
        col_names = ", ".join(col_names_tuple)
        question_marks = ", ".join(["?" for _ in col_names_tuple])
        sql_query = f"INSERT INTO {table_name} ({col_names})\n"
        sql_query += f"VALUES ({question_marks});"
        return self.sql_execute(sql_query, entry_tuple)

    def sql_execute(self, query, *item):
        print(query + "\n")
        if item:
            print(str(item[0]) + "\n")
            result = self.db_cursor.execute(query, item[0])
        else:
            result = self.db_cursor.execute(query)
        if self.db_cursor.rowcount > 0:
            print(str(self.db_cursor.rowcount) + " entry has been updated\n")
        return result

    def sql_execute_many(self, query, items):
        print(query + "\n")
        print(items)
        result = self.db_cursor.executemany(query, items)
        if self.db_cursor.rowcount > 0:
            print("\n" + str(self.db_cursor.rowcount) + " entries have been updated")
        print("\n")
        return result

    def setup_tables(self):  # initializing function that sets up db tables
        meals_table = ["meal_id INTEGER PRIMARY KEY",
                       "meal_name TEXT NOT NULL UNIQUE"]
        self.tables["meals"] = meals_table

        ingredients_table = ["ingredient_id INTEGER PRIMARY KEY",
                             "ingredient_name TEXT NOT NULL UNIQUE"]
        self.tables["ingredients"] = ingredients_table

        measures_table = ["measure_id INTEGER PRIMARY KEY",
                          "measure_name TEXT UNIQUE"]
        self.tables["measures"] = measures_table

        recipes_table = ["recipe_id INTEGER PRIMARY KEY",
                         "recipe_name TEXT NOT NULL",
                         "recipe_description TEXT"]
        self.tables["recipes"] = recipes_table

        serve_table = ["serve_id INTEGER PRIMARY KEY",
                       "recipe_id INTEGER NOT NULL",
                       "meal_id INTEGER NOT NULL",
                       "FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE ON UPDATE CASCADE",
                       "FOREIGN KEY (meal_id) REFERENCES meals(meal_id) ON DELETE CASCADE ON UPDATE CASCADE"]
        self.tables["serve"] = serve_table

        quantity_table = ["quantity_id INTEGER PRIMARY KEY",
                          "quantity INTEGER NOT NULL",
                          "recipe_id INTEGER NOT NULL",
                          "measure_id INTEGER NOT NULL",
                          "ingredient_id INTEGER NOT NULL",
                          "FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE ON UPDATE CASCADE",
                          "FOREIGN KEY (measure_id) REFERENCES measures(measure_id) ON DELETE CASCADE ON UPDATE CASCADE",
                          "FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE ON UPDATE CASCADE"]
        self.tables["quantity"] = quantity_table
        # TODO make list of tables and keys within each table
        # TODO make standalone future function that can create db tables with parameters

    def ask_recipe(self):
        print("Pass the empty recipe name to exit")
        recipe_name = input("Recipe name: ")
        recipe_meal_pairs = []
        while recipe_name:
            recipe_description = input("Recipe description: ")
            insert_result = self.insert_entry("recipes",
                                              ("recipe_name", "recipe_description"),
                                              (recipe_name, recipe_description))
            recipe_id = insert_result.lastrowid
            meal_times_tuple = self.ask_meal_time()
            for meal_id in meal_times_tuple:
                recipe_meal_pairs.append((recipe_id, meal_id))
            # insert a self.ask_ingredients() call here
            self.ask_ingredients(recipe_id)
            recipe_name = input("Recipe name: ")
        print("\n")
        if recipe_meal_pairs:
            self.insert_entries("serve", ("recipe_id", "meal_id"), recipe_meal_pairs)

    def ask_meal_time(self):
        meals_result = self.get_entries("meals", ("meal_id", "meal_name"), order_by="meal_id")
        meals_list = meals_result.fetchall()
        meal_string = f"{meals_list[0][0]}) {meals_list[0][1]}"
        meals_list.remove(meals_list[0])
        for meal_id, meal_name in meals_list:
            meal_string += f"  {meal_id}) {meal_name}"
        meal_string += "\n"
        user_response = input(meal_string + "When the dish can be served: ")
        result = tuple(user_response.split())
        return result

    def ask_ingredients(self, r_id):
        # initialize input to something random
        ingredient_input = "placeholder"
        # while loop not blank
        while ingredient_input:  # TODO enforce input format better
            ingredient_input = input("Input quantity of ingredient <press enter to stop>: ")
            if not ingredient_input.strip():
                break
            ingredient_list = ingredient_input.strip().split()
            if len(ingredient_list) == 3:
                amount, measure, ingredient = ingredient_list
                measure_result = self.get_entries("measures",
                                                  ("measure_id",),
                                                  f"measure_name LIKE '{measure}%'")
                measure_entries = measure_result.fetchall()
                if not len(measure_entries) == 1:
                    print("The measure is not conclusive!")
                    continue
                measure_id = measure_entries[0][0]
            elif len(ingredient_list) == 2:
                amount, ingredient = ingredient_list
                measure_result = self.get_entries("measures",
                                                  ("measure_id",),
                                                  "measure_name = ''")
                measure_id = measure_result.fetchall()[0][0]
            else:
                print("Invalid input!")
                continue
            amount = int(amount)
            ingredient_result = self.get_entries("ingredients",
                                                 ("ingredient_id",),
                                                 f"ingredient_name LIKE '%{ingredient}%'")
            ingredient_entries = ingredient_result.fetchall()
            if not len(ingredient_entries) == 1:
                print("The ingredient is not conclusive!")
                continue
            ingredient_id = ingredient_entries[0][0]
            result = self.insert_entry("quantity",
                                       ("quantity", "recipe_id", "measure_id", "ingredient_id"),
                                       (amount, r_id, measure_id, ingredient_id))

    def get_entries(self, table_name, col_tuple, where=None, order_by=None):
        col_names = ", ".join(col_tuple)
        sql_query = f"SELECT {col_names}\n"
        sql_query += f"FROM {table_name}"
        if where:
            sql_query += f"\nWHERE {where}"
        if order_by:
            sql_query += f"\nORDER BY {order_by}"
        sql_query += ";"
        result = self.sql_execute(sql_query)
        return result

    def get_recipes(self, ingredients=None, meals=None):  # should clean this up for future iteration
        ingredients_tuple = tuple()
        meals_tuple = tuple()
        if ingredients:
            ingredients_tuple = ingredients.split(",")
        if meals:
            meals_tuple = meals.split(",")
        sql_query = "SELECT recipe_name \nFROM recipes \nWHERE \n\t"
        for ingredient in ingredients_tuple:
            sql_query += f"EXISTS(\n\t\t{self.make_exist_query('ingredients', ingredient)}) \n\tAND \n\t"
        if meals:
            sql_query += "("
            for meal in meals_tuple:
                sql_query += f"EXISTS(\n\t\t{self.make_exist_query('meals', meal)}) \n\tOR \n\t"
            sql_query = sql_query[:-8] + ");"
        else:
            sql_query = sql_query[:-9] + ";"
        result = self.sql_execute(sql_query)
        recipes_list = result.fetchall()
        if recipes_list:
            recipe_string = ""
            for recipe in recipes_list:
                recipe_string += recipe[0] + ", "
            recipe_string = recipe_string[:-2]
            print(f"Recipes selected for you: {recipe_string}")
        else:
            print("There are no such recipes in the database.")

    @staticmethod
    def make_exist_query(table_name, item):  # really convoluted query that can be simplified
        if table_name == "ingredients":
            table = "quantity"
        else:
            table = "serve"
        sql_query = f"SELECT * \n\t\tFROM {table} \n\t\tWHERE "
        sql_query += f"\n\t\t{table_name[:-1]}_id IN (\n\t\t\tSELECT {table_name[:-1]}_id \n\t\t\tFROM "
        sql_query += f"{table_name} \n\t\t\tWHERE {table_name[:-1]}_name = '{item}') \n\t\tAND \n\t\t"
        sql_query += "recipe_id = recipes.recipe_id"
        return sql_query

    def close_db(self):
        self.db_conn.commit()
        self.db_conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recipe db granma")
    parser.add_argument("db_name")
    parser.add_argument("--ingredients")
    parser.add_argument("--meals")
    arg_parse = parser.parse_args()
    ingredients_input = arg_parse.ingredients
    meals_input = arg_parse.meals
    my_recipe_db = RecipeDB(arg_parse.db_name)
    if ingredients_input or meals_input:
        my_recipe_db.get_recipes(ingredients_input, meals_input)
    else:
        my_recipe_db.ask_recipe()
    my_recipe_db.close_db()
