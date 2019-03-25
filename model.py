'''
This file contains our model and the neccessary steps to deploy it. I have chosen to
apply logistic regression, using the scikit-learn ML library.

SOURCE:
https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
'''
# Imports to be able to retrieve dataset
from wrangler import get_wrangled_df

# Useful Imports
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Get our data in a var
wrangled_df = get_wrangled_df("engagement_report.log")

# Split into y (target i.e. what we want to classify as), X = feature matrix
X = wrangled_df[['company_type','total_times_logged']]
y = wrangled_df.subscribed_after_free_trial
#print(X)
#print(y)

# Split data into train and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=13)

# Init model with default params/settings
log_reg = LogisticRegression()
# Train model
log_reg.fit(X_train, y_train)

# Output training and Test accuracy
print("Training decimal accuracy : " + str(log_reg.score(X_train, y_train)))
print("Test decimal accuracy     : " + str(log_reg.score(X_test, y_test)))

# On my machine /w train_test_split random_state = 42:
# Training decimal accuracy : 0.973314606742
# Test decimal accuracy     : 0.978991596639

# On my machine /w train_test_split random_state = 13:
# Training decimal accuracy : 0.97893258427
# Test decimal accuracy     : 0.96218487395

# On my machine /w train_test_split random_state = 66:
# Training decimal accuracy : 0.976123595506
# Test decimal accuracy     : 0.970588235294

'''
    With our very basic model using the default settings & params we achieve ~97% accuracy on
    the test set. Pretty good! The first train_test_split actually gave us higher test accuracy
    than training accuracy, which can in theory happen, but shouldn't really. As we split our data
    again, this differential turns in the opposite direction (as would be expected).

    Next steps would include further diagnostics of the model (plotting learning curves etc.) to suggest
    possible improvements. This should be done before deciding to try different parameters or other
    improvements (increasing dataset size etc.).

    More on this in the attached presentation ("presentation" in the current directory).

    Look forward to hearing from you!

    Sincerely,

    Erik Hakansson
'''
