import os
import time

import click
import cv2 as cv

'''
example:
python video_frame_capture.py --videos-root "E:\Desktop\YM" --save-root "E:\Desktop\image_spyder\road_disease2"
python video_frame_capture.py -r "E:\Desktop\DCIM4-20200615" -s "E:\Desktop\image_spyder\road_disease2"  --screen-scale 0.6 --speed-up-rate 2 
'''


@click.command()
@click.option('-r', '--videos-root', type=str, required=True,
              help="存储视频文件的根目录")
@click.option('-s', '--save-path', type=str, required=True,
              help="截取的视频帧图像保存的根路径")
@click.option('--screen-scale', default=None, type=float,
              help="屏幕缩放系数，改变窗口大小百分比，不影响截取的帧，截取的帧是原始分辨率大小")
@click.option('--begin-video-filename', default=None, type=str,
              help="需要跳过前面的视频，从某个视频开始，需要输入这个视频名称")
@click.option('--speed-up-rate', default=2, type=int,
              help="加速速率大小, 默认2倍速")
def main(videos_root, save_path, screen_scale, begin_video_filename, speed_up_rate):
    '''
    图片截图脚本，将视频放在一个文件夹里，运行此脚本会自动搜索该文件夹下面所有的视频，按顺序播放。
    在这个过程中，可以按【d】开启下一个视频，按【a】开启上一个视频，如播放时间超过10秒，重播此视频。
    按【s】保存这一帧图像，按【Esc】结束进程，按【w】暂停和恢复，按【e】视频加速和恢复。
    '''

    # 遍历文件夹树，提取出所有视频
    def iter_folder_tree(rootdir):
        '''遍历整个文件夹树，将所有视频文件的路径提取出来'''
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                path = os.path.join(subdir, file)
                if os.path.basename(path).endswith('.mp4') or \
                        os.path.basename(path).endswith('.avi'):
                    yield path

    # 视频帧保存函数
    def save_frame(frame, save_image_id):
        path = f'{save_path}/{str(save_image_id).zfill(5)}.jpg'
        idx = 1
        while os.path.exists(path):
            path = f'{save_path}/{str(save_image_id).zfill(5)}_{idx}.jpg'
            idx += 1
        cv.imwrite(path, frame)

    # 如果保存路径不存在，便创建
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 保存图片的id
    save_image_id = 1

    # 遍历的所有视频路径字符串数组
    video_paths_list = [video_path for video_path in iter_folder_tree(videos_root)]

    video_id = 0

    # 视频播放速度
    video_speed = 1

    while video_id < len(video_paths_list):
        # 当前视频路径
        video_path = video_paths_list[video_id]

        # 当前视频文件名
        video_filename = os.path.basename(video_path)
        print(video_path)

        # 如果设置了begin_video_filename参数，则跳过前面的视频直到这个视频为止
        if begin_video_filename:
            if video_filename != begin_video_filename:
                video_id += 1
                continue
            else:
                begin_video_filename = None

        # 开启视频流
        cap = cv.VideoCapture(video_path)

        # 无效视频跳过
        if not cap.isOpened():
            video_id += 1
            continue

        # 记录视频打开时间
        open_time = time.process_time()
        # print(open_time)

        # 视频流
        while True:
            # 视频加速
            if video_speed > 1:
                r = 1
                ret = cap.grab()
                while ret and r < video_speed - 1:
                    ret = cap.grab()
                    r += 1
                if not ret:
                    break

            # 读取视频
            ret, frame = cap.read()

            # 到达视频尾帧，结束循环
            if not ret:
                break
            # print(ret,frame)

            # 帧缩放
            if screen_scale:
                frame2 = cv.resize(frame, (0, 0), fx=screen_scale, fy=screen_scale, interpolation=cv.INTER_AREA)
                cv.imshow(video_filename, frame2)
            else:
                cv.imshow(video_filename, frame)

            # 读取输入字符
            key = cv.waitKey(1)
            # print(key)

            # 按【Esc】键退出
            if key == ord('\033'):
                exit()

            # 按【d】下一个视频
            elif key == ord('d'):
                break

            # 按【a】上一个视频
            elif key == ord('a'):
                time_interval = time.process_time() - open_time
                if time_interval > 10:
                    video_id -= 1
                else:
                    video_id -= 2
                break

            # 按【s】保存这一帧
            elif key == ord('s'):
                save_frame(frame, save_image_id)
                save_image_id += 1

            # 按【w】暂停和恢复
            elif key == ord('w'):
                while True:
                    key2 = cv.waitKey(0)
                    if key2 == ord('w'):
                        break
                    elif key2 == ord('s'):
                        save_frame(frame, save_image_id)
                        save_image_id += 1

            # 按【e】加速和恢复
            elif key == ord('e'):
                video_speed = speed_up_rate if video_speed == 1 else 1

        # 关闭视频页面
        cv.destroyAllWindows()

        # 视频结束，切换到下一个视频
        video_id += 1


if __name__ == '__main__':
    main()
