from tabulate import tabulate
from argparse import ArgumentParser as prsr
parser = prsr()
parser.add_argument('--file', type=str, nargs="+",
                    default=None, help='path to file')
parser.add_argument('--report', type=str, default=None, help='report')


class Endpoint:
    def __init__(self, timestamp, status, url, request_method, response_time, http_user_agent):
        self.timestamp = timestamp
        self.status = status
        self.url = url
        self.request_method = request_method
        self.response_time = [float(response_time)]
        self.http_user_agent = http_user_agent
        self.total = 1

    def add_request(self, response_time):
        self.response_time.append(float(response_time))
        self.total += 1

    def get_average(self):
        return self.url, self.total, sum(self.response_time)/len(self.response_time)


class Loader:
    def __init__(self):
        self.dict_endpoint = {}

    @staticmethod
    def pars_log(list_args):
        res = []
        for arg in list_args:
            res.append(arg.split(': ')[1])
        return res

    def load_log(self, args):
        for path in args:
            with open(path) as file:
                for line in file:
                    timestamp, status, url, request_method, response_time, http_user_agent = Loader.pars_log(
                        line[1:-1].split(','))
                    if self.dict_endpoint == {}:
                        self.dict_endpoint[url] = Endpoint(
                            timestamp, status, url[1:-1], request_method, response_time, http_user_agent)
                    else:
                        if url in self.dict_endpoint:
                            self.dict_endpoint[url].add_request(response_time)
                        else:
                            self.dict_endpoint[url] = Endpoint(
                                timestamp, status, url[1:-1], request_method, response_time, http_user_agent)

    def render_average(self):
        list_result = []
        for endpoint in self.dict_endpoint.values():
            list_result.append([*endpoint.get_average()])
        list_result = sorted(list_result, key=lambda x: x[1], reverse=True)
        table = tabulate(list_result, tablefmt="fancy_grid", showindex=range(1, len(list_result) + 1), headers=[
                         '№', 'handler', 'total', 'avg_response_time'])
        print(table)
