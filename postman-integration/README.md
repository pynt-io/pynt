![pynt-logo](https://user-images.githubusercontent.com/107360829/176185125-b2b9fce3-c9fc-4048-baa5-e5a21af5c31b.png)

## Description:

Pynt is an API security solution which generates automated security tests based on your existing functional test collection.

Pynt dynamic security test covers the OWASP-10 top API categories and retrieves the results in few minutes.


## Prerequisites:

1. Ensure you are working with Postman app (install from https://www.postman.com/downloads). 
Note that Pynt solution is based on docker, so it doesn't work with Postman for web, only with the desktop app.
2. Ensure Docker desktop is available and running on your machine (install Docker from
https://www.docker.com/products/docker-desktop/).
3. Enable The 'Expose daemon on tcp://localhost:2375 without TLS' option in the General section of your Docker desktop settings.
![image](https://user-images.githubusercontent.com/107360829/184631176-f68bffaa-5f78-4f30-8368-8694acba6862.png)
4. Ensure your functional test collection is available in your workspace.
5. If your functional tests requires environment variables, make sure they are set.
6. Make sure your target is up.


## Important Notes:

- Please verify the above by running your functional test collection vs. your target before executing the Pynt security test.
- Pynt utilizes your functional tests to inform the security tests. \
The more extensive the functional tests are, the more the security tests will cover. 
For example, more APIs, more users, more requests and full use of the parameters will trigger broader and richer dynamic security tests.

## Getting started:

- Download by right click->'save link as'
<a id='raw-url' href="https://raw.githubusercontent.com/pynt-io/pynt/main/postman-integration/Pynt%20For%20Windows.postman_collection.json" download="Pynt%20For%20Windows.postman_collection.json" Download="https://raw.githubusercontent.com/pynt-io/pynt/main/postman-integration/Pynt%20For%20Windows.postman_collection.json" download="Pynt%20For%20Windows.postman_collection.json">'Pynt for Windows' collection</a>

- Import the collection into your Workspace in Postman app
- Follow the steps described below (You can also view the run instractions in Postman as part of the 'Pynt for Windows'collection documentation).

## How to Run:
 
1. Click on the 'Variables' tab of the 'Pynt for Windows' collection and fill the values of required parameters:
- API-KEY - your postman API key - If you previously saved and have your API key, enter it here under the 'Current Value' tab. If not, enter       https://postman.co/settings/me/api-keys to generate or regenarete your API key as it can be copied only when created for security reasons. You won't need to modify     this parameter till your API-key will expire.
- COLLECTION-NAME - your functional test collection name, e.g. 'Test Collection 1'. Pynt will refer to this collection to generate the automated security tests.
- port - Pynt will use this port. Change to other than 5001 if this port already in use.
2. Run the 'Pynt for Windows' collection. A new forked collection of your chosen collection will be created with the label of API-Security.
3. Run the new security collection to get the security results!
4. In case you modified your functional test collection or you wish to refer to another test collection, go back to step 1b.


## EULA and Privacy Policy

Please read the [EULA](https://github.com/pynt-io/pynt/blob/main/EULA.md) and the [privacy policy](https://github.com/pynt-io/pynt/blob/main/Privacy-Policy.md) carefully before downloading or using Pynt.

## Need Support?

If you have questions or need any help, please email us at support@pynt.io.
