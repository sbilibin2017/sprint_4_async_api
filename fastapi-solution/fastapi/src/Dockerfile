# base image
FROM python:3.10-slim
# enviironment variables

ENV HOME=/
ENV APP_HOME=/src
ENV GROUP=fastapi
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create app directory
# create app directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN groupadd -r $GROUP && \
    useradd -d $APP_HOME -r -g $GROUP $GROUP && \
    chown $GROUP:$GROUP -R $APP_HOME    

# install dependancies
RUN apt-get update && \
    apt-get install -y gettext && \
    apt install -y ncat && \
    python -m pip install --upgrade pip && \
    pip3 install poetry

# copy files
COPY . $APP_HOME

# install dependancies
RUN poetry config virtualenvs.create false
RUN poetry install

# changing mode of entrypoint
RUN chmod +x ./docker-entrypoint.sh

USER $GROUP

EXPOSE 8000

# run script 
ENTRYPOINT ["./docker-entrypoint.sh"]

