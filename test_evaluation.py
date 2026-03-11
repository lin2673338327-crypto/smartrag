"""SmartRAG系统能力评估测试脚本"""
import sys
import os
import time

# 设置UTF-8编码输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from smartrag.api.rag_pipeline import RAGPipeline
from smartrag.config.settings import settings

def test_retrieval_accuracy():
    """测试1：检索准确性 - 能否找到相关内容"""
    print("\n" + "="*60)
    print("测试1：检索准确性测试")
    print("="*60)
    print("目的：验证系统能否准确找到与查询相关的文档片段")
    
    pipeline = RAGPipeline()
    
    # 测试查询
    test_cases = [
        {
            "query": "什么是RAG？",
            "expected_keywords": ["检索", "增强", "生成", "RAG", "retrieval"]
        },
        {
            "query": "向量数据库的作用",
            "expected_keywords": ["向量", "数据库", "存储", "检索", "embedding"]
        },
        {
            "query": "如何选择chunk size",
            "expected_keywords": ["chunk", "分块", "大小", "size"]
        }
    ]
    
    total_score = 0
    for i, case in enumerate(test_cases, 1):
        print(f"\n查询 {i}: {case['query']}")
        results = pipeline.vector_store.similarity_search(case['query'], k=3)
        
        if not results:
            print("  ❌ 未检索到任何结果")
            continue
            
        print(f"  检索到 {len(results)} 个结果:")
        
        relevance_score = 0
        for j, (text, score) in enumerate(results, 1):
            # 检查是否包含期望的关键词
            matched_keywords = [kw for kw in case['expected_keywords'] 
                              if kw.lower() in text.lower()]
            
            is_relevant = len(matched_keywords) > 0
            relevance_score += 1 if is_relevant else 0
            
            print(f"  [{j}] 相似度: {score:.3f} | 相关: {'✓' if is_relevant else '✗'}")
            print(f"      匹配关键词: {matched_keywords if matched_keywords else '无'}")
            print(f"      内容预览: {text[:80]}...")
        
        case_score = relevance_score / len(results)
        total_score += case_score
        print(f"  本查询得分: {case_score:.2f} ({relevance_score}/{len(results)}个相关)")
    
    avg_score = total_score / len(test_cases)
    print(f"\n总体准确性得分: {avg_score:.2f}")
    print(f"评级: {'优秀' if avg_score > 0.7 else '良好' if avg_score > 0.5 else '需改进'}")
    
    return avg_score


def test_semantic_understanding():
    """测试2：语义理解能力 - 能否理解同义词和相关概念"""
    print("\n" + "="*60)
    print("测试2：语义理解能力测试")
    print("="*60)
    print("目的：验证系统能否理解同义词、相关概念，而非仅匹配关键词")
    
    pipeline = RAGPipeline()
    
    # 同义词对测试
    synonym_pairs = [
        ("文档", "资料"),
        ("检索", "搜索"),
        ("模型", "算法")
    ]
    
    print("\n同义词理解测试:")
    synonym_scores = []
    
    for word1, word2 in synonym_pairs:
        results1 = pipeline.vector_store.similarity_search(word1, k=3)
        results2 = pipeline.vector_store.similarity_search(word2, k=3)
        
        if not results1 or not results2:
            print(f"  '{word1}' vs '{word2}': 无法比较（缺少结果）")
            continue
        
        # 比较两个查询的结果相似度
        texts1 = set([r[0][:50] for r in results1])
        texts2 = set([r[0][:50] for r in results2])
        overlap = len(texts1 & texts2) / max(len(texts1), len(texts2))
        
        synonym_scores.append(overlap)
        print(f"  '{word1}' vs '{word2}': 结果重叠度 {overlap:.2f} {'✓' if overlap > 0.3 else '✗'}")
    
    avg_synonym = sum(synonym_scores) / len(synonym_scores) if synonym_scores else 0
    print(f"\n同义词理解得分: {avg_synonym:.2f}")
    print(f"评级: {'优秀' if avg_synonym > 0.5 else '良好' if avg_synonym > 0.3 else '需改进'}")
    
    return avg_synonym


def test_performance():
    """测试3：性能测试 - 响应速度"""
    print("\n" + "="*60)
    print("测试3：性能测试")
    print("="*60)
    print("目的：测试系统的响应速度和稳定性")
    
    pipeline = RAGPipeline()
    
    test_queries = [
        "什么是RAG",
        "向量数据库",
        "embedding模型"
    ]
    
    times = []
    print("\n执行10次查询测试...")
    
    for i in range(10):
        query = test_queries[i % len(test_queries)]
        start = time.time()
        pipeline.vector_store.similarity_search(query, k=5)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"  查询 {i+1}: {elapsed*1000:.1f}ms")
    
    avg_time = sum(times) / len(times)
    p95_time = sorted(times)[int(len(times) * 0.95)]
    
    print(f"\n平均响应时间: {avg_time*1000:.1f}ms")
    print(f"P95响应时间: {p95_time*1000:.1f}ms")
    
    if avg_time < 0.2:
        rating = "优秀"
    elif avg_time < 0.5:
        rating = "良好"
    else:
        rating = "需改进"
    
    print(f"评级: {rating}")
    
    return avg_time


def test_query_length_adaptability():
    """测试4：查询长度适应性 - 不同长度查询的效果"""
    print("\n" + "="*60)
    print("测试4：查询长度适应性测试")
    print("="*60)
    print("目的：验证系统对短查询和长查询的处理能力")
    
    pipeline = RAGPipeline()
    
    queries = [
        ("短查询", "RAG"),
        ("中查询", "什么是RAG系统"),
        ("长查询", "请详细解释RAG系统的工作原理，包括检索和生成两个阶段")
    ]
    
    scores = []
    for query_type, query in queries:
        results = pipeline.vector_store.similarity_search(query, k=3)
        
        if results:
            avg_score = sum([score for _, score in results]) / len(results)
            scores.append(avg_score)
            print(f"\n{query_type}: '{query}'")
            print(f"  平均相似度: {avg_score:.3f}")
            print(f"  检索到 {len(results)} 个结果")
        else:
            print(f"\n{query_type}: '{query}'")
            print(f"  ❌ 未检索到结果")
    
    if len(scores) >= 2:
        variance = max(scores) - min(scores)
        print(f"\n相似度方差: {variance:.3f}")
        print(f"评级: {'优秀' if variance < 0.1 else '良好' if variance < 0.2 else '需改进'}")
        return variance
    
    return 0


def test_top_k_quality():
    """测试5：Top-K结果质量 - 排序是否合理"""
    print("\n" + "="*60)
    print("测试5：Top-K结果质量测试")
    print("="*60)
    print("目的：验证检索结果的排序是否合理（相似度递减）")
    
    pipeline = RAGPipeline()
    
    query = "向量数据库的作用"
    results = pipeline.vector_store.similarity_search(query, k=5)
    
    print(f"\n查询: {query}")
    print(f"检索到 {len(results)} 个结果:\n")
    
    is_sorted = True
    for i, (text, score) in enumerate(results, 1):
        print(f"[{i}] 相似度: {score:.4f}")
        print(f"    内容: {text[:100]}...\n")
        
        if i > 1 and score > results[i-2][1]:
            is_sorted = False
    
    print(f"排序正确性: {'✓ 相似度递减' if is_sorted else '✗ 排序异常'}")
    
    # 检查分数分布
    if len(results) >= 2:
        score_range = results[0][1] - results[-1][1]
        print(f"分数范围: {score_range:.4f}")
        print(f"区分度: {'优秀' if score_range > 0.1 else '良好' if score_range > 0.05 else '需改进'}")
    
    return is_sorted


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("SmartRAG系统能力评估")
    print("="*60)
    print(f"配置信息:")
    print(f"  - Embedding模型: {settings.embedding_model}")
    print(f"  - 向量数据库: {settings.vector_store_type}")
    print(f"  - Chunk大小: {settings.chunk_size}")
    print(f"  - Chunk重叠: {settings.chunk_overlap}")
    
    # 检查是否有数据
    try:
        pipeline = RAGPipeline()
        test_result = pipeline.vector_store.similarity_search("测试", k=1)
        if not test_result:
            print("\n⚠️  警告: 向量数据库为空，请先上传文档！")
            print("请通过Gradio界面上传文档后再运行评估。")
            return
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("请确保系统正常运行。")
        return
    
    results = {}
    
    # 运行各项测试
    try:
        results['accuracy'] = test_retrieval_accuracy()
    except Exception as e:
        print(f"\n❌ 准确性测试失败: {e}")
    
    try:
        results['semantic'] = test_semantic_understanding()
    except Exception as e:
        print(f"\n❌ 语义理解测试失败: {e}")
    
    try:
        results['performance'] = test_performance()
    except Exception as e:
        print(f"\n❌ 性能测试失败: {e}")
    
    try:
        results['adaptability'] = test_query_length_adaptability()
    except Exception as e:
        print(f"\n❌ 适应性测试失败: {e}")
    
    try:
        results['quality'] = test_top_k_quality()
    except Exception as e:
        print(f"\n❌ 质量测试失败: {e}")
    
    # 总结
    print("\n" + "="*60)
    print("评估总结")
    print("="*60)
    
    if 'accuracy' in results:
        print(f"✓ 检索准确性: {results['accuracy']:.2f} - 能找到相关内容的能力")
    
    if 'semantic' in results:
        print(f"✓ 语义理解: {results['semantic']:.2f} - 理解同义词和相关概念的能力")
    
    if 'performance' in results:
        print(f"✓ 响应速度: {results['performance']*1000:.1f}ms - 查询响应的快慢")
    
    if 'quality' in results:
        print(f"✓ 结果排序: {'正确' if results['quality'] else '异常'} - 结果按相关性排序的能力")
    
    print("\n各项能力说明:")
    print("1. 检索准确性：决定了能否找到用户真正需要的信息")
    print("2. 语义理解：决定了能否理解用户的真实意图，而非仅匹配关键词")
    print("3. 响应速度：决定了用户体验的流畅度")
    print("4. 结果排序：决定了最相关的内容是否排在前面")
    
    print("\n评估完成！")


if __name__ == "__main__":
    main()
