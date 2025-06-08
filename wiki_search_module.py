import wikipedia
import re

# 한국어 설정
wikipedia.set_lang("ko")

def get_definition(term):
    try:
        page = wikipedia.page(term)
        content = page.content.strip()

        # 1500자 이내로 자르되, 문장 단위로 자르기
        cutoff = 1500
        partial = content[:cutoff]

        # 마침표 기준으로 문장 단위 자르기 (정규표현식으로 문장 나누기)
        sentences = re.split(r'(?<=[.!?다요])\s+', partial)
        cleaned = ' '.join(sentences[:-1]) if len(sentences) > 1 else sentences[0]

        # 문장이 너무 짧으면 추가 문장 붙이기
        if len(cleaned) < 200:
            cleaned += " 이 용어는 다양한 분야에서 중요한 개념으로 활용되고 있습니다."

        return {"type": "definition", "content": cleaned.strip()}

    except wikipedia.exceptions.DisambiguationError as e:
        return {"type": "disambiguation", "options": e.options}
    except wikipedia.exceptions.PageError:
        return {"type": "error", "message": "문서 없음"}
    except Exception as e:
        return {"type": "error", "message": str(e)}


"""
사용 예


# 입력받기
term = input()
    
# 검색 실행
result = get_definition(term)

# 정상적으로 검색될 경우 결과 출력
if result["type"] == "definition":
        print(result["content"])
        
# 검색결과기 여러개일 때 후보목록 출력
elif result["type"] == "disambiguation":
    for option in result["options"][:10]:
        print(option)
            
    # 후보 중 원하는 제목 재입력
    choice = input()
    second = get_definition(choice)
    if second["type"] == "definition":
        print(second["content"])
            
# 기타 오류
elif result["type"] == "error":
    print(result["message"])
"""
