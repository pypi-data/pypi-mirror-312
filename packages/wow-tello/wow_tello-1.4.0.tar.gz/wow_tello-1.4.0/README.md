# WOW_Tello

# 프로젝트 개요
Tello Edu, Tello TT와 연동하여 드론을 제어할 수 있는 라이브러리이다.

단일 드론 제어 및 군집 드론도 활용할 수 있다.

드론의 기본 제어 및 미션패드 연동, 비행정보 수신, RC제어, 영상 수신 등 다양한 기능 탑재

화면을 받아서 처리하는 부분은 h264decoder가 필요하며, 해당 패키지는 직접 설치하여야 한다.

# 목차
- [개요](#프로젝트-개요)
- [목차](#목차)
- [요구사항](#require)
- [시작하기](#getting-started)
	- [설치](#installing)
- [버전 관리](#versioning)
- [PyPI](#pypi)
- [기여](#contributiong--기여)
- [라이선스](#license--라이선스)
- [감사의 말씀](#acknowledgments)
- [예제](#examples)
	- [1. 단일 연결](#single-connect)
		- [1. 초기화](#1-initialization)
		- [2. 접속 대기](#2-wait-to-connect)
		- [3. 이륙](#3-takeoff)
		- [4. 착륙](#4-landing)
	- [2. 군집 연결](#swarm-drones)
		- [1. 초기화](#2-1-initialization)
		- [2. 접속 대기](#2-2-wait-to-connect)
		- [3. 이륙](#2-3-takeoff)
		- [4. 착륙](#2-4-landing)
	- [3. 외부 모듈 연결](#외부-모듈-연결)

## Require
- Windows only
- Must install h264decoder(https://github.com/DaWelter/h264decoder)


## Getting Started
- Python3.6 버전 이상 파이썬 설치
- Visual Code 등으로 수정 가능
- 최종 및 안정화 버전은 PyPI에 업로드 할 수 있으며, 관련 방법은 사내에서 공유되는 자료를 확인
- h264decoder 설치 필요 - https://github.com/DaWelter/h264decoder

### Installing

WIP Library를 사용하기 위해선 아래의 명령어로 설치 가능하다.
```
pip install wowtello
```


## Versioning
* 업데이트 시 반드시 버전 관련 설정 수정할 것
* 버전 수정안할 시 업데이트 사항이 정상적으로 적용안될 수 있다.

## PyPI
(https://pypi.org/project/)

## Built With
* [이승명(nobu)](nobu1015@naver.com, nobu1015@wowsystem.co.kr)


## Contributiong / 기여

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us. / [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) 를 읽고 이에 맞추어 pull request 를 해주세요.

## License / 라이선스
협의 필요

## Acknowledgments
* Thanks to DaWelter (https://github.com/DaWelter)

## Examples
### Single connect
#### 1. Initialization
단일 접속 시 Tello 클래스를 사용한다.
```python
import time
import wowtello.wowtello

wowtello.wowtello._WOW_TELLO_DEBUG_ENABLE = True

t = wowtello.wowtello.Tello('192.168.10.1')
```

#### 2. Wait to connect
```is_connected()``` 메소드를 활용하여 접속 여부를 체크한다.
```python
print("접속 대기...")
while(not t.is_connected()):
	time.sleep(0.1)
print("접속 완료")
```

#### 3. Takeoff
```python
print("이륙 시작")
t.takeoff()
time.sleep(1)
print("이륙 완료")
```

#### 4. Landing
```python
print("착륙 시작")
t.land()
time.sleep(1)
print("착륙 완료")
```

### Swarm drones
#### 2-1. Initialization
군집 드론은 하나의 AP에 접속되며, IP는 보통 DHCP로 설정된다.
군집 드론을 제어하기 위해선 여러 대의 드론을 제어할 수 있게 해주는 관제탑이 필요하다.

```TelloControlTower``` 클래스로 관제탑을 생성할 수 있다.

```python
import wowtello.wowtello
tower = wowtello.wowtello.TelloControlTower()

print("비행정보 수신 활성화")
tower.start_to_receive_flight_data()
time.sleep(1)

tower.searchTrafficInNetwork('192.168.0.', 2, 20)
time.sleep(1)
print(tower.tello_ip_list)
```

```searchTrafficInNetwork``` 메소드는 ```TelloControlTower``` 클래스 안에 선언된 메소드로, 특정 IP 대역으로 명령을 전송하여 드론을 탐색한다.
첫 번째 인자는 IP이며, 맨 마지막 자리 숫자는 비워둔다.
두 번째, 세 번째 인자는 IP 탐색 시작 및 끝 번호이며, 192.168.0.2~192.168.0.20 까지 탐색하겠다는 의미이다.

#### 2-2. Wait to connect
```python
tl = [] # traffic list
for i in tower.tello_ip_list:
    tt = wowtello.wowtello.TelloTraffic(i)
    tower.appendTraffic(tt)
    tl.append(tt)

while not tower.checkAllTrafficIsConnected():
    time.sleep(1)
```
```searchTrafficInNetwork``` 메소드로 탐색이 완료되면, 사용가능한 드론의 정보는 ```tello_ip_list```에 저장된다.
탐색된 드론 수에 맞게 for문을 돌면서 ```TelloTraffic``` 클래스로 IP 주소를 입력하며, 각 드론의 객체를 생성한다.

객체를 생성하였으면 ```appendTraffic``` 메소드로 드론 트래픽을 추가한다.
```tl``` 리스트는 객체를 사용자 정의 리스트에도 추가하여 편하게 관리할 수 있도록 한다.

#### 2-3. Takeoff
```python
for tt in tl:
    tt.setWaitFlag(False)

for tt in tl:
    tt.takeoff()

tower.waitAllCommandProcessed()
time.sleep(2.5)
```
보통 객체 하나에 명령을 전달 할 때에는 tl 리스트에서 꺼내쓰고, 전체적인 관리 등을 활용할 떄에는 tower를 쓴다.

기본적으로 ```takeoff()``` 메소드 등 드론을 제어하는 메소드는 명령이 수신될 때 까지 대기하게 된다.
하지만 모든 드론에 동시에 명령을 보내고, 동시에 명령 도착이 되었는 지 확인해야 하므로, ```setWaitFlag```를 ```False```로 설정하고, tower의 ```waitAllCommandProcessed()```로 모든 명령이 처리되었는 지 확인한다.

#### 2-4. Landing
```python
for tt in tl:
    tt.land()
time.sleep(1)

tower.waitAllCommandProcessed()
```
### 외부 모듈 연결
[외부 모듈 예제](examples/ext_module_test.py) 를 확인하세요
