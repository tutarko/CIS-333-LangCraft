import chef

while True:
	text = input('chef > ')
	result, error = chef.run('<stdin>', text)

	if error: print(error.as_string())
	else: print(result)