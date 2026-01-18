# BOJ Controller

백준 온라인 저지 문제 뷰어 및 컨트롤러 툴입니다. 브라우저를 열지 않고 터미널에서 백준 문제를 보고, 솔루션 템플릿을 생성하고, 샘플 입출력으로 테스트할 수 있습니다.

## 기능

- 📖 터미널에서 백준 문제 조회
- 📝 솔루션 파일 템플릿 자동 생성
- 🧪 샘플 입출력으로 솔루션 테스트
- 🎲 티어별 랜덤 문제 추천
- 💡 빠른 입력 패턴 자동 적용

## 설치

### 의존성 설치

```bash
pip install requests beautifulsoup4 rich
```

### 다운로드

```bash
git clone <repository-url>
cd baekjoon/boj_controller
```

## 사용법

### 문제 조회

```bash
# 문제 전체 내용 보기
python3 boj_ctrl.py <문제번호>

# 예시
python3 boj_ctrl.py 1001
```

### 샘플 입출력만 보기

```bash
python3 boj_ctrl.py <문제번호> --sample

# 예시
python3 boj_ctrl.py 1001 --sample
```

### 솔루션 템플릿 생성

```bash
# 솔루션 파일 생성
python3 boj_ctrl.py <문제번호> --init

# 예시
python3 boj_ctrl.py 1001 --init
```

생성된 파일 `{문제번호}.py`에는:
- 빠른 입력 패턴 (`input = sys.stdin.readline`)
- `main()` 함수 구조
- 샘플 입출력 주석 포함

### 솔루션 테스트

```bash
# 솔루션 파일을 샘플 입출력으로 테스트
python3 boj_ctrl.py <문제번호> --test

# 예시 (먼저 --init로 파일 생성 후)
python3 boj_ctrl.py 1001 --test
```

### 랜덤 문제 추천

```bash
# 티어별 랜덤 문제 추천
python3 boj_ctrl.py --random <티어>

# 티어 코드
# 브론즈: b1(I), b2(II), b3(III), b4(IV)
# 실버: s1(I), s2(II), s3(III), s4(IV)
# 골드: g1(I), g2(II), g3(III), g4(IV)
# 플래티넘: p1(I), p2(II), p3(III), p4(IV)
# 다이아몬드: d
# 루비: r

# 예시
python3 boj_ctrl.py --random b4  # Bronze IV
python3 boj_ctrl.py --random s2  # Silver II
python3 boj_ctrl.py --random g1  # Gold I
```

### 솔루션 파일 직접 실행

```bash
python3 <문제번호>.py

# 예시
python3 1001.py
```

## 작업 흐름 예시

```bash
# 1. 랜덤 문제 추천
python3 boj_ctrl.py --random s1

# 2. 문제 확인 및 샘플 입출력만 보기
python3 boj_ctrl.py 1032 --sample

# 3. 솔루션 템플릿 생성
python3 boj_ctrl.py 1032 --init

# 4. 솔루션 작성 (vim, nano 등 사용)
vim 1032.py

# 5. 솔루션 테스트
python3 boj_ctrl.py 1032 --test

# 6. 제출 (백준 웹사이트에서)
```

## 솔루션 파일 예시

`boj_ctrl.py --init`으로 생성되는 템플릿:

```python
# A-B
import sys
input = sys.stdin.readline

def main():
    # Write your solution here
    pass

if __name__ == "__main__":
    main()

# Sample Input/Output for testing:
# Sample 1:
# Input:
# 3 2
# Output:
# 1
```

## 템플릿 수정

기존 파일을 덮어쓰려면 `--force` 옵션을 사용하세요:

```bash
python3 boj_ctrl.py <문제번호> --init --force
```

## 테스트 결과

테스트 결과는 다음과 같이 표시됩니다:

```
Sample 1: PASSED
Sample 2: PASSED

All tests passed!
```

또는 실패 시:

```
Sample 1: FAILED
Expected:
1
Actual:
2

Some tests failed.
```

## 프로젝트 구조

```
boj_controller/
├── boj_ctrl.py          # 메인 CLI 도구
├── 1001.py             # 생성된 솔루션 파일들
├── 1032.py
├── ...
├── README.md
└── AGENTS.md           # 코드 스타일 가이드
```

## 요구사항

- Python 3.7+
- requests
- beautifulsoup4
- rich

## 라이선스

MIT License

## 기여

Pull Request를 환영합니다!

## 문제 신고

[Issues](https://github.com/your-repo/boj_controller/issues)에 문제를 신고해주세요.

## 관련 링크

- [백준 온라인 저지](https://www.acmicpc.net/)
- [solved.ac](https://solved.ac/)
