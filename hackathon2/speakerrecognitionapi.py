import json
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64
import types
import time

SubscriptionKey = "f4a94c4043764ae3910f58b43b3cf5e7"


def GetHeaders(operate_id, headers):
    if operate_id == 1:
        headers["Ocp-Apim-Subscription-Key"] = SubscriptionKey
        return
    if operate_id == 2 or operate_id == 3 or operate_id == 4:
        print("1.application/octet-stream or 2.multipart/form-data ?")
        style_id = int(input())
        if style_id == 1:
            style = "application/octet-stream"
        elif style_id == 2:
            style = "multipart/form-data"
        else:
            print("enter error number")
            return
        headers["Content-Type"] = style
        headers["Ocp-Apim-Subscription-Key"] = SubscriptionKey
        return
    if operate_id == 5:
        headers["Content-Type"] = "application/json"
        headers["Ocp-Apim-Subscription-Key"] = SubscriptionKey
    return


def GetBody(operate_id):
    if operate_id == 1:
        return {}
    if operate_id == 2 or operate_id == 3 or operate_id == 4:
        file_str = input("input your file name:")
        with open(file_str, "rb") as f:
            data = f.read()
            return data
    if operate_id == 5:
        print("enter locale:1.English US 2.Chinese Mandarin")
        enter_id = int(input())
        body = {}
        if enter_id == 1:
            body["locale"] = "en-us"
        elif enter_id == 2:
            body["locale"] = "zh-CN"
        else:
            print("enter wrong number!")
            return GetBody(operate_id)
        return body


def Getparams(operate_id):
    if operate_id == 1 or operate_id == 3 or operate_id == 5:
        params = urllib.parse.urlencode({})
        return params
    if operate_id == 2 or operate_id == 4:
        print("Is short audio?1.True 2.False")
        res = int(input())
        dict_params = {}
        if res == 1:
            dict_params["shortAudio"] = True
        elif res == 2:
            dict_params["shortAudio"] = False
        else:
            print("enter wrong number!")
            return Getparams(operate_id)
        params = urllib.parse.urlencode(dict_params)
        return params
    return ""


def GetHttpMethod(operate_id):
    if operate_id == 1:
        return "GET"
    if operate_id == 2 or operate_id == 3 or operate_id == 4 or operate_id == 5:
        return "POST"
    return ""


def GetUrl(operate_id, strv):
    same_str = "/spid/v1.0/"
    if operate_id == 1:
        if strv == "":
            operationid = input("enter operationid:")
        else:
            operationid = strv
        return same_str + "operations/" + operationid + "?"
    if operate_id == 2:
        identificationProfileIds = input("enter identificationProfileIds:")
        return same_str + "identify?identificationProfileIds=" + identificationProfileIds + "&"
    if operate_id == 3:
        verificationProfileId = input("enter verificationProfileId:")
        return same_str + "verify?verificationProfileId=" + verificationProfileId + "&"
    if operate_id == 4:
        identificationProfileId = input("enter identificationProfileId:")
        return same_str + "identificationProfiles/" + identificationProfileId + "/enroll?"
    if operate_id == 5:
        return same_str + "identificationProfiles?"


def main(strg, strv):  # strg ,strv 用于方便询问operation结果
    if strg == 1:
        operate_id = strg
        time.sleep(1.2)
    elif strg == 4:
        operate_id = 4
    elif strg == 2:
        operate_id = 2
    elif strg == 5:
        operate_id = 5
    else:
        print("1.get operation status\n2.identification\n")
        print("4.create enrollment\n5.create profile")
        operate_id = int(input())
    headers = {}
    GetHeaders(operate_id, headers)
    body = GetBody(operate_id)
    httpmethod = GetHttpMethod(operate_id)
    url = GetUrl(operate_id, strv)
    params = Getparams(operate_id)
    print(url)
    print(params)
    try:
        coon = http.client.HTTPSConnection("westus.api.cognitive.microsoft.com")
        if operate_id == 2 or operate_id == 3 or operate_id == 4:
            true_body = body
        else:
            true_body = json.dumps(body)
        coon.request(httpmethod, url + params, true_body, headers)
        response = coon.getresponse()
        if operate_id == 4 or operate_id == 2:
            # print(response.msg)
            infos = response.msg["Operation-Location"].split('/')
            print(infos[-1])  # return operation-id
            return main(1, infos[-1])  # return answer
        else:
            data = response.read()
            data_utf8 = data.decode()
            print(data_utf8)
            rdata = json.loads(data_utf8)
            if operate_id == 5:
                return rdata
            elif rdata["status"] == "running":
                return main(1, strv)
            else:
                return rdata
    except Exception as e:
        print("Errno %d] %d" % (e.errno, e.strerror))
    # finally:
        # print("want to continue?")
        # res = input()
        # if res == "yes" or res == "y":
        #    main(0, "")
        # return

module_name = "speaker-recongnition-api"
if __name__ == "__main__":
    main(0, "")

