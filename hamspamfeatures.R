```{r message=FALSE, warning=FALSE}

library(caret)
rdat = read.csv("preprocessed.csv")

inTrain = createDataPartition(y=rdat$category, p=.7, list=F)
training = rdat[inTrain,]
testing = rdat[-inTrain,]

modFitAll = train(category ~ upperCaseWords+dollarSigns+you+million+weightLoss+free+win+porn+sex+nude+jackpot+prize+discount+sale+virus+congrats+award+urgent+client+customer+cash+number+claim+private+exclusive+guarantee+apply+asap+money+subscribe, method="glm", data=training)
predictions = predict(modFitAll, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ upperCaseWords, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ dollarSigns, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ you, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ million, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ weightLoss, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ free, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ win, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ porn, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ sex, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ nude, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ jackpot, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ prize, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ discount, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ sale, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ virus, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ congrats, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ award, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ urgent, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ client, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ customer, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ cash, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ number, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ claim, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ private, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ exclusive, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ guarantee, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ apply, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ asap, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ money, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

modFit = train(category ~ subscribe, method="glm", data=training)
predictions = predict(modFit, newdata = testing)
confusionMatrix(predictions, testing$category)

```