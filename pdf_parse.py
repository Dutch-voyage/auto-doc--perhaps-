from zai import ZhipuAiClient
import argparse

client = ZhipuAiClient(api_key="a47d0cf3ca5943fd9eaaf48d7d47ef9f.LsCBmp8Hicfywyq6")

def file_parser_sync_example(input_path, output_path):
    """
    示例：提交文件解析任务并等待结果返回。
    """
    # 创建解析任务
    # 使用命令行参数指定的文件路径
    file_path = input_path
    with open(file_path, 'rb') as f:
        print("正在提交文件解析任务 ...")
        response = client.file_parser.create_sync(
            file=f,
            file_type="pdf",
            tool_type="prime-sync",
        )
        print("任务创建成功，响应如下：")

    # 使用命令行参数指定的输出路径
    md_file_name = output_path

    # 确保输出目录存在
    import os
    os.makedirs(os.path.dirname(md_file_name), exist_ok=True)

    with open(md_file_name, 'w', encoding='utf-8') as f:
        f.write(f"{response.content}")

    print("File parser demo completed.")

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='PDF文件解析工具')
    parser.add_argument('input_path', help='输入PDF文件的路径')
    parser.add_argument('output_path', help='输出Markdown文件的路径')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    file_parser_sync_example(args.input_path, args.output_path)
