import requests
import bs4 as bs

# скачиваем исходный html код с сайта
source = requests.get("ссылку сами вставьте").text

# Воспользуемся библиотекой, которая поможет быстро искать нужные элементы.
# Для этого из модуля bs вызовем объект и передадим туда наш исходный код и формат
soup = bs.BeautifulSoup(source, 'lxml')

# теперь soup - объект из BeautifulSoup и мы можем пользоваться реализованными им методами.
# например, быстро искать определенный элемент.
# Это делается так: мы указываем нужный тег элемента, но таких элементов же много, поэтому давайте
# укажем, что нам нужен такой div, у которого есть атрибут class со значением ... ну вы поняли.
# Нам нужен блок кода только с пиццами, а если вы посмотрите в инструменте разработчика, то это именно он
just_pizza = soup.find('div', {"class" : "product-grid product-grid-pizza"})

# Если вы посмотрите на этот блок кода со всеми пиццами, то увидите много одинаковых элементов - пицц,
# которые отличаются только значениями. Так вот давайте все это сложим в список.
products = just_pizza.find_all('div', {"class": "product-item"})

# инфу о пицце будем сохранять сюда. Нам необходимо создать переменную вне цикла, чтобы ее
# область видимости была вне цикла.
pizza = {}

# теперь мы можем итерироваться по каждому кусочку кода с информацией о пицце и доставать нужную
# нам информацию
for product in products:

	# для нашего примера хотелось бы доставать имена, цену и информацию об ингредиентах

	# если посмотреть на исходной страничке, то можем увидеть, что имя лежит в теге div, у которого
	# есть атрибут class, который называется product-info и в нем есть еще несколько тегов.
	# Имя лежит в обернутом теге h3 со свойством itemprop, у которого значение name.
	name = product.find_all('div', {"class" : "product-info"})[0].find_all('h3', {'itemprop' : 'name'})
	
	# find_all - возвращает список, на самом деле можно воспользоваться просто find,
	# так вот так как это список, то нам нужен первый элемент и у него надо взять текст.
	# забрать текст можно таким методом
	name = name[0].get_text()
	
	# еще мы хотим большую пиццу, на сайте она называется medium, информация об о ценах
	# на все размеры пиццы лежит в div с атрибутом class и значением product-value
	medium_pizza = product.find_all('div', {"class" : "product-value"})
	
	# цена за большую пиццу лежит вторым элементом (первый отвечает за маленькую)
	# а еще этот текст возвращается со знаком Р, что там не надо, потому что мы хотим
	# строку конвертировать в число. Этот знак является последним элементом в строке и мы
	# можем просто взять слайс от первого до предпоследнего элемента [:-1]
	price = medium_pizza[1].find('div', {"class" : "product-price"}).get_text()[:-1]
	price = int(price)

	# информация об ингредиентах лежит в теге div с атрибутом class, который имеет значение 
	# product-summary, собственно достаем его и берем текст
	summary = product.find('div', {"class" : "product-summary"}).get_text()

	# теперь все, что бы наскрапили кладем в структуру словаря такого вида:
	# ключ - имя пиццы, значение - список из двух элементов: первый  - цена, второй - ингредиенты
	# {'имя пиццы': [цена, ингредиенты]}
	pizza[name] = [price, summary]

# так мы можем итерироваться по элементам словаря
for name, attribute in pizza.items():
	print("{}\n price: {}\n ingredients: {}\n\n".format(name, attribute[0], attribute[1]))


## вывести только с определенными ингредиентами
## ограничить цену
## исключить ингредиент
