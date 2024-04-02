# pyzbar dependency with: Visual C++ Redistributable Packages for Visual Studio 2013
# install first: vcredist_x64.exe
# pip install opencv-python
# pip install pyzbar

import cv2
from pyzbar.pyzbar import decode
import streamlit as st


def read_barcode(_run: bool, _cam: cv2.VideoCapture, _frame: st.image) -> str:
    """
    Read barcode using the webcam. "q" exits, otherwise, it stays up till it reads the first barcode

    Params: _run: bool
    Params: _cam: opencv frame
    Params: _frame: streamlit embedded frame
    Returns: barcode value: string
    """

    while _run:
        ret, frame = _cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray)

        for _barcode in barcodes:
            x, y, w, h = _barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            barcode_data = _barcode.data.decode("utf-8")

            # _cam.release()
            # cv2.destroyAllWindows()
            _run = False
            return barcode_data

        if _frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            _frame.image(frame)  # FRAME_WINDOW.image(frame)
        else:
            cv2.imshow('Barcode Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    _cam.release()
    cv2.destroyAllWindows()
    _run = False
    return '-1'


# if __name__ == "__main__":
#     cam = cv2.VideoCapture(0)
#     barcode = read_barcode(True, cam, None)  #
#     if barcode != '-1':
#         print("Barcode Data:", barcode)
