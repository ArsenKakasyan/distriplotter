import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

class GraphGenerator:
    def __init__(self):
        self.df = None

    def drawNormDistr(self, mean, std):
        dist_type = 'norm'
        #https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html
        data = np.random.normal(mean, std, 1000)
        x = np.array(data)
        x = np.sort(x)
        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html#scipy.stats.gaussian_kde
        kde = gaussian_kde(x)
        y = kde.pdf(x)
        return self.plot_graph(x, y, dist_type)
    
    def drawExpDistr(self, lmbda):
        dist_type = 'exp'
        x = np.linspace(0, 10, 1000)
        y = lmbda * np.exp(-lmbda * x)
        return self.plot_graph(x, y, dist_type)

    def drawDistrFromExcel(self, excel_file, listn: str, coln: int):
        dist_type = 'file'
        self.df = pd.read_excel(excel_file, sheet_name=listn)
        column_c_values = self.df.iloc[:, coln].values
        x = np.array(column_c_values)
        x = np.sort(x)
        kde = gaussian_kde(x)
        y = kde.pdf(x)
        return self.plot_graph(x, y, dist_type)
    
    def plot_graph(self, x, y, dist_type):
        plt.figure()
        if(dist_type == 'exp'):
            plt.plot(x, y, marker='o', markerfacecolor='blue', markersize=5, color='skyblue', linewidth=1)
        else:
            plt.hist(x, bins='auto', density=True, alpha=0.6, color='darkblue', label='Искомое распределение')
            plt.plot(x, y, marker='o', markerfacecolor='blue', markersize=5, color='skyblue', label='Плотность вероятности')
            plt.axvline(x.min(), color='r', linestyle='dashed', linewidth=2)  
            plt.axvline(x.max(), color='g', linestyle='dashed', linewidth=2)  
            plt.axvline(x.mean(), color='k', linestyle='dashed', linewidth=2)
            plt.legend()
            
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return 'data:image/png;base64,{}'.format(graph_url)