#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试通过chunk_size参数优化实现按行分割
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
import config_data as config

def test_recursive_splitter_behavior():
    """测试RecursiveCharacterTextSplitter的分割行为"""
    
    print("=== RecursiveCharacterTextSplitter 分割行为测试 ===")
    
    # 测试不同chunk_size下的分割效果
    test_cases = [
        (50, "小chunk_size"),
        (100, "中等chunk_size"),
        (200, "当前配置"),
        (500, "大chunk_size"),
    ]
    
    test_text = """身高：155-165cm， 体重：75-95 斤，建议尺码S。
身高：160-170cm， 体重：90-115斤，建议尺码M。
身高：165-175cm， 体重：115-135斤，建议尺码L。
身高：170-178cm， 体重：135-160斤，建议尺码XL。
身高：178-185cm， 体重：160-180斤，建议尺码2XL。
身高：180-190cm， 体重：180-210斤，建议尺码3XL。
身高：190cm+，体重：210斤+，建议尺码4XL。"""
    
    lines_count = len(test_text.strip().split('\n'))
    print(f"测试文本长度: {len(test_text)}")
    print(f"文本行数: {lines_count}")
    print()
    
    for chunk_size, description in test_cases:
        print(f"--- {description} (chunk_size={chunk_size}) ---")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )
        
        chunks = splitter.split_text(test_text)
        print(f"分割块数: {len(chunks)}")
        
        for i, chunk in enumerate(chunks):
            print(f"  块 {i+1} (长度: {len(chunk)}): {repr(chunk[:50])}...")
        print()

def test_optimal_chunk_size():
    """寻找最优chunk_size实现按行分割"""
    
    print("=== 寻找最优chunk_size实现按行分割 ===")
    
    # 分析文本行长度分布
    test_text = """身高：155-165cm， 体重：75-95 斤，建议尺码S。
身高：160-170cm， 体重：90-115斤，建议尺码M。
身高：165-175cm， 体重：115-135斤，建议尺码L。
身高：170-178cm， 体重：135-160斤，建议尺码XL。
身高：178-185cm， 体重：160-180斤，建议尺码2XL。
身高：180-190cm， 体重：180-210斤，建议尺码3XL。
身高：190cm+，体重：210斤+，建议尺码4XL。"""
    
    lines = [line.strip() for line in test_text.strip().split('\n') if line.strip()]
    line_lengths = [len(line) for line in lines]
    
    print("文本行长度分析:")
    print(f"总行数: {len(lines)}")
    print(f"最小行长度: {min(line_lengths)}")
    print(f"最大行长度: {max(line_lengths)}")
    print(f"平均行长度: {sum(line_lengths) / len(line_lengths):.1f}")
    print(f"行长度分布: {line_lengths}")
    print()
    
    # 根据行长度确定最优chunk_size
    max_line_length = max(line_lengths)
    optimal_chunk_size = max_line_length + 10  # 留一些余量
    
    print(f"推荐chunk_size: {optimal_chunk_size}")
    print(f"理由: 最大行长度为{max_line_length}，设置chunk_size为{optimal_chunk_size}可确保每行独立成块")
    print()
    
    # 测试推荐配置
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=optimal_chunk_size,
        chunk_overlap=0,  # 按行分割时不需要重叠
        separators=["\n"],  # 优先使用换行符分割
        length_function=len
    )
    
    chunks = splitter.split_text(test_text)
    print("=== 推荐配置分割效果 ===")
    print(f"分割块数: {len(chunks)} (期望: {len(lines)})")
    
    if len(chunks) == len(lines):
        print("✅ 成功实现按行分割!")
    else:
        print("❌ 分割效果不理想")
    
    for i, chunk in enumerate(chunks):
        print(f"  块 {i+1}: {repr(chunk)}")

def test_separators_priority():
    """测试分隔符优先级"""
    
    print("\n=== 分隔符优先级测试 ===")
    
    # 测试不同分隔符配置
    separator_configs = [
        (["\n"], "仅换行符"),
        (["\n", "。"], "换行符优先"),
        (["。", "\n"], "句号优先"),
        (["\n\n", "\n", "。"], "多级分隔符"),
    ]
    
    test_text = "第一行。第二行\n第三行。第四行\n\n第五行"
    
    for separators, description in separator_configs:
        print(f"--- {description} ({separators}) ---")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=50,
            chunk_overlap=0,
            separators=separators,
            length_function=len
        )
        
        chunks = splitter.split_text(test_text)
        print(f"分割结果: {len(chunks)} 块")
        for i, chunk in enumerate(chunks):
            print(f"  块 {i+1}: {repr(chunk)}")
        print()

if __name__ == "__main__":
    test_recursive_splitter_behavior()
    test_optimal_chunk_size()
    test_separators_priority()