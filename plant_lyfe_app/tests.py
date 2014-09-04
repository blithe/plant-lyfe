from django.test import TestCase
from plant_lyfe_app.models import Plant

class PlantTestCase(TestCase):
    def setUp(self):
        Plant.objects.create(common_name="bigleaf maple",
                             subclass="Rosidae",
                             order="Sapindales",
                             family="Aceraceae",
                             genus="Acer L.",
                             species="Acer macrophyllum Pursh",
                             )

    def test_plants_have_subclasses(self):
        """Plants have all the correct attributes"""
        maple = Plant.objects.get(common_name="bigleaf maple")
        self.assertEqual(maple.subclass, 'Rosidae')
        self.assertEqual(maple.order, 'Sapindales')
        self.assertEqual(maple.family, 'Aceraceae')
        self.assertEqual(maple.genus, 'Acer L.')
        self.assertEqual(maple.species, 'Acer macrophyllum Pursh')
