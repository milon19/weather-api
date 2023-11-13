# Weather API

## Installation

#### Installation

- Set up `.env` file with proper configuration. The required fields in the `.env.example`.

> See `.env.example` for better understanding with sample value

```dotenv
DEBUG=True # This is optional, Default: False
DJANGO_SECRET='' # Value given in .env.example
POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
POSTGRES_PORT=<POSTGRES_PORT>
POSTGRES_HOST=<POSTGRES_HOST>
POSTGRES_DB=<POSTGRES_DB>
POSTGRES_USER=<POSTGRES_USER>
```

- Go to project root where `manage.py` file is located.
- Create a virtual environment.

```shell
virtualenv <name>
```

- Active the environment.

```shell
source ./<name>/bin/activate
```

- Install `requirements.txt`

```shell
pip install -r requirements.txt
```

- Setup the `.env` with the above configuration.
- Now open a terminal and run the migration command to migrate db. (You need to create a db first.)
- ```shell
  python manage.py migrate
  ```
- Now, run the project with a flowing command.
- ```shell
   python manage.py runserver
  ```

Your project should be running.

> NOTE: This installation is only used for development.

# APIs

## Next 7 days Forcast for 10 coolest districts API:

API endpoint: `/api/forcast/`

Method: `GET`

Response:

```json
[
    {
        "id": "6",
        "division_id": "3",
        "name": "Kishoreganj",
        "bn_name": "কিশোরগঞ্জ",
        "lat": "24.444937",
        "long": "90.776575",
        "average_temp": 28.038928985595703
    }
    ...
]
```

## API for Given Place:

API endpoint: `/api/forcast-specific-loc/?from_loc=Kishoreganj&to_loc=Mymensingh&max_temp=29`

Method: `GET`

Query Params:

- from_loc: From location, name of district.
- to_loc: To location, name of district.
- date: Date of travel. `2023-10-11` in this formate
- max_temp: 29, A threshold value for decided whether we are going or not.

Response:

```json
[
  {
    "id": "10",
    "division_id": "8",
    "name": "Mymensingh",
    "bn_name": "ময়মনসিংহ",
    "lat": "24.7471",
    "long": "90.4203",
    "average_temp": 30.64349937438965,
    "can_visit": true
  },
  {
    "id": "6",
    "division_id": "3",
    "name": "Kishoreganj",
    "bn_name": "কিশোরগঞ্জ",
    "lat": "24.444937",
    "long": "90.776575",
    "average_temp": 30.66750144958496,
    "can_visit": true
  }
]
```
