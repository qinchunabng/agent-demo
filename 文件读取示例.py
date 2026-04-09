#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python文件读取示例
演示多种读取文本文件的方法
"""

import os

def read_whole_file(file_path):
    """方法1：读取整个文件内容"""
    print("=== 方法1：读取整个文件 ===")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
            print(f"文件总字符数: {len(content)}")
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
    print()

def read_line_by_line(file_path):
    """方法2：逐行读取"""
    print("=== 方法2：逐行读取 ===")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line_number = 1
            for line in file:
                print(f"第{line_number}行: {line.strip()}")
                line_number += 1
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
    print()

def read_all_lines(file_path):
    """方法3：读取所有行到列表"""
    print("=== 方法3：读取所有行到列表 ===")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"总共有 {len(lines)} 行")
            for i, line in enumerate(lines, 1):
                print(f"第{i}行: {line.strip()}")
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
    print()

def read_with_readline(file_path):
    """方法4：使用readline()逐行读取"""
    print("=== 方法4：使用readline()逐行读取 ===")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line_number = 1
            line = file.readline()
            while line:
                print(f"第{line_number}行: {line.strip()}")
                line = file.readline()
                line_number += 1
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
    print()

def read_with_chunks(file_path, chunk_size=10):
    """方法5：分块读取大文件"""
    print("=== 方法5：分块读取（适合大文件） ===")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            chunk_number = 1
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                print(f"块{chunk_number}: {repr(chunk)}")
                chunk_number += 1
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
    print()

def check_file_info(file_path):
    """检查文件信息"""
    print("=== 文件信息 ===")
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        print(f"文件路径: {file_path}")
        print(f"文件大小: {file_size} 字节")
        print(f"文件存在: 是")
    else:
        print(f"文件不存在: {file_path}")
    print()

def main():
    """主函数"""
    file_path = "D:\\Workspace\\ai\\agent-demo\\示例文本.txt"
    
    # 检查文件信息
    check_file_info(file_path)
    
    # 演示各种读取方法
    read_whole_file(file_path)
    read_line_by_line(file_path)
    read_all_lines(file_path)
    read_with_readline(file_path)
    read_with_chunks(file_path, chunk_size=15)

if __name__ == "__main__":
    main()