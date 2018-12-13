# Ansible piolink Module

## 1. Install python

Python 2.7이상의 버전이 설치 되어 있어야 합니다.

http://www.python.org/

## 2. Install Ansible 

2.5 버전 이상의 Ansible이 설치 되어 있어야 합니다.

http://docs.ansible.com/ansible/latest/intro_installation.html

## 3. Ansible Piolink Module

OS에 파이썬과 앤서블을 설치한 후, PAS-K의 기능을 실행 하기 위한 모듈을 설치 합니다.
설치 과정은 다음과 같습니다

1. 압축된 PAS-K 모듈 파일을 다운로드 합니다
2. 압축을 해제하면 3개의 폴더를 확인 할 수 있습니다.

- library: PAS-K 모듈 유틸
- module_utils: PAS-K 모듈 유틸
- example: 플레이북 스크립트 예제

3. 앤서블 설정 파일을 수정하여 모듈 폴더와 모듈 유틸 폴더의 위치를 지정합니다.
기본 설정 파일 경로: /etc/ansible/ansible.cfg

다음은 경로 지정 방법에 대한 예시입니다.
```
[defaults]
# some basic default values...
library = /usr/share/library/
module_utils = /usr/share/module_utils/
```
4. 설정 파일을 저장하면 모듈 설치가 완료 됩니다.

- 앤서블 설정 파일 상세 정보 : https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html
