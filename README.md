<p>실시간으로 웹캠에 주어지는 이미지를 받고, 물체를 감지하여 클래스 별로 분류하는 GUI 프로그램을 만든다.</p>
<h2 id="gui-디자인">GUI 디자인</h2>
<p><img src="https://user-images.githubusercontent.com/45510328/90504178-a4371b00-e18b-11ea-908a-af5b9ce8c77e.png" alt="0818-gui"></p>
<ul>
<li>웹캠은 640x480 의 고정된 사이즈로 받는다. (1280x720 웹캠 테스트 결과 에러 없음)</li>
<li>start 버튼을 클릭하지 않아도 디폴트로 웹캠이 연결된다. model 과 weight 파일을 select 하고, start 버튼을 클릭하면 detection 결과가 표시된 화면이 출력된다.</li>
<li>model 과 weight 파일을 불러오는데 에러가 생기면 에러메세지를 알람으로 띄우고, 화면은 기본 웹캠 입력으로 바뀐다. 특정 확장명(.h5 와 .weights)만을 읽을 수 있다.</li>
<li>파일의 경로가 너무 길 경우, 파일명이 표시될 수 있도록 중간 문자열을 생략한다.</li>
<li>record 버튼을 클릭하면, 화면이 녹화되며 버튼의 값은 stop 으로 바뀐다. stop 버튼을 클릭하면 비디오가 저장되며, 값은 다시 record 로 바뀐다.</li>
</ul>
<h2 id="프로그램-설계">프로그램 설계</h2>
<ol>
<li><code>device.py</code><br>
사용할 웹캠을 지정하고, 프레임을 읽어온다.</li>
</ol>
<ul>
<li>q 키를 눌러야 창이 닫힌다.</li>
</ul>
<ol start="2">
<li><code>gui.py</code><br>
위의 gui 를 조합하고, 웹캠에서 받아온 프레임을 표시한다.</li>
</ol>
<ul>
<li>timer를 사용해 표시할 프레임을 업데이트 한다.</li>
</ul>
<ol start="3">
<li>
<p><code>detect.py</code><br>
yolo 를 활용하여 프레임에서 애호박의 위치를 찾는다.</p>
</li>
<li>
<p><code>classify.py</code><br>
애호박의 위치를 전달받아, 학습된 모델로 애호박의 클래스를 분류한다.
</li>
<li>
<p><code>main.py</code><br>
GPU 의 사용 제한을 풀고, 통합된 프로그램을 실행한다.</p>
</li>
</ol>


## 사용방법
* 웹캠 대신 동영상을 넣고 싶을 경우

    `main.py` 29번째 줄 0 대신에 동영상 경로로 수정
    ``` python
    # start_window = StartWindow(0)
    start_window = StartWindow("zuc/zuc.avi")
    ```

* min confidence 수정하고 싶을 경우

    `coordinate.py` 11번째 줄 수정
    ``` python
    self.min_confidence = 0.5
    ```