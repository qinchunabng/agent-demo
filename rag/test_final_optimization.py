#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试通过参数优化实现的按行分割效果
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
import config_data as config

def test_optimized_config():
    """测试优化后的配置参数"""
    
    print("=== 优化后的配置参数 ===")
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
    
    # 测试文本
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
    print("=== 分割结果 ===")
    
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

def test_with_real_file():
    """使用真实文件测试"""
    
    print("\n" + "="*60)
    print("=== 使用真实文件测试 ===")
    
    try:
        with open("../data/尺码推荐.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"文件长度: {len(content)}")
        print(f"max_split_char_number: {config.max_split_char_number}")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )
        
        if len(content) > config.max_split_char_number:
            print("✓ 文件长度超过max_split_char_number，将进行分割")
            chunks = splitter.split_text(content)
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

def test_parameter_explanation():
    """参数配置说明"""
    
    print("\n" + "="*60)
    print("=== 参数配置说明 ===")
    
    print("1. chunk_size = 50")
    print("   - 设置较小的chunk_size确保每行文本能独立成块")
    print("   - 根据测试，尺码推荐文本每行长度约30-35字符")
    print("   - 设置50可确保每行独立，同时留有余量")
    print()
    
    print("2. chunk_overlap = 0")
    print("   - 按行分割时不需要重叠内容")
    print("   - 每行尺码信息是独立的语义单元")
    print("   - 重叠会破坏语义完整性")
    print()
    
    print("3. separators = ['\\n', '。', '!', '！', '?', '？', '.', ' ', '']")
    print("   - 换行符(\\n)作为最高优先级分隔符")
    print("   - 其他标点符号作为备选分隔符")
    print("   - 确保在各种文本格式下都能正确分割")
    print()
    
    print("4. max_split_char_number = 30")
    print("   - 设置较小的阈值确保文本能被分割")
    print("   - 尺码推荐文本每行都超过30字符")
    print("   - 确保分割逻辑被触发")

if __name__ == "__main__":
    test_optimized_config()
    test_with_real_file()
    test_parameter_explanation()