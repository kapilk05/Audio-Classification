# Audio Classification Using Deep Learning and Reinforcement Learning

## Overview
This project implements an audio classification model using deep learning and reinforcement learning (RL) techniques. 

## Features
- Utilizes **Librosa** for audio feature extraction (MFCCs)
- Implements **TensorFlow/Keras** for deep learning model development
- Applies **Reinforcement Learning (RL)** for adaptive learning and hyperparameter tuning
- Achieves **87% accuracy** on the test set

## Model Architecture
The deep learning model follows a **fully connected feedforward neural network** structure:
1. **Input Layer**: MFCC features extracted from audio samples
2. **Hidden Layers**:
   - Dense layers with **ReLU activation**
   - **Dropout layers (50%)** for regularization
3. **Output Layer**: Softmax activation for multi-class classification

## Reinforcement Learning Enhancements
RL-based techniques were used to optimize:
- **Feature selection**: Dynamic selection of the most relevant MFCC features
- **Hyperparameters**: Adaptive tuning of learning rate, batch size, and layer configurations
- **Training strategy**: Adjusting dropout rates and activation functions based on validation performance

## Results & Performance
- **Training Accuracy**: 92%
- **Test Accuracy**: 87%
- **Baseline Model Accuracy**: 78%
- **Improvement**: RL-based optimizations led to a **9% accuracy increase**


