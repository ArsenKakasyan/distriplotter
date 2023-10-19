from flask import Flask, render_template, request
from utils import GraphGenerator

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.graph_generator = GraphGenerator()
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route('/')(self.home)
        self.app.route('/norm', methods=['GET', 'POST'])(self.norm)
        self.app.route('/exp', methods=['GET', 'POST'])(self.exp)
        self.app.route('/file', methods=['GET', 'POST'])(self.file)
    
    def run(self):
        self.app.run()
    
    def home(self):
        return render_template('home.html')
    
    def norm(self):
        if request.method == 'POST':
            mean = float(request.form.get('mean'))
            std = float(request.form.get('std'))
            graph = self.graph_generator.drawNormDistr(mean, std)
            return render_template('norm.html', graph=graph)
        else:
            return render_template('norm.html')
    
    def exp(self):
        if request.method == 'POST':
            lmbda = float(request.form.get('lambda'))
            graph = self.graph_generator.drawExpDistr(lmbda)
            return render_template('exp.html', graph=graph)
        else:
            return render_template('exp.html')
    
    def file(self):
        if request.method == 'POST':
            file = request.files['file']
            listn = str(request.form.get('listn'))
            coln = int(request.form.get('coln'))
            excel_file = file.read()
            graph = self.graph_generator.drawDistrFromExcel(excel_file, listn, coln)
            return render_template('file.html', graph=graph)
        else:
            return render_template('file.html')

if __name__ == '__main__':
    server = Server()
    server.run()
