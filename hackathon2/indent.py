import speakerrecognitionapi
import speechtotext


def enrollment():
    name1 = input("enter name1:")
    # file1 = input("enter file1:")
    profileid1 = input("enter profile 1:")
    name2 = input("enter name2:")
    # file2 = input("enter file2:")
    profileid2 = input("enter profile 2:")
    rdata = speakerrecognitionapi.main(4, "")
    if rdata["status"] == "succeeded":
        with open("indentity.txt", "w") as ind:
            ind.write(name1+','+profileid1+'\n')
    elif rdata["status"] == "failed":
        print(rdata["message"])
    rdata = speakerrecognitionapi.main(4, "")
    if rdata["status"] == "succeeded":
        with open("indentity.txt", "a") as ind:
            ind.write(name2+','+profileid2+'\n')
    elif rdata["status"] == "failed":
        print(rdata["message"])


indentity = {}
indentity_list = []
unknow_str = "00000000-0000-0000-0000-000000000000"


def readindentityfile():
    with open("indentity.txt", "r") as f:
        for i in f.readlines():
            infos = i.split(',')
            indentity[infos[1]] = infos[0]
            indentity_list.append(infos[1])
        indentity[unknow_str] = "unknown"
        indentity_list.append(unknow_str)
    return


def indentify():
    t = False  # remark unkown_str has exist?
    for i in range(len(indentity_list)):
        rdata = speakerrecognitionapi.main(2, "")
        if rdata["status"] == "succeeded":
            istr = rdata["processingResult"]["identifiedProfileId"]
            if istr != unknow_str:
                return indentity[istr]
            else:
                t = True
    if t:
        return indentity_list[unknow_str]


def Conversation():
    file_path = input("enter file_path:")
    name = indentify()
    content = speechtotext.func()
    with open("conversation.txt", "a") as f:
        f.write(name+": "+content+'\n')
    return


def Createfile():
    for i in range(2):
        rdata = speakerrecognitionapi.main(5, "")
        print(rdata["identificationProfileId"])
    return


def Total():
    Createfile()
    enrollment()
    readindentityfile()
    num = int(input("enter audio file num:"))
    for i in range(num):
        Conversation()
    return

if __name__ == "__main__":
    Total()
