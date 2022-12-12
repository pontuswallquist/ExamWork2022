FROM tensorflow/tensorflow:latest

COPY DQN_agent.py /tmp
COPY cards.py /tmp
COPY player.py /tmp
COPY game.py /tmp
COPY trainAgent.py /tmp
COPY testAgent.py /tmp
COPY model_14.h5 /tmp
COPY requirements.txt /tmp
WORKDIR /tmp

RUN pip install -r requirements.txt


