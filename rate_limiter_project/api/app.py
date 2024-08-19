from flask import Flask, request, jsonify
from rate_limiter import RedisRateLimiter  # or BasicRateLimiter

app = Flask(__name__)

# Configuration
app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379
app.config['RATE_LIMIT'] = 10
app.config['WINDOW_SECONDS'] = 60

# Initialize Redis client
import redis
redis_client = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=0)
rate_limiter = RedisRateLimiter(redis_client, rate_limit=app.config['RATE_LIMIT'], window_seconds=app.config['WINDOW_SECONDS'])

@app.route('/check', methods=['GET'])
def check_rate_limit():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    allowed = rate_limiter.is_allowed(user_id)
    return jsonify({'allowed': allowed})

if __name__ == "__main__":
    app.run(port=5000)
