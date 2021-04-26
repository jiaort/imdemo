from tencent_client.im_client import IMClient


if __name__ == '__main__':
    im = IMClient()
    res, err = im.send_msg()
    print(res, err)
