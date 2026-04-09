#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试按行分割功能
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
import config_data as config

def test_line_split():
    """测试按行分割"""
    
    print("=== 当前配置参数 ===")
    print(f"chunk_size: {config.chunk_size}")
    print(f"chunk_overlap: {config.chunk_overlap}")
    print(f"separators: {repr(config.separators)}")
    print(f"max_split_char_number: {config.max_split_char_number}")
    print()
    
    # 创建分割器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=config.separators,
        length_function=len
    )
    
    # 测试文本（尺码推荐内容，每行一个尺码信息）
    test_text = """身高：155-165cm， 体重：75-95 斤，建议尺码S。
身高：160-170cm， 体重：90-115斤，建议尺码M。
身高：165-175cm， 体重：115-135斤，建议尺码L。
身高：170-178cm， 体重：135-160斤，建议尺码XL。
身高：178-185cm， 体重：160-180斤，建议尺码2XL。
身高：180-190cm， 体重：180-210斤，建议尺码3XL。
身高：190cm+，体重：210斤+，建议尺码4XL。"""
    
    print("=== 测试文本 ===")
    print(f"文本长度: {len(test_text)}")
    print("文本内容:")
    print(test_text)
    print()
    
    # 模拟knowledge_base.py中的逻辑
    print("=== 按行分割结果 ===")
    
    if len(test_text) > config.max_split_char_number:
        print("✓ 文本长度超过max_split_char_number，将进行分割")
        knowledge_chunks = splitter.split_text(test_text)
        print(f"✓ 分割后的文档数量: {len(knowledge_chunks)}")
        print()
        
        print("=== 分割结果详情 ===")
        for i, chunk in enumerate(knowledge_chunks):
            print(f"文档 {i+1} (长度: {len(chunk)}):")
            print(repr(chunk))
            print("---")
    else:
        print("✗ 文本长度小于max_split_char_number，不会分割")
        print("原文本将直接使用")

def test_manual_line_split():
    """手动按行分割对比"""
    
    print("\n" + "="*60)
    print("=== 手动按行分割对比 ===")
    
    test_text = """身高：155-165cm， 体重：75-95 斤，建议尺码S。
身高：160-170cm， 体重：90-115斤，建议尺码M。
身高：165-175cm， 体重：115-135斤，建议尺码L。
身高：170-178cm， 体重：135-160斤，建议尺码XL。
身高：178-185cm， 体重：160-180斤，建议尺码2XL。
身高：180-190cm， 体重：180-210斤，建议尺码3XL。
身高：190cm+，体重：210斤+，建议尺码4XL。"""
    
    # 手动按行分割
    manual_chunks = test_text.strip().split('\n')
    print(f"手动按行分割结果: {len(manual_chunks)} 个文档")
    
    for i, chunk in enumerate(manual_chunks):
        print(f"文档 {i+1}: {repr(chunk)}")

def test_edge_cases():
    """测试边界情况"""
    
    print("\n" + "="*60)
    print("=== 边界情况测试 ===")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=config.separators,
        length_function=len
    )
    
    # 测试空行
    test_cases = [
        "单行文本",
        "第一行\n第二行\n第三行",
        "第一行\n\n第三行",  # 有空行
        "",  # 空文本
        "\n\n\n",  # 只有换行符
    ]
    
    for i, text in enumerate(test_cases):
        print(f"\n测试 {i+1}:")
        print(f"输入: {repr(text)}")
        
        if text.strip():  # 非空文本
            chunks = splitter.split_text(text)
            print(f"分割结果: {len(chunks)} 个文档")
            for j, chunk in enumerate(chunks):
                print(f"  文档 {j+1}: {repr(chunk)}")
        else:
            print("空文本，不进行分割")

if __name__ == "__main__":
    test_line_split()
    test_manual_line_split()
    test_edge_cases()