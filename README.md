## 프로젝트 구조

app
 - crud.py - DB에 CRUD를 하는 함수 기록
 - database.py - DB설정
 - main.py - FastAPI 시작 및 라우터
 - models.py - sqlalchemy 모델 기록
 - schemas.py - Pydantic 스키마 기록(유효성검사와 API 요청 및 응답 구조 정의)
 - utils.py - url을 인코딩하기 위한 유틸리티 함수 기록

tests
 - test_main.py - 테스트코드 파일

---
## 개발환경
파이썬 버전: 3.10.6  
사용 DB: PostgreSQL  
데이터 구조가 확정되었고 기획 상 추가적인 변경·확장이 없을 예정이며  
쿼리에 주로 활용하게 될 short_url의 unique한 특성으로 이를 PK삼을 경우 성능이 조금이나마 더 나을 것으로 예상되어  
NoSQL을 사용하지 않고 SQL(RDB)를 사용하기로 함.  
프로젝트 규모를 봤을 때는 SQLite가 적합해 보이나 서비스의 특성을 고려했을 경우 만료시간 관련 datetime연산이 필요하고  
많은 사용자가 동시에 접근 할 가능성이 높은 서비스이기에 동시성 처리성능이 필요해 보여 PostgreSQL을 채택함

## 설치방법
1. requirements.txt를 이용하여 필요 패키지 설치
2. 'surl'을 이름으로 한 데이터베이스 생성 
3. 루트 디렉토리에 .env파일을 생성하여 'DATABASE_URL'라는 이름으로 'surl'DB에 접속하는 postgreSQL 환경변수 설정  
혹은 database.py의 8번줄에 직접 기입한 뒤 7, 5, 4번 줄 제거
4. 루트 디렉토리 기준 'uvicorn app.main:app'으로 실행

## API
- create_short_url  
URI : /shorten  
Method : POST  
Request : {"url":str, "ttl":int(optional) }  
Response : {"short_url": str} 


- redirect_url  
URI : /{short_url}  
Method : GET  
Request : short url: str  
Response : Redirect / HTTPException


- get_stats  
URI : /stats/{short_url}  
Method : GET  
Request : short url: str  
Response : { "origin_url": str, "short_url": str, "click_cnt": int }


- swagger API Doc  
URI : /docs