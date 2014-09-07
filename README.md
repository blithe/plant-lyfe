# Plant Lyfe

Production: [http://plant-lyfe.herokuapp.com](http://plant-lyfe.herokuapp.com) is hosted on
[Heroku](http://www.heroku.com).

## Getting Setup

### Dependencies

* Python >= 2.7.8
* PostgreSQL >= 9.2
* Homebrew
* virtualenv

### Environment

We use Python's [os](https://docs.python.org/2/library/os.html) and a `.env` file to manage environment variables in development and test environments. We also set the same environment variables in production using [heroku
config](https://devcenter.heroku.com/articles/config-vars). See the list of required environment variables in the `.env.example` file in the root directory.

```bash
# Checkout the repo
git clone git@github.com:bignerdranch/plant-lyfe.git
cd plant-lyfe

# Use virtualenv to set up a virtual environment
virtualenv ENV
source bin/activate

# Install dependencies
pip install -r requirements.txt

# Install other dependencies
brew install postgresql

# Note: If using Postgres.app ensure that your path is set correctly
PATH="/Applications/Postgres.app/Contents/MacOS/bin:$PATH"

# Get the database ready
psql
CREATE DATABASE plant_lyfe_dev;
\q

# Setup remote branches

git remote add origin git@github.com:blithe/plant-lyfe.git
git remote add heroku git@heroku.com:plant-lyfe.git

# Start the app

foreman start

# Visit the site in your browser
open http://localhost:5000
```


### Testing

Testing is done using unittest

``python manage.py test``

## Production

The app is deployed on Heroku at http://plant-lyfe.herokuapp.com

```
$ git push heroku master
```

will deploy master to production. Afterwards, you'll need to sync the database with:

```
$ python manage.py syncdb
```

and then restart the app with ``heroku restart``.


## API Specifications

### Resources Types:

  Plant - General plant information
    Example JSON representation:

      {
        "id": "plant-12345",
        "common_name": "bigleaf maple",
        "subclass": "Rosidae",
        "order": "Sapindales",
        "family": "Aceraceae",
        "genus": "Acer L.",
        "species": "Acer macrophyllum Pursh",
        "leaves": [ 
          "/dicots/bigleaf-maple/leaf/110",
          "/dicots/bigleaf-maple/leaf/111"
        ]
      }

  Leaf  - Description of actual leaf specimen associated with a Plant
    Example JSON representation:

      {
        "id": "leaf-110",
        "plant": "plant-12345",
        "placement": "opposite",
        "blade": "palmately compound",
        "veins": "penniveined",
        "location": "Vancouver, BC",
        "date_found": "2014-01-01"
      }

### Supported Functionality:
  Creating a Plant resource
  Creating a Leaf resource subordinate to a Plant resource
  Deleting a Leaf resource
  Deleting a Plant resource (should delete linked Leaf resources)
  Updating a Plant or Leaf resource
  Retrieving a representation of a Plant or Leaf resource
  Searching for Leaf resources based on taxonomic criteria

### Specific API Calls:

  URL: /dicots
  Accepted HTTP methods:
    GET - Should return a list of all Plant resources.
      Example Request:

        GET /dicots HTTP/1.1
        Host: subdomain.example.com:80
        Accept: */*
      
      Example Response:

        {
          "plants": [
            {
              "id": "plant-12345",
              "common_name": "bigleaf maple",
              "species": "Acer macrophyllum Pursh",
              "leaves": [
                "/dicots/bigleaf-maple/leaf/110",
                "/dicots/bigleaf-maple/leaf/111"
              ]
            },
            {
              "id": "plant-12346",
              "common_name": "big green thing"
              "species": "latinus nameus",
              "leaves": [
                "/dicots/big-green-thing/leaf/144",
                "/dicots/big-green-thing/leaf/201",
                "/dicots/big-green-thing/leaf/206"
              ]
            }
          ]
        }

  URL: /dicots/{plant-name}
  Accepted HTTP methods:
    GET - Should return a representation of the Plant, including a list of linked Leaf resources
      Example Request:

        GET /dicots/bigleaf-maple

      Example Response:

        {
          "id": "plant-12345",
          "common_name": "bigleaf maple",
          "subclass": "Rosidae",
          "order": "Sapindales",
          "family": "Aceraceae",
          "genus": "Acer L.",
          "species": "Acer macrophyllum Pursh",
          "leaves": [
            "/dicots/bigleaf-maple/leaf/110",
            "/dicots/bigleaf-maple/leaf/111"
          ]
        }

    PUT - Should create a Plant resource
      Example Request:

        PUT /dicots/mahogany HTTP/1.1

        {
          "common_name": "mahogany",
          "subclass": "Rosidae",
          "order": "Sapindales",
          "family": "Meliaceae",
          "genus": "Swietenia",
          "species": "Sweitenia mahagoni"
        }

      Example Response:

        HTTP/1.1 201 Created
        Date: Wed, 3 Sep 2014 18:01:01 GMT
        Content-Length: 1234
        Content-Type: application/json
        Location: http://example.org/dicots/mahogany

        {
          "id": "plant-14423",
          "common_name": "mahogany",
          "subclass": "Rosidae",
          "order": "Sapindales",
          "family": "Meliaceae",
          "genus": "Swietenia",
          "species": "Sweitenia mahagoni"
        } 

    DELETE - Should delete the Plant resource and subordinate Leaf resources
      Example Request:

        DELETE /dicots/mahogany HTTP/1.1

      Example Response:

        HTTP/1.1 204 No Content

    POST - Either:
      a) Update the Plant resource OR
        Example Request:

          POST /dicots/mahogany HTTP/1.1

          {
            "common_name": "mahogany",
            "subclass": "I dunno",
            "order": "something else",
            "family": "Whee!",
            "genus": "Swietenia",
            "species": "Sweitenia mahagoni"
          } 

        Example Response:
          
          HTTP/1.1 200 OK
          Date: Wed, 3 Sep 2014 18:01:01 GMT
          Content-Length: 1234
          Content-Type: application/json
          Location: http://example.org/dicots/mahogany

          {
            "id": "plant-14423",
            "common_name": "mahogany",
            "subclass": "I dunno",
            "order": "something else",
            "family": "Whee!",
            "genus": "Swietenia",
            "species": "Sweitenia mahagoni"
          } 

      b) Create a Leaf resource subordinate to the Plant resource
        Example Request:

          POST /dicots/mahogany HTTP/1.1

          {
            "placement": "opposite",
            "blade": "palmately compound",
            "veins": "penniveined",
            "location": "Vancouver, BC",
            "date_found": "2014-01-01"
          }

        Example Response:

          HTTP/1.1 201 Created
          Date: Wed, 3 Sep 2014 18:01:01 GMT
          Content-Length: 1234
          Content-Type: application/json
          Location: http://example.org/dicots/mahogany/leaf/307

          {
            "id": "leaf-307",
            "plant": "plant-14423",
            "placement": "opposite",
            "blade": "palmately compound",
            "veins": "penniveined",
            "location": "Vancouver, BC",
            "date_found": "2014-01-01"
          }

  URL: /dicots/{plant-name}/leaf/{leaf-id}
  Accepted HTTP methods (examples omitted, see above for similar):
    GET - Should return a representation of the Leaf
    DELETE - Should delete the Leaf resource
    POST - Should update the Leaf resource

  URL: /dicots/leaf/search
  Accepted HTTP methods:
    GET - Should return a list of Leaf resources matching the submitted criteria
      Example Request:

        GET /dicots/leaf/search?placement=opposite&blade=plamately%20compound HTTP/1.1

      Example Response:

        HTTP/1.1 200 OK
        Date: Wed, 3 Sep 2014 18:01:01 GMT
        Content-Length: 1234
        Content-Type: application/json
        Location: http://example.com/dicots/leaf/search?placement=opposite&blade=plamately%20compound

        {
          "leaves": [
            {
              "id": "leaf-307",
              "plant": "plant-14423"
            },
            {
              "id": "leaf-110",
              "plant": "plant-12345"
            }
          ]
        }
