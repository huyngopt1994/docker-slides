from flask import Flask

app = Flask(__name__)

def fib():
	a,b =0,1
	while 1:
		yield str(a)
		a,b =b,a+b

@app.route('/<number>')
def count(number):
	h = fib()
	my_list = []
	print(number)
	for i in range(0,int(number)):
		my_list.append(next(h))
	print(my_list)
	return ' '.join(my_list)

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=6000, debug=True)

