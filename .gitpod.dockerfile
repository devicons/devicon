FROM gitpod/workspace-full-vnc

RUN sudo apt-get update \
    && sudo apt-get install -y \
    firefox \
    gulp \
    && python -m pip install --upgrade pip \
    && pip install selenium==4.1.0 requests==2.25.1
