from django.urls import reverse
from tests.BaseTestWithDB import BaseTestWithDB
from tests.resources.ResourcesTestDataGenerator import ResourcesTestDataGenerator
from utils.import_resource_module import import_resource_module
from utils.create_query_string import query_string
from utils.resource_valid_test_configurations import resource_valid_test_configurations


class TreasureHuntResourceViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = ResourcesTestDataGenerator()
        self.language = "en"

    def test_treasure_hunt_resource_form_view(self):
        resource = self.test_data.create_resource(
            "treasure-hunt",
            "Treasure Hunt",
            "resources/treasure-hunt.html",
            "treasure_hunt.py",
        )
        kwargs = {
            "resource_slug": resource.slug,
        }
        url = reverse("resources:resource", kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_treasure_hunt_resource_generation_valid_configurations(self):
        resource = self.test_data.create_resource(
            "treasure-hunt",
            "Treasure Hunt",
            "resources/treasure-hunt.html",
            "treasure_hunt.py",
        )
        kwargs = {
            "resource_slug": resource.slug,
        }
        base_url = reverse("resources:generate", kwargs=kwargs)
        resource_module = import_resource_module(resource)
        valid_options = resource_module.valid_options()
        combinations = resource_valid_test_configurations(valid_options)
        print()
        for combination in combinations:
            print("   - Testing combination: {} ... ".format(combination), end="")
            url = base_url + query_string(combination)
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)

            if combination["prefilled_values"] == "blank":
                range_text = "blank"
            else:
                range_min = 0
                if combination["prefilled_values"] == "easy":
                    range_max = 99
                elif combination["prefilled_values"] == "medium":
                    range_max = 999
                elif combination["prefilled_values"] == "hard":
                    range_max = 9999
                SUBTITLE_TEMPLATE = "{} - {} to {}"
                number_order_text = combination["number_order"].title()
                range_text = SUBTITLE_TEMPLATE.format(number_order_text, range_min, range_max)

            if combination["art"] == "colour":
                art_style_text = "full colour"
            else:
                art_style_text = "black and white"

            if combination["instructions"]:
                instructions_text = "with instructions"
            else:
                instructions_text = "without instructions"

            subtitle = "{} - {} - {} - {}".format(
                range_text,
                art_style_text,
                instructions_text,
                combination["paper_size"]
            )

            self.assertEqual(
                response.get("Content-Disposition"),
                'attachment; filename="Resource Treasure Hunt ({subtitle}).pdf"'.format(subtitle=subtitle)
            )
            print("ok")

    def test_treasure_hunt_resource_generation_missing_prefilled_values_parameter(self):
        resource = self.test_data.create_resource(
            "treasure-hunt",
            "Treasure Hunt",
            "resources/treasure-hunt.html",
            "treasure_hunt.py",
        )
        kwargs = {
            "resource_slug": resource.slug,
        }
        url = reverse("resources:generate", kwargs=kwargs)
        get_parameters = {
            "number_order": "sorted",
            "instructions": True,
            "art": "colour",
            "paper_size": "letter",
            "header_text": "",
        }
        url += query_string(get_parameters)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_treasure_hunt_resource_generation_missing_number_order_parameter(self):
        resource = self.test_data.create_resource(
            "treasure-hunt",
            "Treasure Hunt",
            "resources/treasure-hunt.html",
            "treasure_hunt.py",
        )
        kwargs = {
            "resource_slug": resource.slug,
        }
        url = reverse("resources:generate", kwargs=kwargs)
        get_parameters = {
            "prefilled_values": "hard",
            "instructions": True,
            "art": "colour",
            "paper_size": "letter",
            "header_text": "",
        }
        url += query_string(get_parameters)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_treasure_hunt_resource_generation_missing_instructions_parameter(self):
        resource = self.test_data.create_resource(
            "treasure-hunt",
            "Treasure Hunt",
            "resources/treasure-hunt.html",
            "treasure_hunt.py",
        )
        kwargs = {
            "resource_slug": resource.slug,
        }
        url = reverse("resources:generate", kwargs=kwargs)
        get_parameters = {
            "prefilled_values": "hard",
            "number_order": "sorted",
            "art": "colour",
            "paper_size": "letter",
            "header_text": "",
        }
        url += query_string(get_parameters)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_treasure_hunt_resource_generation_missing_art_parameter(self):
        resource = self.test_data.create_resource(
            "treasure-hunt",
            "Treasure Hunt",
            "resources/treasure-hunt.html",
            "treasure_hunt.py",
        )
        kwargs = {
            "resource_slug": resource.slug,
        }
        url = reverse("resources:generate", kwargs=kwargs)
        get_parameters = {
            "prefilled_values": "hard",
            "number_order": "sorted",
            "instructions": True,
            "paper_size": "letter",
            "header_text": "",
        }
        url += query_string(get_parameters)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_treasure_hunt_resource_generation_missing_paper_size_parameter(self):
        resource = self.test_data.create_resource(
            "treasure-hunt",
            "Treasure Hunt",
            "resources/treasure-hunt.html",
            "treasure_hunt.py",
        )
        kwargs = {
            "resource_slug": resource.slug,
        }
        url = reverse("resources:generate", kwargs=kwargs)
        get_parameters = {
            "prefilled_values": "hard",
            "number_order": "sorted",
            "instructions": True,
            "art": "colour",
            "header_text": "",
        }
        url += query_string(get_parameters)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_treasure_hunt_resource_generation_missing_header_text_parameter(self):
        resource = self.test_data.create_resource(
            "treasure-hunt",
            "Treasure Hunt",
            "resources/treasure-hunt.html",
            "treasure_hunt.py",
        )
        kwargs = {
            "resource_slug": resource.slug,
        }
        url = reverse("resources:generate", kwargs=kwargs)
        get_parameters = {
            "prefilled_values": "hard",
            "number_order": "sorted",
            "instructions": True,
            "art": "colour",
            "paper_size": "letter",
            "header_text": "",
        }
        url += query_string(get_parameters)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        filename = "Resource Treasure Hunt (Sorted - 0 to 9999 - full colour - with instructions - letter).pdf"
        self.assertEqual(
            response.get("Content-Disposition"),
            'attachment; filename="{}"'.format(filename)
        )