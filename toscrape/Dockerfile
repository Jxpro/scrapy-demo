FROM python:3.10
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirement.txt
EXPOSE 9080
CMD scrapyrt -i 0.0.0.0