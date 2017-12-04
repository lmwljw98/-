import requests
import json
from django.shortcuts import render

mediaCode_list = []
mediaFre_list = []
base_url = "http://cjpiporigin.myskcdn.com/VOD/"

mydict = []


def searchCode(request):
    if "OK" in request.POST:
        form = Inputform(request.POST)
        keyword = form.save()

        mediaCode_list.clear()
        mediaFre_list.clear()
        params = {'kwd': keyword.input, 'pageSize': 1000}
        mediaCode_request = requests.get('http://search.tving.com:8080/search/getFind.jsp', params=params)
        mediaCode = json.loads(mediaCode_request.text)

        for i in range(len(mediaCode['vodBCRsb']['dataList'])):
            mediaCode_list.append(mediaCode['vodBCRsb']['dataList'][i]['epi_cd'])
            mediaFre_list.append(mediaCode['vodBCRsb']['dataList'][i]['frequency'])

        for m in range(len(mediaCode_list)):
            second_params = {'mediaCode': mediaCode_list[m], 'info': 'Y'}
            programCode_request = requests.get('http://api.tving.com/v1/media/stream/info', params=second_params,
                                               proxies={'http': 'http://210.101.131.229:8080'})
            programCode = json.loads(programCode_request.text)

            realCode = programCode['body']['content']['info']['program']['enm_code']
            fre_number = mediaFre_list[m]

            mydict.append(base_url + realCode + "/" + realCode + "_" + fre_number + ".mp4")

        return render(request, 'tving/tving.html', {'list': mydict, 'form': form})

    else:
        form = Inputform()
        return render(request, 'tving/tving_f.html', {'form': form})
