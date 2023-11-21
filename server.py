from flask import Flask, render_template, request
from utils import GraphGenerator
import asyncio
import random

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.graph_generator = GraphGenerator()
        self.broker = Broker()
        self.trader = Trader(self.broker)
        self.setup_routes()
        
    def setup_routes(self):
        self.app.route('/')(self.home)
        self.app.route('/norm', methods=['GET', 'POST'])(self.norm)
        self.app.route('/exp', methods=['GET', 'POST'])(self.exp)
        self.app.route('/file', methods=['GET', 'POST'])(self.file)
    
    def run(self):
        asyncio.run(self.trader.generate_requests())
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

class Trader():
    def __init__(self, broker):
        self.broker = broker
        self.requests = []
    
    async def generate_requests(self):
        while True:
            request = random.choice(['buy', 'sell'])
            amount = random.randint(1, 100)
            price = random.uniform(1.0, 100.0)
            task_id = random.randint(1, 1000)
            self.requests.append({task_id: (request, amount, price)})
            self.broker.broker_tasks[task_id] = asyncio.create_task(self.broker.handle_request(task_id, request, amount, price))
            print(self.requests)
            print(self.broker.broker_tasks)
            sleep_time = random.randint(1, 10)
            await asyncio.sleep(sleep_time)

class Broker():
    def __init__(self):
        self.broker_semaphores = {}
        self.broker_tasks = {}
   
    async def handle_request(self, task_id, request, amount, price ):
        if task_id not in self.broker_semaphores:
            self.broker_semaphores[task_id] = asyncio.Semaphore(1)

        if await self.is_previous_message_not_answered_yet(task_id): 
            return
        print("Запрос на выполнение: ", request, amount, price)

        return {'status': 'success'}

    async def is_previous_message_not_answered_yet(self, task_id):
        if self.broker_semaphores[task_id].locked():
            try:
                text = "⏳ Запрос на выполнении, ожидайте!\n"
                print(text)
                return True
            except Exception as e:
                print(e)
        else:
            return False


if __name__ == '__main__':
    server = Server()
    server.run()
