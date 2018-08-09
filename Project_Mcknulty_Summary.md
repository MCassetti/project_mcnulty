**Summary:** 

Project Design: The main focus of my project was  music classification of Rush and Metallica, which were chosen as there may overlap sonically and be hard to distiguish without clever chose of feature space. This is an introductory step to genre classification and music recommeders. 
   
Tools: Audio Feature Extraction: Librosa
       Audio conversion: Pydub
       Visualization: Flask, T-SNE
        
Data: My own music library of Mp3s, Youtube. Data is sampled at 30second intervals (sweeping window) and ultimately ~10000 data points are generated. 

Feature Extraction: Combination of Librosa's built in features BPM, RMSE, spectral flatness, spectral centroid, and zero crossing rate) and custom built features. For the RMSE, the mean and max were captured per sample. Additional a routine that searches for the instances for which the signal frame to frame crosses the mean RMSE and calculates the percentage of the time the signal is above the mean. An additional look at the number of times the derivative of the signal results in a large delta frame to frame would signify a change in high to lower energy state.
One other custom feature was extracted, which was the percentage of harmonic to rythmic content the signal contains. The hope was to distinguish between the atonality of metallica and the more melodic verses that are present in Rush. 

Notes on Features:
Ultiamtely, the RMSE, ZCR, and Spectral content were important. However, more understanding of how sensitive these parameters are to small changes is necessarly to cateogrize this data and will require further investigation. The reason being, when the youtube mp4 was converted to an mp3, the signal was signficantly compressed and lowered the ADR(available dynamic range). This made the predictions from the flask demo wildly osciliate. Chosing a higher resolution in the audio seemed to stablize the predictions. The RMSE was impacted, however I suspect the "squashing" of the signal also contributed to spectral centroids/spectral flatness as well as trying to quatify the percent of the signal was really spent above the mean. Understanding how to correct this in the conversion would require a custom update to the pydub conversion library as specifying a standard bitrate across the signal is not enough to correct for the bit loss due to compression. 


Algorithms: Explored Random Forest, Decision Tree, Bagging Classifier, SVC, Logistic, SGD, Gradient Boostered, GaussianNB, KNN. 


Best model: SVM with RBF kernel with 88% accuracy. The reason to optimize on accuracy was due to the nature that there isn't really a target variable. It's either Rush or Metallica) and therefore misclassification of either would need to be captured.

Additional Models to explore: I did create another model that was made by taking the chromagraph and flattening along the x-axis (time). This time I used PCA after flatteing and explored tuning the number of PCA-features. I explored several training models as I did with my first model and it appeared the random forest performed the best in accuracy in both the training and testing set. I believe that this is due to choice in feature array. I think adding a model per flattened spectrograph would be the most optimal way to approach this problem. I also believed I should have explored RNN with these input arrays. 
The final step would be to bag these models using a voting classifier to resolve the probabilities. However before I just plug and chug into these models I would really like to spend time understanding if the extract feature information would separet out the difficult to classify Rush and Metallica songs.

I was suprised to find that the model was insenstive to the major shift in Metallica's band sound post-1988. Looking closer it appears that I have about the same amount of misclassifications per album, (give or take). This means that perhaps something about the 30 second clips themselves (such as a bridge/intro/outro section) may not be separating well with the given features.

The flask app looked cool and felt very accesible. Some challenges I had to not get the prediction to converge along the same value were as follows:
I needed to sample the song in the middle of the track as long intros and leading silence tended to skew the predicitions. Additionally, I introduced some random offset just so I didn't happen to take exactly the same data as that of training set, although the compression seemed to take care of that inherently. 

I enjoyed this project but feel like I have some work to do on really making sure I understanding computationally how expensive tasks are (in both time , energy, and cpu cycles) as I would have liked to explore outside the required algorithms to really get a highly accurate model.


 
 
          