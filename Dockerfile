FROM python:3.10

RUN useradd --create-home twiner_user

RUN apt-get update

ENV PATH="/home/netcord_user/.local/bin:${PATH}"

COPY . /twiner
WORKDIR /twiner

RUN chown -R twiner_user:twiner_user /twiner
USER twiner_user

RUN pip install --upgrade pip setuptools --user && \
    pip install -r requirements.txt --user

CMD ["python3.10", "twiner.py"]