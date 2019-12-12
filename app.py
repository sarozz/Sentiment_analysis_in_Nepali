from flask import Flask, render_template, url_for, flash, redirect, request, Response
from forms import SearchForm, TrainForm
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer,TfidfTransformer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
app = Flask(__name__)  
app.config['SECRET_KEY'] = '18871a99bd42fd0dfb4b7909d9c5c7f309'

@app.route("/", methods = ['GET','POST'])
def home():
    data1 = pd.read_csv('data.csv')
    data1 = data1[data1.label!='nu']
    x=data1.iloc[:,0].values
    y= data1.iloc[:,1].values
    vectorizer = TfidfVectorizer(encoding='utf-8')
    x = vectorizer.fit_transform(data1['text'])
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.25, random_state=50)
    model = svm.SVC(gamma='auto',probability=True)
    model.fit(x_train,y_train)
    x_score = model.score(x_train,y_train)
    y_score = model.score(x_test,y_test)
    sform = SearchForm()
    # pos = 10
    # neg = 18
    if sform.validate_on_submit():
         sent = sform.text.data
         sent1 = np.array(list(sent))
         se = vectorizer.transform(sent1)
         pre =model.predict_proba(se)
         pos = pre[0][0]*100
         neg = pre[0][1]*100
         flash(f'Training accuracy:{x_score}, and Testing accuracy: {y_score}','success')
         return render_template('search.html',form=sform,pos=pos,neg=neg)
    else:
        return render_template('home.html',form=sform)
    
    tform = TrainForm()
    if tform.validate_on_submit():
        flash('Training in progress','success')
        return render_template('search.html',form='tform')
    else:
        flash('You should first train your model','danger')

if __name__ == '__main__':
    app.run(debug=True)