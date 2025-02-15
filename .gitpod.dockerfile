FROM gitpod/workspace-full-vnc:2025-02-12-08-12-04

# Hadolint complains about sudo; however gitpod recommends using sudo to install packages
# hadolint ignore=DL3004
RUN sudo apt-get update \
    && sudo apt-get install -y \
    firefox \
    gulp \
    && sudo apt-get clean \
    && python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir selenium==4.1.0 'requests<3'
