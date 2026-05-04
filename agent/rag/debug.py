#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试vector_store.py的文件加载问题
"""

import os
from agent.utils.config_handler import chroma_conf
from agent.utils.path_tool import get_abs_path
from agent.utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from agent.utils.logger_handler import logger

def debug_file_loading():
    """调试文件加载功能"""
    
    print("=== 调试文件加载功能 ===")
    
    # 检查配置
    print(f"data_path配置: {chroma_conf['data_path']}")
    print(f"允许的文件类型: {chroma_conf['allow_knowledge_file_type']}")
    
    # 获取绝对路径
    data_path = get_abs_path(chroma_conf["data_path"])
    print(f"数据目录绝对路径: {data_path}")
    print(f"数据目录是否存在: {os.path.exists(data_path)}")
    
    if os.path.exists(data_path):
        print(f"数据目录中的文件: {os.listdir(data_path)}")
    
    # 测试文件列表获取
    try:
        allowed_files = listdir_with_allowed_type(
            data_path,
            tuple(chroma_conf["allow_knowledge_file_type"])
        )
        print(f"允许的文件列表: {allowed_files}")
        
        # 测试单个文件加载
        if allowed_files:
            test_file = allowed_files[0]
            print(f"\n测试加载文件: {test_file}")
            print(f"文件是否存在: {os.path.exists(test_file)}")
            
            # 测试MD5计算
            md5 = get_file_md5_hex(test_file)
            print(f"文件MD5: {md5}")
            
            # 测试文件加载
            if test_file.endswith('.txt'):
                print("尝试加载TXT文件...")
                documents = txt_loader(test_file)
                print(f"加载的文档数量: {len(documents)}")
                if documents:
                    print(f"第一个文档内容预览: {documents[0].page_content[:100]}...")
            elif test_file.endswith('.pdf'):
                print("尝试加载PDF文件...")
                documents = pdf_loader(test_file)
                print(f"加载的文档数量: {len(documents)}")
                if documents:
                    print(f"第一个文档内容预览: {documents[0].page_content[:100]}...")
                    
    except Exception as e:
        print(f"调试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_file_loading()