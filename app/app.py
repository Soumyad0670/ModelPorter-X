import gradio as gr
import joblib

# Load your ML model
model = joblib.load("model.pkl")

def predict(text):
    # Example: you might need to preprocess text
    return model.predict([text])[0]

demo = gr.Interface(
    fn=predict,
    inputs="text",
    outputs="text",
    title="My Model Demo",
    description="Enter input text or features and get prediction"
)

demo.launch()
