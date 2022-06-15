# Pynt

# Description:
Pynt is an API Security testing solution built on top of Newman - a postman collection runner.

Do you test your cloud app with Newman ? now you can easily test for common API Security issues with the Pynt docker.

You can use Pynt docker in the same way you use Newman, with Pynt you get the both the Functional tests and the Security results.



# Getting started:

Download Pynt docker:

`docker pull ghcr-io/overcast-security/pynt:latest`
  
Run docker linux

`docker run -v <full path folder>:/etc/pynt/ --network="host" ghcr.io/overcast-security/pynt:latest -c <collection name>`


# Command line options
`-e <environment_file>` 

# EULA:
Beta version - use this for educational purposes only
