#!/bin/sh

DEPLOYMENT_NS="4-test"
# ENV_FILE="../.env.deploy"

# if ! test -f "${ENV_FILE}"; then
#     echo "${ENV_FILE} does not exist."
#     exit 1
# fi

# . ${ENV_FILE}

oc new-project ${DEPLOYMENT_NS}

oc delete secret ml-models -n ${DEPLOYMENT_NS}
oc create secret generic ml-models --from-file=../models/model.joblib -n ${DEPLOYMENT_NS}

# oc delete secret ml-models -n ${DEPLOYMENT_NS}
# oc create secret generic ml-models --from-env-file=${ENV_FILE} -n ${DEPLOYMENT_NS}

helm template ml ml/ --set organization=${DEPLOYMENT_NS} | oc apply -n ${DEPLOYMENT_NS} -f -

# oc start-build bc/kitchensink-bot -n ${DEPLOYMENT_NS}