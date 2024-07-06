# SOCIAL MEDIA MANAGER AI (3SIDES)

This is project connected with a `YouTube`[series](https://www.youtube.com/playlist?list=PLkF5PJHwaQCRcnt8q9nm-pY-TkxAm3eRQ)

## Aim

The aim is to enanche capabilities of italian micro startups (0-9 employees) by using & developing affordable and democratic AI tools.
In this particular project we built a Social Media Manager AI (SMMAI), for 3Sides a streeweare brand located in Baronissi (SA)🇮🇹.

It will help the shop owner to automatically select the most aestetich photo and then write an angaging caption with it, to be ready to be posted on `Instagram`.

## Where is AI

Two main AI models are involved in this project:

- An image ranking model
- A text to image model (OpenAI GPT)

## Development setup

To ensure stability and coherence during development, it is better to have control over the python env you use.
To ensure this, we will use `conda` in this project.

- First install `miniconda` or `anaconda` using the instruction [here](https://docs.anaconda.com/free/miniconda/)
- Check your conda installation by running this command in a new terminal

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

- Initilize the environment

If you are currently in a virtual env, you can exit it by running

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

- once the previous command finishes, activate your dev environment by typing

```bash
$ conda activate 3-Sides-dev
```

- now install all the dependencies

```bash
$ pip install -r requirements.txt
``` 

You now have a fresh and coherent environment to work with. In case you mess up the libraries and you want to restore
the environment, just run the following:

```bash
$(3-Sides-dev) conda deactivate
$ conda remove --name 3-Sides-dev --all
$ conda env create -f environment.yml
$ conda activate 3-Sides-dev
$(3-Sides-dev) pip install -r requirements.txt