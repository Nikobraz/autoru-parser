import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy
import auto

city = 'chelyabinsk'
manufacter = 'vaz'
model = 'granta'

df = auto.load_data(f'https://auto.ru/{city}/cars/{manufacter}/{model}/all/')
#df = df[(df['year'] == 1999) & (df['mileage'] <= 180000)]

print('Средняя цена по найденным объявлениям = ' + str(int(df['price'].mean(skipna=0))))
print('Средний пробег найденным объявлениям = ' + str(int(df['mileage'].mean(skipna=0))))
print('Средний год по найденным объявлениям = ' + str(int(df['year'].mean(skipna=0))))

ax = df.plot.scatter(x='year', y='price', c='mileage', colormap='viridis')
ax.set_title(f'{city} {manufacter} {model}')
# Только целые числа в шкалах
ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:.0f}'))
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:.0f}'))
# Размер тика в шкалах
ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(100000))
# Нарисовать сетку
ax.grid()
plt.show()