FROM tensorflow/tensorflow:latest-gpu

COPY DQN_agent.py /tmp
COPY cards.py /tmp
COPY player.py /tmp
COPY game.py /tmp
COPY trainAgent.py /tmp
COPY testAgent.py /tmp
COPY requirements.txt /tmp
COPY model_23.h5 /tmp
COPY model_14.h5 /tmp
WORKDIR /tmp

RUN pip install -r requirements.txt


