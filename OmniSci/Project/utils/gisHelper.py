import requests


class GisHelper:
    def fetch_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 真实ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 代理ip

        return ip

    def gaode(self,ip):
    # 高德地图
        key = '4d13ff9018b5357695f1b354ef63ee33'
        res = requests.get("http://restapi.amap.com/v3/ip?ip={}&key={}".format(ip,key)).json()
        return res

    def baidu(self,ip):
    # 百度地图
        key = 'fqgI2Qs4waaabpnHz8dR3n01lYWxm8NY&coor=bd09ll'
        res = requests.get("http://api.map.baidu.com/location/ip?ip={}&ak={}".format(ip,key)).json()
        return res

    # 高德地图status=1表示成功,百度地图status=0表示成功
    '''
        高德地图
    {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "province": "北京市",
        "city": "北京市",
        "adcode": "110000",
        "rectangle": "116.0119343,39.66127144;116.7829835,40.2164962"
    }
    百度地图
    {
        "address": "CN|北京|北京|None|DXTNET|0|0",
        "content": {
            "address": "北京市",
            "address_detail": {
                "city": "北京市",
                "city_code": 131,
                "district": "",
                "province": "北京市",
                "street": "",
                "street_number": ""
            },
            "point": {
                "x": "116.40387397",
                "y": "39.91488908"
            }
        },
        "status": 0
    }
    '''

    def query(self,ip):
        res = self.gaode(ip)
        if res.get('status') == '1' and res['city'] != []:
            return res['city'],res['province']
        else:
            res = self.baidu(ip)
            if res.get('status') == 0:
                print(res)
                return res['content']['address'], res['content']['address_detail']['province']
            else:
                return '', ''

