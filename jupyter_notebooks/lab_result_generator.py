#!/usr/bin/env python
import os
import time
import elasticsearch
import certifi

import result


# environment variables
es = os.getenv("ESGEN_HOST", elasticsearch.Elasticsearch())
index = os.getenv("ESGEN_INDEX", "test_lab_data_stream")
doc = os.getenv("ESGEN_DOCTYPE ", "auto_lab_result")

# Use to specify elastic-cluster with auth if wanted
# es = Elasticsearch(
#     ['localhost', 'otherhost'],
#     http_auth=('user', 'secret'),
#     port=443,
#     use_ssl=True,
#     verify_certs=True,
#     ca_certs=certifi.where(),
# )

while 1:
    for _ in range(2):
        lab_data = result.Result()
        lab_data.r_ts = lab_data.r_ts.isoformat()
        lab_data.o_ts = lab_data.o_ts.isoformat()
        lab_data.c_ts = lab_data.c_ts.isoformat()
        lab_data_json = lab_data.tojson()

        # ignore 400 cause by IndexAlreadyExistsException when creating an index
        es.indices.create(index=index, ignore=400)
        es.index(index=index, doc_type=doc, body=lab_data_json)

    time.sleep(5)
