import redis
import bottle
import json

client = redis.Redis(host='redis', port=6379, db=0)

@bottle.get('/')
def healthcheck():
    return

@bottle.post('/')
def index():
    client.publish('transactions', json.loads(bottle.request.json))
    return

if __name__ == "__main__":
    bottle.run(host='0.0.0.0', port=8000)