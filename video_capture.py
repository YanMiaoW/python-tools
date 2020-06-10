import cv2 as cv
import numpy
import click
import os
import time


'''
example:
python video_capture.py
python video_capture.py --scale 0.6 --begin-id 229 --begin-video-filename hiv00084.mp4 
'''

@click.command()
@click.option('--videos-path', default=r'E:\Desktop\YM', type=str,
              help="视频文件夹路径")
@click.option('--scale', default=None, type=float,
              help="屏幕缩放系数")
@click.option('--save-path', default=r'E:\Desktop\image_spyder\road_sign', type=str,
              help="截取的图像保存路径")
@click.option('--begin-id', default=1, type=int,
              help="开始的图片id")
@click.option('--begin-video-filename', default=None, type=str,
              help="开始的图片id")
@click.option('--cover/--no-cover',is_flag=True,
              help="覆盖截图图像")
def main(videos_path,scale,save_path,begin_id,begin_video_filename,cover):
    '''图片截图脚本，将视频放在一个文件夹里，运行此脚本会自动搜索该文件夹下面所有的视频，按顺序播放。
    在这个过程中，可以按【d】开启下一个视频，按【a】开启上一个视频，如播放时间超过10秒，重播此视频。
    按【s】保存这一帧图像，按【esc】结束进程，按【w】暂停和恢复，按【e】跳过5秒。


    '''
    #遍历文件夹树，提取出所有视频
    def iter_folder_tree(rootdir):
        '''遍历整个文件夹树，将所有视频文件的路径提取出来'''
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                path = os.path.join(subdir, file)
                if os.path.basename(path).endswith('.mp4') or \
                    os.path.basename(path).endswith('.avi'):
                    yield path

    def save_frame(frame,save_image_id):
        path =f'{save_path}/{str(save_image_id).zfill(5)}.jpg'
        if not cover:
            idx=1
            while os.path.exists(path):
                path=f'{save_path}/{str(save_image_id).zfill(5)}_{idx}.jpg'
                idx+=1
        cv.imwrite(path, frame)

    #保存图片的id
    save_image_id=begin_id

    video_paths_list=[video_path for video_path in iter_folder_tree(videos_path)]

    video_id=0

    while video_id < len(video_paths_list):
        #当前视频路径
        video_path = video_paths_list[video_id]

        #当前视频文件名
        video_filename=os.path.basename(video_path)
        print(video_path)

        if begin_video_filename:
            if video_filename != begin_video_filename:
                video_id+=1
                continue
            else:
                begin_video_filename=None



        #开启视频流
        cap = cv.VideoCapture(video_path)
        if not cap.isOpened():
            video_id+=1
            continue

        #视频帧数
        fps=cap.get(cv.CAP_PROP_FPS)

        #记录打开时间
        open_time=time.process_time()
        # print(open_time)

        # 视频流
        while True:
            #读取视频
            ret, frame = cap.read()
            if not ret:
                break
            # print(ret,frame)
            # show a frame
            #显示图片缩放
            if scale:
                frame2=cv.resize(frame,(0,0),fx=scale,fy=scale,interpolation=cv.INTER_AREA)
                cv.imshow(video_filename, frame2)
            else:
                cv.imshow(video_filename, frame)
            key = cv.waitKey(1)
            # print(key)
            #按【esc】键退出
            if key == ord('\033'):
                exit()
            #按【d】下一个视频
            elif key == ord('d'):
                break
            #按【a】上一个视频
            elif key == ord('a'):
                time_interval=time.process_time()-open_time
                if time_interval>10:
                    video_id-=1
                else:
                    video_id-=2
                break
            #按【s】保存这一帧
            elif key == ord('s'):
                save_frame(frame,save_image_id)
                save_image_id+=1
            #按【w】暂停和恢复
            elif key == ord('w'):
                while True:
                    key2=cv.waitKey(0)
                    if key2 == ord('w'):
                        break
                    elif key2 == ord('s'):
                        save_frame(frame,save_image_id)
                        save_image_id += 1
            #按【e】跳过5秒
            elif key == ord('e'):
                for i in range(int(5*fps)):
                    if not cap.grab():
                        break

        #关闭页面
        cv.destroyAllWindows()


        #视频结束，切换到下一个视频
        video_id+=1





if __name__ == '__main__':
    main()