if [ ! -d "venv" ]; then
  python3.9 -m venv venv
fi

source venv/bin/activate
source .env

pip install -r requirements.txt

export PYTHONPATH="$PWD"

alembic upgrade head

fuser -n tcp -k 8000

nohup python manage.py serve --workers 3 &> app.logs &

echo "Server running"
