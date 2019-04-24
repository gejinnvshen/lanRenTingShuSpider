import requests
import bs4
import os
import json
import re
import math
import sys
import time
import threading
from contextlib import closing
requests.packages.urllib3.disable_warnings()


# # 重写Thread
# class StoppableThread(threading.Thread):
#   def __init__(self, *args, **kwargs):
#       super(StoppableThread, self).__init__()
#       self._stop_event = threading.Event()
#   def stop(self):
#       self._stop_event.set()
#   def stopped(self):
#       return self._stop_event.is_set()


class Spider():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }
        print('[INFO]:Douyin App Video downloader...')
        print('[Version]: V2.0')
        print('[Author]: Charles')
    # 外部调用运行
    def run(self):
        user_id = input('Enter the ID:')
        wm = input('With WaterMark<1> or without<0>:')
        if wm == '1':
            mark = True
        elif wm == '0':
            mark = False
        else:
            print('[Error]:Enter cannot recognized...')
            return
        video_names, video_urls, nickname = self._parse_userID(user_id)
        if nickname not in os.listdir():
            os.mkdir(nickname)
        videos_num = len(video_urls)
        print('[INFO]:Number of Videos <%s>' % videos_num)
        def download(videos_num, start, thread_num, task_num):
            i = 0
            while True:
                if ((start+i) > (videos_num-0.5)) or (i > task_num-0.5):
                    # if thread_num == 0:
                    #   t.stop()
                    # elif thread_num == 1:
                    #   t1.stop()
                    # elif thread_num == 2:
                    #   t2.stop()
                    # elif thread_num == 3:
                    #   t3.stop()
                    # elif thread_num == 4:
                    #   t4.stop()
                    break
                print('[Thread %s]:Parsing <No.%d> <Url:%s>' % (thread_num, start+i+1, video_urls[start+i]))
                temp = video_names[start+i].replace('\\', '')
                video_name = str(thread_num) + '_' + str(i) + temp.replace('/', '')
                self._downloader(video_urls[start+i], os.path.join(nickname, video_name), mark)
                print('\n')
                time.sleep(1)
                i += 1
        # 开4个线程
        threads_num = 4.0
        if videos_num < 10:
            t = threading.Thread(target=download, args=(videos_num, 0, 0, videos_num))
            t.start()
        else:
            task_num = math.ceil(videos_num / threads_num)
            t1 = threading.Thread(target=download, args=(videos_num, 0, 1, task_num))
            t2 = threading.Thread(target=download, args=(videos_num, task_num, 2, task_num))
            t3 = threading.Thread(target=download, args=(videos_num, task_num*2, 3, task_num))
            t4 = threading.Thread(target=download, args=(videos_num, task_num*3, 4, task_num))
            t1.start()
            time.sleep(0.5)
            t2.start()
            time.sleep(0.5)
            t3.start()
            time.sleep(0.5)
            t4.start()
    # 视频下载
    def _downloader(self, video_url, path, mark):
        size = 0
        download_url = self._get_download_url(video_url, mark)
        with closing(requests.get(download_url, headers=self.headers, stream=True, verify=False)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                sys.stdout.write('[File Size]: %0.2f MB\n' % (content_size/chunk_size/1024))
                with open(path, 'wb') as f:
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        size += len(data)
                        f.flush()
                        sys.stdout.write('[Progress]: %0.2f%%' % float(size/content_size*100) + '\r')
                        sys.stdout.flush()
    # 获得视频下载地址
    def _get_download_url(self, video_url, mark=True):
        res = requests.get(url=video_url, verify=False, headers=self.headers)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        script = soup.find_all('script')[-1]
        video_url_js = re.findall('var data = \[(.+)\];', str(script))[0]
        html = json.loads(video_url_js)
        download_url = html['video']['play_addr']['url_list'][0]
        return download_url if mark else download_url.replace('playwm', 'play')
    # 通过user_id获取该用户发布的所有视频
    def _parse_userID(self, user_id):
        video_names = []
        video_urls = []
        unique_id = ''
        while unique_id != user_id:
            search_url = 'https://api.amemv.com/aweme/v1/discover/search/?keyword={}&count=1&type=1&aid=1128'.format(user_id)
            res = requests.get(url=search_url, verify=False, headers=self.headers)
            res_dic = json.loads(res.text)
            print(res_dic)
            uid = res_dic['user_list'][0]['user_info']['uid']
            aweme_count = res_dic['user_list'][0]['user_info']['aweme_count']
            nickname = res_dic['user_list'][0]['user_info']['nickname']
            unique_id = res_dic['user_list'][0]['user_info']['unique_id']
        # 若视频数量和实际不符，可将最后的aweme_count改为aweme_count+10
        user_url = 'https://www.douyin.com/aweme/v1/aweme/post/?user_id={}&max_cursor=0&count={}'.format(uid, aweme_count)
        res = requests.get(url=user_url, verify=False, headers=self.headers)
        res_dic = json.loads(res.text)
        i = 1
        for each in res_dic['aweme_list']:
            share_desc = each['share_info']['share_desc']
            if '抖音-原创音乐短视频社区' == share_desc:
                video_names.append(str(i) + '.mp4')
                i += 1
            else:
                video_names.append(share_desc + '.mp4')
            video_urls.append(each['share_info']['share_url'])
        return video_names, video_urls, nickname




if __name__ == '__main__':
    sp = Spider()
    sp.run()
    # while True:
    #   sp.run()
    #   print('[INFO]:All done,restart...')



