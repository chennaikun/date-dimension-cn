FROM python:3.12
WORKDIR /api

COPY ./requirements.txt /tmp/requirements.txt
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple && \
    pip config set install.trusted-host mirrors.aliyun.com && \
    && pip install --no-cache-dir -r ./holiday-cn/dev-requirements.txt \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD ["python", "main.py"]