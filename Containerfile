FROM registry.access.redhat.com/ubi8/python-311:1-13

ENV ARGOCD_VERSION=v2.7.7
ENV OC_VERSION=4.12.22
ENV YQ_VERSION=4.11.2
ENV HELM_VERSION=3.11.2

USER root

RUN dnf install -y tar gzip openssh-clients jq rsync

RUN curl -o /tmp/argocd -L https://github.com/argoproj/argo-cd/releases/download/${ARGOCD_VERSION}/argocd-linux-amd64 && cd /usr/bin && cp /tmp/argocd . && chmod a+x /usr/bin/argocd && rm -f /tmp/argocd
RUN curl -o /tmp/oc.tar.gz -L https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/${OC_VERSION}/openshift-client-linux-${OC_VERSION}.tar.gz && cd /usr/bin && tar -xvzf /tmp/oc.tar.gz && chmod a+x /usr/bin/oc && chmod a+x /usr/bin/kubectl && rm -f /tmp/oc.tar.gz
RUN curl -s -o /tmp/yq -L https://github.com/mikefarah/yq/releases/download/v${YQ_VERSION}/yq_linux_amd64 && cd /usr/bin && cp /tmp/yq . && chmod a+x /usr/bin/yq && rm -f /tmp/yq
RUN curl -s -o /tmp/helm.tar.gz -L https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz && cd /usr/bin && tar -xvzf /tmp/helm.tar.gz linux-amd64/helm && mv /usr/bin/linux-amd64/helm /usr/bin/helm && rm -rf /usr/bin/linux-amd64 && chmod a+x /usr/bin/helm && rm -f /tmp/helm.tar.gz

RUN dnf -y clean all --enablerepo='*'

RUN mkdir ${HOME}/.config && chgrp -R 0 ${HOME} && chmod -R g=u ${HOME}

USER 1001

# Create directory for application resources
COPY --chown=1001 *.py /deployments/
COPY --chown=1001 requirements.txt /deployments/
COPY --chown=1001 datasets/ /deployments/datasets/
COPY --chown=1001 util/ /deployments/util/

WORKDIR /deployments

# Install dependencies
RUN pip install -r requirements.txt

# Configure container port and UID
EXPOSE 8080
USER 1001

# Run application
# CMD ["python", "/deployments/predict-async.py"]
CMD ["hypercorn", "--graceful-timeout", "5", "--bind", "0.0.0.0:8080", "predict-async:app"]