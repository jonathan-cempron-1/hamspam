```{r message=FALSE, warning=FALSE}

library(caret)
rdat = read.csv("preprocessed.csv")

inTrain = createDataPartition(y=rdat$category, p=.7, list=F)
training = rdat[inTrain,]
testing = rdat[-inTrain,]

modFitAll = train(category ~ upperCaseWords+dollarSigns+you+million+weightLoss+free+win+porn+sex+nude+jackpot+prize+discount+sale+virus+congrats+award+urgent+client+customer+cash+number+claim+private+exclusive+guarantee+apply+asap+money+subscribe, method="glm", data=training)
predictions = predict(modFitAll, newdata = testing)
confusionMatrix(predictions, testing$category)

modFitQualified = train(category ~ free+win+porn+sex+jackpot+prize+discount+congrats+award+urgent+customer+cash+number+claim+private+guarantee+apply+subscribe, method="glm", data=training)
predictions = predict(modFitQualified, newdata = testing)
confusionMatrix(predictions, testing$category)

modFitQualified = train(category ~ free+win+porn+sex+jackpot+prize+discount+congrats+award+urgent+customer+cash+number+claim+private+guarantee+apply+subscribe+upperCaseWords+you+sale, method="glm", data=training)
predictions = predict(modFitQualified, newdata = testing)
confusionMatrix(predictions, testing$category)

```