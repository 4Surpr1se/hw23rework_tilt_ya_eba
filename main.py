import os
import re
from re import Pattern
from typing import Optional, Dict, List, Set, Union, Iterable, AnyStr

from flask import Flask, request, abort

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class QueryExeption(Exception):
    pass


def build_query(it: Iterable[str], cmd: Optional[str], value: str) -> Union[List[str], Set[str]]:
    psy: Iterable[str] = map(lambda v: v.strip(), it)
    res = psy
    if cmd == 'filter':
        res = list(filter(lambda v: value in v, res))
    if cmd == 'sort':
        sort_argument = bool(value)
        res = sorted(res, reverse=sort_argument)
    if cmd == 'unique':
        res = set(res)
    if cmd == 'limit':
        limit_argument: int = int(value)
        res = list(res)[:limit_argument]
    if cmd == 'map':
        map_argument = int(value)
        res = list(map(lambda l: l.split(' ')[map_argument], res))
    if cmd == 'regex':
        regex_argument: str = value
        regex: Pattern[str] = re.compile(regex_argument)
        res = list(filter(regex.findall, res))  # Read Note below
    else:
        res = ['']
    return res


def reply(file_name: str, cmd_list: List[str], value_list: List[str]) -> str:
    with open(f'./data/{file_name}') as file:
        it: Union[List[str], Set[str]] = build_query(file, cmd_list[0], value_list[0])
        it = build_query(it, cmd_list[1], value_list[1])

    return '<br>'.join(it)


@app.route("/perform_query")
def perform_query() -> str:
    cmd_list = []
    value_list = []
    try:
        request_args: Dict[str, str] = request.args
        for k, v in request_args.items():
            if k not in ['cmd1', 'value1', 'cmd2', 'value2', 'file_name']:
                raise QueryExeption
        cmd_list.extend([request_args.get('cmd1', ''), request_args.get('cmd2', '')])
        value_list.extend([request_args.get('value1', ''), request_args.get('value2', '')])
        file_name: str = request_args['file_name']
    except QueryExeption as e:
        abort(501, e)

    try:
        with open(f'./data/{file_name}') as f:
            pass
    except FileNotFoundError as e:
        abort(401, e)

    return reply(file_name, cmd_list, value_list)


if __name__ == '__main__':
    app.run()
