import urllib

from flask import json

import pandas as pd
from flask import Blueprint, render_template  # 导入 Flask 中的蓝图 Blueprint 模块
from flask import request

app_api = Blueprint("api", __name__, static_folder="static", template_folder="templates")
LA51FLOWDAYURL = 'https://web.51.la/report/flow/day?comId=%s'
# 　仅允许如下comId访问，避免滥用,如果为空则不限制comId
comIdList = list()
headers = { 'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.88Safari/537.36'}


def transDf2MultiChartsMap(dataDf, extMap={}, typeMap={}, yAxisIndexMap={}):
    seriesList = list()
    for column in dataDf.columns.to_list():
        # name: '邮件营销',
        # type: 'line',
        # stack: '总量',
        # data: [120, 132, 101, 134, 90, 230,
        tmpMap = dict()
        tmpMap['name'] = column
        tmpMap['type'] = typeMap.get(column, 'line')
        tmpMap['yAxisIndex'] = yAxisIndexMap.get(column, 0)
        tmpMap['stack'] = column
        tmpMap['data'] = dataDf[column].to_list()
        seriesList.append(tmpMap)

    resultMap = dict()
    resultMap['legend_data'] = dataDf.columns.to_list()
    resultMap['xAxis_data'] = dataDf.index.to_list()
    resultMap['series'] = seriesList
    resultMap.update(extMap)
    return json.dumps(resultMap, default=str,encoding='utf8')


@app_api.route('/la51FlowDay', methods=['get'])
def la51FlowDay():
    comId = request.args.get('comId')
    startDate = request.args.get('startDate', '2020-01-01')
    if comIdList and (not comId or comId not in comIdList):
        return "{}"
    allMaps = dict()
    allMaps['comId'] = comId
    allMaps['startDate'] = startDate
    return render_template('api/la51FlowDay.html', **allMaps)


@app_api.route('/echarts/la51FlowDay', methods=['get'])
def echarts_la51FlowDay():
    comId = request.args.get('comId')
    if comIdList and (not comId or comId not in comIdList):
        return "{}"
    htmlUrl = LA51FLOWDAYURL % comId
    req = urllib.request.Request(htmlUrl, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode()
    htmlPdList = pd.read_html(data)
    recent30Df = htmlPdList[0][:-1]
    recent30Df = recent30Df[['时间', '页面浏览量(PV)', '访客数(UV)']].set_index(['时间']).sort_index()
    return transDf2MultiChartsMap(recent30Df)
