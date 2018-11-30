steps

1. run preprocessor.py
requires: rawdata.csv
output: preprocessed.csv
description: appends columns of counts of regular expression matches. list of regular expression noted in regexes.txt
2. run hamspamfeatures.R and knit
requires: preprocessed.csv
output: confusion matrices of prediciton where all-features and each-feature used
description: use this to analyze which predictor to include for actual predictor
3. run hamspamPredictors and knit
requires: preprocessed.csv
output: confusion matrices of prediction where all-fetures and qualified-features used. Qualified features are those with relation with the email category. Feature relation qualifier noted in qualifiedPredictors.txt
description: use this as basis for excluding other features as predictors. More accurate, less processing required.
4. TO DO: actual email spam predictor program
