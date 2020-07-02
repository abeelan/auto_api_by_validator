import logging
import requests
from config import get_params_ini
from requests_toolbelt import MultipartEncoder


_timeout = get_params_ini.GetParamsIni().get_timeout()


def request(method, url, data=None, headers=None, cookies=None, timeout=int(_timeout)):
    if not url.startswith('http://'):
        url = 'http://%s' % url

    try:
        response = requests.request(
            method=method,
            url=url,
            params=data,
            headers=headers,
            cookies=cookies,
            timeout=timeout
        )

    except requests.RequestException as e:
        logging.error('RequestException URL : %s' % url)
        logging.error('RequestException Info: %s' % e)
        return

    except Exception as e:
        logging.error('Exception URL : %s' % url)
        logging.error('Exception Info: %s' % e)
        return

    time_total = response.elapsed.total_seconds()
    status_code = response.status_code

    logging.info("-" * 100)
    logging.info('[ api name    ] : {}'.format(url.rsplit("/")[-1]))
    logging.info('[ request url ] : {}'.format(response.url))
    logging.info('[ method      ] : {}'.format(method.upper()))
    logging.info('[ status code ] : {}'.format(status_code))
    logging.info('[ time total  ] : {} s'.format(time_total))

    if "application/json" in response.headers.get("Content-Type"):
        logging.info('[ response json ] : %s' % response.json())
    else:
        logging.info('[ response text ] : %s' % response.text)
    logging.info("-" * 100)

    return response


def get(url: str, params=None, headers=None, cookies=None):
    return request('GET', url=url, data=params, headers=headers, cookies=cookies)


def post(url: str, params=None, form_data=None, headers=None, cookies=None):
    data = {**params, **form_data}
    return request('POST', url=url, data=data, headers=headers, cookies=cookies)


def put(url: str, data=None, headers=None, cookies=None):
    return request('PUT', url=url, data=data, headers=headers, cookies=cookies)


def params_splicing_url(api, payload):
    """
    主要用于将post请求的参数拼接为URL
    :param api: API接口
    :param payload: 传参（dict）
    :return: URL
    """
    params = []
    for key in payload.keys():
        value = payload[key]
        param = key + '=' + str(value)
        params.append(param)
    url = api + '?' + '&'.join(params)
    return url


if __name__ == '__main__':

    pass
