#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试文本分割功能
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
import config_data as config

def test_split_functionality():
    """测试分割功能"""
    
    print("=== 当前配置参数 ===")
    print(f"chunk_size: {config.chunk_size}")
    print(f"chunk_overlap: {config.chunk_overlap}")
    print(f"separators: {config.separators}")
    print(f"max_split_char_number: {config.max_split_char_number}")
    print()
    
    # 创建分割器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=config.separators,
        length_function=len
    )
    
    # 测试文本（模拟尺码推荐内容）
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
    print("=== 模拟knowledge_base.py分割逻辑 ===")
    
    if len(test_text) > config.max_split_char_number:
        print("✓ 文本长度超过max_split_char_number，将进行分割")
        knowledge_chunks = splitter.split_text(test_text)
        print(f"✓ 分割后的文档数量: {len(knowledge_chunks)}")
        print()
        
        print("=== 分割结果详情 ===")
        for i, chunk in enumerate(knowledge_chunks):
            print(f"块 {i+1} (长度: {len(chunk)}):")
            print(repr(chunk))
            print("---")
    else:
        print("✗ 文本长度小于max_split_char_number，不会分割")
        print("原文本将直接使用")

def test_separators_effect():
    """测试分隔符效果"""
    
    print("\n" + "="*60)
    print("=== 分隔符效果测试 ===")
    
    # 创建较小的分割器用于测试分隔符
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=50,  # 小尺寸便于观察分隔效果
        chunk_overlap=10,
        separators=config.separators,
        length_function=len
    )
    
    test_cases = [
        "第一句。第二句。第三句。",
        "第一句！第二句！第三句！",
        "第一句？第二句？第三句？",
        "第一句\n第二句\n第三句",
        "第一句\n\n第二句\n\n第三句",
    ]
    
    for i, text in enumerate(test_cases):
        print(f"\n测试 {i+1}:")
        print(f"输入: {repr(text)}")
        chunks = splitter.split_text(text)
        print(f"分割结果: {len(chunks)} 块")
        for j, chunk in enumerate(chunks):
            print(f"  块 {j+1}: {repr(chunk)}")

if __name__ == "__main__":
    test_split_functionality()
    test_separators_effect()