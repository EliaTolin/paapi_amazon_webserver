<br/>
<p align="center">
  <a href="https://github.com/EliaTolin/paapi_amazon_webserver">
    <img src="https://user-images.githubusercontent.com/60351315/197619270-95b9dd60-6e73-4191-a309-a54104b60d86.png" alt="Logo" width="720">
  </a>

  <h3 align="center">PAAPI Amazon Webserver</h3>

  <p align="center">
    Implementing the Amazon PA API using Flask as a webserver and Redis for caching offers.
    <br/>
    <br/>
    <br/>
    <br/>
    <a href="https://github.com/EliaTolin/paapi_amazon_webserver/issues">Report Bug</a>
    .
    <a href="https://github.com/EliaTolin/paapi_amazon_webserver/issues">Request Feature</a>
  </p>
</p>

![Contributors](https://img.shields.io/github/contributors/EliaTolin/paapi_amazon_webserver?color=dark-green) ![Forks](https://img.shields.io/github/forks/EliaTolin/paapi_amazon_webserver?style=social) ![Stargazers](https://img.shields.io/github/stars/EliaTolin/paapi_amazon_webserver?style=social) ![Issues](https://img.shields.io/github/issues/EliaTolin/paapi_amazon_webserver) ![License](https://img.shields.io/github/license/EliaTolin/paapi_amazon_webserver) 

## About The Project

PAAPI Amazon Webserver is a webserver that simplifies operations through api pa.

 It allows the caching of offers of the requested categories, for a configurable time, saved in a Redis database.
It is possible to use this server as a backend for applications or web pages where offers are displayed.

PAAPI Amazon Server has the automatisms you are looking for for offers and limit the consumption of API requests.

## Built With

The server use Redis for the cache and Flask as the web server.
Use a wrapper for pa api.

* [PAAPI Amazon Python wrapper](https://github.com/sergioteula/python-amazon-paapi)

## Getting Started

It is recommended to use a virtualenv.
A Docker is provided that allows the use of Redis, if you want you can use your own Redis database.

### Installation

1. Get AP Amazon credentials.
2. Clone the repo

```shell
git clone https://github.com/EliaTolin/paapi_amazon_webserver/
```

3. Install dependencies

```shell
pip install -r requirements.txt
```

4. Enter your API Credentials in `config.py`

```py
AMAZON_ACCESS_KEY = 'YOUR_ACCESS_KEY'
AMAZON_SECRET_KEY = 'YOUR_SECRET_KEY'
AMAZON_PARTNER_ID = 'YOUR_PARTNER_ID'
AMAZON_COUNTRY = 'YOUR_COUNTRY_ID'
```

4. Start webserver.

```shell
python main.py
```

Be sure you have a redis instance.

Otherwise use the Docker-compose for development but before configure the config.py file.

```shell
docker-compose up -d
```


## Usage

The webserver provides two endpoints, others will be in development if requested.
- **/api/v1/pa_amazon/search_product**

	Use this to have products returned to you based on the parameters provided.


- **/api/v1/pa_amazon/get_category_offers**

	Use this to make you return the products on offer or not regarding a certain category, it saves it in the DB with a timeout, if it is requested 	again it provides the results saved in the cache without re-downloading them. It has systems to handle the TooManyRequest error.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GPL-3.0 License. See [LICENSE](https://github.com/EliaTolin/paapi_amazon_webserver/blob/master/LICENSE) for more information.

## Authors

* **Elia Tolin** - *Founder of Aurora Digital* - [Elia Tolin](https://github.com/EliaTolin/) -
