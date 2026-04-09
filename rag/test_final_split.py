#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试按行分割功能
"""

import config_data as config

def test_line_split_logic():
    """测试按行分割逻辑"""
    
    print("=== 当前配置参数 ===")
    print(f"max_split_char_number: {config.max_split_char_number}")
    print()
    
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
    
    # 模拟修改后的knowledge_base.py中的逻辑
    print("=== 按行分割结果 ===")
    
    if len(test_text) > config.max_split_char_number:
        print("✓ 文本长度超过max_split_char_number，将进行按行分割")
        # 按行分割：使用换行符分割文本，并过滤空行
        knowledge_chunks = [line.strip() for line in test_text.split('\n') if line.strip()]
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

def test_edge_cases():
    """测试边界情况"""
    
    print("\n" + "="*60)
    print("=== 边界情况测试 ===")
    
    test_cases = [
        ("单行文本", "单行文本"),
        ("第一行\n第二行\n第三行", "多行文本"),
        ("第一行\n\n第三行", "包含空行"),
        ("  有前后空格的文本  \n  第二行  ", "包含前后空格"),
        ("", "空文本"),
        ("\n\n\n", "只有换行符"),
        ("   \n   \n   ", "只有空格的空行"),
    ]
    
    for text, description in test_cases:
        print(f"\n测试: {description}")
        print(f"输入: {repr(text)}")
        
        if len(text) > config.max_split_char_number or len(text) == 0:
            # 按行分割：使用换行符分割文本，并过滤空行
            chunks = [line.strip() for line in text.split('\n') if line.strip()]
            print(f"分割结果: {len(chunks)} 个文档")
            for j, chunk in enumerate(chunks):
                print(f"  文档 {j+1}: {repr(chunk)}")
        else:
            print("文本长度小于max_split_char_number，不分割")
            print(f"原文本: {repr(text)}")

def test_with_real_file():
    """使用真实文件测试"""
    
    print("\n" + "="*60)
    print("=== 使用真实文件测试 ===")
    
    try:
        with open("../data/尺码推荐.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"文件长度: {len(content)}")
        print(f"max_split_char_number: {config.max_split_char_number}")
        
        if len(content) > config.max_split_char_number:
            print("✓ 文件长度超过max_split_char_number，将进行按行分割")
            # 按行分割：使用换行符分割文本，并过滤空行
            chunks = [line.strip() for line in content.split('\n') if line.strip()]
            print(f"✓ 分割后的文档数量: {len(chunks)}")
            
            print("前5个文档预览:")
            for i in range(min(5, len(chunks))):
                print(f"文档 {i+1}: {repr(chunks[i])}")
            
            if len(chunks) > 5:
                print(f"... 还有 {len(chunks) - 5} 个文档")
        else:
            print("✗ 文件长度小于max_split_char_number，不会分割")
            
    except FileNotFoundError:
        print("测试文件不存在")

if __name__ == "__main__":
    test_line_split_logic()
    test_edge_cases()
    test_with_real_file()