# -*- coding: utf-8 -*-
# @Time    : 2019-03-05 10:28
# @Author  : Deng Yue


def extract_arrow(img):

    import numpy as np
    import cv2

    img = cv2.imread('b.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 127, 255, 1)
    cv2.imshow('thresh', thresh)

    _, contours, _ = cv2.findContours(thresh, 1 , 2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 7:
            print("arrow")
            cv2.drawContours(img, [cnt], 0, (0, 254, 0), -1)

    color = [
        ([0, 250, 0], [0, 255, 0])
    ]

    for (lower, upper) in color:
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)

        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        _, output = cv2.threshold(output, 127, 255, 1)
        cv2.imshow("images", output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return output


extract_arrow(1)
# cv2.imshow('img',img)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
