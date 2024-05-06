##Inspiration
During evenings and weekends, the availability of X-ray services in emergencies is hampered by a shortage of doctors, leaving numerous machines unused. However, this tool can expedite the analysis process, improving in that way the service quality without incurring significant costs, even with the same number of doctors on duty. Furthermore, this approach enables the utilization of healthcare workers, freeing up doctors for more pertinent responsibilities.

##What it does
The project covers the analysis process:

Administrative worker inserts a new record with one or more X-ray images for a patient
When the image is submitted automatically the model predicts the presence or absence of fracture and the number of them.
A doctor examines the pre-processed image and can agree or not with the machine learning model result.
If the doctor doesn't agree with the prediction, he has to modify the result of the fracture report. The image is inserted in the training set with the correct label. In the next training iteration, it will be used to improve the accuracy of the model.
For each record, the systems send a PDF report to the patient.
##How we built it
Django project integrated with MongoDB as backend database.
CNN for classification. Cross data validation with 80% training and 20% validation. Best model accuracy with 10 epochs and step activation function with 0.35 threshold. 4083 X-ray images selected from the following journal paper: https://www.nature.com/articles/s41597-023-02432-4.
##Challenges we ran into
We cannot train the model to recognize more than 2 fractures because we don't have available sufficient number of historical data to cover this.

##Accomplishments that we're proud of
Integration of MongoDB with the project. A good accuracy (about 82%) of the machine learning model. Microservices architecture.
##What we learned
Integration of a machine learning model inside a ready-to-production project.
Managing of a Django back-end.
Implementation of the event-driven pattern in Django.
##What's next for XRay AI fractures
Extraction of the feature member which is the body part involved in the XRay
Extracting a criticism level of a fracture
Developing a more accessible client for the patient as a React Native app.
Improving the post-processing with MongoDB to summarize the distribution in time of access to the clinic according to the created_at attribute of the class Report.
Improving the post-processing with MongoDB to summarize the open Report per each doctor.
Introduction of async tasks and integration with celery for orchestration.
In this link you will find the ML models developed for data classification.
