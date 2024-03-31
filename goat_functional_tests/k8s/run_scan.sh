#!/bin/bash

if [ $# -eq 0 ]; then
	echo "No argument provided. Please pass your pynt-id as an argument."
	exit 1
fi

# Store the value from the argument in a variable
arg_value=$1

namespace=pynt-scan

# Encode the arg value as base64
encoded_value=$(echo -n "$arg_value" | base64)

escaped_value=$(printf '%s\n' "$encoded_value" | sed -e 's/[\/&]/\\&/g')

# Replace PYNT_ID with encoded_value in the secret.yaml file
sed -i '' -e "s/PYNT_ID/$escaped_value/g" pynt-manifests/secret.yaml

kubectl create namespace $namespace
kubectl apply -f pynt-manifests/secret.yaml -n $namespace
kubectl apply -f pynt-manifests/app.yaml -n $namespace
kubectl apply -f scan-trigger/job.yaml -n $namespace