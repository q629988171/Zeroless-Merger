import argparse

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
    parser.add_argument('--video_file', help='视频文件的路径')
    parser.add_argument('--audio_file', help='音频文件的路径')
    parser.add_argument('--output_file', help='输出文件的路径')
    # 解析命令行参数
    args = parser.parse_args()
    # 移除视频和音频文件开头的9个0字节
    remove_nine_zeros(args.video_file, args.video_file)
    remove_nine_zeros(args.audio_file, args.audio_file)
    # 合并视频和音频文件
    merge_video_audio(args.video_file, args.audio_file, args.output_file)


if __name__ == '__main__':
    main()
