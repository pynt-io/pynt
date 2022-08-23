![pynt-logo](https://user-images.githubusercontent.com/107360829/176185125-b2b9fce3-c9fc-4048-baa5-e5a21af5c31b.png)

## Description:

Pynt is an API security solution which generates automated security tests based on your existing functional test collection.
Pynt dynamic security test covers the OWASP-10 top API categories and retrieves the results in few minutes.


## Prerequisites:

1. Ensure you are working with Postman app (install from https://www.postman.com/downloads). 
Note that Pynt solution is based on docker and requires access to local host, so it doesn't support the Postman web.
2. Ensure Docker desktop is available and running on your machine (for Windows, install Docker from
https://www.docker.com/products/docker-desktop/).
3. Ensure your functional test collection is available in your workspace.
4. If your functional tests requires environment variables, make sure they are set.
5. Make sure your target is up.


## Important Notes:

- Please verify the above by running your functional test collection vs. your target before executing the Pynt security test.
- Pynt utilizes your functional tests to inform the security tests. \
The more extensive the functional tests are, the more the security tests will cover. 
For example, more APIs, more users, more requests and full use of the parameters will trigger broader and richer dynamic security tests.

## Getting started:

Fork 'Pynt' collection to you workspace:
1. Enter https://www.postman.com/pynt-io/workspace/pynt
2. From 'Pynt' collection menu, choose 'Create a fork' to fork 'Pynt' collection to your Workspace.
![image](https://user-images.githubusercontent.com/107360829/185942430-3a06263b-6ddc-4748-89e6-01444d3fa7fb.png)
3. Open your workspace from Postman desktop app.
4. Download and run Pynt docker by executing the following command via cmd 

Windows cmd or Mac terminal:
```
docker run -p 5001:5001 -d --pull always ghcr.io/pynt-io/pynt:postman-latest
```
(the left port can be changed if already taken on your machine)

Linux terminal:
```
docker run -d --pull always --network=host ghcr.io/pynt-io/pynt:postman-latest
```

This step should be repeated if you restarted your PC.

## How to Run:

To run Pynt from your workspace, continue from the instructions in Pynt's collection description (also available below).
![image](https://user-images.githubusercontent.com/107360829/186156656-dcc00c94-cc79-40ad-8b47-fc47d952ab9d.png)

1. Click on the 'Variables' tab of the 'Pynt' collection and fill the values of required parameters:
- API-KEY - your postman API key - If you previously saved and have your API key, enter it here under the 'Current Value' tab. If not, enter       https://postman.co/settings/me/api-keys to generate or regenarete your API key as it can be copied only when created for security reasons. You won't need to modify     this parameter till your API-key will expire.
![image](https://user-images.githubusercontent.com/107360829/184632643-ba29d4d6-b4f6-4d8b-a025-bf42b5662639.png)
- port - the left port number used in the docker run command (default-5001).
- COLLECTION-NAME - your functional test collection name, e.g. 'Test Collection 1'. Pynt will refer to this collection to generate the automated security tests.
![image](https://user-images.githubusercontent.com/107360829/185961165-76d9a2a2-e695-4d72-ac80-f98b41bad7ce.png)
2. Run the 'Pynt' collection. A new forked collection of your chosen collection will be created with the label of API-Security.
![image](https://user-images.githubusercontent.com/107360829/185963531-1751f616-0cc9-427a-9df5-b413cf5f343f.png)
3. Run the new security collection to get the security results:

a. The security results for OWASP-10 categories will appear on the main console screen.
![image](https://user-images.githubusercontent.com/107360829/186161712-0a121843-55f4-4e29-83ee-0083f02bfba8.png)
b. For a failed test, click on the category, and then 'Response Body' to view the detailed result.
![image](https://user-images.githubusercontent.com/107360829/186162606-1374285c-ff23-4251-b07c-5afdcae22616.png)
c. Click on 'View Summary' to view the results summary.
![image](https://user-images.githubusercontent.com/107360829/186162151-36c79cbe-fc71-4c9b-8ae5-bffb0ec417a5.png)
4. In case you modified your functional test collection or you wish to refer to another test collection, go back to step 1.

## EULA and Privacy Policy

Please read the [EULA](https://github.com/pynt-io/pynt/blob/main/EULA.md) and the [privacy policy](https://github.com/pynt-io/pynt/blob/main/Privacy-Policy.md) carefully before downloading or using Pynt.

## Need Support?

If you have questions or need any help, please email us at support@pynt.io.
