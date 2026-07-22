from datetime import datetime
import os

from flask_caching import Cache
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message
from celery import Celery
from celery.schedules import crontab



load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USER')

mail = Mail(app)




# ============================
# Flask-Caching with Redis
# ============================
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 1
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/1'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60
cache = Cache(app)


app.config['broker_url'] = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
app.config['result_backend'] = os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0')

celery = Celery(app.name, broker=app.config['broker_url'], backend=app.config['result_backend'])
celery.conf.broker_connection_retry_on_startup = True

# ============================
# Celery Context Setup
# ============================
def init_celery(flask_app):
    celery_app = Celery(
        flask_app.import_name,
        broker=flask_app.config['broker_url'],
        backend=flask_app.config['result_backend']
    )
    celery_app.conf.update(flask_app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return super().__call__(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

celery = init_celery(app)



celery.conf.timezone = 'Asia/Kolkata'
celery.conf.beat_schedule = {
    'daily-reminder': {
        'task': 'tasks.daily_reminder',
        'schedule': crontab(minute='*/1')  # Every 1 minute for testing purposes,
    },
    'monthly-report-generation': {
        'task': 'tasks.report_generation',
        'schedule': crontab()
    }
}




@celery.task(name="tasks.daily_reminder")
def daily_reminder():

    # users = User.query.all()
    # email_list =[]
    # for user in users:
    #     email_list.append(user.email)

    msg = Message(
        'Hello',
        recipients=['22F2000625@ds.study.iitm.ac.in'],
        body='This is a daily reminder email!'
    )
    mail.send(msg)

    return 'daily reminder task completed'



@celery.task(name="tasks.report_generation")
def download_report():
   
   return 'report downloaded successfully'

@app.route('/report_gen')
def report_gen():
    download_report.delay()
    return 'report generation task started'

@app.route('/')
def send_email():
  msg = Message(
    'Hello',
    recipients=['22F2000625@ds.study.iitm.ac.in'],
    body='This is a test email sent from Flask-Mail!'
  )
  mail.send(msg)
  return 'Email sent succesfully!'


@app.route('/cache')
@cache.cached()
def cache_test():
  now_time = datetime.now()
  formated_time =  now_time.strftime("%Y-%m-%d %H:%M:%S")
  return formated_time


@app.route('/clear_cache')
def clear_cache():
  cache.clear()
  return 'cache cleared'



if __name__ == '__main__':
    app.run(debug=True)
