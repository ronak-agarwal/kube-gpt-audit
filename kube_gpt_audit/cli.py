# -*- coding: utf-8 -*-
"""Console script kube audit."""
# pylint: disable=W1203,E1205,C0301

import argparse
import logging
import colorlog
import json
from kubernetes import client, config
from .audit import run_audit, create_printtable_table

from rich.console import Console

BLACKLIST_RESOURCE_HIT_4097_TOKEN = [
    "ebs-csi-controller"
]

console = Console()

logger = logging.getLogger('log')
if not logger.handlers:
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            '# %(log_color)s%(asctime)s %(levelname)s:\t%(name)s: %(message)s',
            datefmt='%m-%d %H:%M:%S'
        )
    )
    logger = colorlog.getLogger('log')
    logger.addHandler(handler)

# Define a function to remove a list of keys from a JSON object
def remove_keys(obj, keys):
    if isinstance(obj, dict):
        # If the object is a dictionary, remove the specified keys
        for key in keys:
            if key in obj:
                del obj[key]
        # Recursively call the function on the values of the dictionary
        for k, v in obj.items():
            remove_keys(v, keys)
    elif isinstance(obj, list):
        # If the object is a list, recursively call the function on each element
        for item in obj:
            remove_keys(item, keys)

class KubernetesCluster:
    def __init__(self):
        self.api_client = None
        try:
            # Load Kubernetes configuration from default location
            config.load_kube_config()
        except config.config_exception.ConfigException:
            # Fall back to in-cluster configuration if no default config found
            config.load_incluster_config()

        # Create a Kubernetes API client
        self.api_client = client.ApiClient()

    def audit_deployments(self):
        api = client.AppsV1Api(api_client=self.api_client)
        deployments = api.list_deployment_for_all_namespaces().items
        for deployment in deployments:
            if deployment.metadata.name not in BLACKLIST_RESOURCE_HIT_4097_TOKEN:
                data = json.loads(json.dumps(self.api_client.sanitize_for_serialization(deployment)))
                remove_keys(data, ["managedFields", "status", "creationTimestamp", "uid", "resourceVersion", "labels", "annotations"])
                audit_result: str = run_audit("deployment", json.dumps(data))
                print("\n")
                table_title = f"\U0001f916 Audit for the Kubernetes Deployment => {deployment.metadata.name}"
                console.print(create_printtable_table(audit_result, table_title, False))
                print("\n")

def main(args):
    """ Main entry point of the app """
    # set our logging level from the CLI options.
    if args.debug:
        logger.setLevel('DEBUG')
    elif args.quiet:
        logger.setLevel('ERROR')
    else:
        logger.setLevel('INFO')

    if args.audit:
        target_cluster = KubernetesCluster()
        target_cluster.audit_deployments()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Print debug messages')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')
    parser.add_argument('--audit', action='store_true', help='Audit kube cluster')

    args = parser.parse_args()
    main(args)