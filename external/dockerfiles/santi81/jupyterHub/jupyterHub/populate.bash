#!/bin/bash
set -e
PROJECT=$(jq -r '.gcloud.project' 'docker-settings.json')
ZONE=$(jq -r '.gcloud.zone' 'docker-settings.json')

CONTEXT="gke_${PROJECT}_${ZONE}_${1}"
IMAGE_SPEC="${2}"
# Pull this container in all of the nodes in current kubernetes context, 16 nodes at a time
# Also explicitly set the username used to ssh as lowercase, since ssh seems to fail for partial uppercase users
kubectl --context=${CONTEXT} get node --no-headers --output=custom-columns=NAME:.metadata.name | parallel --bar --no-notice -j16 "gcloud compute ssh ${USER,,}@{} --zone='${ZONE}' -- '/usr/share/google/dockercfg_update.sh && docker pull ${IMAGE_SPEC}'"

echo "Pulled ${IMAGE_SPEC}"
