FROM dmickels/sdapov-baseimage:latest
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Configure Script and GIT variables
ENV python_script sdapodfastforward.py
ENV GIT_REPO https://github.com/ankanani/sdapovfastforward.git
ENV GIT_BRANCH selfservelabs

WORKDIR /usr/src/app

RUN git clone $GIT_REPO
#RUN git checkout $GIT_BRANCH

COPY ../requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD python3 $python_script
