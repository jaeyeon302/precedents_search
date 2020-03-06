# Case_search
대한민국 판례를 찾는 PyQt5 프로그램입니다. ___2002도995_, _2012다13507___ 같은 판례번호를 입력하면 해당 판례를 가져와 __판시사항, 판결요지, 참조조문__ 을 저장할 수 있게해주는 프로그램입니다.

![GUI of this app](https://user-images.githubusercontent.com/20160167/76059249-ae8ca080-5fc1-11ea-8d7f-ebb59d7cd77f.png)

## 시작하기
### 아래의 것들이 필요해요!  
각각의 링크에 설치 방법이 설명되어 있는 홈페이지가 링크되어있습니다.
1. [pytnon3](https://www.python.org/downloads/)
2. modules
    - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
    - [PyQt5](https://pypi.org/project/PyQt5/)
    - [python-docx](https://python-docx.readthedocs.io/en/latest/user/install.html)

### 실행방법
`src/app.py` 이 프로그램을 돌리는 __main__ 파일입니다.
```
$ python3 app.py
```

1. __판례번호__ input field에 쉽표(__,__)로 구분하여 판례번호를 넣어주고 __Enter__ 를 치면 됩니다.  
2. 판시사항, 판결요지, 참조조문 중 원하는 체크박스에 __check__ 하시고 저장버튼을 눌러주시면 저장됩니다.
3. 저장되는 경로를 잘봐주세요! `python3 app.py`가 실행되는 폴더에 저장됩니다.

### 주의사항!!!
1. 판시사항, 판결요지, 참조조문 중 __하나라도 없는__ 판례는 함께 저장되지 않습니다. 저장된 결과파일을 다시 한번 확인해주세요.
2. 데이터를 가져오고 저장하는데 시간이 걸립니다. 로딩 버튼이 떠도 정상작동 중이니 기다려주세요

--- 

### 참고사항
- [국가법령정보 공동활용 - 개발자LAB/법령한글정보](http://open.law.go.kr/LSO/lab/hangulAddr.do)를 이용해 [국가법령정보센터](www.law.go.kr)로부터 판례정보를 크롤링해오고 있습니다.
