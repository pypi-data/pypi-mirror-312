import unittest
from karolis_s_mod1_atsiskaitymas.main import *

class TestGintarineCrawl(unittest.TestCase):

    def test_crawl_gintarine(self):
        products = crawl_gintarine()

        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 0, "Produktų sąrašas yra tuščias.")

        first_product = products[0]
        self.assertIn("title",first_product)
        self.assertIn("price",first_product)
        self.assertIsInstance(first_product["title"], str)
        self.assertIsInstance(first_product["price"], str)

    def test_save_as_csv(self):

        test_data = [
            {"title": "Produktas 1", "price": "10.99 €"},
            {"title": "Produktas 2", "price": "15.49 €"}
        ]
        filename = "test_output.csv"

        result_filename = save_as_csv(test_data, filename)

        self.assertEqual(result_filename, filename)

        with open(filename, "r") as f:
            lines = f.readlines()

        self.assertEqual(lines[0].strip(), "title,price")
        self.assertIn("Produktas 1", lines[1])
        self.assertIn("Produktas 2", lines[2])

if __name__ == "__main__":
    unittest.main()