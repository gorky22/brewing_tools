import unittest
from modules.brewing_tools import BeerRecipe

# % python -m unittest discover tests


class TestBeerRecipe(unittest.TestCase):
    def test_valid_initialization(self):
        recipe = BeerRecipe(
            ingredients=[{"name": "Malt", "amount": "2kg"},
                         {"name": "Hops", "amount": "50g"}],
            resulting_beer_volume=20.0,
            sparging_water_volume=10.0,
            desired_resulting_beer_volume=20.0
        )
        self.assertEqual(recipe.resulting_beer_volume, 20.0)

    def test_invalid_ingredients_type(self):
        with self.assertRaises(TypeError):
            BeerRecipe("not_a_list", 20.0, 10.0, 20.0)

    def test_negative_volume(self):
        with self.assertRaises(ValueError):
            BeerRecipe([{"name": "Malt"}], -5.0, 10.0, 20.0)

    def test_get_ratio_negative_inputs(self):
        recipe = BeerRecipe([{"name": "Malt"}], 25.0, 10.0, 40.0)

        self.assertEqual(recipe.get_ratio(
            10.0, -20.0) - 40.0 / 25.0 <= 0.01, True)

        self.assertEqual(recipe.get_ratio(-10.0, 20.0) -
                         40.0 / 25.0 <= 0.01, True)

    def test_get_ratio_no_input_params(self):
        recipe = BeerRecipe([{"name": "Malt"}], 25.0, 10.0, 40.0)

        self.assertEqual(recipe.get_ratio() - 40 / 25 <= 0.01, True)

    def test_get_ratio_invalid_types(self):
        recipe = BeerRecipe([{"name": "Malt"}], 25.0, 10.0, 40.0)

        with self.assertRaises(TypeError):
            recipe.get_ratio('aa')

        with self.assertRaises(TypeError):
            recipe.get_ratio(1.0, 'aa')


# Run the tests
if __name__ == "__main__":
    unittest.main()
