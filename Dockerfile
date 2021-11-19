FROM python:3.9.6-alpine as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev 

RUN pip install --upgrade pip

# install dependencies
COPY /capstone/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#####################################################################################################
# FINAL #
#########
FROM python:3.9.6-alpine

ENV AppDir=/app StaticDir=$AppDir/static mediaDir=$AppDir/media  

RUN mkdir -p $AppDir $StaticDir $mediaDir

WORKDIR ${AppDir}
# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY  /entrypoint.sh $AppDir
RUN chmod +x $AppDir/entrypoint.sh 
 
COPY /capstone/ $AppDir

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser ${AppDir}
USER appuser

EXPOSE 8000
ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
