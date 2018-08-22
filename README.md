# Assigment Solution

*All 6 requirements have been fullfilled, I might have misinterpreted some instructions*
-----------------------------------------------------------------------------------------

- [x] The models in the app are very similar to what is mention in [api.models](https://github.com/rjdp/grabbngo_test/blob/master/api/models.py)

- [x] The API for fetching Restaurant details can be found [here](https://github.com/rjdp/grabbngo_test/blob/master/api/views.py#L18)

- [x]  At API `/stores/<uuid>` , in case the UUID is valid identifier for a restaurant on uber eats, the details will be fetched from databse if present in local db else Uber eats API will be checked and will be populated in the local db and then sent in response, if the restaurant with the `uuid` is invalid it will cause `404`

- [x] The XLSX is available at `stores-xlsx/<uuid>/` as per the specification, did not use CSV as the concepts sheets is not possible with CSV format, the sample XLSX file can be viewed [here](https://github.com/rjdp/grabbngo_test/blob/master/assets/DELIBOX-2018_08_22-13_47_22.004414.xlsx)

- [x] This is fullfilled by `stores-xlsx/<uuid>/` as well.

- [x] Dockerized the app.


### How to run ?

1) from root of project dir. run `docker-compose up db` (required only once to intiatlize db with some data to start with and avoid migration).

2) `docker-compose up` to run the app, visit ```http://localhost:8000/stores``` 


###### Thanks 😊
 
