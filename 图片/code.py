import re
import os
import requests
from requests.adapters import HTTPAdapter
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool,freeze_support
try:
    f = open('config.txt', 'r')
    config = str(f.read()).split('\n')
    page = config[0]
    fid = config[1]
    CLSQ = config[2]
except Exception as e:
    print("请在当前目录下创建config.txt, 请按顺序填写页码,fid,域名并敲回车!")


def SavePic(Item):
    try:
        try:
            AllHtml = queryurl("{}{}".format(CLSQ,Item['href']))
        except Exception as e:
            print(e)
            pass
        finally:
            pass
        soup = BeautifulSoup(AllHtml, 'lxml')
        datas = soup.find_all(attrs={"type": "image"})
        length = len(datas)
        dir_name = re.sub('[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+', '', (Item.string))
        dir = ("{}/{}/{}/{}/{}".format(os.getcwd(),time.strftime("%Y%m%d"), fid, page,dir_name.strip()))
        if not os.path.exists((dir)):
            os.makedirs((dir))

        for i in range(length):
            filename = os.path.basename(datas[i].attrs["src"])
            try:
                pic_content = queryurl(datas[i].attrs["src"])
            except Exception as e:
                print(e)
                pass
            finally:
                pass



            if(pic_content):
                picfile = '{}/{}'.format(dir,  filename)
                if os.path.exists(picfile):
                    print('{}此文件已存在'.format(picfile))
                else:
                    with open(file=picfile, mode='wb') as f:
                        f.write(pic_content)
                        f.close()
                    print("{}已保存".format(picfile))
    except Exception as e:
        print(e)
        pass
    finally:
        pass



def queryurl(URL):
    try:
        s = requests.Session()
        s.mount( 'http: //', HTTPAdapter(max_retries=2))
        s.mount('https: //', HTTPAdapter(max_retries=2))

        content=s.get(URL, timeout = 1)
        if content.status_code == 200:
            return content.content
        return None
    except Exception as e:
        print("失败链接:"+(URL))
        with open('error.txt', 'a') as f:
            f.write((URL )+ "\n")
        pass
    finally:
        pass


def main(offset):
    try:

        ClIndex = '{}thread0806.php?fid={}&search=&page={}'.format(CLSQ, fid, page)
        AllUrl = queryurl(ClIndex)
        soup = BeautifulSoup(AllUrl, 'lxml')
        data = soup.select('h3 a')
        for item in range(offset,offset+20):
            SavePic(data[item])
    except Exception as e:
        print(e)
        pass
    finally:
        pass


if __name__ == '__main__':
    freeze_support()
    group = [x * 20 for x in range(0, 5)]
    p = Pool()
    p.map(main, group)
    p.close()
    p.join()