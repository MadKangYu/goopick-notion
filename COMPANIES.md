# 법인 구분

## 구조

```
goopick-notion/
├── goopick/           # 구픽 (메인)
├── dojangminjok/      # 도장민족
├── madstamp/          # 매드스탬프 (개인회사)
└── madstampinc/       # 매드스탬프 (법인회사)
```

## 회사 정보

| 코드 | 회사명 | 유형 | 대표 | 비고 |
|------|--------|------|------|------|
| goopick | 구픽(주) | 법인 | 진수근 | |
| dojangminjok | 도장민족(주) | 법인 | 진수근 | |
| madstamp | 매드스탬프 | 개인회사 | 강유 | → 도장민족(주) 하위 예정 |
| madstampinc | 매드스탬프(주) | 법인회사 | 강유 | → 도장민족(주) 하위 예정 |

### 장기 조직 구조 (예정)
```
구픽(주) [진수근]
도장민족(주) [진수근]
├── 매드스탬프 [강유] (개인)
└── 매드스탬프(주) [강유] (법인)
```

## 각 폴더 구조

```
[회사명]/
├── backups/    # Notion 백업
└── exports/    # 마크다운 내보내기
```

## 사용법

### 회사별 동기화
```bash
python scripts/sync.py --company goopick
python scripts/sync.py --company madstamp
```

### 전체 동기화
```bash
python scripts/sync.py --all
```
