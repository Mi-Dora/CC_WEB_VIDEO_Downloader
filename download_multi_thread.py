from urllib import request, error
import os
import argparse
import tqdm
import threading


server_path = 'http://vireo.cs.cityu.edu.hk/webvideo/'
videos_path = server_path + 'videos/'
keyframes_path = server_path + 'Keyframes/'


def download_url(url, to_save, try_time=10, miss_file=''):
    for i in range(0, try_time):
        try:
            if not os.path.exists(to_save):
                request.urlretrieve(url, to_save)
                return 0
            else:
                # print(to_save, ' exists.')
                return 1
        except:
            continue
    with open(miss_file, 'a') as f:
        f.write(url + '\n')
    print(url, ' missing!')
    return -1


def read_file_info(file_path):
    infos = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            infos.append(line.rstrip('\n').split('\t'))
    return infos


def download_videos(infos, num_thread):
    print('Downloading Vidoes')
    print('Using %d threads' % num_thread)
    pbar = tqdm.tqdm(total=len(infos))
    num_info = len(infos)

    def thread_download(tid, num_t):
        print('Thread %d begin downloading' % tid)
        for i in range(0, (num_info//num_t)+1):
            if tid+i*num_t >= num_info:
                return
            info = infos[tid+i*num_t]
            QueryID, VideoName = info[1], info[3]
            url = videos_path + QueryID + '/' + VideoName
            os.makedirs(path_save_video + QueryID, exist_ok=True)
            to_save = path_save_video + QueryID + '/' + VideoName
            ret = download_url(url, to_save, miss_file='miss_video.txt')
            if ret == 0 or ret == 1:
                # print(to_save, ' saved.')
                pbar.update(1)

    thread_list = []
    for i in range(num_thread):
        thread_list.append(threading.Thread(target=thread_download, args=(i, num_thread)))
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    pbar.close()


def download_Keyframes(infos, num_thread):
    print('Downloading Keyframes')
    print('Using %d threads' % num_thread)
    pbar = tqdm.tqdm(total=len(infos))
    num_info = len(infos)

    def thread_download(tid, num_t):
        print('Thread %d begin downloading' % tid)
        for i in range(0, (num_info//num_t)+1):
            if tid+i*num_t >= num_info:
                return
            info = infos[tid+i*num_t]
            KeyframeName, VideoID = info[1], info[2]
            KID = str(int(VideoID) // 100)
            url = keyframes_path + KID + '/' + KeyframeName + '.jpg'
            os.makedirs(path_save_keyframes + KID, exist_ok=True)
            to_save = path_save_keyframes + KID + '/' + KeyframeName + '.jpg'
            ret = download_url(url, to_save, miss_file='miss_keyframe.txt')
            if ret == 0 or ret == 1:
                # print(to_save, ' saved.')
                pbar.update(1)

    thread_list = []
    for i in range(num_thread):
        thread_list.append(threading.Thread(target=thread_download, args=(i, num_thread)))
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    pbar.close()


parser = argparse.ArgumentParser()
parser.add_argument('--save_path', type=str, default='downloaded/',
                    help='Path to save the CC_WEB_VIDEO dataset to be downloaded.')
parser.add_argument('--num_thread', type=int, default=8,
                    help='Number of thread using for downloading.')
parser.add_argument('--no_keyframes', action="store_false",
                    help='Whether download Keyframes.')
parser.add_argument('--no_videos', action="store_false",
                    help='Whether download videos.')
args = parser.parse_args()
save_path = args.save_path
num_thread = args.num_thread
path_save_video = save_path + 'videos/'
path_save_keyframes = save_path + 'Keyframes/'
if args.no_keyframes:
    keyframe_infos = read_file_info('Shot_Info.txt')
    download_Keyframes(keyframe_infos, num_thread)
    print('Done.')
if args.no_videos:
    video_infos = read_file_info('Video_List.txt')
    download_videos(video_infos, num_thread)
    print('Done')

