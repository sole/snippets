# You can customly sort lists with a lambda function
items = []
items.append({'x': 0, 'y': 1})
items.append({'x': 0, 'y': -10})

# returns: [{'y': -10, 'x': 2}, {'y': 1, 'x': 0}]
sorted(items, key=lambda item: item['y'])

# Reverse sort:
# returns [{'y': 1, 'x': 0}, {'y': -10, 'x': 2}]
sorted(items, key=lambda item: item['y'], reverse=True)

# More info on sorting: http://wiki.python.org/moin/HowTo/Sorting
