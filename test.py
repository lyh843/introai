import spacy

# 加载法语句法分析模型（基于 transformer）
nlp = spacy.load("fr_dep_news_trf")

def analyze_sentence(sentence: str):
    """分析法语句子中的直接宾语与间接宾语"""
    doc = nlp(sentence)

    print(f"\n输入句子：{sentence}\n")
    print("词汇与依存关系：")
    print(f"{'Token':<15}{'POS':<10}{'Dep':<15}{'Head':<15}")
    for token in doc:
        print(f"{token.text:<15}{token.pos_:<10}{token.dep_:<15}{token.head.text:<15}")

    direct_objects = []
    indirect_objects = []

    for token in doc:
        if token.dep_ == "obj":
            direct_objects.append((token.text, token.head.text))
        # spaCy 的法语模型使用 "obl:arg" 或 "obl" 表示 COI
        elif token.dep_ in ["iobj", "obl:arg", "obl"]:
            # 仅当该词有介词引导（例如 "à", "de"）时才算 COI
            if any(child.dep_ == "case" and child.text in ["à", "de"] for child in token.children):
                indirect_objects.append((token.text, token.head.text))


    # 输出结果
    print("\n=== 宾语分析结果 ===")
    if direct_objects:
        for obj, verb in direct_objects:
            print(f"直接宾语 (COD): {obj} ← 动词: {verb}")
    else:
        print("未检测到直接宾语 (COD)")

    if indirect_objects:
        for obj, verb in indirect_objects:
            print(f"间接宾语 (COI): {obj} ← 动词: {verb}")
    else:
        print("未检测到间接宾语 (COI)")

    # 指代标注（简化示例：检测代词指代）
    print("\n=== 宾语指代标注 ===")
    for token in doc:
        if token.pos_ == "PRON" and token.dep_ in ["obj", "iobj"]:
            print(f"代词 '{token.text}' 可能指代上文实体（上下文需进一步语义分析）")

def main():
    print("=== 法语宾语分析器 ===")
    print("1. 手动输入句子")
    print("2. 从文本文件读取")
    choice = input("请选择模式 (1/2): ").strip()

    if choice == "1":
        sentence = input("请输入法语句子：\n> ").strip()
        analyze_sentence(sentence)

    elif choice == "2":
        file_path = input("请输入txt文件路径：\n> ").strip()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            print(f"\n从文件读取内容：\n{text}\n")
            analyze_sentence(text)
        except FileNotFoundError:
            print("文件未找到，请检查路径。")

    else:
        print("无效选择。程序退出。")

if __name__ == "__main__":
    main()
