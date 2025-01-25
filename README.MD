## 기술적 의사결정
<details><summary>백엔드</summary>
- Python
- Django-rest-framework

  <details><summary>Celery</summary>
  
  | **특징**           | **Celery**                          | **Scarpy**                                      | **BeautifulSoup+ Requests**              | **AWS Lambda**                             |
  |---------------------|-------------------------------------|------------------------------------------------|------------------------------------------|--------------------------------------------|
  | **설치/설정 복잡성** | 브로커 설정 필요                    | 파이썬 패키지로 간단하게 설치 가능              | 파이썬 내장 라이브러리로 간단하게 사용 가능 | AWS 계정 및 Lambda 함수 설정 필요           |
  | **비동기 처리**      | 지원                                | 제한적 (scarpy-redis 사용)                      | 직접 구현 필요                            | 자동 확장                                   |
  | **주기 작업 관리**   | 지원 (django-celery-beat)           | 지원하지 않음 (스케줄러 별도로 필요)            | cron 작업이나 celery 연동 필요             | 지원 (EventBridge)                          |
  | **확장성**          | 워커 수를 조절하여 확장 가능         | Redis 기반으로 확장 가능                        | 확장성 낮음                               | 작업량에 따라 자동 확장                     |
  | **유지 보수**       | 브로커와 워커 관리 필요              | Scrapy 프로젝트 구조로 통합 관리 용이           | 관리가 간단함                             | 함수 단위로 유지보수 필요                   |
  | **웹사이트 유형**    | 모든 유형                           | 정적 및 일부 동적 웹사이트                      | 정적 웹사이트에 더 적합                   | 모든 유형                                   |
  | **단점**            | 설정이 복잡할 수 있음                | 비동기 처리와 확장성이 제한적임                 | 동적 크롤링과 그 이후의 과정까지 한번에 처리하기 어려움 | 실행 시간 제한(15분) → 작업 병렬처리 필요 |
  
  - 본 프로젝트는 데이터셋 크롤링/api로 받아온 후 챗봇에 데이터를 전달, 챗봇 작업물의 DB저장까지를 비동기로 처리하고 주기적(1일 1회)으로 작업을 하도록 설정하는 것이 중요함
  - 따라서 비동기 처리와 주기 작업 관리에 유리한 도구를 우선으로 고려
  - Celery와 AWS Lambda가 다른 도구들에 비해 우수했는데, AWS Lambda는 15분까지만 실행되므로 작업을 작은 단위로 나눠서 병렬로 처리해줘야 하는 어려움과 도구를 별도로 학습을 한 후 적용해야 한다는 점 때문에 Celery를 선택
  </details>

- PostgreSQL: Django와 호환성이 좋은 관계형 데이터베이스
- Redis: 빠른 데이터 읽기/쓰기로 캐싱 및 Celery의 브로커로 사용  
- JWT(JSON Web Token): 서버-클라이언트 간 토큰을 사용하는 인증방식으로 웹 뿐 아니라 모바일에서도 사용할 수 있어 확장성이 좋아 선택
- Oauth(Open Authorization): 사용자가 비밀번호를 제공하지 않고도 타사 애플리케이션이 사용자 정보, 프로필 등의 자원에 안전하게 접근할 수 있도록 허용하는 프로토콜로 django allauth를 통해 쉽게 구현할 수 있음
</details>

<details><summary>배포</summary>
- Docker: 컨테이너 기반 가상화 플랫폼으로, 애플리케이션을 독립된 환경에서 효율적으로 빌드, 배포 및 실행
</details>


## 적용 기술 방법
<details><summary>Celery와 CeleryBeat</summary>
- 비동기 작업 처리 (Celery)
  Celery를 사용해 외부 API와 통신하거나 크롤링 작업을 비동기로 처리하여 응답 속도를 최적화하고 서버 부하를 줄임     
  Redis를 브로커로 사용해 빠르고 안정적인 작업 큐 관리가 가능하도록 설정  
  **주요 구현 내용**
  - 작업 구조: Celery에서 @shared_task로 정의한 작업은 Redis 브로커에 전달되며, Worker가 큐에서 작업을 실행
  - 사용 예시: CNN 사이트에서 크롤링으로 뉴스 데이터를 수집하고 데이터베이스에 저장

  ```python
  @shared_task
  def fetch_and_store_cnn_news():
      categories = Category.objects.all()
      if not categories.exists():
          print("No categories found in the database.")
          return
  
      for category in categories:
          source_category = category.get_source_category(category.name, "CNN")
          if not source_category:
              print(f"No mapping found for category '{category.name}' in source 'CNN'.")
              continue
  
  ```

  - 장점: 확장성 있는 비동기 처리와 오류 로그 관리를 통해 안정적인 대규모 작업 처리 가능

- 주기적인 작업 스케줄링 (Celery Beat)
  Celery Beat를 활용해 작업 스케줄링을 구현 
  
  **주요 구현 내용**
  - IntervalSchedule 및 PeriodicTask: IntervalSchedule로 작업 간격을 설정하고, PeriodicTask로 특정 작업을 주기적으로 실행
  - 스케줄링 예시: 하루에 한 번 fetch_and_store_news 작업을 실행하여 최신 데이터를 수집
 
```python
  def setup_periodic_tasks():
      try:
          schedule = IntervalSchedule.objects.get(every=1, period=IntervalSchedule.DAYS)
      except IntervalSchedule.MultipleObjectsReturned:
          schedules = IntervalSchedule.objects.filter(every=1, period=IntervalSchedule.DAYS)
          schedule = schedules.first()
          schedules.exclude(id=schedule.id).delete()
      except IntervalSchedule.DoesNotExist:
          schedule = IntervalSchedule.objects.create(every=1, period=IntervalSchedule.DAYS)
  
      PeriodicTask.objects.update_or_create(
          name='Fetch and Store CNN News Daily',
          defaults={
              'interval': schedule,
              'task': 'materials.tasks.fetch_and_store_cnn_news',
              'args': '[]',
              'kwargs': '{}',
              'enabled': True,
          },
      )
  ```

</details>

<details><summary>DB 설계</summary>

</details>
