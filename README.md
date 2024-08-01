# SOCIAL MEDIA MANAGER AI (3SIDES)

This project is connected with a [YouTube series](https://www.youtube.com/playlist?list=PLkF5PJHwaQCRcnt8q9nm-pY-TkxAm3eRQ).

## Aim

The aim is to enhance the capabilities of Italian micro startups (0-9 employees) by using and developing affordable and democratic AI tools.

In this particular project, we built a Social Media Manager AI (SMMAI) for 3Sides, a streetwear brand located in Baronissi (SA)🇮🇹. It will help the shop owner automatically select the most aesthetic photo and write an engaging caption to be ready to post on Instagram.

## Where is AI

Two main AI models are involved in this project:

- An image ranking model
- A llm model `gpt-4o-mini` with vision ability.


## How to run it

### Prerequisite

Before running the software, make sure you have the following prerequisites:

1. **Docker**: You need to have Docker installed on your machine.
2. **.env file**: This file contains environment variables needed for the application, including the OpenAI API keys.

#### Installing Docker

##### Windows

1. **Download Docker Desktop**:
   - Visit the [Docker Desktop for Windows](https://desktop.docker.com/win/stable/amd64/Docker%20Desktop%20Installer.exe) page.
   - Download the installer.

2. **Install Docker Desktop**:
   - Run the installer.
   - Follow the installation instructions.
   - After installation, start Docker Desktop.

3. **Verify Installation**:
   - Open PowerShell or Command Prompt.
   - Run the command: `docker --version`
   - You should see the Docker version information.

##### macOS

1. **Download Docker Desktop**:
   - Visit the [Docker Desktop for Mac](https://desktop.docker.com/mac/stable/amd64/Docker.dmg) page.
   - Download the `.dmg` file.

2. **Install Docker Desktop**:
   - Open the downloaded file and drag Docker to the Applications folder.
   - Start Docker from the Applications folder.

3. **Verify Installation**:
   - Open Terminal.
   - Run the command: `docker --version`
   - You should see the Docker version information.

##### Linux

1. **Install Docker Engine**:
   - Open a terminal and run the following commands:

     ```bash
     sudo apt-get update
     sudo apt-get install \
         ca-certificates \
         curl \
         gnupg \
         lsb-release

     curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

     echo \
       "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

     sudo apt-get update
     sudo apt-get install docker-ce docker-ce-cli containerd.io
     ```

2. **Verify Installation**:
   - Run the command: `docker --version`
   - You should see the Docker version information.

The `.env` file contains the necessary configuration for your application, it has to contains all
the information inisde the `.env_template`, mainly the `OPENAI_API_KEY`.
Please follow the instruction [here](https://platform.openai.com/docs/quickstart).

### Run with docker

```bash
$ docker pull dmastricci/3sidesai
```

```bash
$ docker run -d --env-file .env -p 8080:8501 dmastricci/3sidesai:latest
```

and got to [http:\\\localhost:8080](http:\\localhost:8080)

## Development Setup

To ensure stability and coherence during development, it is better to have control over the Python environment you use. To ensure this, we will use `conda` in this project.

- First, install `miniconda` or `anaconda` using the instructions [here](https://docs.anaconda.com/free/miniconda/).
- Check your conda installation by running this command in a new terminal:

```bash
$ conda list
```

You should see something like this:

```bash
# packages in environment at /home/<user>/miniconda3:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                       1_gnu  
boltons                   23.0.0          py311h06a4308_0  
brotlipy                  0.7.0           py311h5eee18b_1002  
bzip2                     1.0.8                h7b6447c_0  
c-ares                    1.19.0               h5eee18b_0  
ca-certificates           2023.05.30           h06a4308_0  
certifi                   2023.5.7        py311h06a4308_0  
```

### Initialize the Environment

If you are currently in a virtual environment, you can exit it by running:

```bash
$ source deactivate
```

or

```bash
$ conda deactivate
```

Then run the following command:

```bash
conda env create -f environment.yml
```

Once the previous command finishes, activate your development environment by typing:

```bash
$ conda activate 3-Sides-dev
```

Now install all the dependencies:

```bash
$ pip install -r requirements.txt
``` 

You now have a fresh and coherent environment to work with. In case you mess up the libraries and want to restore the environment, just run the following:

```bash
$(3-Sides-dev) conda deactivate
$ conda remove --name 3-Sides-dev --all
$ conda env create -f environment.yml
$ conda activate 3-Sides-dev
$(3-Sides-dev) pip install -r requirements.txt
```

### Using Docker

To build and run the app using Docker, first build the project:
```bash
$ docker build -t dmastricci/3sidesai:last .
```

then run it on the desider port, here it is used 8080:
```bash
$ docker run --env-file .env -p 8080:8501 dmastricci/3sidesai:last
```