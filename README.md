# Pynt

## Description:
Pynt is an API Security testing solution built on top of Newman - a postman collection runner.

Do you test your cloud app with Newman ? now you can easily test for common API Security issues with the Pynt docker.

You can use Pynt docker in the same way you use Newman, with Pynt you get both the functional and the security tests results.

## Requirements:
- Docker (you can install from https://www.docker.com/products/docker-desktop/)

## Getting started:

Download Pynt docker (Make sure Docker is running):

```
docker pull ghcr.io/overcast-security/pynt:latest
```
  
Run docker:

```
docker run -v <full path folder>:/etc/pynt/ --rm --network="host" ghcr.io/overcast-security/pynt:latest -c <postman collection file> -e <postman environment file>
```

## Command line options:

Postman collection file - required:
```
-c <postman collection file>
```

Postman environment file - optional:
```
-e <postman environment file>
```

## Example:

To test your:
- `my_collection.postman_collection.json` Postman collection file
- `my_environment.postman_environment.json` Postman environment file
- Both files located under your /Users/admin/AmazingProject/api_tests directory

You can use the following command line:
```
docker run -v /Users/admin/AmazingProject/api_tests:/etc/pynt/ --rm --network="host"  ghcr.io/overcast-security/pynt:latest -c my_collection.postman_collection.json -e my_environment.postman_environment.json
```

## EULA:
Beta version - use this for educational purposes only
