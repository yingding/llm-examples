# llm-examples
this repository contains codes for loading and training open source llm models e.g. LlaMA2

## update the venv on local mac host
```shell
python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir -r ./setup/requirements310mac.txt
```

## Add a jupyter notebook kernel to VENV
```shell
VENV_NAME="llm3.10"
VENV_DIR="$HOME/VENV"
source ${VENV_DIR}/${VENV_NAME}/bin/activate;
python3 -m pip install --upgrade pip
python3 -m pip install ipykernel
deactivate
```

We need to reactivate the venv so that the ipython kernel is available after installation.
```shell
VENV_NAME="llm3.10"
VENV_DIR="$HOME/VENV"
source ${VENV_DIR}/${VENV_NAME}/bin/activate;
# ipython kernel install --user --name=shap3.10
python3 -m ipykernel install --user --name=${VENV_NAME} --display-name ${VENV_NAME}
```
Note: 
* restart the vs code, to select the venv as jupyter notebook kernel


Reference:
* https://ipython.readthedocs.io/en/stable/install/kernel_install.html
* https://anbasile.github.io/posts/2017-06-25-jupyter-venv/

## Remove ipykernel
```shell
# jupyter kernelspec uninstall -y <VENV_NAME>
jupyter kernelspec uninstall -y shap3.10
```

## Remove all package from venv
```
python3 -m pip freeze | xargs pip uninstall -y
python3 -m pip list
```

## Sync AIMLflow
```shell
aim_repo_path=./aimruns
mlflow_uri=./mlruns
mkdir ${aim_repo_path}
cd ${aim_repo_path}
aim init
cd ..
# start a watch process
aimlflow sync --mlflow-tracking-uri=${mlflow_uri} --aim-repo=${aim_repo_path}
# start a second terminal
aim up --repo=${aim_repo_path}
```

## Restart MLflow UI
If the default port 5000 is used
```shell
ps -A | grep gunicorn
pkill -f gunicorn
ps -A | grep gunicorn
mlflow ui
# mlflow server --host 127.0.0.1 --port 8080
```

Reference:
* https://stackoverflow.com/questions/60531166/how-to-safely-shutdown-mlflow-ui/63141642#63141642

# Relevant tech info

* [LLM tech docs](./LLM.md)
* mlflow https://mlflow.org/docs/latest/llms/langchain/guide/index.html
* mlflow langchain flavour https://mlflow.org/docs/latest/llms/langchain/index.html

