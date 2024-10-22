import redis

client = redis.Redis(host='redis', port=6379, db=0)
print(client.ping())
client.config_set('notify-keyspace-events', 'KEA')