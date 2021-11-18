FROM python:alpine as builder

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:${PATH}
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

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
FROM python:alpine

ENV AppDir=/home/capstone/app StaticDir=$AppDir/static mediaDir=$AppDir/media 

RUN mkdir -p $AppDir $StaticDir $mediaDir

#RUN addgroup -S app && adduser -S app -G app \
RUN pip install --upgrade pip  

WORKDIR ${AppDir}
# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY  /entrypoint.sh $AppDir
RUN chmod +x $AppDir/entrypoint.sh 
 
COPY /capstone/ $AppDir

#COPY --chown=userGroup:userGroup . . ## this feature is only supported in lunix containers 
## otherwie use #RUN chown -R node:node  foldertoCopy dist
#RUN chown -R app:app ${AppDir}

EXPOSE 8000
ENTRYPOINT ["/bin/sh","/home/capstone/app/entrypoint.sh"]




