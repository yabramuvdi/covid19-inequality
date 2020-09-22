sudo apt update
sudo apt install python3-pip

python3 -m pip install -U pip setuptools wheel
python3 -m pip install -r requirements.txt
python3 data_generation.py
python3 app.py
