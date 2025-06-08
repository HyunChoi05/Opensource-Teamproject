import wikipedia

# 한국어로 설정
wikipedia.set_lang("ko")

def get_definition(term, sentences=1):
    # 검색 결과를 요약해서 반환
    try:
        summary = wikipedia.summary(term, sentences=sentences)
        return {"type": "definition", "content": summary}
    # 검색결과 여러개일 때
    except wikipedia.exceptions.DisambiguationError as e:
        return {"type": "disambiguation", "options": e.options}
    # 검색결과가 없을 때
    except wikipedia.exceptions.PageError:
        return {"type": "error", "message": "문서 없음"}
    # 기타 오류
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
