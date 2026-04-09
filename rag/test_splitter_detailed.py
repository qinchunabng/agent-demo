#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细测试文本分割器
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
import config_data as config

def test_with_long_text():
    """测试长文本分割"""
    
    # 创建分割器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=config.separators,
        length_function=len
    )
    
    # 创建长文本（超过max_split_char_number）
    long_text = """这是第一段内容。这是第一段内容。这是第一段内容。这是第一段内容。这是第一段内容。

这是第二段内容！这是第二段内容！这是第二段内容！这是第二段内容！这是第二段内容！

这是第三段内容？这是第三段内容？这是第三段内容？这是第三段内容？这是第三段内容？

这是第四段内容！这是第四段内容！这是第四段内容！这是第四段内容！这是第四段内容！

这是第五段内容。这是第五段内容。这是第五段内容。这是第五段内容。这是第五段内容。

这是第六段内容。这是第六段内容。这是第六段内容。这是第六段内容。这是第六段内容。

这是第七段内容。这是第七段内容。这是第七段内容。这是第七段内容。这是第七段内容。

这是第八段内容。这是第八段内容。这是第八段内容。这是第八段内容。这是第八段内容。

这是第九段内容。这是第九段内容。这是第九段内容。这是第九段内容。这是第九段内容。

这是第十段内容。这是第十段内容。这是第十段内容。这是第十段内容。这是第十段内容。"""
    
    print("=== 长文本分割测试 ===")
    print(f"文本长度: {len(long_text)}")
    print(f"max_split_char_number: {config.max_split_char_number}")
    
    if len(long_text) > config.max_split_char_number:
        chunks = splitter.split_text(long_text)
        print(f"分割后的块数: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            print(f"块 {i+1} (长度: {len(chunk)}): {repr(chunk[:50])}...")
    else:
        print("文本长度小于max_split_char_number，不会被分割")
    
    print()

def test_separators():
    """测试分隔符"""
    
    # 创建分割器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,  # 设置较小的chunk_size
        chunk_overlap=20,
        separators=config.separators,
        length_function=len
    )
    
    # 测试不同分隔符
    test_cases = [
        ("句号分隔。这是第二句。", "句号分隔"),
        ("感叹号分隔！这是第二句！", "感叹号分隔"),
        ("问号分隔？这是第二句？", "问号分隔"),
        ("换行分隔\n这是第二行", "换行分隔"),
        ("双换行分隔\n\n这是第二段", "双换行分隔"),
        ("空格分隔 这是第二部分", "空格分隔"),
    ]
    
    print("=== 分隔符测试 ===")
    for i, (test_text, description) in enumerate(test_cases):
        print(f"测试 {i+1}: {description}")
        print(f"测试文本: {repr(test_text)}")
        chunks = splitter.split_text(test_text)
        print(f"分割结果: {len(chunks)} 块")
        for j, chunk in enumerate(chunks):
            print(f"  块 {j+1}: {repr(chunk)}")
        print()

def test_real_scenario():
    """模拟真实场景"""
    
    # 读取实际文件
    try:
        with open("../data/尺码推荐.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            
        print("=== 实际文件测试 ===")
        print(f"文件长度: {len(content)}")
        print(f"max_split_char_number: {config.max_split_char_number}")
        
        if len(content) > config.max_split_char_number:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap,
                separators=config.separators,
                length_function=len
            )
            chunks = splitter.split_text(content)
            print(f"分割后的块数: {len(chunks)}")
            print("前5个块预览:")
            for i in range(min(5, len(chunks))):
                print(f"块 {i+1} (长度: {len(chunks[i])}): {repr(chunks[i][:100])}...")
        else:
            print("文件长度小于max_split_char_number，不会被分割")
            
    except FileNotFoundError:
        print("测试文件不存在")

if __name__ == "__main__":
    test_with_long_text()
    test_separators()
    test_real_scenario()