"""Module provides tool for working with recipe (storing, loading, counting volumes of ingredients)"""


class BeerRecipe:
    """ Class for handling tools for brewing
    """

    def __init__(self, ingredients: list[dict],
                 resulting_beer_volume: float,
                 sparging_water_volume: float,
                 desired_resulting_beer_volume: float):

        if not isinstance(ingredients, list) or not all(isinstance(i, dict) for i in ingredients):
            raise TypeError("ingredients must be a list of dictionaries.")
        if not isinstance(resulting_beer_volume, float):
            raise TypeError("resulting_beer_volume must be a float.")
        if not isinstance(sparging_water_volume, float):
            raise TypeError("sparging_water_volume must be a float.")
        if not isinstance(desired_resulting_beer_volume, float):
            raise TypeError("desired_resulting_beer_volume must be a float.")

        if resulting_beer_volume <= 0:
            raise ValueError("resulting_beer_volume must be positive.")
        if sparging_water_volume <= 0:
            raise ValueError("sparging_water_volume must be positive.")
        if desired_resulting_beer_volume <= 0:
            raise ValueError("desired_resulting_beer_volume must be positive.")

        self.ingredients = ingredients
        self.resulting_beer_volume = resulting_beer_volume
        self.sparging_water_volume = sparging_water_volume
        self.desired_resulting_beer_volume = desired_resulting_beer_volume

    def get_ratio(self, resulting_beer_volume: float = 0.0, desired_resulting_beer_volume: float = 0.0) -> float:
        """
            Calculates the ratio of the original beer volume to the desired beer volume, 
            useful for adjusting ingredient quantities based on kettle size.

            Args:
                resulting_beer_volume (float, optional): Volume of the final beer in the original recipe.
                desired_resulting_beer_volume (float, optional): Desired final beer volume, based on the available kettle's maximum volume.

            Returns:
                float: Ratio of the original beer volume to the desired beer volume.
        """

        if not isinstance(resulting_beer_volume, float) or not isinstance(desired_resulting_beer_volume, float):
            raise TypeError("input parameters must be a float.")

        if resulting_beer_volume <= 0.0:
            resulting_beer_volume = self.resulting_beer_volume
        if desired_resulting_beer_volume <= 0.0:
            desired_resulting_beer_volume = self.desired_resulting_beer_volume

        return desired_resulting_beer_volume / resulting_beer_volume

    def print_ingredients(self, calculate_with_ratio: bool = False) -> None:
        """
            Prints the ingredients needed for the recipe.

            Args:
                calculate_with_ratio (bool, optional): If True, prints ingredients recalculated with the desired ratio. Defaults to False.
        """

        ratio = 1.0

        if calculate_with_ratio:
            ratio = self.get_ratio()

        print(f'{"="*20} Ingredients {"="*20}')
        for ingredient in self.ingredients:

            print(f'{ingredient['name']}: {ingredient['amount'] * ratio}g')


# Example of usage
try:
    recipe = BeerRecipe(
        ingredients=[{"name": "Pilzner Malt", "type": "Malt", "amount": 2000},
                     {"name": "Citra", "type": "Hop", "amount": 50}],
        resulting_beer_volume=20.0,
        sparging_water_volume=10.0,
        desired_resulting_beer_volume=10.0
    )
    print("Recipe created successfully!")

    print(recipe.get_ratio())

    recipe.print_ingredients()
except (TypeError, ValueError) as e:
    print(f"Error creating recipe: {e}")
