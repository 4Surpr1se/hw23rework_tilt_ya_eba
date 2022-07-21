import os

from flask import Flask, request, abort

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class QueryExeption(Exception):
    pass

@app.route("/perform_query")
def perform_query():
    cmd_list = []
    value_list = []
    try:
        request_args = request.args
        for k, v in request_args.items():
            if k not in ['cmd1', 'value1', 'cmd2', 'value2', 'file_name']:
                raise QueryExeption  # error 400 вернуть
            # exec("%s = %d" % (k,v))
        cmd_list.extend([request_args.get('cmd1'), request_args.get('cmd2')])
        value_list.extend([request_args.get('value1'), request_args.get('value2')])
        file_name = request_args['file_name']
    except QueryExeption as e:
        abort(501, e)  # err 404 zabil kak

    try:
        with open(f'./data/{file_name}') as f:
            pass
    except FileNotFoundError as e:
        abort(401, e)

    def build_query(it, cmd, value):
        res = map(lambda v: v.strip(), it)
        if cmd == 'filter':
            res = list(filter(lambda v: value in v, res))
        if cmd == 'sort':
            value = bool(value)
            res = sorted(res, reverse=value)
        if cmd == 'unique':
            res = set(res)
        if cmd == 'limit':
            value = int(value)
            res = list(res)[:value]
        if cmd == 'map':
            value = int(value)
            res = list(map(lambda v: v.split(' ')[value], res))
        return res

    with open(f'./data/{file_name}') as file:
        res = build_query(file, cmd_list[0], value_list[0])
        res = build_query(res, cmd_list[1], value_list[1])
    # file = open(f'./data/{file_name}')
    # res = file.read()
    # file.close()
    # it = res.split('\n')
    # print(it)
    # it = build_query(it, cmd_list[0], value_list[0])
    # it = build_query(it, cmd_list[1], value_list[1])
    # print('\n'.join(it))

    return '<br>'.join(res)

if __name__ == '__main__':
    app.run()
