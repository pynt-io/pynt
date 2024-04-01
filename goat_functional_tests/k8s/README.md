# Kubernetes (k8s) Configuration

This directory contains the Kubernetes (k8s) configuration files for the Goat Functional Tests.

## Purpose

The purpose of the k8s content is to provide the necessary configuration files to deploy and run the Goat Functional Tests on a Kubernetes cluster. These tests are designed to validate the functionality and performance of the Goat application in a Kubernetes environment.

## Prerequisites

Before running the Goat Functional Tests, ensure that you have the following prerequisites:

- A running Kubernetes cluster
- `kubectl` command-line tool installed and configured to connect to the cluster

## Usage

To use the k8s content and run the Goat Functional Tests, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/pynt-io/pynt.git
   cd pynt/goat_functional_tests/k8s && ./run_scan.sh $PYNT_ID
	```