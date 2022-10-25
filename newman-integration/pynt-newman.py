import tempfile
import docker
import shutil
import os
import argparse
import sys

def main():

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
    
    print("Setting up Pynt docker...")
    
    try:
        client = docker.from_env()
    except docker.errors.DockerException as e: 
        print("Docker daemon is not running or not installed,", e)
        exit()

    try:
        image = client.images.pull("ghcr.io/pynt-io/pynt", "newman-latest")
    except docker.errors.DockerException as e: 
        print("There was an error while pulling the Pynt image,", e)
        exit()
  
    with tempfile.TemporaryDirectory(dir = os.getcwd()) as runningDir:
        cName = os.path.split(c)[-1]
        shutil.copy(c, os.path.join(runningDir, cName))
        
        command = ["-c", cName, "--no-upload-logs"]
        if args.environment:
            eName = os.path.split(e)[-1]
            shutil.copy(e, os.path.join(runningDir, eName))
            command.extend(["-e", eName])

        run = client.containers.create(image=image, command=command,
                                        network="host", volumes=[runningDir + ":/etc/pynt"], auto_remove=True)
        output = run.attach(stdout=True, stream=True, logs=True)
        run.start()
        for line in output:
            try:
                decoded = line.decode("utf-8")
            except UnicodeDecodeError:
                decoded = line
            sys.stdout.write(decoded) ; sys.stdout.flush()
        run.wait()

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
