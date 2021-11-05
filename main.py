import matplotlib.pyplot as plt
import scipy
import auto


df = auto.load_data('https://auto.ru/chelyabinsk/cars/vaz/kalina/all/')
df.plot.scatter(x='year', y='price', c='mileage')
plt.show()
