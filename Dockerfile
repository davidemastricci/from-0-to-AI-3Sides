FROM continuumio/miniconda3

WORKDIR /app

COPY src/ /app/src
COPY environment.yml /app/environment.yml
COPY LICENSE /app/LICENSE 
COPY README.md /app/README.md
COPY requirements.txt /app/requirements.txt

RUN conda env create -f environment.yml && \
    conda clean -a -y

SHELL ["conda", "run", "-n", "3-Sides-dev", "/bin/bash", "-c"]

RUN pip install -r requirements.txt

ENV PATH /opt/miniconda/envs/3-Sides-dev/bin:$PATH


CMD ["conda", "run", "--no-capture-output", "-n", "3-Sides-dev", "python", "src/main.py"]
EXPOSE 8501