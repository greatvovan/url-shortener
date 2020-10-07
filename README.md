# URL Shortener Service

A simple HTTP API that can be used for URL shortening (no UI).

The service uses [Tarantool](https://www.tarantool.io/) database as the primary storage and a small in-process TTL cache.

## Installation

1. Clone the repository:  
`$ git clone https://github.com/greatvovan/url-shortener`  

1. Launch the services.  
`$ cd url-shortener`  
`$ docker-compose up -d --build`  

1. Initialize the storage (first time only).  
The service uses pre-generated space of keys, that work as path in short URLs.
You need to decide the length of keys you want to use. The service uses 64 characters as alphabet base,
so the number of keys is specified by the formula:  
_N = 64^length_  
As the generation takes time, consider small numbers for the beginning (e.g. 3):  
`$ docker-compose exec storage console`  
`unix/:/var/run/tarantool/tarantool.sock> init_storage(3)`

1. Run tests (first time only):  
`docker-compose exec httpapi pytest`

1. Run the benchmark (first time only):  
`$ docker-compose exec httpapi python benchmark.py`  
`1049 shortenings done in 1.5 (684/s)`  
`1049 redirects done in 1.5 (721/s)`

1. When you are down with playing, you can shut down everything by:  
`$ docker-compose down`  
`docker-compose` will create a volume named `urlstorage` to persist the data,
so next time you launch `docker-compose up` in the same directory and all urls will be in place.
If you want to delete the volume (and the data) say  
`$ docker volume rm urlstorage`  
(you may need to remove containers for that) or use `-v` option of `docker-compose down`.

## Endpoints

### `/`

Store a URL and get a short redirection link or key.
 
**HTTP request**

`POST /`

**Query parameters**
- `rawkey`: return only key (defaults to `false`). Otherwise return a full URL formatted according to `LINK_TEMPLATE`.
- `days`: number of days to store the URL (see the note below).

**Body**

Long URL as a string encoded in UTF-8.

**Response codes**
- `200`: the URL was stored and a key returned.
- `400`: Too long URL (see `URL_MAX_LENGTH`).
- `500`: unexpected error occured. 


**Response body**

A short key for the submitted URL, or a link formatted according to `LINK_TEMPLATE`.

### `/{key}`

Get redirection to the original URL for a previously returned key.

**HTTP request**

`GET /{key}`

**Query parameters**

The method has no query parameters.

**Response codes**
- `308`: the key was found and redirection location returned.
- `404`: the key was not found.

## Notes

- This service does not perform any validation of a URL being stored (neither format, nor link availability).
If such validation is necessary, it should be performed on the client side.

- The service is not protected from abuse (storing overwhelming amount of meaningless long URLs).
Such protection should be considered and put as a filter in front of this API.

- Expiration date is set for a key, but expiration/recycling job is not implemented.
