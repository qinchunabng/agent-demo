#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文本分割器
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
import config_data as config

def test_splitter():
    """测试文本分割器"""
    
    # 创建分割器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=config.separators,
        length_function=len
    )
    
    # 测试文本
    test_text = """这是第一段内容。

这是第二段内容！

这是第三段内容？

这是第四段内容！

这是第五段内容。"""
    
    print("=== 测试文本 ===")
    print(test_text)
    print(f"文本长度: {len(test_text)}")
    print(f"chunk_size: {config.chunk_size}")
    print(f"chunk_overlap: {config.chunk_overlap}")
    print(f"separators: {config.separators}")
    print(f"max_split_char_number: {config.max_split_char_number}")
    print()
    
    # 测试分割
    print("=== 分割结果 ===")
    chunks = splitter.split_text(test_text)
    print(f"分割后的块数: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"块 {i+1} (长度: {len(chunk)}): {repr(chunk)}")
    
    print()
    
    # 测试边界条件
    print("=== 边界条件测试 ===")
    short_text = "这是一个很短的文本。"
    print(f"短文本长度: {len(short_text)}")
    
    if len(short_text) > config.max_split_char_number:
        chunks_short = splitter.split_text(short_text)
        print(f"短文本分割块数: {len(chunks_short)}")
    else:
        print("短文本未分割（长度小于max_split_char_number）")

if __name__ == "__main__":
    test_splitter()