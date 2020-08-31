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