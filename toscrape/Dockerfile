FROM python:3.10
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirement.txt
CMD scrapy crawl quotes