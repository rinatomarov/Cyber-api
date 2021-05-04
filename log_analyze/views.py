import os

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
import pandas as pd
import pickle
from io import BytesIO
from django.http import HttpResponse
import warnings
import codecs
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import nltk
import pickle

warnings.filterwarnings("ignore")
import pandas as pd
import glob


# ViewSets define the view behavior.
class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        original_df = pd.DataFrame(file_uploaded)
        acunetix = [x.decode('utf8').strip() for x in file_uploaded]
        acu = list(self.fileModify(acunetix))
        count_Normal = acu.count('Normal')
        count_SQL = acu.count('SQL Injection')
        count_XSS = acu.count('XSS attack')
        content_type = file_uploaded.content_type
        return Response({"Normal": count_Normal,
                         "SQL Injection": count_SQL,
                         "XSS attack": count_XSS})

    def fileModify(self, log_data):
        host_ip = []
        c_id = []
        user = []
        dateTime = []
        offset = []
        method = []
        loc = []
        httpver = []
        code = []
        size = []

        x = 0
        for line in range(0, len(log_data)):
            s = log_data[line].split(" ")
            if len(s) > 1:
                host_ip.append((s[0]).replace("\"", ""))
                c_id.append(s[1])
                user.append(s[2])
                dateTime.append(s[3].replace('[', ""))
                offset.append(s[4].replace(']', ""))
                method.append((s[5]).replace("\"", ""))
                loc.append(s[6])
                httpver.append((s[7]).replace("\"", ""))
                code.append(s[8])
                size.append(s[9])
                x += 1

        log_dict = {}
        log_dict['Host'] = host_ip
        log_dict['Client_ID'] = c_id
        log_dict['User_Name'] = user
        log_dict['Date'] = dateTime
        log_dict['Offset'] = offset
        log_dict['Method'] = method
        log_dict['Loc'] = loc
        log_dict['HTTPver'] = httpver
        log_dict['Status_Code'] = code
        log_dict['Size'] = size

        log_df = pd.DataFrame(log_dict)
        original_df = log_df
        log_df.Loc = log_df.Loc.str.lower()

        def length(x):
            return len(x)

        def parameters(x):
            return len(x.split('&'))

        log_df['URL_Length'] = log_df['Loc'].map(length)
        log_df['Parameters'] = log_df['Loc'].map(parameters)

        final_acunetix_df = log_df.drop(['Host', 'Client_ID', 'User_Name', 'Date', 'Offset', 'HTTPver', 'Size', 'Loc'],
                                        axis=1)
        categorical_col = ['Method', 'Status_Code']
        for col in categorical_col:
            dummies = pd.get_dummies(final_acunetix_df[col], col)
            final_acunetix_df.drop(col, axis=1, inplace=True)
            final_acunetix_df = pd.concat([final_acunetix_df, dummies], axis=1)

        filename = 'log_analyze/finalized_model.sav'

        loaded_model = pickle.load(open(filename, 'rb'))
        result = loaded_model.predict(final_acunetix_df)
        original_df['result'] = result
        original_df.to_excel('res.xlsx', index=False)
        return result


class ReturnFile(APIView):
    def get(self, request):
        original_df = pd.read_excel('res.xlsx')
        print(original_df)
        return Response({
            'Host': original_df['Host'],
            'Client_ID': original_df['Client_ID'],
            'User_Name': original_df['User_Name'],
            'Date': original_df['Date'],
            'Offset': original_df['Offset'],
            'Method': original_df['Method'],
            'Loc': original_df['Loc'],
            'HTTPver': original_df['HTTPver'],
            'Status_Code': original_df['Status_Code'],
            'Size': original_df['Size'],
            'URL_Length': original_df['URL_Length'],
            'Parameters': original_df['Parameters'],
            'result': original_df['result']
        })
