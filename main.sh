sudo apt update
sudo apt install python3-pip tmux htop

python3 -m pip install -U pip setuptools wheel
python3 -m pip install -r requirements.txt
pip3 install gunicorn

#sudo apt-get install nginx
# https://www.twilio.com/blog/deploy-flask-python-app-aws
# tmux new -s app

python3 data_generation.py
gunicorn app:app.server -b :8000
#python3 app.py
