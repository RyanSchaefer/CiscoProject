## Things to improve

* Further decouple what storage medium is being used from the lambda
  * Could be done with something like a db connection and a function to call on that connection
* Introduce further mocking to extensively test handler functions

## Things to add
* creating/reading/updating/deleting just a specific key in an item through a specific url path (ex. `{"birthday": "new"}` -> `PUT {api}/{uid}/birthday`
  updates the birthday key to "new")
* Compare costs of running in DynamoDB to S3 and potentially switch to a low latency S3
  bucket
* Introducing a security token to protect certain objects (public / private setting)
  * Api call to see how many objects you stored with a private key
