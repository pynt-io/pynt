import tempfile
import docker
import shutil
import os
import argparse
import sys

def main():
    # if sys.platform == "win32":
    #     os.system('color')

    parser = argparse.ArgumentParser(usage="pynt-newman.py <postman collection file> -e [postman environment file]")
    parser.add_argument('collection', help="path to your Postman collection")
    parser.add_argument('-e','--environment',metavar='', help="path to Postman environment file, if needed")
    args = parser.parse_args()

    if args.collection:
        c = args.collection
        if not os.path.exists(c):
            print("Collection file not found")
            exit()

    if args.environment:
        e = args.environment

        if not os.path.exists(e):
            print("Environment file not found")
            exit()

    try:
        client = docker.from_env()
    except docker.errors.APIError:
        print("Docker daemon is not running or not installed")
        exit()

    # try:
    image = client.images.pull("ghcr.io/pynt-io/pynt", "newman-latest")
    # except Exception as e:
    #     print(e) #Golan's bug- docker was stuck- client was created but unable to run commands.

    with tempfile.TemporaryDirectory(dir = os.getcwd()) as runningDir:
        shutil.copy(c, os.path.join(runningDir, "c.json"))
        
        command = ["-c", "c.json","--no-upload-logs"]
        if args.environment:

            shutil.copy(e, os.path.join(runningDir, "e.json"))
            command.extend(["-e", "e.json"])

        run = client.containers.create(image="ghcr.io/pynt-io/pynt:newman-latest", command=command,
                                        network="host", volumes=[runningDir + ":/etc/pynt"], auto_remove=True)
        output = run.attach(stdout=True, stream=True, logs=True)
        run.start()
        # try:
        for line in output:
            try:
                decoded = line.decode("utf-8")
            except UnicodeDecodeError:
                decoded = line
            sys.stdout.write(decoded) ; sys.stdout.flush()
        run.wait()
        # except Exception as e:
        #     print(e) #Ofer's error- most likely docker version

if __name__ == "__main__":
    if sys.platform == "win32":
        os.system('color')
        import pywintypes
        try:
            main()
        except pywintypes.error as e:
            print(e)
    else:
        main()
