"""Module provides tool for working with recipe (storing, loading, counting volumes of ingredients)"""
from colorama import Fore, Style, init


class BeerRecipe:
    """ Class for handling tools for brewing
    """

    def __init__(self, ingredients: dict[str, dict],
                 resulting_beer_volume: float,
                 sparging_water_volume: float,
                 kettle_volume: float):

        # if not isinstance(ingredients, dict) or not all(isinstance(i, list) for i in ingredients):

        #   raise TypeError("ingredients must be a list of dictionaries.")
        if not isinstance(resulting_beer_volume, float):
            raise TypeError("resulting_beer_volume must be a float.")
        if not isinstance(sparging_water_volume, float):
            raise TypeError("sparging_water_volume must be a float.")
        if not isinstance(kettle_volume, float):
            raise TypeError("kettle_volume must be a float.")

        if resulting_beer_volume <= 0:
            raise ValueError("resulting_beer_volume must be positive.")
        if sparging_water_volume <= 0:
            raise ValueError("sparging_water_volume must be positive.")
        if kettle_volume <= 0:
            raise ValueError("kettle_volume must be positive.")

        self.kettle_volume = kettle_volume
        self.ingredients = ingredients
        self.resulting_beer_volume = resulting_beer_volume
        self.sparging_water_volume = sparging_water_volume
        self.sparging_water_volume_in_ratio = self.__calculate_sparging_water_in_ratio()
        self.input_water = self.__calculate_input_water_in_ratio()

    def get_ratio(self, resulting_beer_volume: float = 0.0, kettle_volume: float = 0.0, volume_of_ingredients=0.0) -> float:
        """
            Calculates the ratio of the original beer volume to the desired beer volume,
            useful for adjusting ingredient quantities based on kettle size.

            Args:
                resulting_beer_volume (float, optional): Volume of the final beer in the original recipe.
                kettle_volume (float, optional): Desired final beer volume, based on the available kettle's maximum volume.

            Returns:
                float: Ratio of the original beer volume to the desired beer volume.
        """

        if not isinstance(resulting_beer_volume, float) or not isinstance(kettle_volume, float):
            raise TypeError("input parameters must be a float.")

        if resulting_beer_volume <= 0.0:
            resulting_beer_volume = self.resulting_beer_volume
        if kettle_volume <= 0.0:
            kettle_volume = self.kettle_volume
        if volume_of_ingredients <= 0.0:
            volume_of_ingredients = self.__calculate_volume_of_ingredients()

        return (kettle_volume - volume_of_ingredients) / resulting_beer_volume

    def __calculate_volume_of_ingredients(self):
        """_summary_

        Args:
            ingredients (dict, optional): _description_. Defaults to None.
        """

        ingredients = self.ingredients

        volume = 0.0

        for ingredient in ingredients['mashing']['ingredients']:
            volume += ingredient['amount']

        return volume

    def __calculate_input_water_in_ratio(self):
        """

        """

        input_water_volume_in_ratio = self.kettle_volume - \
            self.__calculate_volume_of_ingredients() - self.sparging_water_volume_in_ratio

        return input_water_volume_in_ratio

    def __calculate_sparging_water_in_ratio(self):
        """

        """

        ratio = self.get_ratio()

        sparging_water_volume_in_ratio = self.sparging_water_volume * ratio

        return sparging_water_volume_in_ratio

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
        print(f'{"-"*20} Water {"-"*20}')
        print(f'Input Water: {self.input_water * ratio:.2f} liters')
        print(f'Sparging Water: {
            self.sparging_water_volume_in_ratio * ratio:.2f} liters')

        for stage, details in self.ingredients.items():

            print('\n')
            print(f'{"-"*20} {stage.capitalize()} {"-"*20}')
            # Print stage-specific info, if any
            if "info" in details:
                for key, value in details["info"].items():
                    print(f'{key.capitalize()}: {value}')

            if "ingredients" in details:
                # Handle simple ingredients list
                for ingredient in details["ingredients"]:
                    print(f'{ingredient["name"]}: {
                        ingredient["amount"] * ratio:.2f}g')

            else:
                # Handle nested time-based stages like Hop_stage
                print("Hop stage")
                for stage, details in details.items():
                    print(f"stage {stage}")
                    print(f"    info:")
                    print(f'        time: {details['info']['time']}')
                    print(f'        temperature: {
                        details['info']['temperature']}')
                    for stage_hop in details['ingredients'].keys():
                        print(stage_hop)
                        for hop in details['ingredients'][stage_hop]:
                            print(f'            {hop['name']}: {
                                  hop["amount"] * ratio: .2f}g')


# Example of usage
try:
    recipe = BeerRecipe(
        ingredients={
            "mashing": {
                "ingredients": [
                    {"name": "pale ale finest maris otter",
                     "type": "Malt", "amount": 4420.0},
                    {"name": "dextrin 13", "type": "Malt", "amount": 370.0}
                ]
            },
            "Hop_stage": {
                "Hop_grower": {
                    "info": {"time": "60 min", "temperature": 100.0},
                    "ingredients": {
                        "30 min": [
                            {"name": "Mosaic", "type": "Hop", "amount": 8.0}
                        ],
                        "10 min": [
                            {"name": "Mosaic", "type": "Hop", "amount": 8.0},
                            {"name": "Ekuanot", "type": "Hop", "amount": 8.0},
                            {"name": "Rakau", "type": "Hop", "amount": 8.0}
                        ],
                        "3 min": [
                            {"name": "Mosaic", "type": "Hop", "amount": 8.0},
                            {"name": "Ekuanot", "type": "Hop", "amount": 8.0},
                            {"name": "Rakau", "type": "Hop", "amount": 8.0}
                        ]
                    }
                },
                "Whirlpool": {
                    "info": {"time": "30 min", "temperature": 80.0},
                    "ingredients": {"10 min": [
                        {"name": "Mosaic", "type": "Hop", "amount": 8.0},
                        {"name": "Ekuanot", "type": "Hop", "amount": 8.0},
                        {"name": "Rakau", "type": "Hop", "amount": 8.0}
                    ]}
                }
            },
            "fermentation": {
                "ingredients": [
                    {"name": "Mango", "type": "Fruit", "amount": 3.0}
                ]
            }
        },
        resulting_beer_volume=23830.0,
        sparging_water_volume=5870.0,
        kettle_volume=43500.0
    )
    print("Recipe created successfully!")

    print(recipe.get_ratio())

    recipe.print_ingredients(calculate_with_ratio=True)
except (TypeError, ValueError) as e:
    print(f"Error creating recipe: {e}")
