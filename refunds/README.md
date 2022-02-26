# *Viajando Anuncia* Channel's Data Collector

## Retrieve and filter travel's refunds

## Pre-requisites

In order to use this script you must have installed Python 3.8 or greater

## Clone repository

````text
git clone path/to/url/project
````

## Configuration

### Create a virtual enviroment

````text
python3 -m venv venv
````

### Activate it

````text
source venv/bin/activate
````

### Install requirements

````text
pip install -r refunds/requirements/base.txt
````

### Usage

Before running the script you will need a Telegram API id and hash to sign in. Follow the instructions given [here](https://docs.telethon.dev/en/stable/basic/signing-in.html)

Then create a `.env` file in `refunds` folder following the variables as the `env_example` file:

````.env
APP_API_ID=your_api_id
APP_API_HASH=your_api_hash
````

Also you need to be joined to this [channel](https://t.me/apkviajandoinfo)

Now, you can run the script:

````text
python refunds/datacollector.py
````

````sh
python refunds/datacollector.py -origin "La Habana" -destination Matanzas -day_of_week vie
````

## Use case

You may want use the script to get notified when a specific travel origin and destination are founded
