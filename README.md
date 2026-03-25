# Premium Python Counter with Supabase

이 프로젝트는 Flask 백엔드와 Supabase 데이터베이스를 연동한 현대적인 카운터 웹 어플리케이션입니다.

## 주요 기능
- **증가/감소/초기화**: 로컬 세션에서 숫자를 조작합니다.
- **데이터베이스 저장**: "SAVE" 버튼을 누르면 현재 숫자가 Supabase DB에 영구 저장됩니다.
- **프리미엄 UI**: Glassmorphism 디자인과 상태 변화에 따른 버튼 피드백이 적용되었습니다.

## 실행 방법

### 1. 사전 준비 (Supabase 설정)
1. [Supabase](https://supabase.com/)에서 새 프로젝트를 생성합니다.
2. 'SQL Editor'에서 다음 명령어를 실행하여 테이블을 생성합니다:
   ```sql
   create table counter_data (
     id int8 primary key,
     value int8 default 0
   );
   
   -- 초기 데이터 삽입
   insert into counter_data (id, value) values (1, 0);
   ```
3. 프로젝트 설정의 'API' 메뉴에서 `URL`과 `anon key`를 복사하여 프로젝트 루트의 `.env` 파일에 붙여넣습니다.

### 2. 패키지 설치
```bash
pip install flask supabase python-dotenv
```

### 3. 서버 실행
```bash
python app.py
```

## 프로젝트 구조
- `app.py`: Flask 백엔드 (Supabase 연동)
- `.env`: API 키 설정 파일
- `templates/`: HTML 템플릿
- `static/`: CSS 스타일 및 JS 로직
