import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
# from google.colab import drive

import joblib

# drive.mount('/content/drive')

pipe_lr = joblib.load(open("model/pkl/text_emotion_balanced_dataset_emotion_attached_LR.pkl", "rb"))
# pipe_rf = joblib.load(open("model/pkl/text_emotion_balanced_dataset_emotion_attached_RF_final.pkl", "rb"))
# pipe_rf = joblib.load(open('/content/text_emotion_balanced_dataset_emotion_attached_RF.pkl','rb'))
pipe_svm = joblib.load(open("model/pkl/text_emotion_balanced_dataset_emotion_attached_SVM_final.pkl", "rb"))


# emotions_emoji_dict = {"anger": "😠😡", "disgust": "🤮", "fear": "😨😱", "happy": "🤗", "joy": "😂", "neutral": "😐", "sad": "😔",
#                        "sadness": "😔", "shame": "😳", "surprise": "😮"}
emotions_emoji_dict = {"anger": "😠😡", "disgust": "🤮", "fear": "😨😱", "joy": "😂", "neutral": "😐",
                       "sadness": "😔", "shame": "😳", "surprise": "😮"}

# emotions_emoji_dict = {("anger",): "😠😡", ("disgust",): "🤮", ("fear",): "😨😱", ("joy",): "😂", ("neutral",): "😐",
#                         ("sadness",): "😔", ("shame",): "😳", ("surprise",): "😮"}


def predict_emotions_lr(docx):
    results = pipe_lr.predict([docx])
    return results[0]

def predict_emotions_svm(docx):
    results = pipe_svm.predict([docx])
    return results[0]

# def predict_emotions_rf(docx):
#     results = pipe_rf.predict([docx])
#     return results[0]

def get_prediction_proba_lr(docx):
    results = pipe_lr.predict_proba([docx])
    return results


def get_prediction_proba_svm(docx):
    results = pipe_svm.predict_proba([docx])
    return results


# def get_prediction_proba_rf(docx):
#     results = pipe_rf.predict_proba([docx])
#     return results


def main():
    st.title("Text Emotion Detection")
    st.subheader("Detect Emotions In Text")

    with st.form(key='my_form'):
        raw_text = st.text_area("Type Here")
        submit_text = st.form_submit_button(label='Submit')

    if submit_text:
        col1, col2 = st.columns(2)

        lr_prediction = predict_emotions_lr(raw_text)
        lr_probability = get_prediction_proba_lr(raw_text)
        # print(prediction)

        svm_prediction = predict_emotions_svm(raw_text)
        svm_probability = get_prediction_proba_svm(raw_text)
        
        # rf_prediction = predict_emotions_rf(raw_text)
        # rf_probability = get_prediction_proba_rf(raw_text)
        
        voting_prediction = max(set([svm_prediction, lr_prediction]), key=list(set([svm_prediction, lr_prediction])).count)
        # voting_probability = max(set([svm_probability.tolist(), lr_probability.tolist()]), key=list(set([svm_probability.tolist(), lr_probability.tolist()])).count)

        voting_probability = {}
        for i, emotion in enumerate(pipe_lr.classes_):
            lr_prob = lr_probability[0][i]
            svm_prob = svm_probability[0][i]
            if lr_prob or svm_prob:
                voting_probability[emotion] = (lr_prob + svm_prob) / 2
        emotion_with_highest_prob = max(voting_probability, key=voting_probability.get)
        confidence = voting_probability[emotion_with_highest_prob]



        emotion_attached_text = f"{raw_text} <{voting_prediction}>"
        data = {'Emotion-Attached Text': [emotion_attached_text]}
        df1 = pd.DataFrame(data)

        # Append the DataFrame to the CSV file
        with open('emotion_predictions.csv', 'a') as f:
            df1.to_csv(f, header=False, index=False)

        with col1:
            st.success("Original Text")
            st.write(raw_text)

            st.success("Linear Regression Prediction")
            emoji_icon = emotions_emoji_dict[lr_prediction]
            st.write("{}:{}".format(lr_prediction, emoji_icon))
            st.write("Confidence:{}".format(np.max(lr_probability)))

            st.success("SVM Prediction")
            emoji_icon = emotions_emoji_dict[svm_prediction]
            st.write("{}:{}".format(svm_prediction, emoji_icon))
            st.write("Confidence:{}".format(np.max(svm_probability)))

            # st.success("Random Forest Classifier Prediction")
            # emoji_icon = emotions_emoji_dict[rf_prediction]
            # st.write("{}:{}".format(rf_prediction, emoji_icon))
            # st.write("Confidence:{}".format(np.max(rf_probability)))

            st.success("Ensemble Model Prediction")
            emoji_icon = emotions_emoji_dict[voting_prediction]
            st.write("{}:{}".format(emotion_with_highest_prob, emoji_icon))
            st.write("Confidence:{}".format(confidence))

        with col2:
            st.success("Linear regression Prediction Probability")
            proba_df_lr = pd.DataFrame(lr_probability, columns=pipe_lr.classes_)
            proba_df_lr_clean = proba_df_lr.T.reset_index()
            proba_df_lr_clean.columns = ["emotions", "probability"]

            fig = alt.Chart(proba_df_lr_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
            st.altair_chart(fig, use_container_width=True)

            # -----------------------------------

            st.success("SVM Prediction Probability")
            proba_df_svm = pd.DataFrame(svm_probability, columns=pipe_svm.classes_)
            proba_df_clean_svm = proba_df_svm.T.reset_index()
            proba_df_clean_svm.columns = ["emotions", "probability"]

            fig = alt.Chart(proba_df_clean_svm).mark_bar().encode(x='emotions', y='probability', color='emotions')
            st.altair_chart(fig, use_container_width=True)

            # ------------------------------------------

            # st.success("Random Forest Classifier Prediction Probability")
            # proba_df_rf = pd.DataFrame(rf_probability, columns=pipe_rf.classes_)
            # proba_df_clean_rf = proba_df_rf.T.reset_index()
            # proba_df_clean_rf.columns = ["emotions", "probability"]

            # fig = alt.Chart(proba_df_clean_rf).mark_bar().encode(x='emotions', y='probability', color='emotions')
            # st.altair_chart(fig, use_container_width=True)

            # -----------------------------------------------

            
            st.success("Ensemble Model Prediction Probability")
            proba_df_ensemble = pd.DataFrame(confidence, columns=voting_prediction.classes_)
            proba_df_clean_ensemble = proba_df_ensemble.T.reset_index()
            proba_df_clean_ensemble.columns = ["emotions", "probability"]


            fig = alt.Chart(proba_df_clean_ensemble).mark_bar().encode(x='emotions', y='probability', color='emotions')
            st.altair_chart(fig, use_container_width=True)






if __name__ == '__main__':
    main()
