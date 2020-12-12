FROM python:3.8

# Create validator directory
RUN apt update && apt -y install nasm gcc-multilib
RUN mkdir /validator
WORKDIR /validator
ENV HOME /validator

# Add Python dependencies
COPY requirements.txt /validator/requirements.txt
RUN pip install --requirement /validator/requirements.txt
RUN python -m pip install --upgrade pip
COPY tasks.zip /validator/tasks.zip
COPY tasks.yaml /validator
COPY runner.py /validator

ENV VPORT SEDMYPORT
ENV SUBMISSION_ID SEDMYSUBMISSION
ENTRYPOINT ["python", "/validator/runner.py", "checker"]