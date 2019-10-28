# Use local image instead of remote image
FROM scratch

ARG APPLICATION
ARG APPLICATION_TYPE

# Set the local image
ADD docker/alpine-minirootfs-3.9.2-x86_64.tar.gz /

# Set the app folder as working directory
WORKDIR /app

COPY docker/requirements.txt requirements.txt

# Install python3
RUN apk add --no-cache python3 nmap nmap-scripts  file && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache && \
    mkdir log/

# Install required python3 libraries
RUN pip install -r requirements.txt

COPY utils/ utils/
COPY ${APPLICATION}/constants/ constants/
COPY ${APPLICATION}/${APPLICATION_TYPE} .

ENTRYPOINT ["python3"]
CMD ["main.py"]
