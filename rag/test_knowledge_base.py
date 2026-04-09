#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试knowledge_base.py中的文本分割功能
"""

import knowledge_base as kb

def test_knowledge_base_split():
    """测试知识库的分割功能"""
    
    # 创建知识库服务实例
    kb_service = kb.KnowledgeBaseService()
    
    # 测试文本
    test_text = """身高：155-165cm， 体重：75-95 斤，建议尺码S。
身高：160-170cm， 体重：90-115斤，建议尺码M。
身高：165-175cm， 体重：115-135斤，建议尺码L。
身高：170-178cm， 体重：135-160斤，建议尺码XL。
身高：178-185cm， 体重：160-180斤，建议尺码2XL。
身高：180-190cm， 体重：180-210斤，建议尺码3XL。
身高：190cm+，体重：210斤+，建议尺码4XL。"""
    
    print("=== 测试knowledge_base.py分割功能 ===")
    print(f"测试文本长度: {len(test_text)}")
    print()
    
    # 模拟upload_by_str方法中的分割逻辑
    if len(test_text) > kb.config.max_split_char_number:
        print("文本长度超过max_split_char_number，将进行分割")
        chunks = kb_service.splitter.split_text(test_text)
        print(f"分割后的文档数量: {len(chunks)}")
        
        for i, chunk in enumerate(chunks):
            print(f"块 {i+1} (长度: {len(chunk)}):")
            print(repr(chunk))
            print()
    else:
        print("文本长度小于max_split_char_number，不会分割")
        print("原文本:")
        print(repr(test_text))

def test_with_real_file():
    """使用真实文件测试"""
    
    try:
        with open("../data/尺码推荐.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            
        print("=== 使用真实文件测试 ===")
        print(f"文件长度: {len(content)}")
        
        kb_service = kb.KnowledgeBaseService()
        
        # 模拟upload_by_str调用
        result = kb_service.upload_by_str(content, "测试文件")
        print(f"上传结果: {result}")
        
    except FileNotFoundError:
        print("测试文件不存在")
    except Exception as e:
        print(f"测试过程中出错: {e}")

if __name__ == "__main__":
    test_knowledge_base_split()
    print("\n" + "="*50 + "\n")
    test_with_real_file()