FROM rasa/rasa-sdk:3.0.2
WORKDIR /app

# Copia para o container arquivo que define as dependências externas

# Utiliza o root user para instalar as dependências
USER root
COPY actions/requirements-actions.txt ./
RUN pip install -r requirements-actions.txt

# Copia as actions para o workdir
COPY ./actions /app/actions

USER 1001