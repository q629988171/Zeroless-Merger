import argparse
import os
import tempfile

import ffpb


def remove_nine_zeros(filename, new_filename):
    """以二进制读取模式打开文件移除开头9个0字节

    :param filename: 要修改的文件
    :param new_filename: 保持后的文件
    :return:
    """
    # 二进制方式打开文件
    with open(filename, 'rb') as file:
        data = file.read()

    # 检查并移除开头的9个0字节
    if data.startswith(b'0' * 9):
        data = data[9:]

    # 将修改后的数据写回文件或保存到新文件
    with open(new_filename, 'wb') as file:
        file.write(data)


def merge_video_audio(video_file, audio_file, output_file):
    """
    使用ffmpeg合并视频和音频文件。

    :param video_file: 视频文件的路径
    :param audio_file: 音频文件的路径
    :param output_file: 输出文件的路径
    """
    ffpb.main(
        [
            "-i", video_file,
            "-i", audio_file,
            "-c", "copy",
            output_file
        ]
    )


def main():
    # 创建一个ArgumentParser对象
    parser = argparse.ArgumentParser(description='移除开头的9个0字节，并合并视频和音频文件。')
    # 添加参数
    parser.add_argument('--video_file', help='视频文件的路径', required=True)
    parser.add_argument('--audio_file', help='音频文件的路径', required=True)
    parser.add_argument('--output_file', help='输出文件的路径', required=True)
    # 解析命令行参数
    args = parser.parse_args()
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False) as video_temp, \
            tempfile.NamedTemporaryFile(delete=False) as audio_temp:
        # 移除视频和音频文件开头的9个0字节，并保存到临时文件
        remove_nine_zeros(args.video_file, video_temp.name)
        remove_nine_zeros(args.audio_file, audio_temp.name)
        # 合并视频和音频文件
        merge_video_audio(video_temp.name, audio_temp.name, args.output_file)

    # 显式地删除临时文件
    os.remove(video_temp.name)
    os.remove(audio_temp.name)


if __name__ == '__main__':
    main()
