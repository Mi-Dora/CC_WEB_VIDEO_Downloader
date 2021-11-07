# CC_WEB_VIDEO Downloader

Python downloader for CC_WEB_VIDEO dataset.

[Official Download Instruction](http://vireo.cs.cityu.edu.hk/webvideo/Download.htm)

### Single thread version

```shell
python download.py --save_path='./downloaded'
```

```shell
usage: download.py [-h] [--save_path SAVE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --save_path SAVE_PATH
                        Path to save the CC_WEB_VIDEO dataset to be downloaded

```

### Multi thread version

```shell
python download_multi_thread.py --save_path='./downloaded' --num_thread=8
```

```shell
usage: download_multi_thread.py [-h] [--save_path SAVE_PATH] [--num_thread NUM_THREAD] [--no_keyframes] [--no_videos]

optional arguments:
  -h, --help            show this help message and exit
  --save_path SAVE_PATH
                        Path to save the CC_WEB_VIDEO dataset to be downloaded.
  --num_thread NUM_THREAD
                        Number of thread using for downloading.
  --no_keyframes        Whether download Keyframes.
  --no_videos           Whether download videos.

```

The dataset provider suggest to use single thread to avoid the overload of the server. So tradeoff the thread you need to use.
