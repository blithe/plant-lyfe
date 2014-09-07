from django.test import TestCase
from plant_lyfe_app.models import Plant, Leaf

from rest_framework import status
from rest_framework.test import APITestCase
import json

class ApiTestCase(APITestCase):
    def test_get_dicots_returns_plant_list(self):
      """URL: /dicots GET - Should return a list of all Plant resources."""
      self.maxDiff=None
      plant1 = Plant.objects.create(common_name="bigleaf maple",
                             subclass="Rosidae",
                             order="Sapindales",
                             family="Aceraceae",
                             genus="Acer L.",
                             species="Acer macrophyllum Pursh",
                             )
      plant2 = Plant.objects.create(common_name="big green thing",
                           subclass="Rosidae",
                           species="latinus nameus",
                           )
      leaf1 = Leaf.objects.create(plant=plant1, date_found="2014-01-01")
      leaf2 = Leaf.objects.create(plant=plant1, date_found="2014-01-01")
      leaf3 = Leaf.objects.create(plant=plant2, date_found="2014-01-01")
      leaf4 = Leaf.objects.create(plant=plant2, date_found="2014-01-01")
      leaf5 = Leaf.objects.create(plant=plant2, date_found="2014-01-01")

      response = self.client.get('/dicots')
      expected_data = {
          "plants": [
            {
              "id": "plant-%i" % (plant1.id),
              "common_name": plant1.common_name,
              "species": plant1.species,
              "leaves": [
                "/dicots/%s/leaf/%i" % (plant1.slug, leaf2.id),
                "/dicots/%s/leaf/%i" % (plant1.slug, leaf1.id)
              ]
            },
            {
              "id": "plant-%i" % (plant2.id),
              "common_name": plant2.common_name,
              "species": plant2.species,
              "leaves": [
                "/dicots/%s/leaf/%i" % (plant2.slug, leaf5.id),
                "/dicots/%s/leaf/%i" % (plant2.slug, leaf4.id),
                "/dicots/%s/leaf/%i" % (plant2.slug, leaf3.id)
              ]
            }
          ]
        }
      self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_get_dicot_name_returns_plant_details(self):
      """URL: /dicots/bigleaf-maple GET-Should return a representation of the Plant, including a list of linked Leaf resources"""
      plant = Plant.objects.create(common_name="bigleaf maple",
                             subclass="Rosidae",
                             order="Sapindales",
                             family="Aceraceae",
                             genus="Acer L.",
                             species="Acer macrophyllum Pursh",
                             )
      leaf1 = Leaf.objects.create(plant=plant, date_found="2014-01-01")
      leaf2 = Leaf.objects.create(plant=plant, date_found="2014-01-01")
      expected_data = {
          "id": "plant-%i" % (plant.id),
          "common_name": plant.common_name,
          "subclass": plant.subclass,
          "order": plant.order,
          "family": plant.family,
          "genus": plant.genus,
          "species": plant.species,
          "leaves": [
            "/dicots/%s/leaf/%i" % (plant.slug, leaf2.id),
            "/dicots/%s/leaf/%i" % (plant.slug, leaf1.id)
          ]
        }

      response = self.client.get('/dicots/bigleaf-maple')
      self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_put_dicot_name_creates_plant(self):
      """PUT /dicots/mahogany - Should create a Plant resource"""
      request_data = {
                "common_name": "mahogany",
                "subclass": "Rosidae",
                "order": "Sapindales",
                "family": "Meliaceae",
                "genus": "Swietenia",
                "species": "Sweitenia mahagoni"
              }
      response = self.client.put('/dicots/mahogany', request_data, format='json')
      created_plant = Plant.objects.latest('id')
      expected_data = {
          "id": "plant-%i" % (created_plant.id),
          "common_name": created_plant.common_name,
          "subclass": created_plant.subclass,
          "order": created_plant.order,
          "family": created_plant.family,
          "genus": created_plant.genus,
          "species": created_plant.species,
          "leaves": []
        }
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertJSONEqual(response.content, json.dumps(expected_data))


    def test_delete_dicot_name_deletes_plant(self):
      """DELETE /dicots/mahogany - Should delete a Plant resource"""
      Plant.objects.create(common_name="mahogany plant",
                           species="Acer macrophyllum Pursh",
                           )
      response = self.client.delete('/dicots/mahogany-plant')
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_dicot_name_updates_plant(self):
      """POST /dicots/mahogany - Should update a Plant resource"""
      plant = Plant.objects.create(common_name="mahogany",
                                   subclass="Rosidae",
                                   order="Sapindales",
                                   family="Aceraceae",
                                   genus="Acer L.",
                                   species="Acer macrophyllum Pursh",
                                   )
      request_data = {
                "common_name": "mahogany",
                "subclass": "I dunno",
                "order": "something else",
                "family": "Whee!",
                "genus": "Swietenia",
                "species": "Sweitenia mahagoni"
              }
      expected_data = {
          "id": "plant-%i" % (plant.id),
          "common_name": "mahogany",
          "subclass": "I dunno",
          "order": "something else",
          "family": "Whee!",
          "genus": "Swietenia",
          "species": "Sweitenia mahagoni",
          "leaves": []
        }

      response = self.client.post('/dicots/mahogany', request_data, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertJSONEqual(response.content, json.dumps(expected_data))


    def test_post_dicot_name_creates_leaf(self):
      """POST /dicots/mahogany - Should Create a Leaf resource subordinate to the Plant resource"""
      plant = Plant.objects.create(common_name="mahogany",
                                   subclass="Rosidae",
                                   order="Sapindales",
                                   family="Aceraceae",
                                   genus="Acer L.",
                                   species="Acer macrophyllum Pursh",
                                   )
      request_data = {
                "placement": "opposite",
                "blade": "palmately compound",
                "veins": "penniveined",
                "location": "Vancouver, BC",
                "date_found": "2014-01-01"
              }
      response = self.client.post('/dicots/mahogany', request_data, format='json')
      created_leaf = Leaf.objects.latest('id')
      expected_data = {
          "id": "leaf-%i" % (created_leaf.id),
          "plant": "plant-%i" % (plant.id),
          "placement": "opposite",
          "blade": "palmately compound",
          "veins": "penniveined",
          "location": "Vancouver, BC",
          "date_found": "2014-01-01"
        }

      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_get_leaf_name_returns_leaf_details(self):
      """URL: /dicots/bigleaf-maple/leaf/110 GET-Should return a representation of the Leaf"""
      plant = Plant.objects.create(common_name="bigleaf maple",
                             subclass="Rosidae",
                             order="Sapindales",
                             family="Aceraceae",
                             genus="Acer L.",
                             species="Acer macrophyllum Pursh",
                             )
      leaf = Leaf.objects.create(plant=plant,
                                 placement="opposite",
                                 blade="palmately compound",
                                 veins="penniveined",
                                 location="Vancouver, BC",
                                 date_found="2014-01-01"
                                )
      expected_data = {
          "id": "leaf-%i" % (leaf.id),
          "plant": "plant-%i" % (plant.id),
          "placement": "opposite",
          "blade": "palmately compound",
          "veins": "penniveined",
          "location": "Vancouver, BC",
          "date_found": "2014-01-01"
        }

      response = self.client.get("/dicots/bigleaf-maple/leaf/%i" % (leaf.id))
      self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_delete_leaf_name_deletes_leaf(self):
      """URL: /dicots/bigleaf-maple/leaf/110 DELETE - Should delete the Leaf resource"""
      plant = Plant.objects.create(common_name="bigleaf maple",
                             subclass="Rosidae",
                             order="Sapindales",
                             family="Aceraceae",
                             genus="Acer L.",
                             species="Acer macrophyllum Pursh",
                             )
      leaf = Leaf.objects.create(plant=plant,
                                 placement="opposite",
                                 blade="palmately compound",
                                 veins="penniveined",
                                 location="Vancouver, BC",
                                 date_found="2014-01-01"
                                )

      response = self.client.delete("/dicots/bigleaf-maple/leaf/%i" % (leaf.id))
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_leaf_updates_leaf(self):
      """POST /dicots/mahogany/leaf/110 - POST - Should update the Leaf resource"""
      plant = Plant.objects.create(common_name="mahogany",
                             subclass="Rosidae",
                             order="Sapindales",
                             family="Aceraceae",
                             genus="Acer L.",
                             species="Acer macrophyllum Pursh",
                             )
      leaf = Leaf.objects.create(plant=plant,
                                 placement="opposite",
                                 blade="palmately compound",
                                 veins="penniveined",
                                 location="Vancouver, BC",
                                 date_found="2014-01-01"
                                )
      request_data = {
                "placement": "other side",
                "blade": "not sure",
                "veins": "ALL the veins",
                "location": "Oakland, CA",
                "date_found": "2010-10-10"
              }
      expected_data = {
          "id": "leaf-%i" % (leaf.id),
          "plant": "plant-%i" % (plant.id),
          "placement": "other side",
          "blade": "not sure",
          "veins": "ALL the veins",
          "location": "Oakland, CA",
          "date_found": "2010-10-10"
        }

      response = self.client.post("/dicots/mahogany/leaf/%i" % (leaf.id), request_data, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_get_leaf_search_returns_leaf_list(self):
      """URL: GET /dicots/leaf/search?placement=opposite&blade=plamately%20compound GET - Should return a list of Leaf resources matching the submitted criteria"""
      self.maxDiff=None
      plant1 = Plant.objects.create(common_name="bigleaf maple",
                             subclass="Rosidae",
                             order="Sapindales",
                             family="Aceraceae",
                             genus="Acer L.",
                             species="Acer macrophyllum Pursh",
                             )
      plant2 = Plant.objects.create(common_name="big green thing",
                           subclass="Rosidae",
                           species="latinus nameus",
                           )
      leaf1 = Leaf.objects.create(plant=plant1, placement="opposite", blade="palmately compound", date_found="2014-01-01")
      leaf2 = Leaf.objects.create(plant=plant1, placement="opposite", blade="other", date_found="2014-01-01")
      leaf3 = Leaf.objects.create(plant=plant2, placement="opposite", blade="palmately compound", date_found="2014-01-01")
      leaf4 = Leaf.objects.create(plant=plant2, placement="other", blade="something else", date_found="2014-01-01")
      leaf5 = Leaf.objects.create(plant=plant2, placement="I dunno", blade="that one kind", date_found="2014-01-01")

      response = self.client.get('/dicots/leaf/search?placement=opposite&blade=palmately%20compound')
      expected_data = {
          "leaves": [
            {
              "id": "leaf-%i" % (leaf1.id),
              "plant": "plant-%i" % (plant1.id)
            },
            {
              "id": "leaf-%i" % (leaf3.id),
              "plant": "plant-%i" % (plant2.id)
            }
          ]
        }
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertJSONEqual(response.content, json.dumps(expected_data))
