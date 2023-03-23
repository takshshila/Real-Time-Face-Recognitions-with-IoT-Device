FROM public.ecr.aws/lambda/python:3.8

COPY app/ ${LAMBDA_TASK_ROOT}

COPY requirements.txt  .

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [ "eval_face_recognition.handler"]
