import numpy as np
import matplotlib.pyplot as plt

# Создаем случайные данные
data = np.random.normal(0, 1, 1000)

# Создаем график плотности вероятности
plt.hist(data, bins='auto', density=True, alpha=0.6, color='darkblue', label='Искомое распределение')

# Рисуем линию плотности вероятности
plt.plot(data, (1 / (np.std(data) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((data - np.mean(data)) / np.std(data)) ** 2), marker='o', markerfacecolor='blue', markersize=5, color='skyblue', label='Плотность вероятности')

plt.show()
