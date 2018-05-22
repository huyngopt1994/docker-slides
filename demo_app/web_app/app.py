from flask import Flask, render_template, redirect, request
from redis import Redis
import requests

app = Flask(__name__)

redis = Redis(host='redis', port=6379)

@app.route('/')
def index():
	count = redis.incr('hits')
	url='http://generate_fibonaci:6000/%s' % count
	result= requests.get(url)
	fibo = str(result.text)

	return render_template('index.html',count=count,
	                       fibo=fibo)

@app.route('/', methods=['POST'])
def custom_index():
	count = redis.get('hits')
	try:
		number = int(request.form['selected_number'])
	except:
		return render_template('index.html', error='Please validate your input', count=str(count),
		                       fibo='')
	if number <0:
		return render_template('index.html', error='Please validate your input', count=str(count),fibo='')

	redis.setex('hits',0,600)

	for _ in range(number-1):
		redis.incr('hits')
	return redirect('/')
@app.route('/reset')
def reset():
	redis.setex('hits',0, 600)
	return redirect('/')

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)

