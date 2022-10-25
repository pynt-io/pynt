# ------------------------------------------------------------------------------
# Copyright 2022 Pynt
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

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
            exit(1)

    if args.environment:
        e = args.environment
        if not os.path.exists(e):
            print("Environment file not found")
            exit(1)
    
    print("Setting up Pynt docker...")
    
    try:
        client = docker.from_env()
    except docker.errors.DockerException as e: 
        print("Docker daemon is not running or not installed,", e)
        exit(1)

    try:
        image = client.images.pull("ghcr.io/pynt-io/pynt", "latest")
    except docker.errors.DockerException as e: 
        print("There was an error while pulling the Pynt image,", e)
        exit(1)
  
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
