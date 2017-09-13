#!usr/bin/env python
# coding:utf8

import requests
from bs4 import BeautifulSoup
import json
import time


def crawl_detail(id):
    url = 'https://www.lagou.com/jobs/%s.html' % id
    print url
    headers = {
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E4%B8%8A%E6%B5%B7',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Cookie': 'user_trace_token=20170913151819-ff2db943-63cf-4eaa-b288-a84c9991fd79; LGUID=20170913151820-b870d604-9853-11e7-9173-5254005c3644; index_location_city=%E4%B8%8A%E6%B5%B7; SEARCH_ID=d650ae0343b6420db9f0f19f0bc1a03e; JSESSIONID=ABAAABAACDBAAIA9E052CFCFACA1D96C6F461A01DC5B624; TG-TRACK-CODE=search_code; _gid=GA1.2.184956781.1505287101; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505287102; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505297109; _ga=GA1.2.798149322.1505287101; LGSID=20170913173412-b38460e7-9866-11e7-915c-525400f775ce; '
                  'LGRID=20170913180507-052fef54-986b-11e7-9163-525400f775ce',
    }
    result = requests.post(url=url, headers=headers, timeout=20)
    soup = BeautifulSoup(result.content, 'html.parser')
    job_bt = soup.find('dd', attrs={'class': 'job_bt'})
    return job_bt.text


def main():
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false&isSchoolJob=0'
    headers = {
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E4%B8%8A%E6%B5%B7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'user_trace_token=20170913151819-ff2db943-63cf-4eaa-b288-a84c9991fd79; LGUID=20170913151820-b870d604-9853-11e7-9173-5254005c3644; index_location_city=%E4%B8%8A%E6%B5%B7; JSESSIONID=ABAAABAACDBAAIA9E052CFCFACA1D96C6F461A01DC5B624; TG-TRACK-CODE=search_code; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505287102; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505297155; _gid=GA1.2.184956781.1505287101; _ga=GA1.2.798149322.1505287101; LGSID=20170913173412-b38460e7-9866-11e7-915c-525400f775ce; LGRID=20170913180554-21468c07-986b-11e7-9163-525400f775ce; SEARCH_ID=1b9e956a0d2b42c6b11023766a491034'
    }

    positions = []
    for x in range(1, 16):
        form_data = {
            'first': 'false',
            'pn': x,
            'kd': 'Python',
        }
        result = requests.post(url=url, headers=headers, data=form_data, timeout=20)
        json_result = result.json()
        page_positions = json_result['content']['positionResult']['result']
        # 爬取详情
        for position in page_positions:
            position_dict = {
                "positionName": position['positionName'],
                "workYear": position['workYear'],
                "salary": position['salary'],
                "district": position['district'],
                "companyFullName": position['companyFullName'],
            }
            position_id = position["positionId"]
            position_detail = crawl_detail(position_id)
            position_dict['position_detail'] = position_detail
            positions.append(position_dict)
            #time.sleep(0.5)

        print unicode(page_positions)
        #time.sleep(1)

    line = json.dumps(positions, ensure_ascii=False)
    with open('lagou.json', 'w') as fp:
        fp.write(line.encode('utf-8'))


if __name__ == '__main__':
    main()
