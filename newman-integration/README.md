<p align="center">
<img align = "center" img src="https://user-images.githubusercontent.com/107360829/191698510-f7588e5e-0688-412f-8395-1527b603de84.png" alt="Pynt logo 01b"/>
</p>

## Description:

Pynt is an API Security testing solution built on top of Newman - a Postman collection runner.

Do you test your cloud app with Newman? now you can easily test for common API Security issues with the Pynt docker.

You can use Pynt docker in the same way you use Newman, with Pynt you get both the functional and the security test results.

You should be able also to integrate Pynt into your CI/CD pipeline seamlessly - the same as you do with Newman.


## Prerequisites:

1. Ensure Docker engine is available and running on your machine (install from https://docs.docker.com/engine/install/).
2. Ensure your functional test collection is available in your workspace.
3. If your functional tests requires environment variables, make sure they are set.
4. Make sure your target is up.

## Important Notes:

- Please verify the above by running your functional test collection vs. your target before executing the Pynt security test.
- Pynt utilizes your functional tests to inform the security tests. \
The more extensive the functional tests are, the more the security tests will cover. 
For example, more APIs, more users, more requests and full use of the parameters will trigger broader and richer dynamic security tests.

## Getting started:

Download Pynt docker (make sure Docker is running):

```
docker pull ghcr.io/pynt-io/pynt:latest
```
  
Run docker:

```
docker run -v <full path folder>:/etc/pynt/ --rm --network="host" ghcr.io/pynt-io/pynt:latest -c <postman collection file> -e <postman environment file>
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

## Usage Example:

To test your:
- `my_collection.postman_collection.json` Postman collection file
- `my_environment.postman_environment.json` Postman environment file
- Both files located under your /Users/admin/AmazingProject/api_tests directory

You can use the following command line:
```
docker run -v /Users/admin/AmazingProject/api_tests:/etc/pynt/ --rm --network="host"  ghcr.io/pynt-io/pynt:latest -c my_collection.postman_collection.json -e my_environment.postman_environment.json
```

![pynt_run](https://user-images.githubusercontent.com/107360829/181883204-fed73a15-8c9a-4087-b28b-22f53884ed44.gif)

## EULA and Privacy Policy

Please read the [EULA](https://github.com/pynt-io/pynt/blob/main/EULA.md) and the [privacy policy](https://github.com/pynt-io/pynt/blob/main/Privacy-Policy.md) carefully before downloading or using Pynt.

## Need Support?

If you have questions or need any help, please email us at support@pynt.io.
