FROM laudio/pyodbc:1.0.4

WORKDIR /usr/src/winspeed

# Add your source files.
# COPY ["app", "./app"]
# COPY ["setup.py", "./"]

# RUN pip install .

# CMD ["python", "app/main.py"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/winspeed

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#ENTRYPOINT ["python"]
COPY . /usr/src/winspeed