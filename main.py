from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import torch

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests for local testing

# Load your ML model

@app.route("/train", methods=["POST"])
def train():
    data = request.get_json()
    text = data.get("text", "")
    print('AD-extracted text ','/n',text[:100],'/n')

    if not text:
        return jsonify({"error": "No text provided"}), 400
    
        # Save input text to input.txt
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print('AD-inserted text')
    # Run the model script
    result = subprocess.run(["python", "model.py"], capture_output=True, text=True)
    print('AD-compleated model.py')
        # Read the stored context from file
    with open("context.txt", "r", encoding="utf-8") as f:
        context = f.read()
    print('AD-read context')
    # Extract the output (context variable will be printed in model.py)
    return jsonify({"output": result.stdout, "context": context})

    # Convert input text to tensor
    context = torch.tensor([[stoi[c] for c in text if c in stoi]], dtype=torch.long, device=device)
    
    

    # Generate text
    generated_idx = model.generate(context, max_new_tokens=200)
    generated_text = decode(generated_idx[0].tolist())

    return jsonify({"generated_text": generated_text,"context": context})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
