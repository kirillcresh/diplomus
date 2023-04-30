# diplomus
 VKRMKRMAKARENA

---

- Sosi
  - 123
  - 456

python 3.10

- Logs
  - 123
  - 345

Example .env
```text
SECRET_KEY=django-secret_key
ALLOWED_HOSTS=allowed_hosts_list

DB_NAME=mysql_database_name
DB_USER=mysql_database_user
DB_HOST=mysql_database_host
DB_PASSWORD=mysql_database_password
DB_PORT=mysql_database_port

SERVER_HOST=fastapi_server_host
```

```python

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.abspath(CONFIG_DIR / 'config' / '.env'))
SECRET_KEY = os.getenv('SECRET_KEY')

```