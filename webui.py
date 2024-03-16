import gradio as gr
import subprocess
import tempfile
import os
import random
import string


def generate_random_filename(suffix='.mp4'):
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return os.path.join(tempfile.gettempdir(), f'{random_part}{suffix}')


def remove_nine_zeros(filename):
    # 二进制方式打开文件
    with open(filename, 'rb') as file:
        data = file.read()

    # 检查并移除开头的9个0字节
    if data.startswith(b'0' * 9):
        data = data[9:]

    # 创建临时文件并写入修改后的数据
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(data)
        return temp_file.name


def merge_video_audio(video_path, audio_path, output_path):
    """使用ffmpeg合并视频和音频文件"""
    try:
        subprocess.run(["ffmpeg", "-y", "-i", video_path, "-i", audio_path, "-c", "copy", output_path], check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg error: {e}")
        return None


def process_files(video_file, audio_file):
    """处理上传的文件并返回下载链接"""
    # 移除开头的9个0字节（这里逻辑可能有误，如上文所述）
    video_file_processed = remove_nine_zeros(video_file.name)
    audio_file_processed = remove_nine_zeros(audio_file.name)

    # 合并处理后的视频和音频文件
    output_path = generate_random_filename()
    result = merge_video_audio(video_file_processed, audio_file_processed, output_path)

    # 显式地删除临时文件
    temp_files = [video_file_processed, audio_file_processed]
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)

    # 返回下载链接
    if result:
        return output_path

    # 处理失败时返回None
    return None


def main():
    # 定义Gradio界面
    interface = gr.Interface(
        fn=process_files,
        inputs=[
            gr.File(label="上传视频文件"),
            gr.File(label="上传音频文件")
        ],
        outputs="file",
        title="视频和音频文件处理工具",
        description="上传视频和音频文件，移除开头的9个0字节并合并它们。",
        examples=[
            ["input_video.m4s", "input_audio.m4s"]  # 示例文件需要存在于运行目录中或提供正确的路径
        ]
    )

    # 启动Gradio应用
    interface.launch()


if __name__ == '__main__':
    main()
