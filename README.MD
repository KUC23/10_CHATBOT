## "뉴스 한 스푼으로 채우는 영어실력" - SmartScoop-

## 📖 목차 
1. [팀 소개](#팀소개)
2. [프로젝트 소개](#프로젝트-소개) 
3. [기획의도](#기획의도)
4. [개발기간](#개발기간)
5. [주 사용 기술](#주-사용-기술) 
6. [서비스 아키텍처](#서비스-아키텍처)
6. [주요기능](#주요기능)
7. [기술적 의사결정](#기술적-의사결정)
8. [Trouble Shooting](#trouble-shooting)
9. [향후 개선 계획](#향후-개선-계획)


### 팀소개
#### 10조 런봇(LearnBot)

|강의찬|정윤우|조현민|박수호A|
|:---:|:---:|:---:|:---:|
|팀장|팀원|팀원|서기|
|프론트엔드|챗봇 개발|데이터 크롤링 및 전처리|백엔드|

<br>

### 💡프로젝트 소개
- **사용자가 관심있는 외국 뉴스를 기반으로 학습할 수 있도록 도와주는 챗봇 서비스**입니다.
- 사용자는 **메신저 플랫폼을 통해 요약된 뉴스**와 **해당 기사에서 제공된 단어를 학습자료**로 받아볼 수 있습니다.
- 즉, **외국 뉴스를 기반으로 한 정보습득과 언어의 학습을 목적으로 한 학습용 챗봇**입니다.

<br>

### 💡기획의도
- 많은 사람들이 영어를 배우고자 하는 의지가 있지만, 여러가지 이유로 인해 결과적으로 만족스러운 공부를 하지 못하는 경우가 많습니다.
- 이를 보완하기 위해, 메신저 플랫폼을 이용해 사용자가 따로 신경쓰지 않아도 **그날의 작은 공부거리를 제공하는 것이 ‘SmartScoop’의 기획의도**입니다.
- 더 나아가 의미없는 단어의 나열이 아닌, **외국의 기사를 통한 의미있는 정보습득**이 더 의미가 있다고 생각해 단순한 단어제공이 아닌 외국의 기사를 선택하게 되었습니다.

### 개발기간
- 2024/12/31 ~ 2024/01/31

<br>


### 서비스 아키텍처

<img src="image-10.png" width="500" height="500" alt="alt text">


<br>
<br>

### ⚙️주 사용 기술

<details>
<summary><img src="image.png" width="20" height="20" /> Frontend / UI </summary>
<div markdown="1">

- **React.js** : 사용자 인터페이스를 구축하기 위한 컴포넌트 기반의 JavaScript 라이브러리

</div>
</details>

<details>
<summary><img src="image-1.png" width="20" height="20" /> Backend  </summary>
<div markdown="1">

- **Python** (3.10) : 다양한 라이브러리와 높은 확장성을 제공하는 백엔드 개발 언어

- **Django REST framework** (3.15.2) : API 개발을 위한 Django 기반 프레임워크로, 직관적인 설계와 강력한 기능 지원

</div>
</details>

<details>
<summary><img src="image-2.png" width="20" height="20" /> LLM  </summary>
<div markdown="1">

- **Gemini 1.5 flash** : 기사의 요약본 생성, 기사에서 단어 추출해 단어장에 저장
</div>
</details>

<details>
<summary><img src="image-3.png" width="20" height="20" /> DataBase  </summary>
<div markdown="1">

- **PostgreSQL** (16.6) : 사용자 데이터 및 설정 저장, 뉴스 데이터 영구 저장

- **Redis** (6.2) : 캐싱 및 뉴스 데이터 관리

</div>
</details>

<details>
<summary><img src="image-4.png" width="20" height="20" /> Crawling  </summary>
<div markdown="1">

- **Celery** (5.4.0) :  주기적인 작업 및 대규모 작업 처리에 유용한 비동기 작업 큐

- **BeautifulSoup** (4.12.3) : HTML과 XML 데이터를 쉽게 파싱하고 원하는 정보를 추출할 수 있도록 돕는 Python 라이브러리

- **Selenium** (4.27.1) : 웹 브라우저를 자동화하여 동적 웹페이지의 데이터를 크롤링하거나 테스트할 수 있는 도구
</div>
</details>


<details>
<summary><img src="image-5.png" width="20" height="20" /> Deploy  </summary>
<div markdown="1">

- **Docker** : 컨테이너 기반 가상화 플랫폼으로, 애플리케이션을 독립된 환경에서 효율적으로 빌드, 배포 및 실행
- **AWS EC2** : 클라우드에서 가상 서버를 제공하여 애플리케이션 실행, 테스트, 배포를 지원하는 확장 가능한 컴퓨팅 서비스

</div>
</details>

<br>


### 주요기능

#### LLM을 이용한 외국 기사의 요약 및 번역

- **Gemini 1.5 flash**를 이용하여 가볍게 읽기에 너무나 긴 기사들을 **요약 기능**을 통해, 사용자에게 제공
- **동시에 번역을 제공**하여 **사용자가 정보에 대한 흥미를 갖게 하기 위한 장치**로서 **활용**했으며, **적당한 난이도의 단어제공을 통한 학습효과 유도**

### 메신저 플랫폼을 이용한 접근성

- 현대인이라면 거의 반드시 가지고 있는 스마트폰이라는 매체의 활용을 시도
- 한국에서 가장 사용률이 높은 메신저 플랫폼인 카카오톡을 이용하여 상대적으로 챗봇에 대한 접근성을 높임.

### 외국의 기사의 데이터 크롤링

- 단순한 영어 문장의 전달이 아닌 정보제공으로서의 기능 또한 충족시키기위해 외국의 기사를 크롤링하여 사용자에게 제공할 소스로써 활용

<br>

### 💭기술적 의사결정
<details>
<summary><strong> Gemini 1.5 flash와 다른 모델의 성능 비교 </strong></summary>
<div markdown="1">
- 
    
| **모델** | **기사 요약 소요시간(초)** | **기사 요약 + 추가질의 평균소요시간** |
| --- | --- | --- |
| Gemini pro | 1.97544 | 4.86609 |
| Gemini 1.5 flash | 1.53829 | 3.09793 |
| GPT4o-mini | 3.17234 | 2.92294 |
- **평균소요시간**이란 기사 요약에 걸린 시간과 몇 가지의 추가 질의에 답변하는데 걸린 시간의 총합의 평균시간을 의미
- **Gemini pro**의 경우 추가질의에 대답하는 시간이 다른 모델보다 길었으나 그만큼 답변 내용이 다른 모델보다 상세했음을 확인함.
- 추가 질의에 대한 답변 내용의 정확성 및 기사와의 연관성은 **Gemini Pro > Gemini 1.5 flash > GPT4o-mini** 순으로 더 뛰어남을 확인함.
- 추가 질의에 대한 답변 내용의 정확성 및 기사와의 연관성은 **Gemini Pro > Gemini 1.5 flash > GPT4o-mini** 순으로 더 뛰어남을 확인함.

👉 총합 시간은 근소하게 **GPT4o-mini가 더 빠르나**, **주요기능은 기사를 요약하는데 있기 때문에 Gemini 1.5 flash를 선택**


</div>
</details>



<details>
<summary><strong> RAG를 구성을 하지 않은 이유 </strong></summary>
<div markdown="1">
    
    
- 프로젝트의 기획의도는 ‘외국의 기사의 요약본을 제공해주는 학습용 챗봇’이며, 또한 프로젝트에서의 ‘Gemini 1.5 flash’의 주 역할은 ‘외국 기사의 요약 및 번역’임.
- 기사의 요약 및 번역과 같은 기능은 테스트를 진행해본 결과, 특별한 학습을 진행하지 않더라도, 충분히 만족스러운 결과물을 뽑아낼 수 있는 것을 알아냄.

👉 위와  같은 이유로 본 프로젝트에서 별도의 RAG를 구성하지 않음.

</div>
</details>




<details>
<summary><strong> 캐싱 전략  </strong></summary>
<div markdown="1">
    
    
**✅ 캐시 읽기 전략:  Look aside vs Read Through**

- Look aside 전략은 가장 기본이 되는 캐시 전략이면서 Redis가 다운되어도 서비스 제공 가능
- Read Throguh는 캐싱을 적극적으로 이용할 수 있으나 Redis 다운 시 서비스가 중지됨.

👉 위와 같은 이유로 안정성을 위해 **Look aside 전략 선택**

**✅ 캐시 쓰기 전략: Write Through vs Write Around vs Write Back**

- Write Through 전략은 항상 캐시와 DB의 데이터가 동기화된 상태로 추가적인 동기화 로직을 구현하지 않아도 되며 실시간 요청 처리 속도가 빠름
- Write Around 전략은 사용자의 데이터 요청이 많으면 DB에 부하를 주게 되며 실시간 요청 처리 시 시간이 많이 걸림
- Write Back 전략은 캐시와 DB간 동기화 로직이 필요하며 Redis 장애 시 데이터 손실 가능성이 있음

👉 로직이 비교적 간단하고 빠른 데이터 제공에 유리한 **Write Through 전략 선택**

</div>
</details>




<details>
<summary><strong> 크롤링 및 데이터 전달 시 비동기 작업 도구 선택  </strong></summary>
<div markdown="1">
    
| **특징** | **Celery** | **Scarpy** | **BeautifulSoup+ Requests** | **AWS Lambda** |
| --- | --- | --- | --- | --- |
| 설치/설정 복잡성 | 브로커 설정 필요 | 파이썬 패키지로 간단하게 설치 가능 | 파이썬 내장 라이브러리로 간단하게 사용 가능 | AWS 계정 및 Lambda 함수 설정 필요 |
| 비동기 처리 | **지원** | 제한적 (scarpy-redis 사용) | 직접 구현 필요 | 자동 확장 |
| 주기 작업 관리 | **지원(django-celery-beat)** | 지원하지 않음 (스케줄러 별도로 필요) | cron 작업이나 celery 연동 필요 | 지원(EventBridge) |
| 확장성 | 워커 수를 조절하여 확장 가능 | Redis 기반으로 확장 가능 | 확장성 낮음 | 작업량에 따라 자동 확장 |
| 유지 보수 | 브로커와 워커 관리 필요 | Scrapy 프로젝트 구조로 통합 관리 용이 | 관리가 간단함 | 함수 단위로 유지보수 필요 |
| 웹사이트 유형 | 모든 유형 | 정적 및 일부 동적 웹사이트 | 정적 웹사이트에 더 적합 | 모든 유형 |
| 단점 | 설정이 복잡할 수 있음 | 비동기 처리와 확장성이 제한적임 | 동적 크롤링과 그이후의 과정까지 한번에 처리하기 어려움 | **실행 시간 제한(15분)→작업 병렬처리 필요** |
- 본 프로젝트는 데이터셋 크롤링/api로 받아온 후 챗봇에 데이터를 전달, 챗봇 작업물의 DB저장까지를 비동기로 처리하고 주기적(1일 1회)으로 작업을 하도록 설정하는 것이 중요함.
- 따라서 비동기 처리와 주기 작업 관리에 유리한 도구를 우선으로 생각함.
- Celery와 AWS Lambda가 다른 도구들에 비해 우수했는데, AWS Lambda는 15분까지만 실행되므로 작업을 작은 단위로 나눠서 병렬로 처리해줘야 하는 어려움과 도구를 별도로 학습을 한 후 적용해야 함.

👉  위와 같은 이유로 프로젝트에 더 적합한 **Celery를 선택**함.

</div>
</details>


<details>
<summary><strong> html → React 프론트엔드 교체 </strong></summary>
<div markdown="1">
    
**✅ 연동성 문제로 인한 기술 스택 변경 결정**

- 초기 프론트엔드는 HTML 기반으로 제작을 시도
- 그러나 결과물 구현 과정에서 Django REST Framework(DRF)와의 연동성 부족으로 인해 빈번한 충돌이 발생하는 문제점이 발견됨.
- 이러한 한계점으로 HTML이 프로젝트의 원활한 진행에 적합하지 않다고 판단함.
- React는 컴포넌트 단위로 UI를 설계하여 코드의 재사용성을 극대화할 수 있고, 동일한 기능이나 UI 요소를 프로젝트 전반에서 반복적으로 사용할 수 있어 유지보수가 용이하고, 개발 속도가 비약적으로 향상된다는 장점이 있음.

    👉 위와 같은 이유로 React 기반 프론트엔드 개발을 진행하기로 결정함.

</div>
</details>




<details>
<summary><strong> API 초당 요청 한도 초과  </strong></summary>
<div markdown="1">
    
기사의 요약과 단어 추출 과정에서 사용되는 언어 모델 API의 초당 요청 한도 초과를 피하기 위해 코드 내에 대기시간을 설정함.

| **시간(초)** | **`fetch_and_store_cnn_news.delay()`** | **`fetch_and_store_nyt_news.delay()`** |
| --- | --- | --- |
| 15 | O | O |
| 10 | O | O |
| 5 | O | O |
| 3 | O | O |
| 2 | O | X |
| 1 | O | X |

👉 테스트 결과 API 한도 초과를 피할 수 있는 최소 대기시간은 3초로 결정했고, 요약본과 단어추출을 하는데 3초의 대기시간을 추가함.

</div>
</details>









<br>

### ⚠️Trouble Shooting

<details>
<summary>EC2 서버 에러  </summary>
<div markdown="1">

**✅ 문제 발생 상황** 

웹 페이지를 띄우지 못하고,

```python
docker-compose up --build
```

을 통한 빌드 작업 간에 SQL 체크포인트 생성이라는 오래 걸리지 않는 작업임에도 불구하고,  아래의 로그 상태처럼 진행이 되지 않는 문제가 발생함.

```python
postgres_db | 2025-01-23 14:56:46.905 UTC [25] LOG:  checkpoint starting: time
postgres_db | 2025-01-23 14:56:47.343 UTC [25] LOG:  checkpoint complete: wrote 8 
buffers (0.0%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.410 s, sync=0.008 s, 
total=0.438 s; sync files=7, longest=0.004 s, average=0.002 s; distance=9 kB, 
estimate=9 kB; lsn=0/1A7E7A0, redo lsn=0/1A7E768
```

문제 해결을 위해 어떻게든 빌드 작업을 진행했지만 크롤링이 제대로 진행이 되지 않는 등,  EC2 서버가 제대로 움직이지 않는 문제가 발생함.

**✅ 추정되는 원인**

 `/dev/root` 파일시스템 용량이 80% 이상 차지하고 있었고 이로 인해 서버가 제대로 움직이지 않는다고 판단함.

**✅ 문제 해결 방법**

 AWS EC2 의 콘솔에서 볼륨(스토리지 용량)을 늘려주는 `스케일업` 작업을 실시함.

- AWS EC2 콘솔에서 인스턴스 볼륨을 `8GB → 30GB`로 늘림.
- 적용 방법

```python
# 1.디스크 용량 확인
$ sudo df -h

# 2. 인스턴스에 연결된 볼륨의 디바이스 이름 확인
$ lsblk

# 3. 파티션 확장
$ sudo growpart /dev/xvda 1

# 4. 파티션 확장 확인
$ lsblk # xvda1 파티션을 보면 7.9GB에서 29GB 변경됨을 확인할 수 있음.
```

**✅ 문제 해결**

![alt text](image-6.png)

빌드 과정에서 멈추거나 하는 등의 문제 현상을 부분적으로 해결함.


</div>
</details>


<details>
<summary> npm build 진행 불가   </summary>
<div markdown="1">

**✅ 문제 발생 상황** 

프론트 엔드를 수정한 후에 `npm build` 를 통해 최적화 작업을 실행하였으나, 아래 이미지처럼 진행이 되지 않는 현상이 발생함.

![alt text](image-7.png)

**✅ 문제 원인**

ec2 서버 자체의 성능적 문제 혹은 서버 자체 문제로 build가 정상적으로 진행되지 않는 버그가 있을 수 있다고 판단함.

**✅ 문제 해결 아이디어**

로컬에서 서버와 같은 프론트엔드 환경을 만들어 로컬내에서 build를 실행하여 로컬에 build 파일을 작성함.

![alt text](image-8.png)

**✅ 문제 해결**

로컬 내에서 파일을 작성한 후에,  scp 명령어와  .pem 키를 이용하여, 직접적으로 로컬에서 서버로 이동하는 방법을 선택한 후 빌드에 성공함.

![alt text](image-9.png)

</div>
</details>

 

 ### 향후 개선 계획
